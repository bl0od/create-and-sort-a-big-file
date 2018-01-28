import os
import time

start_time = time.time()
rec_size = 19


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

unsorted_file = open('bigfile.txt', 'rb')
p = 0
for i in range(2**16):
    records = []
    for j in range(52):
        unsorted_file.seek(unsorted_file.tell() + 22)
        record = unsorted_file.read(12)
        if record:
            record += bytes(','.encode('ascii')) + bytes(str(p).ljust(6).encode('ascii'))
            p += 1
        unsorted_file.seek(unsorted_file.tell() + 3)
        records.append(record)
    records.sort()
    run_name = 'runs/run' + str(i) + '.txt'
    runs.append(run_name)
    run = open(run_name, 'wb')
    for k in range(52):
        run.write(records[k])
    run.close()
# ------- end of making runs of level 0 ------- #


# ------- merge runs till remain two runs ------- #
while len(runs) != 2:
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


# ------- merge remained files and create sorted file ------- #
file1 = open('runs/run0.txt', 'rb')
file2 = open('runs/run1.txt', 'rb')
merged = open('runs/output.txt', 'wb')
file1_size = os.stat(file1.name).st_size
file2_size = os.stat(file2.name).st_size
m = 0
n = 0
while (m * rec_size < file1_size) and (n < file2_size):
    file1.seek(m * rec_size)
    file2.seek(n * rec_size)
    rec1 = file1.read(rec_size)
    rec2 = file2.read(rec_size)
    if rec1 < rec2:
        file1.seek(file1.tell() - 6)
        rec1_addr = int(file1.read(6).rstrip())
        unsorted_file.seek(rec1_addr * 37)
        rec1 = unsorted_file.read(37)
        merged.write(rec1)
        m += 1
    else:
        file2.seek(file2.tell() - 6)
        rec2_addr = int(file2.read(6).rstrip())
        unsorted_file.seek(rec2_addr * 37)
        rec2 = unsorted_file.read(37)
        merged.write(rec2)
        n += 1

while m * rec_size < file1_size:
    file1.seek((m * rec_size) + 13)
    rec_addr = int(file1.read(6).rstrip())
    unsorted_file.seek(rec_addr * 37)
    rec = unsorted_file.read(37)
    merged.write(rec)
    m += 1

while n * rec_size < file2_size:
    file2.seek((n * rec_size) + 13)
    rec_addr = int(file2.read(6).rstrip())
    unsorted_file.seek(rec_addr * 37)
    rec = unsorted_file.read(37)
    merged.write(rec)
    n += 1
merged.close()
# ------- end of merging ------- #


os.remove('runs/run0.txt')
os.remove('runs/run1.txt')
os.rename(merged.name, 'sorted_file.txt')
print("--- %s seconds ---" % (time.time() - start_time))
