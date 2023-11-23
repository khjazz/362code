# File: lab11a.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

# Modify code below
from multiprocessing import Pipe, Process

SENTINEL = -1

def not_multiple(conn_in, conn_out, num):
    while True:
        obj = conn_in.recv()
        if obj == SENTINEL:
            conn_out.send(SENTINEL)
            break
        if not obj % num == 0 or obj == num:
            conn_out.send(obj)

if __name__ == "__main__":
    conn1_in, conn1_out = Pipe(False)
    conn2_in, conn2_out = Pipe(False)
    conn3_in, conn3_out = Pipe(False)
    conn4_in, conn4_out = Pipe(False)
    conn5_in, conn5_out = Pipe(False)

    Process(target=not_multiple, args=[conn1_in, conn2_out, 2]).start()
    Process(target=not_multiple, args=[conn2_in, conn3_out, 3]).start()
    Process(target=not_multiple, args=[conn3_in, conn4_out, 5]).start()
    Process(target=not_multiple, args=[conn4_in, conn5_out, 7]).start()

    for i in range(2, 100):
        conn1_out.send(i)
    conn1_out.send(SENTINEL)
    while True:
        obj = conn5_in.recv()
        if obj == SENTINEL:
            break
        print(obj, end=" ", flush=True)

"""
With reference to the above pipe_unidir.py program, write a program that contains a
not_multiple() function and has 4 child processes and 5 pipes.
The function not_multiple(conn_in, conn_out, num) passes from conn_in to conn_out the
integer num and integers that are not multiples of num. For example, when num is 3, the function
passes 1, 2, 3, 4, 5, 7, 8, 10, 11, 13, etc (i.e. it does not pass 6, 9, 12, etc).
The main process, 4 child processes, and 5 unidirectional pipes work as follows:
• The main process sends integers from 2 to 99 (both inclusive) to the first child process.
• The first child process removes multiples of 2 (except 2 itself) and sends the remaining integers
to the second child process.
• The second child process removes multiples of 3 (except 3 itself) and sends the rest to the third
child process.
• The third and fourth child processes do similar tasks by removing multiples of 5 and 7, respectively, in the integers they receive.
• The main process receives integers from the fourth child process and print them out.
The results are the prime numbers between 2 and 99!
2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97
Write the program in the lab11a.py file for submission. Remember to enforce good programming
style in your code
"""