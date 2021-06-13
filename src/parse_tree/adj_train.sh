#!/bin/bash
#SBATCH -n 1
#SBATCH --mem-per-cpu=8G
#SBATCH -o adj_train_op.txt 
#SBATCH --job-name=adj_train
#SBATCH --time=1-00:00:00
#SBATCH -c 8

source ~/.bashrc
conda activate cats
python3 LabelMatcher.py ../../data/subset/train_articles.txt
