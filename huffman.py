# Compression/encoding -- hutter prize
# start with 1GB data

# smaller sample for tests
# * enwik9: 1e9 bytes
# * enwik8: 1e8 bytes
# ...
# * enwik6: 1e6 bytes
#  -- benchmark gzip : 350 KB
#  -- huffman        : 617 KB -_-

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


class HuffmanCoding:
    def __init__(self, text):
        # initialize important fields
        self.text = text
        self.pq = PriorityQueue()
        self.frequencies = defaultdict(int)
        self.encodings = defaultdict()
        self.decodings = dict()

    def encode(self, outfile):
        # calculate frequencies
        for char in self.text:
            self.frequencies[char] += 1

        # construct huffman tree
        for k, v in self.frequencies.items():
            self.pq.put(Leaf(k, v))
        for i in range(self.pq.qsize() - 1):
            min1 = self.pq.get()
            min2 = self.pq.get()
            new_node = Branch(min1, min2)
            self.pq.put(new_node)

        tree = self.pq.get()

        # put encodings into a dict for each char, and flip for decodings
        self._get_encodings(tree)
        self.decodings = {str(v.bin): k for k, v in self.encodings.items()}

        # generate output bit array
        bits_out = BitArray(bin="")
        for char in self.text:
            bits_out.append(self.encodings[char])

        with open(outfile, 'wb') as f:
            bits_out.tofile(f)

        return bits_out

    def decode(self, infile):
        bits_in = BitArray(open(infile, 'rb').read()).bin
        output, current_code = "", ""
 
        # because these are prefix codes, we can look through bit array
        # and append the bits until we get a character 
        for bit in bits_in:
            current_code += bit
            if current_code in self.decodings:
                char = self.decodings[current_code]
                output += char
                current_code = ""

        return output
        
    def _get_encodings(self, node, word=''):
        # method to create encoding dict
        if isinstance(node, Branch):
            self._get_encodings(node.left, word + "0")
            self._get_encodings(node.right, word + "1")
        elif isinstance(node, Leaf):
            self.encodings[node.char] = BitArray(bin=word)
        else:
            raise ValueError

        
initial_text = open("enwik6", 'r').read()

hc = HuffmanCoding(initial_text)
encoding = hc.encode("enwik6encoded")
encode_decode = hc.decode("enwik6encoded")

assert(initial_text == encode_decode)
