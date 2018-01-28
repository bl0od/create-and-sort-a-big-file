import random
from random import randrange
import string
import time

"""
    a method for create a random record.
    record contains of fields: first name(10 bytes), last name(10 bytes),
    student number(12 bytes) and grade (2 bytes).
    return a random 37 bytes length record
"""
def rand_record():
    first_name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    last_name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    record = (first_name + "," + last_name + "," + str(randrange(933000000000, 933999999999)) + "," + str(
        randrange(0, 20))).ljust(37)
    return record
# ----- end of method rand_record ----- #

start_time = time.time()

# create a big file with 1,000,000 record
with open("bigfile.txt", "wb") as file:
    for i in range(10 ** 6):
        data = bytes(rand_record().encode('ascii'))
        file.write(data)

print("--- %s seconds ---" % (time.time() - start_time))