#	The Open Corpus of Newswriting (OCON)
#    Copyright (C) 2014 Mahangu Weerasinghe (mahangu@gmail.com)
	
#	 This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
		
import urlparse
import os
import justext
import urllib2
import re #regex stuff
from ftfy import fix_text #unicode cleanup

INPUT_DIR="input/"
OUTPUT_DIR="output/"

def get_article_list(filename):
	lines = tuple(open(filename, "r"))
	lines_seen = set() # holds lines already seen
	for line in open(filename, "r"):
		if line not in lines_seen: # not a duplicate
			lines_seen.add(line)
	return tuple(lines_seen)

def grab_article(url):
	article = ""
	import requests
	import justext
	#url = "http://archives.dailynews.lk/2008/01/11/news38.asp"
	url = url.strip("\n")
	url = url.strip("\r")
	url = url.strip(" ")
	print url
	
	response = requests.get(url)
	print response
	paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
	for paragraph in paragraphs:
		if not paragraph.is_boilerplate:
			#print paragraph.text
			article = article + unicode(paragraph.text) + "\n\n"
	
	
	
	if article!=None:
		return unicode(article)
	else:
		return None;



for file in os.listdir(INPUT_DIR):
	if file.endswith(".txt"):
		split_filename = re.findall(r"[^\W_]+", file) #splitting up the filename so we can get newspaper name and date from it
		NEWSPAPER = split_filename[0]
		DATE = split_filename[1]
		
		article_url_list = ""
		article_url_list = get_article_list(INPUT_DIR + file)  
		
		print article_url_list
		
		for article_url in article_url_list:
			scheme = urlparse.urlparse(article_url).scheme
			if article_url!="\n" and scheme=="http": #checking for newlines and mailto: links
				hostname = urlparse.urlparse(article_url).hostname
				path = urlparse.urlparse(article_url).path #grab the part after the .TLD
				path = path.replace("/", "") #remove forward slashes
				raw_text = unicode(grab_article(article_url))
				
				if raw_text!=None:
					text = fix_text(raw_text)
					text = text + "\n\n\n\n"
					split_path = re.findall(r"[^\W_]+", path) #sanitising the path so it doesn't end up crazy long
					short_path = split_path[0]
					print short_path
					text_file = open(OUTPUT_DIR + NEWSPAPER + "_" + DATE + "_" + hostname + "_" + short_path + ".txt", "a+")
					text_file.write(text.encode('utf8'))
					text_file.close() 



