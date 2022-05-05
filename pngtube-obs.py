from os.path import dirname,abspath
script_dir=dirname(abspath(__file__))+'/'
pidfile_path=script_dir+'pngtube.pid'

def script_load(settings):
    pidfile=open(pidfile_path,'w')
    from subprocess import Popen
    server=Popen('python pngtube.py',cwd=script_dir)
    pidfile.write(str(server.pid))
    pidfile.close()

def script_unload():
    pidfile=open(pidfile_path,'r')
    from os import kill
    from signal import SIGTERM
    kill(int(pidfile.read()),SIGTERM)
    pidfile.close()
    from os import remove
    remove(pidfile_path)