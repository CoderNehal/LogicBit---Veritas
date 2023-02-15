# Open original file for reconstruction
import sys,os.path
fileM = open("[Restored]" + sys.argv[1], "wb")

folder_name = sys.argv[1].split('.')[0]
# open _metadata.txt from folder with name 
save_path = '/home/nehal/veritas/'

#open metadata file 
path = os.path.join(save_path,folder_name) + '/_metadata.txt'

f = open(path,'r')
content = f.readlines()

# number of chunks



chunk = 0
chunks = content[1].split(' ')[1];
chunks = int(chunks);
# Piece the file together using all chunks from the given directory
while chunk < chunks:
    # Open a temporary file and write a chunk of bytes
    fileN = os.path.join(save_path,folder_name) +'/chunk' + str(chunk) + ".txt"
    fileT = open(fileN, "rb")
    byte = fileT.read()
    fileM.write(byte)
    fileT.close()
 
    chunk += 1