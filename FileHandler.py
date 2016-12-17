import gzip

def extract(filePath, copy):
    e = gzip.open(str(filePath), 'rb').read()
    print (str(filePath + ' opened'))
    if copy:
        f = open(str(filePath + '.xml'), 'w')
        f.write(e.decode('utf-8'))
        f.close()
        print (str('copy written: ' + filePath + '.xml'))
    return e

def compact(data, filePath):
    f = open(str(filePath), 'w')
    f.close()
    with gzip.open(str(filePath), 'wb') as f:
        f.write(data)