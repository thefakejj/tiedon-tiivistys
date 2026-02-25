from huffman import decode_huffman, encode_huffman
from lz import decode_lz, encode_lz
import os

def get_text_from_file(path):
    with open(path, encoding="ASCII") as f:
    #with open(path) as f: <- if I allow utf-8
        text = f.read()
        # if text[-1] == "\n":
        #     last_i = -1
        #     while text[last_i-1] == "\n":
        #         last_i -= 1 #reduce by 1 until line breaks are stripped
        #     return text[:last_i]
        # return text
        return text.strip() # removes leading and trailing whitespace. might have to implement the algorithms without this though.

def compare_file_size(og_path, bin_path):
    og_size = os.path.getsize(og_path)
    bin_size = os.path.getsize(bin_path)
    print(f"Original file size: {og_size} bytes\nBinary file size: {bin_size} bytes\nCompression ratio: {(bin_size/og_size)*100:.2f}%")

if __name__ in "__main__":

    og_path = "./src/sampletexts/johndoe.txt"
    # og_path = "./src/tests/test_texts/16MB.txt"
    filetext = get_text_from_file(og_path)
    print("file has been read\n")
    bin_path = "./binfile.bin"

    # LZ78
    print("saving with lz78\n")
    encode_lz(filetext, bin_path)
    compare_file_size(og_path, bin_path)
    lz_output = decode_lz(bin_path)
    #print(lz_output)
    print(f"text matches: {filetext==lz_output}")

    # HUFFMAN
    print("saving with huffman\n")
    encode_huffman(filetext, bin_path)
    compare_file_size(og_path, bin_path)
    huffman_output = decode_huffman(bin_path)
    #print(huffman_output)
    print(f"text matches: {filetext==huffman_output}")
    