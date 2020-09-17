# Compression/encoding -- hutter prize
# start with 1GB data

# smaller sample for tests
# * enwik9: 1e9 bytes
# * enwik8: 1e8 bytes
# ...
# * enwik6: 1e6 bytes
#  -- benchmark: gzip 350 KB

from collections import defaultdict
from queue import PriorityQueue
from bitstring import BitArray


class Node:
    def __init__(self):
        self.freq = 0

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq


class Branch(Node):
    def __init__(self, left, right):
        super(Branch).__init__()
        self.left = left
        self.right = right
        self.freq = left.freq + right.freq


class Leaf(Node):
    def __init__(self, char, freq):
        super(Branch).__init__()
        self.char = char
        self.freq = freq

enwik6 = open("enwik6", 'r').read()

d = defaultdict(int)
q = PriorityQueue()

for char in enwik6:
    d[char] += 1

for k, v in d.items():
    q.put(Leaf(k, v))

for i in range(q.qsize() - 1):
    a = q.get()
    b = q.get()
    new_node = Branch(a, b)
    q.put(new_node)

tree = q.get()

encodings = defaultdict()

def get_encodings(node, word=""):
    if isinstance(node, Branch):
        get_encodings(node.left, word + "0")
        get_encodings(node.right, word + "1")
    elif isinstance(node, Leaf):
        encodings[node.char] = BitArray(bin=word)
    else:
        raise ValueError

get_encodings(tree)

bits_out = BitArray(bin="")
for char in enwik6:
    bits_out.append(encodings[char])

with open("enwik6encoded", 'wb') as f:
    bits_out.tofile(f)

bits_in = BitArray(open("enwik6encoded", 'rb').read()).bin

unencodings = {str(v.bin): k for k, v in encodings.items()}

output = ""
current_code = ""
for bit in bits_in:
    current_code += bit
    if current_code in unencodings:
        char = unencodings[current_code]
        output += char
        current_code = ""

assert(enwik6 == output)

open("enwik6unencoded", 'w').write(output)

