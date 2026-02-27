import unittest
from lz import *
import os

def get_text_from_file(path):
    with open(path, encoding="ASCII") as f:
        text = f.read()
        return text.strip()

def get_file_sizes(og_path, bin_path):
    og_size = os.path.getsize(og_path)
    bin_size = os.path.getsize(bin_path)
    sizes = (og_size, bin_size)
    return sizes

def create_mock_trie():
    a = Node(0) # ""
    b = Node(1) # "A"
    c = Node(2)
    d = Node(3)
    e = Node(4)
    f = Node(5)

    a.children["A"] = b
    a.children["B"] = e
    a.children["C"] = d

    b.children["B"] = c
    b.children["D"] = f
    return a

class TestLZ(unittest.TestCase):
    def setUp(self):
        self.mock_trie = create_mock_trie()
        self.readbin_path = "./src/tests/test_bin/read_this.bin"
        self.abc_path = "./src/tests/test_bin/aabcbad_lz.bin"
        self.savebin_path = "./src/tests/test_bin/save_this_lz.bin"
        self._1kB = "./src/tests/test_texts/1kB.txt"
        self._4kB = "./src/tests/test_texts/4kB.txt"
        self._16kB = "./src/tests/test_texts/16kB.txt"
        self._64kB = "./src/tests/test_texts/64kB.txt"
        self._256kB = "./src/tests/test_texts/256kB.txt"
        self._1MB = "./src/tests/test_texts/1MB.txt"
        self._4MB = "./src/tests/test_texts/4MB.txt"
        self._16MB = "./src/tests/test_texts/16MB.txt"
        self.testbytes = bytearray()
        self.testbytes.append(255)
        self.abc = "AABCBAD\n\n"
        self.abc_table = [(None, ''), (0, 'A'), (1, 'B'), (0, 'C'), (0, 'B'), (1, 'D')]
        self.abc_binary_string = "0000000000000100000100000000000101000010000000000000010000110000000000000100001000000000000101000100"

    def test_search_existing_string(self): 
        # Result[0] == None means current string doesnt exist,
        # which means we can add it to the trie at the index found in result[1]
        # If result[0] == True, string exists and we don't insert it.
        # This is why we get return values like (1, 1)
        self.assertEqual(self.mock_trie.search(""), (True, 0)) #exists
        self.assertEqual(self.mock_trie.search("A"), (True, 1))

    def test_search_finds_new_string(self): 
        self.assertEqual(self.mock_trie.search("E"), (None, 0)) # doesn't exist
        self.assertEqual(self.mock_trie.search("CE"), (None, 3)) # doesn't exist and previous char C is found at index 3

    def test_insert_new_string(self):
        self.assertEqual(self.mock_trie.search("E"), (None, 0)) # doesn't exist
        self.mock_trie.insert("E", 6)
        self.assertEqual(self.mock_trie.search("E"), (True, 6)) # now exists
        self.assertEqual(self.mock_trie.search("AE"), (None, 1)) # doesnt exist

    def test_insert_continuing_string(self):
        self.assertEqual(self.mock_trie.search("AE"), (None, 1)) # doesn't exist but previous char at index 1
        self.mock_trie.insert("AE", 6)
        self.assertEqual(self.mock_trie.search("AE"), (True, 6)) # now exists
        self.assertEqual(self.mock_trie.search("E"), (None, 0)) # doesnt exist

    def test_create_table(self):
        new = create_table(self.abc)
        self.assertEqual(new, self.abc_table)

    def test_binary_sting_12index_8ascii(self):
        correct = self.abc_binary_string
        output = lz_to_binary_string(self.abc_table)
        self.assertEqual(output, correct)
    
    def test_lz_binary_to_file_abc(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)

        lz_binary_to_file(self.abc_binary_string, self.savebin_path)
        file_exists = os.path.exists(self.savebin_path)

        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(file_exists, True)

    def test_read(self):
        output = lz_binary_to_bytes(self.readbin_path)
        self.assertEqual(output[0], 255)

    def test_bytes_to_bits(self):
        bytes = lz_binary_to_bytes(self.abc_path)
        bits = bytes_to_bits(bytes)
        self.assertEqual(bits, self.abc_binary_string)
    
    def test_bytes_to_text_aabcbad(self):
        table = lz_bits_to_table(self.abc_binary_string)
        self.assertEqual(table, self.abc_table)

    def test_decode_table(self):
        output = lz_decode_table(self.abc_table)
        self.assertEqual(output, self.abc)

    def test_decode_endtoend(self):
        output = decode_lz(self.abc_path)
        self.assertEqual(output, self.abc)
    
    def test_encode_creates_file(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(self.abc, self.savebin_path)
        file_exists = os.path.exists(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path) # removing before assertEqual in case it doesnt pass
        self.assertEqual(file_exists, True)

    def test_encode_endtoend(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(self.abc, self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, self.abc)

    # # tests for different file sizes. Checking compression ratio (and correctness?)
    # def test_encode_1kB(self):
    #     bin_path = self._1kB
    #     filetext = get_text_from_file(bin_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     encode_lz(filetext, self.savebin_path)
    #     output = decode_lz(self.savebin_path)

    #     og_size, bin_size = get_file_sizes(bin_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     self.assertEqual(output, filetext)

