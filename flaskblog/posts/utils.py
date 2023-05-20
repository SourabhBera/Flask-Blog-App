
def convertToBinaryData(filename):
    # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData





def convertToOriginalData(data, newfilename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(newfilename, 'wb') as file:
        file.write(data)


