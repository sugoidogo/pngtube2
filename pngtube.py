from http.server import SimpleHTTPRequestHandler, HTTPServer
import sounddevice
import numpy
import os

class pngtube(SimpleHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def do_POST(self):
        from pathlib import Path
        path=Path.cwd().joinpath(self.path[1:]) # attempt to create absolute path under web root
        if not path.is_relative_to(Path.cwd()): # if the resulting path is not under web root
            self.send_error(403,explain='requested resource is outside web root') # never write to files outside of web root
            return
        try: # attempt to write data to storage
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('wb') as file:
                file.write(self.rfile.read(int(self.headers['Content-Length'])))
        except Exception as e: # writing data failed
            self.send_error(500,explain=str(e))
        else: # writing data succeeded
            self.send_response(200)
    def do_GET(self):
        if(self.headers['Transfer-Encoding']!='chunked'):
            return SimpleHTTPRequestHandler.do_GET(self)
        self.send_response(200)
        self.send_header('Transfer-Encoding','chunked')
        self.send_header('Content-Type','text/plain')
        self.end_headers()
        def send(message):
            try:
                self.wfile.write(str(message).encode())
            except:
                os._exit(0)
        def loop(indata, frames, time, status):
            num=str(numpy.linalg.norm(indata)*10)
            send(len(num))
            send("\r\n")
            send(num)
            send("\r\n")
            self.wfile.flush()
        if(os.fork()==0):
            with sounddevice.InputStream(callback=loop):
                while True:
                    sounddevice.sleep(1)

HTTPServer(('localhost',6000), pngtube).serve_forever()
