import sys
import os

from whoosh.fields import Schema, TEXT, STORED
from whoosh.index import create_in, open_dir
from whoosh.query import *

import tornado.ioloop
import tornado.web

import nltk

SCHEMA = Schema(textfile=TEXT(stored=True),
                content=TEXT(stored=True))


def search(term, max_results):
	#Should probably bring search into this function later on. For some reason I can't seem to pass the results object back correctly.
	ix = open_dir(INDEX_NAME)
	from whoosh.qparser import QueryParser
	with ix.searcher() as searcher:
		query = QueryParser("content", SCHEMA).parse(unicode(term))
		results = searcher.search(query, limit=max_results)
		return results
	
## Tornado Handlers below this point!	
	
class MainHandler(tornado.web.RequestHandler):
    def get(self):
		html_header = open("templates/header.html").read() #I reuse this code in all handles so will bundle into a function soon.
		self.write(html_header)
		
		#self.write('<form id="login_form" action="/search" method="post"><label class="grey" for="query">Search Query</label><br /><input type="text" name="query" style="width:99%" id="query"><br><input type="submit" id="submit" name="submit" value="Search" class="button"><br /></form>')
		
		html_footer = open("templates/footer.html").read()
		self.write(html_footer)
	
	
class SearchHandler(tornado.web.RequestHandler):
	
		
	def post(self):
		html_header = open("templates/header.html").read()
		self.write(html_header)
		max_results = 5 #not using atm
		search_term = "government"
		search_term = self.get_argument('query')
		
		global CORPUS_NAME, CORPUS_INDEX, CORPUS_FILES
		
		if args.corpus!=None:
			CORPUS_NAME = args.corpus
		else:
			CORPUS_NAME = "ocon"	
		
		CORPUS_INDEX = "data/" + CORPUS_NAME + "-index"
		CORPUS_FILES = "data/" + CORPUS_NAME + "-text/"
	
		
		ix = open_dir(CORPUS_INDEX)
		from whoosh.qparser import QueryParser
		with ix.searcher() as searcher:
			query = QueryParser("content", SCHEMA).parse(unicode(search_term))
			
			results = searcher.search(query,limit=None)
			
			results_seen = set() # holds lines already 
			
			all_formatted_results = ""
			
			
			for result in results:
				if result["content"] not in results_seen: # not a duplicate
			
					formatted_result = result["content"] + "<br /><br />"
					formatted_term = '<strong><a href="/context?file=' + result['textfile'] + '">' + search_term + "</a></strong>"
		
					results_seen.add(result["content"] )
					#print results_seen
					#print formatted_result.replace(search_term,strong_term)
					all_formatted_results = all_formatted_results + formatted_result.replace(search_term,formatted_term)
					#self.write(result["content"] + "<br /><br />")
					
			self.write("<strong>" + str(len(results_seen)) + " results found for " + search_term + " out of " + str(searcher.doc_count_all()) + " indexed sentences (and 1,448,323 total tokens).</strong> <br /><br />")
	
			self.write(all_formatted_results)
			html_footer = open("templates/footer.html").read()
			self.write(html_footer)

class ContextHandler(tornado.web.RequestHandler):
	def get(self):
		html_header = open("templates/header.html").read()
		self.write(html_header)
		
		text_file = self.get_argument('file')
		self.write('<strong>' + CORPUS_NAME  + " > " + self.get_argument('file') + "</strong><br /><br />")
		#search_term = self.get_argument('term')
		raw_file = open(CORPUS_FILES + text_file, "r")
		text_file = raw_file.read()
		raw_file.close()
		self.write(text_file.replace('\n', '<br />'))
		html_footer = open("templates/footer.html").read()
		self.write(html_footer)

class AboutHandler(tornado.web.RequestHandler):
	def get(self):
		
		html_header = open("templates/header.html").read()
		html_footer = open("templates/footer.html").read()
		html_about = open("templates/about.html").read()
		
		print html_about
		
		self.write(html_header)
		self.write(html_about)
		self.write(html_footer)


if __name__ == "__main__":			
	
	settings = {
    'debug': True, 
    'static_path': 'templates/static'}
	
	handlers = [
    (r"/", MainHandler),
	(r"/search", SearchHandler),
	(r"/context", ContextHandler),
	(r"/about", AboutHandler),
	(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'templates/static'}),
	]
	
	application = tornado.web.Application(handlers, **settings)
	
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--port")
	parser.add_argument("--corpus")
	args = parser.parse_args()
	
	if args.port!=None:
		application.listen(args.port)
	else:
		application.listen(3050)
	tornado.ioloop.IOLoop.instance().start()			




