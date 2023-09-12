# File: lab00.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

def primes(n):
    ls = []
    for i in range(2, n):
        if all(i % j != 0 for j in range(2, int(i ** 0.5) + 1)):
            ls.append(i)
    return ls

def display_triangle(n):
    for i in range(1, n+1):
        print('*'*i)

def goldbach(n):
    if n <= 5:
        return None
    for x in primes(n):
        for y in primes(n):
            for z in primes(n):
                if x + y + z == n:
                    return [x,y,z]

if __name__ == "__main__":
    display_triangle(10)
    for i in range(100, 110):
        print(i, goldbach(i))

