import requests
from fp.fp import FreeProxy

proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "https://10.10.1.10:1080",
}
myProxy = FreeProxy().get()
myProxy = FreeProxy(country_id=['IND']).get()
myProxy = "".join([list(QuickProxy().keys())[0],'://',list(QuickProxy().values())[0]])
requests.get("http://example.org", proxies=proxies)
