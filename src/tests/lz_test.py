import unittest
import pytest
from lz import *
import os

def get_bytes_from_txt(path):
    with open(path, "rb") as f:
        return f.read()

def get_text_from_txt(path):
    with open(path, "rb") as f:
        output = ""
        bytes = f.read()
        for byte in bytes:
            output += chr(byte)
        return output

def get_file_sizes(og_path, bin_path):
    og_size = os.path.getsize(og_path)
    bin_size = os.path.getsize(bin_path)
    sizes = (og_size, bin_size)
    return sizes

def create_mock_trie():
    a = Node(0) # ""
    b = Node(1) # 65
    c = Node(2)
    d = Node(3)
    e = Node(4)
    f = Node(5)

    a.children[65] = b
    a.children[66] = e
    a.children[67] = d

    b.children[66] = c
    b.children[68] = f
    return a

class TestLZ(unittest.TestCase):
    def setUp(self):
        self.mock_trie = create_mock_trie()

        # there's a lot of these....
        self.readbin_path = "./src/tests/test_bin/read_this.bin"
        self.abc_path = "./src/tests/test_bin/aabcbad_lz.bin"
        self.savebin_path = "./src/tests/test_bin/save_this_lz.bin"
    
        # used chatgpt to write these variable names from command tree src/tests/test_texts
        self._1kB = "./src/tests/test_texts/1kB.txt"
        self._4kB = "./src/tests/test_texts/4kB.txt"
        self._16kB = "./src/tests/test_texts/16kB.txt"
        self._64kB = "./src/tests/test_texts/64kB.txt"
        self._256kB = "./src/tests/test_texts/256kB.txt"
        self._1MB = "./src/tests/test_texts/1MB.txt"

        # Some of these broke LZ before I fixed it.
        self._a9 = "./src/tests/test_texts/a9.txt"
        self._a10 = "./src/tests/test_texts/a10.txt"
        self._a11 = "./src/tests/test_texts/a11.txt"
        self._a12 = "./src/tests/test_texts/a12.txt"

        self._an6 = "./src/tests/test_texts/an6.txt"
        self._an7 = "./src/tests/test_texts/an7.txt"

        self._na = "./src/tests/test_texts/na.txt"
        self._n2a = "./src/tests/test_texts/n2a.txt"
        self._n2an = "./src/tests/test_texts/n2an.txt"
        self._n2an2 = "./src/tests/test_texts/n2an2.txt"

        self._test_aabcbad = "./src/tests/test_texts/test_aabcbad.txt"

    
        self.testbytes = bytearray()
        self.testbytes.append(255)
        self.abc = "AABCBAD"
        self.abc_bytes = bytearray("AABCBAD", encoding="ASCII")
        self.known = "AA"
        self.known_bytes = bytearray("AA", encoding="ASCII")
        self.abc_table = [(None, ''), (0, 'A'), (1, 'B'), (0, 'C'), (0, 'B'), (1, 'D')]
        self.abc_table_bytes = [(None, 0), (0, 65), (1, 66), (0, 67), (0, 66), (1, 68)]
        self.known_end_table = [(None, 0), (0, 65), (1, 0)]
        self.abc_binary_string = "0000000000000100000100000000000101000010000000000000010000110000000000000100001000000000000101000100"

    def test_search_existing_string(self): 
        # Result[0] == None means current string doesnt exist,
        # which means we can add it to the trie at the index found in result[1]
        # If result[0] == True, string exists and we don't insert it.
        # This is why we get return values like (1, 1)
        self.assertEqual(self.mock_trie.search(bytearray()), (True, 0)) #exists
        self.assertEqual(self.mock_trie.search(bytearray("A", encoding="ASCII")), (True, 1))


    # couldnt figure out how to collect coverage of these self.assertRaises things
    def test_search_raises_int(self):
        with self.assertRaises(TypeError) as context:  
            self.mock_trie.search(1)

    def test_search_raisees_str(self):
        with pytest.raises(TypeError) as context:
            self.mock_trie.search("E")

    def test_search_finds_new_string(self): 
        self.assertEqual(self.mock_trie.search(bytearray("E", encoding="ASCII")), (False, 0)) # doesn't exist

    def test_insert_new_string(self):
        self.assertEqual(self.mock_trie.search(bytearray("E", encoding="ASCII")), (False, 0)) # doesn't exist
        self.mock_trie.insert(bytearray("E", encoding="ASCII"), 6)
        self.assertEqual(self.mock_trie.search(bytearray("E", encoding="ASCII")), (True, 6)) # now exists
        self.assertEqual(self.mock_trie.search(bytearray("AE", encoding="ASCII")), (False, 1)) # doesnt exist

    def test_insert_continuing_string(self):
        self.assertEqual(self.mock_trie.search(bytearray("AE", encoding="ASCII")), (False, 1)) # doesn't exist but previous char at index 1
        self.mock_trie.insert(bytearray("AE", encoding="ASCII"), 6)
        self.assertEqual(self.mock_trie.search(bytearray("AE", encoding="ASCII")), (True, 6)) # now exists
        self.assertEqual(self.mock_trie.search(bytearray("E", encoding="ASCII")), (False, 0)) # doesnt exist

    def test_insert_raises_int(self):
        with pytest.raises(TypeError):  
            self.mock_trie.insert(1)

    def test_insert_raisees_str(self):
        with pytest.raises(TypeError):  
            self.mock_trie.insert("E")

    def test_create_table(self):
        new = create_table(self.abc_bytes)
        self.assertEqual(new, self.abc_table_bytes)
    
    def test_create_table_known_string(self):
        new = create_table(bytearray("AA", encoding="ASCII"))
        self.assertEqual(new, self.known_end_table)

    def test_binary_sting_12index_8ascii(self):
        correct = self.abc_binary_string
        output = lz_to_binary_string(self.abc_table_bytes)
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
        encode_lz(self.abc_bytes, self.savebin_path)
        file_exists = os.path.exists(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path) # removing before assertEqual in case it doesnt pass
        self.assertEqual(file_exists, True)

    def test_encode_endtoend(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(self.abc_bytes, self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, self.abc)

    # im lazy so i made known ending decoding test endtoend
    def test_encode_endtoend_known(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(self.known_bytes, self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, self.known)

    def test_encode_endtoend_4096_entries(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(get_bytes_from_txt(self._16kB), self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, get_text_from_txt(self._16kB))
    # CAN ADD ALL FUNNY TESTCASES HERE
    
    def test_encode_endtoend_a9(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(get_bytes_from_txt(self._a9), self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, get_text_from_txt(self._a9))

    def test_encode_endtoend_a10(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(get_bytes_from_txt(self._a10), self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, get_text_from_txt(self._a10))

    def test_encode_endtoend_a12(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(get_bytes_from_txt(self._a12), self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, get_text_from_txt(self._a12))

    def test_encode_endtoend_n2an2(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(get_bytes_from_txt(self._n2an2), self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, get_text_from_txt(self._n2an2))

    def test_encode_endtoend_n2an(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(get_bytes_from_txt(self._n2an), self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, get_text_from_txt(self._n2an))

    def test_encode_endtoend_an7(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_lz(get_bytes_from_txt(self._an7), self.savebin_path)
        output = decode_lz(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        self.assertEqual(output, get_text_from_txt(self._an7))
