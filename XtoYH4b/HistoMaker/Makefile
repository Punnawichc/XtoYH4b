#!/bin/bash
FILE=$1

echo ${FILE}
g++ -g -fno-stack-protector  `root-config --cflags` -I/usr/local/include ${FILE}.C -o ${FILE}.exe `root-config --glibs` -lMinuit
