from contextlib import contextmanager
from multiprocessing.pool import ThreadPool
from threading import Event, Condition
from collections import Counter

from lsm import LSM


def reader(event: Event, cond: Condition, ctx: Counter):
    with LSM("offers_search_prestable.lsmka", readonly=True, mmap=True) as db:
        view = db.items()

        print("Opened")
        with cond:
            ctx["opened"] += 1
            cond.notify()
        event.wait()

        for idx, (key, value) in enumerate(iter(view)):
            pass

        del view

        print(f"Read {idx + 1} items through view")
        with cond:
            ctx["iter_view"] += 1
            cond.notify()
        event.wait()

        for idx, (key, value) in enumerate(db.items()):
            pass

        print(f"Read {idx + 1} items through .items()")
        with cond:
            ctx["iter_items"] += 1
            cond.notify()
        event.wait()

        with db.cursor() as cursor:
            cursor.first()

            for idx, (key, value) in enumerate(cursor):
                pass

            print(f"Read {idx + 1} items through .cursor()")
            with cond:
                ctx["iter_cursor"] += 1
                cond.notify()
            event.wait()

    with cond:
        ctx["done"] += 1
        cond.notify()
    event.wait()


THREADS = 8


with ThreadPool(THREADS) as pool:
    cond = Condition()
    events = []
    ctx = Counter()

    for _ in range(THREADS):
        event = Event()
        pool.apply_async(
            reader, args=(event, cond, ctx),
        )
        events.append(event)

    @contextmanager
    def wait_for(topic):
        with cond:
            cond.wait_for(lambda: ctx[topic] == THREADS)

        yield

        for event in events:
            event.set()

        for event in events:
            event.clear()

    with wait_for("opened"):
        input("Press enter to continue")

    with wait_for("iter_view"):
        input("Press enter to continue")

    with wait_for("iter_items"):
        input("Press enter to continue")

    with wait_for("iter_cursor"):
        input("Press enter to continue")

    with wait_for("done"):
        input("All done. Press enter to continue")

input("Threads done")
