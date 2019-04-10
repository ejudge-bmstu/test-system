import os
fin_name = os.path.dirname(os.path.realpath(__file__)) + "/" + "db_dump.sql"
fout_name = os.path.dirname(os.path.realpath(__file__)) + "/" +"db_dump_test.sql"

buffer = []

with open(fin_name, "r") as fin:
    for line in fin:
        buffer.append(line)

d_count = 0
for i in range(len(buffer) - 1, -1, -1):
    if buffer[i].find("FOREIGN KEY") != -1:
        del buffer[i]
        d_count += 1
    elif d_count > 0:
        del buffer[i]
        d_count -= 1

with open(fout_name, "w") as fout:
    for line in buffer:
        fout.write(line)
    
        
