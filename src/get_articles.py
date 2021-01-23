import xml.sax
import sys
import os
from os import path, listdir
import re
import json
import time
import threading
import psutil
import bz2 
import glob

from xml_parser_withwrite import *

import faulthandler; faulthandler.enable()

page_ids_offset = {}
article_ids = set() 
OUTFOLDER = sys.argv[3]

def get_file_list(mypath):
	onlyfiles = [path.join(mypath, f) for f in listdir(mypath) if path.isfile(path.join(mypath, f))]
	onlyfiles.sort()
	return onlyfiles,len(onlyfiles)

def merge_xmls():
	print("Merging all xmls")
	os.system("xmlmerge "+OUTFOLDER+"*.xml > "+OUTFOLDER+"combine.xml")
	


def get_page_ids(folder_path):

	for file in glob.glob(folder_path+'*_subpages.txt'): 

		print("File from UT for page ids: ", file)
		with open(file, 'r') as f :
			line = f.readline()
			while(line):

				_,page_ids = line.strip("\n,").split(':')
				page_ids = page_ids.split(',')
  
				if page_ids[0] == '':
					line = f.readline()
					continue

				for pid in page_ids:
					page_ids_offset[pid] = -1
					article_ids.add(pid)

				line = f.readline()
	print("page ids in total = ", len(page_ids_offset), len(article_ids))

	

def get_indices(path):

	wiki_files, len_wiki_files = get_file_list(path)
	print("len_wiki_files = ", len_wiki_files)
	
	for it in range(len_wiki_files//2):
		print("\nFile :", wiki_files[it], wiki_files[it+len_wiki_files//2])
		index_file = wiki_files[it]
		article_file = wiki_files[it + len_wiki_files//2]
		
		if it <= 0 :
			continue
	   
		with bz2.BZ2File(index_file, "rb") as indf:
			
			ids_to_search = set()
			line = indf.readline()
			while(line):
				offset, id_title = line.decode('utf-8').strip().split(':',1)
				pageid,pg_title = id_title.split(':',1)           
				
				#append if this page is in our dataset
				if pageid in article_ids:
					page_ids_offset[pageid] = offset
					ids_to_search.add(pageid)
			
				line = indf.readline()
		print("len of ids to search from file = ", len(ids_to_search))
		print(ids_to_search)			
		#x = 0
		#line = artf.readline()
		#while(x<=400):
					
		#	print(line)
		# 	line = artf.readline()
		# 	x+=1
		#exit(0)
		print("Parsing XML")
		parse_xml_file(article_file, OUTFOLDER, ids_to_search)
		print("Parsing done\n")

		break
get_page_ids(sys.argv[1])
get_indices(sys.argv[2])
merge_xmls()


