import unittest
from huffman import *
import os

def get_text_from_file(path):
    with open(path, encoding="ASCII") as f:
        return f.read()
        text = f.read()
        return text.strip()

def get_file_sizes(og_path, bin_path):
    og_size = os.path.getsize(og_path)
    bin_size = os.path.getsize(bin_path)
    sizes = (og_size, bin_size)
    return sizes

def create_mock_tree():
    # creates correct kind of tree
    # creating all nodes
    a = Node(7)
    b = Node(4)
    c = Node(3, 65)
    d = Node(2)
    e = Node(2, 66)
    f = Node(1, 67)
    g = Node(1, 68)
    
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
        self.freq_table = {65: 3, 66: 2, 67: 1, 68: 1}
        self.freq_table2 = {65: 3, 66: 2, 67: 1, 68: 4} #more D's
        self.codes = {65: "0", 66: "10", 67: "110", 68: "111"}
        self.readbin_path = "./src/tests/test_bin/read_this.bin"
        self.abc_path = "./src/tests/test_bin/aabcbad_huff.bin"
        self.savebin_path = "./src/tests/test_bin/save_this_huff.bin"
        self._1kB = "./src/tests/test_texts/1kB.txt"
        self._4kB = "./src/tests/test_texts/4kB.txt"
        self._16kB = "./src/tests/test_texts/16kB.txt"
        self._64kB = "./src/tests/test_texts/64kB.txt"
        self._256kB = "./src/tests/test_texts/256kB.txt"
        self._1MB = "./src/tests/test_texts/1MB.txt"
        self._4MB = "./src/tests/test_texts/4MB.txt"
        self._16MB = "./src/tests/test_texts/16MB.txt"
        self.abc = bytearray("AABCBAD", encoding = "ASCII")
        self.abctext = "AABCBAD"
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
        freq_table = create_freq_table(self.abc)
        self.assertEqual(freq_table[65], 3)
        self.assertEqual(freq_table[66], 2)
        self.assertEqual(freq_table[67], 1)
        self.assertEqual(freq_table[68], 1)

    # def mock_tree_correct(self):
    #     bfs_output = bfs(self.mock_tree)
    #     self.assertEqual(bfs_output, [(65, 3), (66, 2), (67, 1), (68, 1)])

    # def test_tree_creation(self):
    #     root = create_tree(self.freq_table)
    #     bfs_output = bfs(root)
    #     self.assertEqual(bfs_output, [(65, 3), (66, 2), (67, 1), (68, 1)])
    
    def test_huffman_codes_to_characters(self):
        result = huffman_codes_to_characters_connection(self.mock_tree)
        codes = result[0]
        self.assertEqual(codes[65], "0")
        self.assertEqual(codes[66], "10")
        self.assertEqual(codes[67], "110")
        self.assertEqual(codes[68], "111")

        chars = result[1]
        self.assertEqual(chars["0"], 65)
        self.assertEqual(chars["10"], 66)
        self.assertEqual(chars["110"], 67)
        self.assertEqual(chars["111"], 68)

    def test_create_huffman_string(self):
        huffman_string = create_huffman_string(self.abc, self.codes)
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
        self.assertEqual(output, self.abctext)
    
    def test_decode_endtoend(self):
        output = decode_huffman(self.abc_path)
        self.assertEqual(output, self.abctext)

    def test_encode_creates_file(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_huffman(self.abc, self.savebin_path)
        file_exists = os.path.exists(self.savebin_path)
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path) # removing before assertEqual in case it doesnt pass
        self.assertEqual(file_exists, True)
    
    def test_encode_endtoend(self):
        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path)
        encode_huffman(self.abc, self.savebin_path)

        # since decode tests pass we trust this method
        output = decode_huffman(self.savebin_path)

        if os.path.exists(self.savebin_path):
            os.remove(self.savebin_path) # removing before assertEqual in case it doesnt pass
        
        self.assertEqual(output, self.abctext)

    def test_node_lessthan(self):
        a = Node(3, 65)
        b = Node(2, 66)
        c = Node(2, 67)
        self.assertEqual(a<b, False)
        self.assertEqual(a>b, True)
        self.assertEqual(c<b, False)

# # tests for different file sizes. Checking compression ratio (and correctness?)
#     def test_encode_1kB(self):
#         og_path = self._1kB
#         filetext = get_text_from_file(og_path)

