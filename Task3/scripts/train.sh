#!/usr/bin/env bash

# ATTENTION: script should be called from Task3 dir!

python ../MeshCNN/train.py \
--dataroot ../MeshCNN/primitives \
--checkpoints_dir ../MeshCNN/checkpoints \
--name primitives \
--ncf 64 128 256 256 \
--pool_res 1200 900 600 420 \
--ninput_edges 2000 \
--norm group \
--resblocks 1 \
--flip_edges 0.2 \
--slide_verts 0.2 \
--num_aug 20 \
--niter 15 \
--niter_decay 10 \
--print_freq 50