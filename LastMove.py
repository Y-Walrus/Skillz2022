# The purpose of this code is to win the Skillz 2022 coding competition
# Creators: Ben Solomovitch, Ron Bar-El, Yael Meshar, Yegor Stolyarsky
# 01.2022 - ?

# modules we are allowed to import
import collections
import operator
import random
import re
import math
import itertools
import traceback
import abc

def Yegor():
    x = input("Enter your name:")
    print("Hello"+x)

def Ezert(x):
    for i in range(1, x):
        x=x*i
    return x

def Ezert2(x):
    if(x>1):
        return x*Ezert2(x-1)
    return x

print(Ezert2(5))





# note functions we are not allowed to use
