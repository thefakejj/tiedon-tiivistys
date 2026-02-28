from huffman import decode_huffman, encode_huffman
from lz import decode_lz, encode_lz
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

def compare_file_size(og_path, bin_path):
    og_size = os.path.getsize(og_path)
    bin_size = os.path.getsize(bin_path)
    print(f"Original file size: {og_size} bytes\nBinary file size: {bin_size} bytes\nCompression ratio: {(bin_size/og_size)*100:.2f}%")

if __name__ in "__main__":
    og_path = "./src/sampletexts/a.txt"
    # og_path = "./src/sampletexts/johndoe.txt"
    # og_path = "./src/sampletexts/aabcbad.txt"
    # og_path = "./src/tests/test_texts/4kB.txt"
    # og_path = "./src/tests/test_texts/16MB.txt"

    filebytes = get_bytes_from_txt(og_path)
    print("file has been read")
    bin_path = "./binfile.bin"
    # print(filetext)
    # with open(bin_path, "wb") as file:
    #     file.write(filetext)

    # newtext = ""
    # with open(bin_path, "rb") as newfile:
    #     bytes = newfile.read()
    #     print(type(bytes))
    #     print(bytes[0])
    #     for byte in bytes:
    #         print(byte)
    #         print(type(byte))
    filetext = get_text_from_txt(og_path)

    # LZ78
    print("\nsaving with lz78\n")
    encode_lz(filebytes, bin_path)
    compare_file_size(og_path, bin_path)
    lz_output = decode_lz(bin_path)

    # print("\nlz output:")
    # print("ä"+lz_output+"ä")
    # print(len(lz_output))

    # print("\nog output")
    # print("ä"+filetext+"ä")
    # print(len(filetext))

    # print(f"text matches: {filetext==lz_output}")





    # with open("./og.txt", "w") as f: 
    #     f.write(filetext)
    # with open("./new.txt", "w") as f: 
    #     f.write(lz_output)
    
    # HUFFMAN
    print("\nsaving with huffman\n")
    encode_huffman(filebytes, bin_path)
    compare_file_size(og_path, bin_path)
    huffman_output = decode_huffman(bin_path)
    # print("ä"+huffman_output+"ä")
    # print(len(huffman_output))
    print(f"text matches: {filetext==huffman_output}")
    