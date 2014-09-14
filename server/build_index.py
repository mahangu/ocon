import sys
import os

from whoosh.fields import Schema, TEXT, STORED
from whoosh.index import create_in, open_dir
from whoosh.query import *
import nltk.data

SCHEMA = Schema(textfile=TEXT(stored=True),
                content=TEXT(stored=True))

def get_file_lines(filename):
	lines_seen = set() # holds lines already seen
	for line in open(filename, "r"):
		if line not in lines_seen: # not a duplicate
			lines_seen.add(line)
		
		outfile = open(filename, "w")
		for item in lines_seen:
			outfile.write("%s\n" % item)
		outfile.close()
		
	lines = tuple(lines_seen)
	return lines

def add_files(dirname):
	if not os.path.exists(CORPUS_INDEX):
		os.mkdir(CORPUS_INDEX)
	ix = create_in(CORPUS_INDEX,SCHEMA)
	
	for file in os.listdir(dirname):
		if file.endswith(".txt"):
			
			#Deprecated - used this when we were reading entire files intead of line by line.
			raw_file = open(dirname + file, "r")
			text_file = raw_file.read()
			raw_file.close()
			
			#Deprecated - use this when we were reading lines instead of sentences (thank you, NLTK!).
			#file_lines = get_file_lines(dirname + file)
			
			text_file = unicode(text_file,errors='replace')
			
			sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
			sentences = tuple(sentence_detector.tokenize(text_file.strip()))
			
			
			for sentence in sentences:
				if sentence!="" or None:
					writer = ix.writer()
					writer.add_document(textfile=unicode(file),content=sentence)
					writer.commit()


	
if __name__ == "__main__":			
	
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--corpus")
	args = parser.parse_args()
	
	if args.corpus!=None:
		CORPUS_NAME = args.corpus
		CORPUS_INDEX = "data/" + CORPUS_NAME + "-index"
		CORPUS_FILES = "data/" + CORPUS_NAME + "-text/"
		add_files(CORPUS_FILES)
	else:
		CORPUS_NAME = "ocon"	
		CORPUS_INDEX = "data/" + CORPUS_NAME + "-index"
		CORPUS_FILES = "data/" + CORPUS_NAME + "-text/"

