#!/usr/bin/env python3

from collections import defaultdict
from math import log2
import sys


def bitgen(x):
    for c in x:
        for i in range(8):
            yield int((c & (0x80>>i)) != 0)


def simple_encode(byts, n_bits):

    freq = defaultdict(lambda: [1,2])
    prev = [0]*n_bits
    H = 0.
    bg = bitgen(byts)

    for b in bg:
        prev_n = tuple(prev[-n_bits:])
    
        p_1 = freq[prev_n][0] / freq[prev_n][1]
        p_x = p_1 if b == 1 else 1.0 - p_1
    
        h_i = -log2(p_x)
        H += h_i
    
        freq[prev_n][0] += b == 1
        freq[prev_n][1] += 1
    
        prev.append(b)

    return H / 8


if __name__=="__main__":
    enwik4 = open("enwik4", 'rb').read()
    print(f"initial size: {sys.getsizeof(enwik4)} bytes")

    for n in [4,8,16,32]:
        print(f"simple encoding with {n} bit history: {simple_encode(enwik4, n):.5} bytes")
