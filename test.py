import os

file = "training_demo/annotations/list_attr_img.txt"

with open(file, 'r') as fp:
    data = fp.readlines()

attr = data[2].split()[1:]

for i in range(len(attr)):
    if attr[i] != '-1':
        print(i, attr[i])

# print(len(attr))