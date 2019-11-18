#!/bin/sh


#export PYTHONPATH=$PYTHONPATH:/usr/python/:/usr/python/caffe:/usr/python/caffe/test:/usr/python/caffe/proto:/usr/python/caffe/imagenet

rm -rf ./result
mkdir -p result

time python -uB main.py | tee result/run.log



