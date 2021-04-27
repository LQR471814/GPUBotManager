import subprocess
import os
import shutil
import sys
import time
import argparse

import requests
from win10toast import ToastNotifier


# ? Utility functions
def toast(title: str, message: str):
    toaster.show_toast(title, message, duration=10, threaded=True)

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
    func()
    os.chdir('..')

def run_command_process(command: str):
    subprocess.Popen(f'start /wait {command}', shell=True)

# ? Setup functions
def setup_newegg():
    def setup():
        request_and_write('https://raw.githubusercontent.com/Ataraksia/NeweggBot/master/NeweggBot.js', '.\\newegg_bot.js')
        f = open('config.json', 'w')
        # TODO: Change in future
        f.write("""
        {
            "email":"email@email.com",
            "password":"supercoolpassword",
            "cv2":"123",
            "refresh_time":"5",
            "item_number":"N82E16814137595,N82E16814126455",
            "auto_submit":"true",
            "price_limit":"800"
        }
        """)
        f.close()

    run_in_context(setup, absPath)

def setup_amazon():
    # * Get fairgame bot
    create_folder('fairgame-0.6.5')
    get_and_unzip('https://github.com/Hari-Nagarajan/fairgame/archive/refs/tags/0.6.5.zip', '.')

    def setup():
        # * Setup pipenv
        os.system('py -3.8 -m pip install pipenv')
        os.system('py -3.8 -m pipenv install')

        # * Modify settings
        f = open('.\\config\\amazon_config.json', 'w')
        f.write(amazonConfig)
        f.close()

        os.rename('.\\config\\apprise.conf_template', 'apprise.conf')

    run_in_context(setup, f'{absPath}\\fairgame-0.6.5')

def setup_evga():
    def setup():
        request_and_write('https://raw.githubusercontent.com/jarodschneider/evga-bot/master/evga_bot.py', '.\\evga_bot.py')
        create_folder('webdrivers')
        get_and_unzip('https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-win64.zip', '.\\webdrivers')

    run_in_context(setup, absPath)

def setup_bestbuy():
    def setup():
        get_and_unzip('https://github.com/alexxsalazar/Nvidia3080_BB_bot/archive/refs/heads/master.zip', '.')

    run_in_context(setup, absPath)

# ? Bot functions
def startup_warning():
    print('WARNING: Do NOT use this config with a normal credit card, instead, one should opt for a virtual private card WITH spending limits (otherwise some of the bots might end up buying cards at exorbitant prices)\nInsert \'ok\' and press [ENTER] to continue (Note: If you want to exit at any time, press CTRL + C)')
    if input(' > ') != 'ok':
        quit()

def run_bots():
    run_in_context(lambda: run_command_process('node newegg_bot.js'), absPath)

    toast(
        'Setup is running the Amazon bot',
        'Amazon ID = Your Amazon Account\'s email address\nCredential File Password = A separate password to encrypt your password and ID (make sure to remember it)'
    )
    run_in_context(lambda: run_command_process('py -3.8 -m pipenv run py app.py amazon'), f'{absPath}\\fairgame-0.6.5')

def windows_workflow():
    create_folder("tmp")

    # ? Get NodeJS and packages
    create_folder('node-v14.16.1-win-x64')
    get_and_unzip('https://nodejs.org/dist/v14.16.1/node-v14.16.1-win-x64.zip', '.')
    os.system('.\\node-v14.16.1-win-x64\\npm install puppeteer -PUPPETEER_PRODUCT=firefox')

    # ? Setup python, packages and path

    # * Install python38
    request_and_write('https://www.python.org/ftp/python/3.8.9/python-3.8.9-amd64.exe', '.\\tmp\\python38_inst.exe')
    toast('Python Installation Required', 'You will need to go through the python installer to run the bot')
    time.sleep(2) #? To give people time to react
    os.system('.\\tmp\\python38_inst.exe')

    # * Refresh and modify path
    refresh_path()
    sys.path.append(f"{absPath}\\webdrivers\\")

    os.system('py -3.8 -m pip install selenium')

    # ? Setup bots
    setup_amazon()
    setup_newegg()

    run_bots()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sets up and runs a bunch of different bots')
    parser.add_argument('--run', action='store_true', help='Runs the bots without setup')
    args = parser.parse_args()

    startup_warning()

    absPath = os.path.dirname(os.path.abspath(__file__))
    amazonConfig = open('amazon_config.json', 'r').read()

    if os.name == 'nt':
        toaster = ToastNotifier()

        if args.run:
            run_bots()
        else:
            windows_workflow()
    else:
        print('Currently only Windows is supported!')
