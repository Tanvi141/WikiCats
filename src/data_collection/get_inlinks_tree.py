#!/usr/bin/python

import xml.sax
import sys
import os
from os import path, listdir

import re
import json
import time
import threading
import psutil
import requests
import collections

# GLOBAL VARIABLES
CHUNK = 1000
threads = []
article_id_name = {}
ut_page_ids = set()

'''
Function to create new directories
'''
#function to create directories to store results
def create_directory(folder_path):
    my_path = os.getcwd()
    my_path = my_path + '/' +folder_path
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    return my_path

def get_file_list(mypath):
    onlyfiles = [path.join(mypath, f) for f in listdir(mypath) if path.isfile(path.join(mypath, f))]
    return onlyfiles,len(onlyfiles)

def dummy(n):
    print("thread ", n)
    time.sleep(10)
    print("slept 10 for",n)

'''
Class handler to manage and parse 
the XML wiki data accordingly.
'''
class WikiHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.CurrentData = ""
        self.data = ""
        self.page_count = 0
        self.title = ''
        self.text = ''
        self.id = ''
        self.id_capture = False

        self.page_titles = []
        self.page_texts = []
        self.page_ids = []

   # Call when an element starts
    def startElement(self, tag, attributes):
        self.data = ''

    # Call when an elements ends
    def endElement(self, tag):

        if tag == "page":

            self.page_titles.append(self.title)
            self.page_texts.append(self.text)
            self.page_ids.append(self.id)
            self.page_count+=1
            self.id_capture = False

            #create a new thread for every CHUNK pages
            if(self.page_count%CHUNK == 0):
                
                # print("new thread for ", self.page_count, "...")
                # t = threading.Thread(target=process_chunk_pages, args=(self.page_titles, self.page_texts, self.page_ids,))
                # threads.append(t)
                # t.start()

                process_chunk_pages(self.page_titles, self.page_texts, self.page_ids,)

                #reset page arrays
                self.page_titles.clear()
                self.page_texts.clear()
                self.page_ids.clear()
                # exit(0)

        elif tag == "title":
            self.title = self.data
            self.data = ''

        elif tag == "text":
            self.text = self.data
            self.data = ''

        elif tag == 'id':
            if not self.id_capture:
                self.id = self.data
                self.data = ''
                self.id_capture = True

        elif tag == 'mediawiki':
            
            # print("new thread for ", self.page_count, "...")
            # t = threading.Thread(target=process_chunk_pages, args=(self.page_titles, self.page_texts, self.page_ids,))
            # threads.append(t)
            # t.start()

            #collect all threads
            # for t in threads:
                # t.join()

            process_chunk_pages(self.page_titles, self.page_texts, self.page_ids,)

            #reset page arrays
            self.page_titles.clear()
            self.page_texts.clear()
            self.page_ids.clear()     
                        

    # Call when a character is read
    def characters(self, content):
        self.data += content    


'''
Function to process CHUNK sized pages at a time
Each CHUNK will be processed by an individual thread.
'''

def process_chunk_pages(all_title, text, ids):

    print(len(all_title), "title chunk", all_title[0])
    for i in range(len(all_title)):
        try:
            create_inlinks(all_title[i],text[i],ids[i])
        except:
            print(i, len(all_title))
            sys.exit(0)



'''
Function to get all the inlink article edges 
from a given text for an article
'''
def get_edges(text,count_tokens=False):
    
    to_articles = re.findall(r"\[\[(.*?)\]\]", text)
    inlinks = [art.split('|')[0] for art in to_articles]

    #get the pageIDs for the corresponding page titles
        # url = (
        #     'https://en.wikipedia.org/w/api.php'
        #     '?action=query'
        #     '&prop=info'
        #     '&inprop=subjectid'
        #     '&titles=' + '|'.join(to_articles) +
        #     '&format=json')
        # json_response = requests.get(url).json()

        # title_to_page_id  = {
        #     page_info['title']: page_id
        #     for page_id, page_info in json_response['query']['pages'].items()}

        # print(title_to_page_id)
        # print([title_to_page_id[title] for title in to_articles])

    inlink_ids = [article_id_name[art] for art in inlinks if art in article_id_name]

    return(inlink_ids)

'''
Function to extract the infobox from the 
pages of the wikipedia dump
'''

def get_infobox(text):
    
    ind = [m.start() for m in re.finditer(r'{{Infobox|{{infobox|{{ Infobox| {{ infobox', text)]
    ans = []
    for i in ind:
        counter = 0
        end = -1
        for j in range(i, len(text)-1):
            if text[j]=='}' and text[j+1] =='}':
                counter-=1
            elif text[j]=='{' and text[j+1] =='{':
                counter+=1

            if counter == 0:
                end=j+1
                break
        
        ans+= get_edges(text[i:end+1])
    
    return ans

'''
Function to extract the categoris, from the body of the page.
'''

def get_categories(text):
    
    lis = re.split(r"\[\[Category|\[\[ Category", text,1)
    #storing the value for cateogories
    if len(lis)==1:
        category=''
    else:
        category = lis[1]

    return category



'''
Function to create the inlinks for the article
Weighing criteria for the inlinks is as follows :
wt = num_occurances*(10^(isInfobox))
'''
def create_inlinks(title, text, a_id):
    
    categories = get_categories(text)

    text_edges = get_edges(text)
    info_edges = get_infobox(text)

    # print(text_edges, "full text edges")
    # print(info_edges, "infoedges")

    #preparing adjacency list for this article
    count_e = collections.Counter(text_edges)
    count_i = collections.Counter(info_edges)
    all_inlinks = ({int(k): count_e[k] + count_i[k]*10 for k in set(text_edges) | set(info_edges)})
    all_inlinks = dict(sorted(all_inlinks.items()))

    # print(all_inlinks)
    to_write = str(a_id)+":"

    for a_id, count in all_inlinks.items():
        to_write+=str(a_id)+"-"+str(count)+","

    to_write+="\n"
    with open(ADJ_INLINKS_FILE,'a+') as f:
        f.write(to_write)


def create_id_name_json(file):

    with open(file, 'r') as f:
        line = f.readline().strip()
        while(line):
            a_id, a_name = line.split(':',1)
            ut_page_ids.add(a_id)
            article_id_name[a_name] = a_id
            line = f.readline().strip()



article_dump = sys.argv[1]
ADJ_INLINKS_FILE = sys.argv[2]

print("creating json ...")
article_id_name_file = sys.argv[3]
create_id_name_json(article_id_name_file)

print("starting parsing ...")
start = time.time()

# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# override the default ContextHandler
Handler = WikiHandler()
parser.setContentHandler( Handler )
parser.parse(article_dump)

print("Total required Time = ", time.time() - start)