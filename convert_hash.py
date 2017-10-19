class pc:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'

def getPrimaryKey(record):
    start = record.find('(') + 1
    end = record.find(',')
    return record[start:end]

def getPath(line):
    start = line.find('\"') + 1
    end = line[start:].find('\"') + start - 1
    return line[start:end].replace('{$webResourceDomain}','')

def getBody(record):
    start = record.find('<')
    end = record[start:].find(',') + start
    return record[start:end]

def replaceHash(line):
    path = getPath(line)
    start = line.find('\"') + 1
    end = line[start:].find('\"') + start - 1
    print(pc.RED + line + pc.END + "\n" + line[:start] + '{hash path=\"' + path + '}' + line[end:] + "\n")
    return line[:start] + '{hash path=\"' + path + '}"' + line[end:]

mst_file = open('AnnounceMst.txt','r', encoding='utf-8')
records = mst_file.readlines()

output_records = []
for i in range(2, len(records)):
    out_body = ''
    body = getBody(records[i])
    lines = body.split("\\r\\n")
    for j in range(0, len(lines)):
        if lines[j].find('webResourceDomain') != -1 and (lines[j].find('announce') != -1 or lines[j].find('banner') != -1):
            out_body = out_body + replaceHash(lines[j]) + '\n'
        else:
            out_body = out_body + lines[j] + '\n'
    output_records.append('(' + getPrimaryKey(records[i]) + ',\"' + out_body + '\"),')

output_file = open('output.txt','w')
output_file.writelines(output_records)

mst_file.close()
output_file.close()
