#!/usr/bin/env bash

# ATTENTION: script should be called from Task3 dir!

gdown --id 1YbGrSbcanFTKFbIaH-kKDcaqXy4JdNeG
mkdir -p ../MeshCNN/checkpoints/primitives
mv latest_net.pth ../MeshCNN/checkpoints/primitives