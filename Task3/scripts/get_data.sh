DATA_DIR=primitives
if [ -d "$DATA_DIR" ]; then
    echo "WARNING: directory '$DATA_DIR' already exists. Download is canceled."
    exit 1
fi
gdown --id 1xM5diKjMbp_PfNu--JG2A-ZeFk9TLkks
unzip -q dataset-v2.zip
rm dataset-v2.zip
rm -rf $DATA_DIR
mv dataset-v2 $DATA_DIR