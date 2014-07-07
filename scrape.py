import urllib2
import json
from bs4 import BeautifulSoup

base_url = ""
starting_page = ""
json_export = '{ "pages": [ \n'

index = 0
url_list = []
url_list.append(base_url+starting_page)
urls_tested = []


for url in url_list:
  page_json = '{ "page" : \n { "url": "' + url + '", '
  urls_tested.append(url) #add this url as 'tested'

  req = urllib2.Request(url)
  site_html = urllib2.urlopen(req).read()
  soup = BeautifulSoup(site_html)
  # create a list of <a href> links
  all_links = soup.findAll("a", href=True)
  page_json += '"links": ['

  #filter all the links 
  filtered_links = []
  for link in all_links:
  	if ".action" in link["href"]:  # all the .action links
  	  filtered_links.append(link['href'])
  	  if link["href"] not in url_list and base_url+link["href"] not in urls_tested and index < 10: # add to url_list
  	  	url_list.append(base_url+link["href"])
  	  index = index + 1
  	elif "http" in link["href"]:  # all the outside links
  	  filtered_links.append(link['href'])

  for link in filtered_links:
  	page_json += '{ "link": "' + link + '"},\n '
  page_json += "]}\n},"
  json_export += page_json

json_export += ']}'
print json_export
  
