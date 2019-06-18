#!/usr/bin/python
# encoding:utf-8
from analysis import *


def find_same():
    df = pd.read_csv(r'../templates/123.csv')
    for code in df.values:
        print code
    print 123


find_same()
