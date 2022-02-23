import bz2
import re
from tqdm import tqdm
import random
import sys
from .pgn import PGNParser


pgn_file = sys.stdin

parser = PGNParser(pgn_file)

output_filename = './lichess.pgn'
output_filename = './datasets/output.pgn'

classical_pgn = sys.stdout #open(output_filename, 'wb')

rng = random.Random(42)
probability = 1/25

event_types = {}

while parser.has_next():
    headers, moves, data = parser.next()
    if data:
        pass
    if not headers:
        continue
    event = headers['Event'].split(' ')[1]
    event_types[event] = event_types.get(event, 0) + 1
    if event == 'Classical' and rng.random() < probability:
        classical_pgn.write(data)
        classical_pgn.flush()

print(event_types, file=sys.stderr)