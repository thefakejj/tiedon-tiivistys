import heapq

#Huffman-koodaus

class Node:
    def __init__(self, freq: int, char=None):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None

    # less-than operaaito, jotta heap osaa järjestellä nodet
    def __lt__(self, other):
        return self.freq < other.freq

def encode_huffman(filebytes: bytes, binary_path: str):
    freq_table = create_freq_table(filebytes)
    print(freq_table)
    tree = create_tree(freq_table)
    huffman_codes = huffman_codes_to_characters_connection(tree)[0]
    output_string = create_huffman_string(filebytes, huffman_codes)
    tree_in_bits = tree_to_binary_string(tree)
    huffman_string_to_binary_file(tree_in_bits, output_string, binary_path)

def decode_huffman(binary_path: str):
    bindata = get_bytes_from_binfile(binary_path)
    output = bytes_to_text(bindata)
    return output

def create_freq_table(text: str):
    freq_table = {}
    for char in text:
        if not char in freq_table:
            freq_table[char] = 1
        else:
            freq_table[char] += 1
    return freq_table

def create_tree(freq_table: dict):
    prio_queue = []

    for char in freq_table:
        freq = freq_table[char]
        node = Node(freq, char)
        heapq.heappush(prio_queue, node)

    while len(prio_queue) >= 2:
        left = heapq.heappop(prio_queue)
        right = heapq.heappop(prio_queue)
        new_node = Node(left.freq+right.freq)
        new_node.left = left
        new_node.right = right
        heapq.heappush(prio_queue, new_node)

    root = heapq.heappop(prio_queue)
    return root

# rekursiivinen funktio jolla muodostetaan puun lehdille huffman-koodit
def set_huffman_codes(node, codes: dict, current, chars: dict):

    if node is None:
        return
    
    if node.left is None and node.right is None:
        codes[node.char] = current
        chars[current] = node.char
        return

    set_huffman_codes(node.left, codes, current+"0", chars)
    set_huffman_codes(node.right, codes, current+"1", chars)

def huffman_codes_to_characters_connection(root):
    codes = {}
    chars = {}
    set_huffman_codes(root, codes, "", chars)
    return codes, chars

def create_huffman_string(text: str, codes: dict):
    output = ""
    for char in text:
        output+=codes[char]
    return output

def get_bytes_from_binfile(filepath: str):
    with open(filepath, "rb") as binfile:
        bytes = binfile.read()
    return bytes

def bytes_to_text(bytes: list):
    bits = ""
    detected_padding = bytes[0]
    for i in range(1, len(bytes)):
        byte = bytes[i]
        byte = format(byte, "b")
        byte = left_pad_byte(byte)
        bits += byte
    end_index = len(bits) - detected_padding
    bits = bits[0:end_index] # string bits should include all binary starting from tree

    data = binary_string_to_tree(bits)
    tree = data["tree"]
    start_index = data["index"]
    
    bits = bits[start_index:end_index] # string bits should include all binary starting from compressed data
    chars = huffman_codes_to_characters_connection(tree)[1] # this method returns two dicts, we need chars

    current = ""
    output = ""
    for bit in bits:
        current += bit
        character = chars.get(current, None)
        if character == None:
            continue
        output += character
        current = ""
   
    return output

def huffman_string_to_binary_file(huffman_tree: str, huffman_string: str, filepath: str):
    binary_data = huffman_tree + huffman_string
    missing_bits = (8 - len(binary_data)) % 8
    padding = "0"*missing_bits
    binary_data += padding

    bytes = bytearray()
    bytes.append(missing_bits)
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        bytes.append(int(byte, 2))

    with open(filepath, "wb") as binfile:
        binfile.write(bytes)

def tree_to_binary_string(root: Node):
    node = root
    bits = ""
    stack = [node]
    while len(stack) > 0:
        node = stack.pop()
        if node.left == None and node.right == None:
            bits += "1"
            char_ascii = node.char
            # char_ascii = ord(char)
            char_ascii = format(char_ascii, "b")
            char_ascii = left_pad_byte(char_ascii)
            bits += char_ascii
        else:
            bits += "0"
            stack.append(node.right)
            stack.append(node.left)

    return bits

def binary_string_to_tree(bits: str):
    i = 0
    root = Node(1)
    stack = [root] #freq ei väliä, char lisätään myöhemmin. 1 on placeholder freq.
    while True:
        if len(stack) < 1:
            break
        node = stack.pop()
        if bits[i] == "1":
            char = bits[i+1:i+9]
            char = int(char, 2)
            char = chr(char)
            i = i+9
            node.char = char
        elif bits[i] == "0":
            left = Node(1)
            right = Node(1)

            node.left = left
            node.right = right

            stack.append(right)
            stack.append(left)
            i += 1
    data = {"tree": root, "index": i}
    return data

def left_pad_byte(byte: str):
        missing_bits = (8 - len(byte)) % 8
        padding = "0"*missing_bits
        byte = padding+byte
        return byte

# # helper funciton to check trees
# def bfs(root):
#     visited = set()
#     queue = [root]
#     output = []
#     while len(queue)>0:
#         current = queue[0]

#         #print(current.freq)
#         #if current.char:
#            #print(current.char, "char exists")
#         if current not in visited and not None:
#             for child in [current.left, current.right]:
#                 if child != None:
#                     #print(f"{current.freq, current.char} child: {child.freq, child.char}")
#                     queue.append(child)
#             visited.add(current)
#             queue.remove(current)
#         if current.left is None and current.right is None:
#             output.append((current.char, current.freq))
#     return output
