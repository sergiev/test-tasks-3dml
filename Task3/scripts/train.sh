#!/usr/bin/env bash

## run the training
python MeshCNN/train.py \
--dataroot primitives \
--name primitives \
--ncf 64 128 256 256 \
--pool_res 1200 900 600 420 \
--ninput_edges 2000 \
--norm group \
--resblocks 1 \
--flip_edges 0.2 \
--slide_verts 0.2 \
--num_aug 20 \
--niter 25 \
--niter_decay 15 \
--print_freq 50