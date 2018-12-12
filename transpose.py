'''
Author:      Chary Vielma
Description: Program performs a matrix transpose given a text file containing 
             a 2D matrix. MPI is used to communicate each row from the root 
             process to all other processes. Each row is contained in a python
             dictionary. Root proceeds to collect each dictionary one process 
             at a time and generating the new tranposed matrix. 
'''

from mpi4py import MPI
import re

comm = MPI.COMM_WORLD # command line arg
size = comm.Get_size() # number of ranks in comm
rank = comm.Get_rank() # current rank

def readFile(file):
    try:
        lines = [re.sub(' +', ' ',line.rstrip('\n').rstrip()).lstrip() for line in open(file)]
        return [line.split(' ') for line in lines if line]
    except: 
        print 'Error reading text file, check format'

def generateDict(data):
    dataDict = {}
    for index, entry in enumerate(data):
        dataDict[index] = entry
    return dataDict

def transpose(file):
    data = None
    transpose = []
    inputMatrix = []

    # read and add file contents to 2d list, initialize output matrix to proper dimensions with 'None' type
    if rank == 0:
        inputMatrix = readFile(file)
        transpose = [[None for row in range(len(inputMatrix))] for col in range(len(inputMatrix[0]))]
    
    # dispurse 2d list to all processes in communicator
    data = comm.scatter(inputMatrix, root=0)
    
    # wait for all processes to proceed
    comm.barrier()
    
    # each process stores their row elements in a dictionary before transmitting
    myDict = generateDict(data)

    # if not root, send dictionary to root 
    if rank != 0:
        # blocking call, will therefore wait until received by root
        comm.send(myDict, dest=0)

    # if root, iterate through the size of the comm to access every rank and receive their row data
    else:
        for i in range(1, size):
            msgDict = {}
            msgDict = comm.recv(source=i)
            for key in sorted(msgDict):
                transpose[key][i] = msgDict[key]

    # wait for all processes to send their data to root
    comm.barrier()

    # if root, add own row values to the transpose matrix
    if rank == 0:
        for key in sorted(myDict):
            transpose[key][rank] = myDict[key]

        # output transpose matrix to screen
        for row in transpose:
            print row

def main():
    textFile = "input.txt"
    transpose(textFile)


if __name__ == '__main__':
    main()
