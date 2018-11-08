#!/usr/bin/env python3
try:
    from blessings import Terminal
    from MultiMedia_Compression.MyCompress import *
except ImportError:
    print("[!] Error finding one or more libraries\n\n")
    exit(-1)

if __name__ == "__main__":
    t = Terminal()
    Example_str = 'HelloWorld1234HELLOWORLD123498875'

    # LZW Compression and Decompression Example
    myinst = MyCompress()
    compressed = myinst.LZW_Compress(Example_str)

    print(t.white("Original String: ") + t.green("\n{0}".format(Example_str)) + t.white("\nLength: ") + t.red(
        "{0}\n".format(len(Example_str))))
    print(t.white("Compressed String:"))
    print(compressed)
    print(t.white("Length: ") + t.red("{0}\n".format(len(compressed))))

    decompressed = myinst.LZW_Decompress(compressed)

    print(t.white("Decompressed String:\n") + t.green("{0}".format(decompressed)) + "\n" + t.white("Length: ") + t.red(
        "{0}\n".format(len(decompressed))))

    # Huffman Encoding Example
    huff = myinst.HM_Encode(Example_str)
