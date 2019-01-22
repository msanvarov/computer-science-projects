### Description

Data compression involves reducing the amount of space taken up by files. Anyone who has listened to an MP3 file or extracted a file from a zip archive has used compression. Reasons for compressing a file include saving disk space and reducing the time required to transfer the file to another computer.
There are two broad classes of compression algorithms: lossy compression and lossless compression. Lossy compression means that the file gets smaller, but that some information is lost. MP3 is a form of lossy compression: it saves space by throwing away some audio information, and therefore the original audio file can not be recovered. Lossless compression means that the file gets smaller and that the original file can be recovered from the compressed file. FLAC is a form of lossless audio compression: it can’t save as much space as MP3, but it does let you perfectly recover the original file.
In this assignment, we’ll be working with a lossless kind of compression called Huffman coding. When you’re finished the assignment, you’ll be able to compress a file, and then decompress that file to get back the original file.

##### Background
###### Fixed- and Variable-Length Codes
Suppose that we had an alphabet of four letters: a, b, c, and d. Computers store only 0s and 1s (each 0 and 1 is known as a bit), not letters directly. So, if we want to store these letters in a computer, it is necessary to choose a mapping from these letters to bits. That is, it’s necessary to agree on a unique code of bits for each letter.

How should this mapping work? One option is to decide on the length of the codes, and then assign letters to codes in whatever way we wish. Choosing a code length of 2, we could assign codes as follows: a gets 00, b gets 01, c gets 10, and d gets 11. (Note that I chose a code length of 2 because it is the minimum that supports an alphabet of four letters. Using just one bit gives you only two choices | 0 and 1 | and that isn’t sufficient for our four-letter alphabet.) How many bits are required to encode text using this scheme? If we have a text of 50 letters, for example, then it takes 100 bits (two per letter) to encode the text.

Another option is to drop the requirement that codes be the same length, and assign the shortest possible codes to each letter. This might give us the following: a gets 0, b gets 1, c gets 10, and d gets 11. Notice that the codes for a and b are shorter than before, and that the codes for c and d are the same length as before. Using this scheme, we’ll very likely use fewer bits to encode text. For example, the text aaaaa takes only 5 bits, not 10!

Unfortunately, there’s a catch. Suppose that someone gives us the encoding 0011. What text does this code represent? It could be aabb if you take one character at a time from the code. However, it could also equally be cd, if you break up the code into its 00 (c) and 11 (d) pieces. Our encoding is ambiguous! Which is really too bad, because it seemed that we had a way to reduce the number of bits required to encode text. Is there some way we can still proceed with the idea of using variable-length codes?

To see how we can proceed, consider the following encoding scheme: a gets 1, b gets 00, c gets 010, and d gets 011. The trick here is that no code is a prefix of any other code. This kind of code is called a prefix code, and it leads to unambiguous decoding. For example, 0000 decodes to the text bb; there is no other possibility.

What we have here is seemingly the best of both worlds: variable-length codes (not fixed-length codes), and unambiguous decoding. However, note that some of our codes are now longer than before. For example, the code for c is now 010. That’s a three-bit code, even longer than the 2-bit codes we were getting with the fixed-length encoding scheme. This would be OK if c letters didn’t show up very often. If c letters were rare, then we don’t care much that they cause us to use 3 bits. If c letters did show up often, then we’d worry because we’d be spending 3 bits for every occurrence of c.

##### Goal of Algorithm
In general, as hinted above, we want to have short codes for frequently-occurring letters and longer codes for letters that show up less often. For example, if the frequency of a in our text is 10000 and the frequency of b in our text is 50, we’d hope that the code for a would be much shorter than the code for b.
Our goal is to generate the best prefix code for a given text. The best prefix code depends on the frequencies in the text. What do we mean by best prefix code? It’s the one that minimizes the average number of bits per symbol or, alternately, the one that maximizes the amount of compression that we get. If we let C be our alphabet, f (x) denote the frequency of symbol x, and d (x) denote the number of bits used to encode x, then we’re seeking to minimize the sum x 2 C f (x) d (x). That is, we want to minimize the sum of bits over all symbols, where each symbol contributes its frequency times its length.

Let’s go back to our four-letter alphabet: a, b, c, and d. Suppose that the frequencies of the letters in our text are as follows: a occurs 600 times, b occurs 200 times, c occurs 100 times, and d occurs 100 times. The best prefix code for these frequencies turns out to be the one we gave earlier: a gets 1, b gets 00, c gets 010, and d gets 011. Calculate the above sum and you’ll get a value of 1600. There are other prefix codes that are worse; for example: a gets 110, b gets 0, c gets 10, and d gets 111. Calculate the sum for this and convince yourself that it is worse than 1600!
Huffman’s algorithm makes use of binary trees to represent codes. Each leaf is labeled with a symbol from the alphabet. To determine the code for such a symbol, trace a path from the root to the symbol’s leaf. Whenever you take a left branch, append a 0 to the code; whenever you take a right branch, append a 1 to the code. The Huffman tree corresponding to the best prefix code above is as follows:

Huffman’s algorithm generates a tree corresponding to the best prefix code. You’ll see proofs of this fact in future courses; for now, you’ll implement the algorithm.

##### Preliminaries
For this assignment, I’m asking you to do some background reading on several topics that are not explicitly taught in the course. (I don’t think that we give students sufficient opportunity to research on their own and build on the available knowledge. This assignment is an attempt to remedy this.) Here’s what you’ll want to learn:

* Huffman’s algorithm. You’ll want to understand how Huffman’s algorithm works on a conceptual level before working on the implementation.
* Python bytes objects. We’ll be reading and writing binary files, so we’ll be using sequences of bytes (not sequences of characters). bytes objects are like strings, except that each element of a bytes object holds an integer between 0 and 255 (the minimum and maximum value of a byte, respectively). We will consider each byte in an uncompressed file as a symbol.
* Binary numbers. Background on binary numbers will be useful, especially when debugging your code.

You’re strongly encouraged to find and use online resources to learn this background material. Be sure to cite your sources in your assignment submission; include Python comments giving the locations of resources that you found useful.

### Application
Huffman Compression/Decompression involves the use of the Huffman algorithm to compress and decompress files of various sizes (ineffective if real uses but works on small files). Its decompress is inefficient to say the least. But compression works relatively quickly.

### Dependencies
* python-ta (optional)


### Deployment
* Main Files: huffman.py, nodes.py
* Sample Files: anything that isn't a python file
* Unittests: test_huffman_properties.py
* To compile, execute the huffman.py file and follow the instructions. 
###### Make sure to enter the file name without any extensions: book.txt must be inputted as book

