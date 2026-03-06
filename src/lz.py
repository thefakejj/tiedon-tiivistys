class Node:
    def __init__(self, index: int):
        """Trie class to store known strings.

        Args:
            index (int): Table index of node/substring
        """
        self.index = index # current node's table index
        self.children = dict() # children[char] = node. creates trie where routes create substrings (routes to both leaf and non-leaf nodes)

    def search(self, key: bytearray):
        """Searches for substring in trie.

        Args:
            key (bytearray): substring

        Returns:
            tuple: (bool, int) bool: if substring was found. int: table index of latest known substring
        """
        if type(key) != bytearray:
            raise TypeError("Argument key must be of a bytearray.")
        x = self # start from trie root
        prev_index = 0
        for i in range(len(key)):
            if x.children.get(key[i]) == None:
                return (False, prev_index) # if key doesnt exist, result[0] = None
            x = x.children[key[i]]
            prev_index = x.index
        return (True, prev_index) # if key exists, result[0] = True

    def insert(self, key: bytearray, index: int):
        """Inserts new character to create a new substring and gives it latest table index.

        Args:
            key (str or bytes): substring
            index (int): table index
        """
        if type(key) != bytearray:
            raise TypeError("Argument key must be of a bytearray.")
        x = self # start from trie root
        for char in key:
            if x.children.get(char) == None:
                new_node = Node(index)
                x.children[char] = new_node
                return
            x = x.children[char]

    # helper function to traverse tries. doesnt help too much to be honest.
    # def traverse(self):
    #     visited = set()
    #     queue = [self]
    #     output = []

    #     while len(queue) > 0:
    #         current = queue[0]
    #         print(current)
    #         print(current.children)
    #         if current not in visited and not None:
    #             output.append(current.index)
    #             for child in current.children:
    #                 queue.append(current.children[child])
    #             visited.add(current)
    #             queue.remove(current)
    #     return output

# one function that calls all necessary functions for encoding and saving
def encode_lz(filetext: bytes, binary_path: str):
    """Encodes text with LZ78 and saves it to binary file.

    Args:
        filebytes (bytes): Text read as bytes
        binary_path (str): path of save location
    """
    lz_table = create_table(filetext)
    lz_binary = lz_to_binary_string(lz_table)
    lz_binary_to_file(lz_binary, binary_path)

# function that calls all necessary functions for decoding, returns string
def decode_lz(binary_path: str):
    """Decodes LZ78 table in binary file into  a string

    Args:
        binary_path (str): path of binary file

    Returns:
        str: Decoded text
    """
    lz_bytes = lz_binary_to_bytes(binary_path)
    lz_bits = bytes_to_bits(lz_bytes)
    new_lz_table = lz_bits_to_table(lz_bits)
    output = lz_decode_table(new_lz_table)
    return output

def create_table(text: bytes):
    """Creates LZ78 table by using trie

    Args:
        text (bytes): Original text in bytes

    Returns:
        list: list of tuples (previous_index, character)
    """
    # table is a list of (index, character), where index refers to index of correct coding in this table and character is a new character
    # starts with empty node
    # table = [(None, "")]
    table = [(None, 0)]# <- null character

    trie_root = Node(0)

    current = bytearray()
    cur_index = 1
    for char in text:
        current.append(char)
        result = trie_root.search(current)

        prev_index = result[1]
        if result[0] == False:
            # when prev_index 4095 reached, no more new references will be stored.
            # this way the reference can be stored in 12 bits
            if cur_index < 4096:
                trie_root.insert(current, cur_index)
            cur_index += 1
            current = bytearray()
            pair = (prev_index, char)
            table.append(pair)
    print(cur_index)
    if result[0] == True:
        pair = (prev_index, 0)
        table.append(pair)
        # if the last character is a known character,
        # we add it to the end since the if- statement in loop doesn't let it through
    return table

def lz_to_binary_string(table: list):
    """Creates binary string from LZ78 table.

    Args:
        table (list): LZ78 table

    Returns:
        str: String representation of LZ78 table
    """
    # first is empty
    # we're going to create a string with all the bits
    output = ""
    # without the first None "pair"
    for pair in table[1:]:
        reference = pair[0]
    
        ref_twelve = format(reference, "b")
        ref_twelve = left_pad_bits(ref_twelve, 12)

        char_ascii = pair[1]
        # char_ascii = ord(char)
        char_ascii = format(char_ascii, "b")
        char_ascii = left_pad_bits(char_ascii, 8)
        # UNRELATED TO PROJECT https://www.youtube.com/watch?v=rPIt52BwTak 

        entry = ref_twelve+char_ascii
        output += entry
    return output
    
def lz_binary_to_file(binary_string: str, filepath: str):
    """Saves LZ78 table's binary string representation to a binary file

    Args:
        binary_string (str): LZ78 table
        filepath (str): Binary file path
    """
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
    """Returns binary file's content as bytes

    Args:
        filepath (str): Path of binary file

    Returns:
        bytes: Contents of binary file
    """
    with open(filepath, "rb") as binfile:
        bytes = binfile.read()
    return bytes

def bytes_to_bits(bytes: list):
    """Converts bytes to a string of bits

    Args:
        bytes (list): Contents of binary file

    Returns:
        str: bits
    """
    bits = ""
    detected_padding = bytes[0]
    for i in range(1, len(bytes)):
        byte = bytes[i]
        byte = format(byte, "b")
        byte = left_pad_bits(byte, 8)
        bits += byte
    end_index = len(bits) - detected_padding
    bits = bits[0:end_index]
    return bits

def lz_bits_to_table(bits: str):
    """Creates a LZ78 table from bits.

    Args:
        bits (str): Binary file contents as binary string

    Returns:
        list: LZ78 table
    """
    table = [(None, "")]
    # we want to first read 12 bits, which gives us the reference's table index
    # then we want to read 8 bits, which gives the character's acsii code
    for i in range(0, len(bits), 20):
        start = i
        end = i+20

        reference = bits[start:start+12]
        reference = int(reference, 2)
    
        char = bits[start+12:end]
        char = int(char, 2)
        if char == 0:
            char = ""
        else:    
            char = chr(char)

        pair = (reference, char)
        table.append(pair)
    return table

def left_pad_bits(bits: str, target_len: int):
    """Pad reference with target_len 12 and pad character with 8.

    Args:
        bits (str): reference or char
        target_len (int): 12 for ref and 8 for char

    Returns:
        str: bits
    """
    missing_bits = (target_len - len(bits)) % target_len
    padding = "0"*missing_bits
    bits = padding+bits
    return bits

def lz_decode_table(table: list):
    """Decodes original text from a LZ78 table

    Args:
        table (list): LZ78 table

    Returns:
        str: Original text
    """
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
