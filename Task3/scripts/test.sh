#!/usr/bin/env bash

## run the test and export collapses
python test.py \
--dataroot primitives \
--name primitives \
--phase valid \
--ncf 64 128 256 256 \
--pool_res 1200 900 600 420 \
--norm group \
--resblocks 1 \
--export_folder meshes