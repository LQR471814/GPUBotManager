import os
import shutil
import subprocess
import threading
from subprocess import PIPE, STDOUT, Popen
from typing import List, Union

import requests

from shared_context import *


# ? Utility functions
def refresh_path():
    os.system(f'{absPath}\\refreshenv.cmd')

def create_folder(name: str, keep: bool = False):
    if os.path.isdir(name) and not keep:
        shutil.rmtree(name)
    os.mkdir(name)

def request_and_write(url: str, dest: str):
    f = open(dest, 'wb')
    data = requests.get(url).content
    f.write(data)
    f.close()

def get_and_unzip(url: str, dest: str):
    request_and_write(url, '.\\tmp\\tmp_file.zip')
    shutil.unpack_archive('.\\tmp\\tmp_file.zip', dest)
    os.remove('.\\tmp\\tmp_file.zip')

def run_in_context(func, contextDirectory: str):
    os.chdir(contextDirectory)
    result = func()
    os.chdir('..')
    return result

def in_folder(directory: str):
    def wrapper(func):
        run_in_context(func(), directory)
    return wrapper

def run_command_process(command: str, shell=True) -> Popen:
    if shell:
        proc = Popen('start /wait ' + command, shell=True)
    else:
        proc = Popen(command, stdin=PIPE)
    return proc

def spawn_process_readline_thread(p: subprocess.Popen):
    def readline_worker():
        while True:
            out: bytes = p.stdout.readline()
            p.stdout.flush()
            print(out.decode('utf8'), end='')

    threading.Thread(target=readline_worker, daemon=True).start()

def insert_line_to_process(p: subprocess.Popen, stdin: str) -> str:
    p.stdin.write(f'{stdin}\n'.encode('utf8'))
    p.stdin.flush()
