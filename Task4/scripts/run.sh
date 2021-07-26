#!/usr/bin/env bash

# ATTENTION: script should be called from Task4 dir!

python ../MeshCNN/run.py \
--dataroot ../MeshCNN/primitives \
--checkpoints_dir ../MeshCNN/checkpoints \
--name primitives \
--ncf 64 128 256 256 \
--pool_res 1200 900 600 420 \
--ninput_edges 2000 \
--norm group \
--resblocks 1 \
--gpu_ids -1