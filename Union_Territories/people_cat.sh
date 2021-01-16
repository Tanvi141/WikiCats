#!/bin/bash
#SBATCH -A research 
#SBATCH --qos=medium
#SBATCH -c 1
#SBATCH --time=4-00:00:00
#SBATCH --mem-per-cpu=8192
#SBATCH --mail-type=END
#SBATCH -o cit_cats_op.txt 
#SBATCH --job-name=citmeowmeo

source ~/anaconda3/etc/profile.d/conda.sh
conda activate cats
cd /home2/sp504/IRE/
python3 /home2/sp504/WikiCats/get_cat_tree.py "Union Territories of India" 3970272 
