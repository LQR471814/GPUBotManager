import os
import shutil
from subprocess import Popen, PIPE, STDOUT
from typing import List, Union

import pyautogui
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

def run_command_process(command: Union[str, List[str]], shell=True) -> Popen:
    if shell:
        return Popen('start /wait ' + command, shell=True)
    else:
        return Popen(['start', '/K'] + command, stdout=PIPE, stdin=PIPE, stderr=STDOUT, text=True)

def insert_command(keys: str):
    pyautogui.write(keys)
    pyautogui.press('enter')
