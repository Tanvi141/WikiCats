#!/bin/bash
#SBATCH -n 8
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2G
#SBATCH --mail-type=END
#SBATCH -o adj_train_op.txt 
#SBATCH --job-name=adj_train
#SBATCH --time=4-00:00:00
#SBATCH -c 1

python3 LabelMatcher.py ../../data/subset/train_articles.txt
