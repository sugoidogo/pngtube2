import pip
pip.main(['install','sounddevice','numpy'])

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sounddevice, numpy, os, json, shutil, urllib

class pngtube(SimpleHTTPRequestHandler):
    protocol_version='HTTP/1.1'
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
                volume=numpy.linalg.norm(indata)
                message='data: '+str(volume)+'\n\n'
                self.wfile.write(message.encode())
                self.wfile.flush()
            except:
                pass
        with sounddevice.InputStream(device=device,callback=audioLoop):
            while True:
                sounddevice.sleep(1)

ThreadingHTTPServer(('localhost',5000), pngtube).serve_forever()