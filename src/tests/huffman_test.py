import unittest
from huffman import *
import os


def create_mock_tree():
    # creates correct kind of tree
    # creating all nodes
    a = Node(7)
    b = Node(4)
    c = Node(3, "A")
    d = Node(2)
    e = Node(2, "B")
    f = Node(1, "C")
    g = Node(1, "D")
    
    # adding children to nodes
    a.left = c
    a.right = b
    b.left = e
    b.right = d
    d.left = f
    d.right = g
    return a


class TestHuffman(unittest.TestCase):
    def setUp(self):
        self.mock_tree = create_mock_tree()
        self.freq_table = {"A": 3, "B": 2, "C": 1, "D": 1}
        self.freq_table2 = {"A": 3, "B": 2, "C": 1, "D": 4} #more D's
        self.codes = {"A": "0", "B": "10", "C": "110", "D": "111"}
        self.readbin_path = "./src/tests/test_bin/read_this.bin"
        self.abc_path = "./src/tests/test_bin/aabcbad_huff.bin"
        self.savebin_path = "./src/tests/test_bin/save_this_huff.bin"
        self.testbytes = bytearray()
        self.testbytes.append(255)
        self.huffman_string = "0010110100111"
        self.tree_binary = "010100000101010000100101000011101000100"
        # self.stripped_binary_string = "0101000001010100001001010000111010001000010110100111"
        self.padded_binary_string = "01010000010101000010010100001110100010000101101001110000"

    def test_left_pad_1(self):
        byte = "1"
        byte = left_pad_byte(byte)
        self.assertEqual(byte, "00000001")

    def test_left_pad_8(self):
        byte = "11111111"
        byte = left_pad_byte(byte)
        self.assertEqual(byte, "11111111")

    def test_left_pad_0(self):
        byte = ""
        byte = left_pad_byte(byte)
        self.assertEqual(byte, "")

    def test_frequency_table(self):
        freq_table = create_freq_table("AABCBAD")
        self.assertEqual(freq_table["A"], 3)
        self.assertEqual(freq_table["B"], 2)
        self.assertEqual(freq_table["C"], 1)
        self.assertEqual(freq_table["D"], 1)

    def mock_tree_correct(self):
        bfs_output = bfs(self.mock_tree)
        self.assertEqual(bfs_output, [('A', 3), ('B', 2), ('C', 1), ('D', 1)])

    def test_tree_creation(self):
        root = create_tree(self.freq_table)
        bfs_output = bfs(root)
        self.assertEqual(bfs_output, [('A', 3), ('B', 2), ('C', 1), ('D', 1)])
    
    def test_huffman_codes_to_characters(self):
        result = huffman_codes_to_characters_connection(self.mock_tree)
        codes = result[0]
        self.assertEqual(codes["A"], "0")
        self.assertEqual(codes["B"], "10")
        self.assertEqual(codes["C"], "110")
        self.assertEqual(codes["D"], "111")

        chars = result[1]
        self.assertEqual(chars["0"], "A")
        self.assertEqual(chars["10"], "B")
        self.assertEqual(chars["110"], "C")
        self.assertEqual(chars["111"], "D")

    def test_create_huffman_string(self):
        huffman_string = create_huffman_string("AABCBAD", self.codes)
        self.assertEqual(huffman_string, "0010110100111")

    def test_read(self):
        output = get_bytes_from_binfile(self.readbin_path)
        self.assertEqual(output[0], 255)

    def test_tree_binary(self):
        tree_binary = tree_to_binary_string(self.mock_tree)
        self.assertEqual(tree_binary, self.tree_binary)

    def test_save_huffman_to_binfile(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)

        huffman_string_to_binary_file(self.tree_binary, self.huffman_string, self.savebin_path)
        file_exists = os.path.exists(self.savebin_path)

        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path) # removing before assertEqual in case it doesnt pass
        self.assertEqual(file_exists, True)

    def test_saving_saves_correct_data(self): 
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)

        huffman_string_to_binary_file(self.tree_binary, self.huffman_string, self.savebin_path)

        # if reading test passes, we trust this method
        bytes = get_bytes_from_binfile(self.savebin_path)
        bits = ""
        detected_padding = bytes[0] # since the original binary string is length 52, padding is 4 to make the string's length divisible by 8 (56)
        for i in range(1, len(bytes)):
            byte = bytes[i]
            byte = format(byte, "b")
            byte = left_pad_byte(byte)
            bits += byte
        self.assertEqual(bits, self.padded_binary_string)
        self.assertEqual(detected_padding, 4)

        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)

    def test_bytes_to_text_aabcbad(self):
        bytes = get_bytes_from_binfile(self.abc_path)
        output = bytes_to_text(bytes)
        self.assertEqual(output, "AABCBAD")
    
    def test_decode_endtoend(self):
        output = decode_huffman(self.abc_path)
        self.assertEqual(output, "AABCBAD")

    def test_encode_creates_file(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_huffman("AABCBAD", self.savebin_path)
        file_exists = os.path.exists(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path) # removing before assertEqual in case it doesnt pass
        self.assertEqual(file_exists, True)
    
    def test_encode_endtoend(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_huffman("AABCBAD", self.savebin_path)

        # since decode tests pass we trust this method
        output = decode_huffman(self.savebin_path)

        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path) # removing before assertEqual in case it doesnt pass
        
        self.assertEqual(output, "AABCBAD")

    def test_node_lessthan(self):
        a = Node(3, "A")
        b = Node(2, "B")
        c = Node(2, "C")
        self.assertEqual(a<b, False)
        self.assertEqual(a>b, True)
        self.assertEqual(c<b, False)
