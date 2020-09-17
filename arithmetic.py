#!/usr/bin/env python3

'''
Adaptive binary arithmetic coding

'''

from collections import defaultdict
from math import log2
import sys


def bitgen(x):
    for c in x:
        for i in range(8):
            yield int((c & (0x80>>i)) != 0)


def adaptive_encode(byts, n_bits):
    '''
    decoding would need to start from the same dict...
    much more efficient than storing weights or prob dist
    '''
    # start with 50/50 for each context
    freq = defaultdict(lambda: [1,2])

    # initialize context, entropy
    prev = [-1]*n_bits
    H = 0.
    bg = bitgen(byts)

    for b in bg:
        # given context, calculate probability of b
        prev_n = tuple(prev[-n_bits:])
    
        p_1 = freq[prev_n][0] / freq[prev_n][1]
        p_b = p_1 if b == 1 else 1.0 - p_1
    
        h_i = -log2(p_b)
        H += h_i

        # adaptively update probabilities
        # because of this, don't need to save prob dist in order to decode 
        freq[prev_n][0] += b == 1
        freq[prev_n][1] += 1
    
        prev.append(b)

    return H / 8


if __name__=="__main__":
    enwik4 = open("enwik4", 'rb').read()
    print(f"initial size: {sys.getsizeof(enwik4)} bytes")

    for n in [4,8,16,32]:
        print(f"adaptive encoding with {n} bit history: {adaptive_encode(enwik4, n):.5} bytes")
