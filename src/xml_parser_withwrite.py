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
from lxml import etree

article_id_name_file = "article_id_name.txt"

class WikiHandler(xml.sax.ContentHandler):
	
	def __init__(self, write_folder, article_ids):
		self.data = ""
		self.page_count = 0
		self.id = ''
		self.id_capture = False
		self.write_folder = write_folder
		self.article_ids = article_ids
		self.stack = []
		self.id_stack = []
		self.open = False
		self.elem = None
		self.writers = {}
		self.text = []
		self.title = ''

	def _get_writer(self, filename):
		with etree.xmlfile(filename) as xf:
			with xf.element('article'):
				while True:
					el = (yield)
					xf.write(el)
					xf.flush()  # maybe don't flush *every* write

	def _write(self):
		writer = self.writers[self.id] = self._get_writer(self.write_folder+str(self.id)+".xml")
		next(writer)
		writer.send(self.elem)  # write out current `<measure>`
		self.elem = None

	def _add_text(self):
		if self.elem is not None and self.text:
			if self.open:
				self.elem.text = ''.join(self.text)
			else:
				self.elem.tail = ''.join(self.text)
			self.text = []


   # Call when an element starts
	def startElement(self, tag, attributes):
		self.data = ''

		if self.id_capture == False and tag == "id":
			self.elem = etree.Element(tag)
			self.open = True         
			#self.id_stack.append(self.elem)
			#if len(self.id_stack) > 1:
			#	self.id_stack[-2].append(self.elem)


		if self.stack or tag == "page":
			self._add_text()
			self.open = True
			self.elem = etree.Element(tag)         
			self.stack.append(self.elem)
			if len(self.stack) > 1:
				self.stack[-2].append(self.elem)

	# Call when an elements ends
	def endElement(self, tag):

		if tag == 'id':
			if not self.id_capture:
				self.id = self.data
				self.data = ''
				self.id_capture = True      
				if self.id not in self.article_ids:
					self.stack.clear()
				else:
					with open(self.write_folder+article_id_name_file, 'a+') as of:
						of.write(self.id+":"+self.title+"\n")

		if self.stack:

			self._add_text()
			self.open = False
			self.elem = self.stack.pop()            
			if not self.stack:
				self._write()

		if tag == "page":
			self.id_capture = False
			self.page_count+=1
			self.id_capture = False
			self.data = ""
			self.id = ''
			self.title = ''

		elif tag == "title":
			self.title = self.data
			self.data = ''
			  

	# Call when a character is read
	def characters(self, content):
		self.data += content 


		if self.elem is not None:
			self.text.append(content)

	def endDocument(self):
		print("Reached end document")
		# clean up
		k = 0
		for writer in self.writers:
			if k==0:
				print("closing all files")
				k+=1
			self.writers[writer].close()
		print("didn't get stuck in end document")



def parse_xml_file(article_file, write_folder, article_ids):

	# create an XMLReader
	parser = xml.sax.make_parser()
	# # turn off namepsaces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	# override the default ContextHandler
	Handler = WikiHandler(write_folder, article_ids)
	parser.setContentHandler( Handler )
	
	with bz2.BZ2File(article_file, "rb") as artf:
		parser.parse(artf)
	print("finished parsing from parser funciton")

