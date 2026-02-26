class Node:
    def __init__(self, index: int):
        self.index = index # current node's table index
        self.children = dict() # children[char] = node. creates trie where routes create substrings (routes to both leaf and non-leaf nodes)

    def search(self, key: str):
        x = self # start from trie root
        prev_index = 0
        for i in range(len(key)):
            if x.children.get(key[i]) == None:
                return (None, prev_index) # if key doesnt exist, result[0] = None
            x = x.children[key[i]]
            prev_index = x.index
        return (True, prev_index) # if key exists, result[0] = True

    def insert(self, key: str, index: int):
        x = self # start from trie root
        for char in key:
            if x.children.get(char) == None:
                new_node = Node(index)
                x.children[char] = new_node
                return
            x = x.children[char]

    # helper function to traverse tries. doesnt help too much to be honest.
    def traverse(self):
        visited = set()
        queue = [self]
        output = []

        while len(queue) > 0:
            current = queue[0]
            print(current)
            print(current.children)
            if current not in visited and not None:
                output.append(current.index)
                for child in current.children:
                    queue.append(current.children[child])
                visited.add(current)
                queue.remove(current)
        return output

# one function that calls all necessary functions for encoding and saving
def encode_lz(filetext: str, binary_path: str):
    lz_table = create_table(filetext)
    lz_binary = lz_to_binary_string(lz_table)
    lz_binary_to_file(lz_binary, binary_path)

# function that calls all necessary functions for decoding, returns string
def decode_lz(binary_path: str):
    lz_bytes = lz_binary_to_bytes(binary_path)
    lz_bits = bytes_to_bits(lz_bytes)
    new_lz_table = lz_bits_to_table(lz_bits)
    output = lz_decode_table(new_lz_table)
    return output

def create_table(text: str):
    # table is a list of (index, character), where index refers to index of correct coding in this table and character is a new character
    # starts with empty node
    table = [(None, "")]
    trie_root = Node(0)

    current = ""
    cur_index = 1
    for char in text:
        current += char
        result = trie_root.search(current)
        if result[0] == None:
            # when prev_index 4095 reached, no more new references will be stored.
            # this way the reference can be stored in 12 bits
            if cur_index < 4096:
                trie_root.insert(current, cur_index)
            prev_index = result[1]
            pair = (prev_index, char)
            table.append(pair)
            cur_index += 1
            current = ""
    return table

def lz_to_binary_string(table: list):
    # first is empty
    # we're going to create a string with all the bits
    output = ""
    # without the first None "pair"
    for pair in table[1:]:
        reference = pair[0]
    
        ref_twelve = format(reference, "b")
        ref_twelve = left_pad_byte(ref_twelve, 12)

        char = pair[1]
        char_ascii = ord(char)
        char_ascii = format(char_ascii, "b")
        char_ascii = left_pad_byte(char_ascii, 8)
        # UNRELATED TO PROJECT https://www.youtube.com/watch?v=rPIt52BwTak 

        entry = ref_twelve+char_ascii
        output += entry
    return output
    
def lz_binary_to_file(binary_string: str, filepath: str):
    # could create a file saving function since this is almost same as huffman_string_to_binary_file
    missing_bits = (8 - len(binary_string)) % 8
    padding = "0"*missing_bits
    binary_string += padding

    bytes = bytearray()
    bytes.append(missing_bits)
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        bytes.append(int(byte, 2))

    with open(filepath, "wb") as binfile:
        binfile.write(bytes)

def lz_binary_to_bytes(filepath: str):
    with open(filepath, "rb") as binfile:
        bytes = binfile.read()
    return bytes

def bytes_to_bits(bytes: list):
    bits = ""
    detected_padding = bytes[0]
    for i in range(1, len(bytes)):
        byte = bytes[i]
        byte = format(byte, "b")
        byte = left_pad_byte(byte, 8)
        bits += byte
    end_index = len(bits) - detected_padding
    bits = bits[0:end_index] # string bits should include all binary starting from tree
    return bits

def lz_bits_to_table(bits: str):
    table = [(None, "")]
    # we want to first read 12 bits, which gives us a reference
    # then we want to read 8 bits, which gives the character's acsii code
    # True if currently reading reference
    for i in range(0, len(bits), 20):
        start = i
        end = i+20

        reference = bits[start:start+12]
        reference = int(reference, 2)
    
        char = bits[start+12:end]
        char = int(char, 2)
        char = chr(char)

        pair = (reference, char)
        table.append(pair)
    return table

# forgive the repetition this once
def left_pad_byte(byte: str, target_len: int):
    missing_bits = (target_len - len(byte)) % target_len
    padding = "0"*missing_bits
    byte = padding+byte
    return byte

def lz_decode_table(table: list):
    result = ""

    for pair in table[1:]:
        current = pair
        stack =  []
        next = ""
        while current[0] != None:
            stack.append(current[1])
            current = table[current[0]]
        while len(stack) > 0:
            next += stack.pop()

        result += next

    return result
