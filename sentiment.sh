#!/bin/bash
python3 /home/ubuntu/wenti-data/main.py --sentiment
until /home/ubuntu/wenti-data/main.py --sentiment; do
    python3 /home/ubuntu/wenti-data/main.py --sentiment
    sleep 1
done
