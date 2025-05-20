#!/bin/bash
FILE=$1

ONNX_INCLUDE="/afs/desy.de/user/c/chokepra/private/XtoYH4b/tools/onnx_runtime_prebuilt/onnxruntime-linux-x64-1.17.1/include"
ONNX_LIB="/afs/desy.de/user/c/chokepra/private/XtoYH4b/tools/onnx_runtime_prebuilt/onnxruntime-linux-x64-1.17.1/lib"

echo "Checking ONNX paths..."
echo "ONNX_INCLUDE = ${ONNX_INCLUDE}"
echo "ONNX_LIB     = ${ONNX_LIB}"

echo ${FILE}
g++ -g -fno-stack-protector  `root-config --cflags` -I/usr/local/include $(correction config --cflags --ldflags --rpath) ${FILE}.C -o ${FILE}.exe `root-config --glibs` -lMinuit -I${ONNX_INCLUDE} -L${ONNX_LIB} -lonnxruntime