#         if os.path.exists(self.savebin_path):
#             os.remove(self.savebin_path)

#         encode_huffman(filetext, self.savebin_path)
#         #output = decode_huffman(self.savebin_path)

#         og_size, bin_size = get_file_sizes(og_path, self.savebin_path)

#         if os.path.exists(self.savebin_path):
#             os.remove(self.savebin_path)

#         #self.assertEqual(output, filetext)
#         self.assertGreater(og_size, bin_size)
#         ratio = (bin_size/og_size) * 100
#         self.assertLess(ratio, 75)

#     def test_encode_4kB(self):
#         og_path = self._4kB
#         filetext = get_text_from_file(og_path)

#         if os.path.exists(self.savebin_path):
#             os.remove(self.savebin_path)

#         encode_huffman(filetext, self.savebin_path)
#         #output = decode_huffman(self.savebin_path)

#         og_size, bin_size = get_file_sizes(og_path, self.savebin_path)

#         if os.path.exists(self.savebin_path):
#             os.remove(self.savebin_path)

#         #self.assertEqual(output, filetext)
#         self.assertGreater(og_size, bin_size)
#         ratio = (bin_size/og_size) * 100 # in percentage
#         self.assertLess(ratio, 65)

    # def test_encode_16kB(self):
    #     og_path = self._16kB
    #     filetext = get_text_from_file(og_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     encode_huffman(filetext, self.savebin_path)
    #     #output = decode_huffman(self.savebin_path)

    #     og_size, bin_size = get_file_sizes(og_path, self.savebin_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     #self.assertEqual(output, filetext)
    #     self.assertGreater(og_size, bin_size)
    #     ratio = (bin_size/og_size) * 100 # in percentage
    #     self.assertLess(ratio, 65)

    # def test_encode_64kB(self):
    #     og_path = self._64kB
    #     filetext = get_text_from_file(og_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     encode_huffman(filetext, self.savebin_path)
    #     #output = decode_huffman(self.savebin_path)

    #     og_size, bin_size = get_file_sizes(og_path, self.savebin_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     #self.assertEqual(output, filetext)
    #     self.assertGreater(og_size, bin_size)
    #     ratio = (bin_size/og_size) * 100 # in percentage
    #     self.assertLess(ratio, 65)

    # def test_encode_256kB(self):
    #     og_path = self._256kB
    #     filetext = get_text_from_file(og_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     encode_huffman(filetext, self.savebin_path)
    #     #output = decode_huffman(self.savebin_path)

    #     og_size, bin_size = get_file_sizes(og_path, self.savebin_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     #self.assertEqual(output, filetext)
    #     self.assertGreater(og_size, bin_size)
    #     ratio = (bin_size/og_size) * 100 # in percentage
    #     self.assertLess(ratio, 65)

    # def test_encode_1MB(self):
    #     og_path = self._1MB
    #     filetext = get_text_from_file(og_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     encode_huffman(filetext, self.savebin_path)
    #     #output = decode_huffman(self.savebin_path)

    #     og_size, bin_size = get_file_sizes(og_path, self.savebin_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     #self.assertEqual(output, filetext)
    #     self.assertGreater(og_size, bin_size)
    #     ratio = (bin_size/og_size) * 100 # in percentage
    #     self.assertLess(ratio, 65)

    # def test_encode_4MB(self):
    #     og_path = self._4MB
    #     filetext = get_text_from_file(og_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     encode_huffman(filetext, self.savebin_path)
    #     #output = decode_huffman(self.savebin_path)

    #     og_size, bin_size = get_file_sizes(og_path, self.savebin_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     #self.assertEqual(output, filetext)
    #     self.assertGreater(og_size, bin_size)
    #     ratio = (bin_size/og_size) * 100 # in percentage
    #     self.assertLess(ratio, 60)

    # def test_encode_16MB(self):
    #     og_path = self._16MB
    #     filetext = get_text_from_file(og_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     encode_huffman(filetext, self.savebin_path)
    #     #output = decode_huffman(self.savebin_path)

    #     og_size, bin_size = get_file_sizes(og_path, self.savebin_path)

    #     if os.path.exists(self.savebin_path):
    #         os.remove(self.savebin_path)

    #     #self.assertEqual(output, filetext)
    #     self.assertGreater(og_size, bin_size)
    #     ratio = (bin_size/og_size) * 100 # in percentage
    #     self.assertLess(ratio, 60)