import os
import time

start_time = time.time()
rec_size = 37



"""
    a method for merging two files
    return a file that contains merged contents
"""
def merge (file1, file2):
    output = open('runs/output.txt', 'wb')
    file1_size = os.stat(file1.name).st_size
    file2_size = os.stat(file1.name).st_size
    i = 0
    j = 0
    while (i * rec_size < file1_size) and (j < file2_size):
        file1.seek(i * rec_size)
        file2.seek(j * rec_size)
        rec1 = file1.read(rec_size)
        rec2 = file2.read(rec_size)
        if rec1 < rec2:
            output.write(rec1)
            i += 1
        else:
            output.write(rec2)
            j += 1

    while i * rec_size < file1_size:
        file1.seek(i * rec_size)
        rec = file1.read(rec_size)
        output.write(rec)
        i += 1

    while j * rec_size < file2_size:
        file2.seek(j * rec_size)
        rec = file2.read(rec_size)
        output.write(rec)
        j += 1

    output.close()
    return output
# ------- end of method merge ------- #



# ------- making runs of level 0 ------- #
runs = []

with open('bigfile.txt', 'rb') as unsorted_file:

    for i in range(2**17):
        records = []
        for j in range(27):
            record = unsorted_file.read(rec_size)
            records.append(record)
        records.sort()
        run_name = 'runs/run' + str(i) + '.txt'
        runs.append(run_name)
        run = open(run_name, 'wb')
        for k in range(27):
            run.write(records[k])
        run.close()
# ------- end of making runs of level 0 ------- #



# ------- merge runs ------- #
while len(runs) != 1:
    runs_temp = runs.copy()
    runs.clear()
    k = 0
    for i in range(0, len(runs_temp), 2):
        files = [open('runs/run' + str(i) + '.txt', 'rb'), open('runs/run' + str(i + 1) + '.txt', 'rb')]
        merged = merge(files[0], files[1])
        os.remove('runs/run' + str(i) + '.txt')
        os.remove('runs/run' + str(i + 1) + '.txt')
        os.rename(merged.name, 'runs/run' + str(k) + '.txt')
        runs.append('runs/run' + str(k) + '.txt')
        k += 1
# ------- end of while ------- #

os.rename('runs/run0.txt', 'sorted_file.txt')
print("--- %s seconds ---" % (time.time() - start_time))
