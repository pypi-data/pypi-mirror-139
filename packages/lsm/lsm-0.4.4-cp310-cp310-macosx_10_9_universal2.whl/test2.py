from pprint import pprint

from lsm import LSM

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--flush", action="store_true")

arguments = parser.parse_args()
print("Flush is", arguments.flush)

db = LSM('table', binary=True)
db.open()
pprint([key for key in db.keys()])
pprint(dict(db.items()))
