# File to open and break apart
import os.path
import sys
import hashlib
fileR = open(sys.argv[1], "rb")

chunk = 0
chunkSize = int(sys.argv[2])

save_path = '/home/nehal/veritas/'
nameOfFile = sys.argv[1].split('.')[0]


def backup(nameOfFile):
    # add a _metadata file to the directory
    chunk = 0
    Meta = open(os.path.join(save_path, nameOfFile, "_metadata.txt"), "w")
    Hashes = open(os.path.join(save_path, nameOfFile, "_hash.txt"), "a")
    Meta.write("chunkSize: " + str(chunkSize))
    Meta.write("\n")

    byte = fileR.read(chunkSize)
    print("Starting to backup " + sys.argv[1] +
          " in chunks of " + str(chunkSize) + " bytes")
    while byte:

        # Open a temporary file and write a chunk of bytes
        fileN = "chunk" + str(chunk) + ".txt"
        print("Writing chunk " + str(chunk) + " to " + fileN)
        FileN = os.path.join(save_path, nameOfFile) + \
            '/chunk' + str(chunk) + ".txt"
        fileT = open(FileN, "wb")
        fileT.write(byte)
        fileT.close()
        Hashes.write(hashlib.sha256(byte).hexdigest())
        Hashes.write("\n")
        byte = fileR.read(chunkSize)

        chunk += 1

    print("Backup complete. " + str(chunk) + " chunks created.")

    # number of chunks in _metadata file
    Meta.write("chunks: " + str(chunk))
    Meta.close()
    Hashes.close()
# check if hash of the chunk is changes then replace it with new chunk


def replaceChunksWithHash(nameOfFile):
    # chnaged to check hash change
    changed = False
    # open hash file
    Hashes = open(os.path.join(save_path, nameOfFile, "_hash.txt"), "r")
    hashes = Hashes.readlines()
    Hashes.close()

    # open metadata file
    Meta = open(os.path.join(save_path, nameOfFile, "_metadata.txt"), "a+")
    content = Meta.readlines()
    Meta.close()
    # number of chunks
    chunks = content[1].split(' ')[1]
    chunks = int(chunks)
    # chunk size
    size = int(content[0].split(' ')[1])
    # Piece the file together using all chunks from the given directory
    chunk = 0
    byte = fileR.read(size)

    while byte:
        # Open a temporary file and write a chunk of bytes
        fileN = os.path.join(save_path, nameOfFile) + \
            '/chunk' + str(chunk) + ".txt"
        # fileT = open(fileN, "rb")
        if (chunk >= chunks or hashes[chunk][:-1] != hashlib.sha256(byte).hexdigest()):
            # fileT.close()
            changed = True
            if (chunk >= chunks):

                hashes.append(hashlib.sha256(byte).hexdigest()+'\n')
                print("hash of chunk " + str(chunk) + " is created")

            else:
                hashes[chunk] = hashlib.sha256(byte).hexdigest()+'\n'
                print("hash of chunk " + str(chunk) + " is changed")

            fileT = open(fileN, "wb")
            fileT.write(byte)
            fileT.close()
        # fileT.close()
        # print(hashes[chunk][:-1],hashlib.sha256(byte).hexdigest())

        byte = fileR.read(size)
        chunk += 1
    if (chunk!=chunks):
        Meta = open(os.path.join(save_path, nameOfFile, "_metadata.txt"), "w")
        Meta.write("chunkSize: " + str(chunkSize))
        Meta.write("\n")
        Meta.write("chunks: " + str(chunk))
        Meta.close()
    if (chunk!=chunks):
        Hashes = open(os.path.join(save_path, nameOfFile, "_hash.txt"), "w")
        c = 0
        for i in range(chunk):
            # print(i)
            Hashes.write(hashes[i])

            c += 1
        Hashes.close()
        while(chunk<chunks):
            fileN = os.path.join(save_path, nameOfFile) + \
            '/chunk' + str(chunk) + ".txt"
            print("Removed chunk"+str(chunk))
            
            #remove file    
            os.remove(fileN)
            chunk+=1

# print(nameOfFile)
# make directory with name of 1
if (not os.path.exists(os.path.join(save_path, nameOfFile))):
    # print("idhar")
    os.mkdir(os.path.join(save_path, nameOfFile))
    backup(nameOfFile)
else:
    replaceChunksWithHash(nameOfFile)
