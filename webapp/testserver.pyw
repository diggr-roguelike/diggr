import CGIHTTPServer
import BaseHTTPServer

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ["/scripts"]

httpd = BaseHTTPServer.HTTPServer(("", 80), Handler)
httpd.serve_forever()
