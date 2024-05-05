import requests
from bs4 import BeautifulSoup as bs

proxy_url = "https://github.com/clarketm/proxy-list/blob/master/proxy-list-raw.txt"
r = requests.get(proxy_url)
#soup = bs(r.content,"html.parser").find_all('td',"class":"")
print(r.text)