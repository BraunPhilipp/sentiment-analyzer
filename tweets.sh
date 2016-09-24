#!/bin/bash
python3 /home/ubuntu/wenti-data/main.py --tweets
until /home/ubuntu/wenti-data/main.py --tweets; do
    python3 /home/ubuntu/wenti-data/main.py --tweets
    sleep 1
done
