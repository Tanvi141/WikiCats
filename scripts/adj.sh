#!/bin/bash
#SBATCH -n 1
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2G
#SBATCH --mail-type=END
#SBATCH -o op.txt 
#SBATCH --job-name=adj
#SBATCH --time=4-00:00:00
#SBATCH -c 8

cd ../src/parse_tree/
python3 LabelMatcher.py ../../data/subset/val_articles.txt
