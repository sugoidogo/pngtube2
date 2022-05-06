server=None

def main():
    try:
        import sys
        log=open(script_path()+'pngtube.log','w')
        sys.stdout=log
        sys.stderr=log
    except:
        pass

    import pip
    pip.main(['install','sounddevice','numpy','--no-warn-script-location'])

    from http.server import SimpleHTTPRequestHandler, HTTPServer
    from pathlib import Path
    from threading import Thread
    import sounddevice, numpy, os, json, shutil, urllib
    from os.path import dirname,abspath

    class pngtube(SimpleHTTPRequestHandler):
        protocol_version='HTTP/1.1'
        
        def translate_path(self, path):
            from os.path import dirname,abspath,join
            return join(path,dirname(abspath(__file__)))
        
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
            def audioLoop():
                def audioCallback(indata, frames, time, status):
                    try:
                        volume=numpy.linalg.norm(indata)*10
                        message='data: '+str(volume)+'\n\n'
                        self.wfile.write(message.encode())
                        self.wfile.flush()
                    except:
                        pass
                with sounddevice.InputStream(device=device,callback=audioCallback):
                    while not self.wfile.closed:
                        sounddevice.sleep(1)
            Thread(target=audioLoop).start()

    global server                    
    server=HTTPServer(('localhost',5000), pngtube)
    server.serve_forever()

def script_load(settings):
    from threading import Thread
    Thread(target=main).start()

def script_unload():
    from threading import Thread
    global server
    Thread(target=server.shutdown).start()

if __name__ == '__main__':
    script_load(None)
    input('Press Enter to stop\n')
    script_unload()