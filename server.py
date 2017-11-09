from http.server import BaseHTTPRequestHandler
from urllib import parse
from API import query_spliter
from getComment import getComments
import json
import threading

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(threading.currentThread().getName() + " is working")
        message = ''
        parsed_path = parse.urlparse(self.path)
        path= self.path
        realpath= parsed_path.path
        query= parsed_path.query
        if(query != ''):
            query_dict = query_spliter(query)
            message = getComments(query_dict['access_token'][0],query_dict['since'][0])
        
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))


if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()