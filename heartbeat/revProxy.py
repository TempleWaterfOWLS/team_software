'''
Code shamelessly stolen from the internet by Zack
Used as a reverse proxy to forward all HTTP requests on shore computer to 
the competition computer
Usage: PROXYHOST="127.0.0.1" mitmproxy -p 9090 -R http://127.0.0.1:6666 -s revProxy.py
Runs on port 9090, send requests to 9090 and it routes the request accordingly
'''
import os

proxyHost = os.environ['PROXYHOST']

def request(ctx,r):
    print r.request.path
    if r.request.path.startswith('/333'):
        # Send shit to proxy server
        r.request.headers['Host'] = [proxyHost]
        r.request.scheme = 'http'
        r.request.host = proxyHost
        r.request.port = 3333
    else:
        # Send shit to other proxy server
	# example host = 'google.com'
        r.request.headers['Host'] = [proxyHost]
        r.request.scheme = 'http'
        r.request.host = proxyHost
        r.request.port = 3333
        
