# File: pipe_unidir.py
from multiprocessing import Pipe, Process

SENTINEL = -1

def divisible(conn_in, conn_out, num):
    while True:
        obj = conn_in.recv()
        if obj == SENTINEL:
            conn_out.send(SENTINEL)
            break
        if obj % num == 0:
            conn_out.send(obj)

if __name__ == "__main__":
    conn1_in, conn1_out = Pipe(False)
    conn2_in, conn2_out = Pipe(False)
    conn3_in, conn3_out = Pipe(False)
    Process(target=divisible, args=[conn1_in, conn2_out, 2]).start()
    Process(target=divisible, args=[conn2_in, conn3_out, 5]).start()
    for i in range(100):
        conn1_out.send(i)
    conn1_out.send(SENTINEL)
    while True:
        obj = conn3_in.recv()
        if obj == SENTINEL:
            break
        print(obj, end=" ", flush=True)
