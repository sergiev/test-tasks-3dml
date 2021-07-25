#!/usr/bin/env bash

cp sklearn_test.py MeshCNN
python MeshCNN/sklearn_test.py \
--dataroot primitives \
--name primitives \
--phase $1 \
--ncf 64 128 256 256 \
--pool_res 1200 900 600 420 \
--ninput_edges 2000 \
--norm group \
--resblocks 1