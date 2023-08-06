import lsm

with lsm.LSM(
    "offers_search.lsm", compress="none", readonly=True, mmap=False
) as db:
    for _ in db.items():
        pass

    input("Iterating done")

    with db.cursor() as cur:
        cur.seek(b"", lsm.SEEK_GE)

        for _ in cur:
            pass

        input("Cursor done")
