from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib import parse
from API import *
import time
import json
import threading

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(threading.currentThread().getName() + " is working")
        start = time.time()
        dict_data = {}
        parsed_path = parse.urlparse(self.path)
        path= self.path
        realpath= parsed_path.path
        querys = parsed_path.query 
        if(querys != '' and realpath != '/favicon.ico'):
            dict_data['data'] = navigator(realpath,querys)
        end = time.time()
        print('request respone in : %s secs' % str('%.3f' % (end - start)))
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(dict_data).encode('utf-8'))       

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    try:
        configuration_file = open('configuration','r')
        configuration = {}    
        for line in configuration_file.readlines():
            line = line.strip('\n')
            (key,val) = line.split(':')
            configuration[key] = val
        if 'host' in configuration:
            host = configuration['host']
        if 'port' in configuration:
            port = int(configuration['port'])
        configuration_file.close()
    except:
        configuration_file = open('configuration','w')
        configuration_file.write("host:localhost\nport:8080")
        configuration_file.close()
        print('configuration file is not found : use "localhost" and port : 8080 as default')
        pass
    server = ThreadedHTTPServer((host, port), Handler)
    print('Starting server on %s port: %s, use <Ctrl-C> to stop' % (host, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    cleanup_stop_thread()
    server.server_close()
    print('server is closed.')