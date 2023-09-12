# File: lab01.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

from random import random

def palindrome_recur(s):
    if len(s) == 0 or len(s) == 1:
        return True
    return s[0] == s[-1] and palindrome_recur(s[1:-1])

def myth_value(n):
    count = 0
    for i in range(n):
        x = random()
        y = random()
        if x*x + y*y < 1:
            count = count + 1
    return count / n*4

if __name__ == "__main__":
    print(palindrome_recur(''))
    print(palindrome_recur('a'))
    print(palindrome_recur('abcba'))
    print(palindrome_recur('abba'))
    print('not')
    print(palindrome_recur('great'))
    print(palindrome_recur('no'))
    print(myth_value(10**6))