from huffman import decode_huffman, encode_huffman
from lz import decode_lz, encode_lz
import os
from time import time

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
    
def write_to_txt(path: str, text: str):
    with open(path, "w") as f:
        f.write(text)

def compare_file_size(og_path, bin_path):
    og_size = os.path.getsize(og_path)
    bin_size = os.path.getsize(bin_path)
    print(f"Original file size: {og_size} bytes\nBinary file size: {bin_size} bytes\nCompression ratio: {(bin_size/og_size)*100:.2f}%")

if __name__ in "__main__":
    # og_path = "./src/sampletexts/a.txt"
    # og_path = "./src/sampletexts/johndoe.txt"
    # og_path = "./src/sampletexts/aabcbad.txt"
    # og_path = "./src/tests/test_texts/3MB.txt"
    # og_path = "./src/tests/test_texts/a10.txt"
    og_path = "./src/tests/test_texts/16kB.txt"

    filebytes = get_bytes_from_txt(og_path)
    # print("file has been read")
    bin_path = "./binfile.bin"
    filetext = get_text_from_txt(og_path)

    output_path = "./textfile.txt"



    # # # LZ78
    print("\nsaving with lz78\n")
    # # start_time = time()
    encode_lz(filebytes, bin_path)
    # # print("encode time:", time()-start_time)

    # compare_file_size(og_path, bin_path)

    # # start_time = time()
    lz_output = decode_lz(bin_path)
    # # print("decode time:", time()-start_time)

    print(f"text matches: {filetext==lz_output}")
    # # write_to_txt(output_path, lz_output)


    # HUFFMAN
    #print("\nsaving with huffman\n")
    # start_time = time()
    #encode_huffman(filebytes, bin_path)
    # print("encode time:", time()-start_time)

    #compare_file_size(og_path, bin_path)

    # start_time = time()
    #huffman_output = decode_huffman(bin_path)
    # print("decode time:", time()-start_time)

    #print(f"text matches: {filetext==huffman_output}")
    #write_to_txt(output_path, huffman_output)
    
