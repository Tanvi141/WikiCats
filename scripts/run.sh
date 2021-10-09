#!/bin/bash
#SBATCH -n 1
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2048
#SBATCH --mail-type=END
#SBATCH -o op.txt 
#SBATCH --job-name=cat_from_art
#SBATCH --time=4-00:00:00
#SBATCH -c 8

cd ../src/data_collection/
python3 get_categories_for_articles.py

