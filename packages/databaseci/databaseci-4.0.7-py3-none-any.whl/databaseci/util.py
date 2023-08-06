# Copyright DatabaseCI Pty Ltd 2022

import itertools

BATCH_SIZE = 1000


def chunk(seq, size):
    for b in batched(seq):
        return b


def batched(thing, size=BATCH_SIZE):
    i = iter(thing)

    while True:
        r = list(itertools.islice(i, size))

        if not r:
            break

        yield r
