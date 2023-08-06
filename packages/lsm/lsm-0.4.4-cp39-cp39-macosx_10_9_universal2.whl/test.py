from threading import Thread, Event

from lsm import LSM, SAFETY_OFF
from queue import Queue


lsm_kw = {
    'autocheckpoint': 8 * 1024,  # 8 MB
    'autoflush': 8 * 1024,  # 8 MB
    'multiple_processes': False,
    'safety': SAFETY_OFF,  # do not fsync manually
    'use_log': False,
    'readonly': False
}


def reader(queue: Queue):
    with LSM("offers_search.lsm.lz4", compress="lz4", readonly=True) as db:
        for key, value in db.items():
            queue.put((key, value))

    queue.put(None)


def writer(event: Event, queue: Queue):
    with LSM(
        "offers_search.lsm.none",
        compress="none",
        **lsm_kw
    ) as db:
        pair = queue.get()
        while pair is not None:
            key, value = pair
            db[key] = value
            pair = queue.get()

        db.work(complete=True)
    event.set()


event = Event()
q = Queue(maxsize=1024)
Thread(target=reader, args=(q,)).start()
Thread(target=writer, args=(event, q)).start()
event.wait()
