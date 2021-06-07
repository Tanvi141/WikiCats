#!/bin/bash
#SBATCH -n 8
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2G
#SBATCH --mail-type=END
#SBATCH -o adj_test_op.txt 
#SBATCH --job-name=adj_test
#SBATCH --time=1-00:00:00
#SBATCH -c 1

python3 LabelMatcher.py ../../data/subset/test_articles.txt
