#!/usr/bin/env python3
try:
    import sys, os
    from cStringIO import StringIO
    from heapq import heappush, heappop, heapify
    from collections import defaultdict
except ImportError:
    print("[!] Error finding one or more libraries\n\n")
    exit(-1)

class MyCompress():
    Errmsg = ""

    def LZW_Compress(self, mymsg):

        # Build the ASCII table
        ASCII_TAB_LEN = 256
        ASCII_TAB = dict((chr(i), i) for i in range(ASCII_TAB_LEN))

        # Prepare for compression
        byte = ""
        result = []

        for char in mymsg:
            comb = byte + char
            if comb in ASCII_TAB:
                byte = comb
            else:
                result.append(ASCII_TAB[byte])
                # Add new entry to ASCII table
                ASCII_TAB[comb] = ASCII_TAB_LEN
                ASCII_TAB_LEN += 1
                byte = char

        # Process last character in the input string
        if byte:
            result.append(ASCII_TAB[byte])
        return result


    def LZW_Decompress(self, mymsg):

        # Build the dictionary.
        ASCII_TAB_LEN = 256
        ASCII_TAB = dict((i, chr(i)) for i in range(ASCII_TAB_LEN))

        result = StringIO()
        w = chr(mymsg.pop(0))
        result.write(w)

        for k in mymsg:
            if k in ASCII_TAB:
                entry = ASCII_TAB[k]
            elif k == ASCII_TAB_LEN:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)

            result.write(entry)

            # Add w+entry[0] to the dictionary.
            ASCII_TAB[ASCII_TAB_LEN] = w + entry[0]
            ASCII_TAB_LEN += 1
            w = entry

        return result.getvalue()

    def HM_Encode(self, mymsg):
        Freq_TAB = defaultdict(int)
        for ch in mymsg:
            Freq_TAB[ch] += 1

        # Build heap according to each character's frequency
        heap = [[freq, [symb, ""]] for symb, freq in Freq_TAB.items()]
        heapify(heap)

        # Assign binary to each character
        while len(heap) > 1:
            left = heappop(heap)
            right = heappop(heap)
            for pair in left[1:]:
                pair[1] = '0' + pair[1]
            for pair in right[1:]:
                pair[1] = '1' + pair[1]
            heappush(heap, [left[0] + right[0]] + left[1:] + right[1:])

        # Sort heap
        huff = sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

        # Print Huffman Encoding table
        print("\n\nChar\tFrequency\tHuffman Code")
        for p in huff:
            print("%s\t%s\t\t%s" % (p[0], Freq_TAB[p[0]], p[1]))