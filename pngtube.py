from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path
import sounddevice, numpy, os, json, shutil, urllib

class pngtube(SimpleHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def do_POST(self):
        path=Path.cwd().joinpath(self.path[1:]) # attempt to create absolute path under web root
        print(path)
        parent=path.parent
        print(parent)
        if not parent.parent.is_relative_to(Path.cwd()): # if the resulting path is not a sub-path in web root
            self.send_error(405) # never write to files outside of web root directories
            return
        try: # attempt to write data to storage
            parent.mkdir(parents=True,exist_ok=True) # make sure parent exists
            size=int(self.headers['Content-Length'])
            if shutil.disk_usage(parent).free < size: # if there's not enough space
                return self.send_error(507)           # error out
            with path.open('wb') as file:
                file.write(self.rfile.read(size))
        except Exception as e: # writing data failed
            self.send_error(500,explain=str(e))
        else: # writing data succeeded
            self.send_response(200)
    def do_GET(self):
        if not self.path.startswith('/audio'):
            return SimpleHTTPRequestHandler.do_GET(self)
        if self.path == '/audio/':
            response=json.dumps(sounddevice.query_devices(kind='input'))
            if response.startswith('{'):
                response="["+response+"]"
            response+="\n"
            self.send_response(200)
            self.send_header('Content-Type','text/json')
            self.send_header('Content-Length',str(len(response)))
            self.end_headers()
            self.wfile.write(response.encode())
            return
        device=urllib.parse.unquote(self.path[len('/audio/'):]) or None
        try:
            sounddevice.check_input_settings(device=device)
            self.send_response(200)
            self.send_header('Content-Type','text/event-stream')
            self.end_headers()
        except Exception as e:
            self.send_error(500,explain=str(e))
        def audioLoop(indata, frames, time, status):
            try:
                message='data: '+str(numpy.linalg.norm(indata)*10)+'\n\n'
                self.wfile.write(message.encode())
                self.wfile.flush()
            except:
                os._exit(0)
        if(os.fork()==0):
            with sounddevice.InputStream(device=device,callback=audioLoop):
                while True:
                    sounddevice.sleep(1)

HTTPServer(('localhost',5000), pngtube).serve_forever()
