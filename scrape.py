import urllib2
from bs4 import BeautifulSoup

base_url = "x"
starting_page = "ShowHome.action"

index = 0
url_list = []
url_list.append(base_url+starting_page)
urls_tested = [] # nodes
master_list_of_links = []
json_links = '"links":[\n'
master_list_of_links.append(base_url+starting_page)

for url in url_list:
  urls_tested.append(url) #add this url as 'tested'

  req = urllib2.Request(url)
  site_html = urllib2.urlopen(req).read()
  soup = BeautifulSoup(site_html)
  # create a list of <a href> links
  all_links = soup.findAll("a", href=True)

  filtered_links = []
  for link in all_links:
  	href = link["href"]

  	if ".action" in href: 
  	  filtered_links.append(base_url+href)
  	  if href not in url_list and base_url+href not in urls_tested and index < 10: 
  	  	url_list.append(base_url+href)
  	  index = index + 1
  	elif "http" in href:  # all the outside links
  	  filtered_links.append(href)	

  for link in filtered_links:
  	if link not in master_list_of_links:
  	  master_list_of_links.append(link)
  	json_links += '{"source":'+str(master_list_of_links.index(url))+',"target":'+str(master_list_of_links.index(link))+',"value":1},\n'

json_links += ']'

nodes = '"nodes":[\n'

for url in master_list_of_links:
	nodes += '{"name":"'+url+'","group":1},\n'

nodes += '],\n'

jsonResult = "{\n"
jsonResult += nodes
jsonResult += json_links
jsonResult += "}"
print jsonResult

