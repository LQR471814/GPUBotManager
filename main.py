import argparse
import json
import os
import sys
import time

from win10toast import ToastNotifier

from shared_context import *
from utils import *


def toast(title: str, message: str):
    toaster.show_toast(title, message, duration=10, threaded=True)

# ? Setup functions
def setup_newegg():
    def setup():
        request_and_write('https://raw.githubusercontent.com/Ataraksia/NeweggBot/master/NeweggBot.js', '.\\newegg_bot.js')
        f = open('config.json', 'w')
        # TODO: Change in future
        f.write(
            json.dumps({
                "email": setup_config['email'],
                "password": setup_config['password'],
                "cv2": setup_config['cvv'],
                "refresh_time": "5",
                "item_number": "N82E16814137595,N82E16814126455",
                "auto_submit": "true",
                "price_limit": setup_config['price_limit']
            })
        )
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

        amazonConfig = json.loads(open(f'{absPath}\\amazon_config.json', 'r').read())
        amazonConfig['reserve_max_1'] = int(setup_config['price_limit'])

        # * Modify settings
        with open('.\\config\\amazon_config.json', 'w') as f: f.write(json.dumps(amazonConfig))

        os.rename('.\\config\\apprise.conf_template', 'apprise.conf')

    run_in_context(setup, f'{absPath}\\fairgame-0.6.5')

def setup_evga():
    def setup():
        with open('evga.key', 'w') as f: f.write(f"{setup_config['email']}\n{setup_config['password']}")
        with open('payment.key', 'w') as f: f.write(f"{setup_config['card_holder_name']}\n{setup_config['password']}\n{setup_config['cvv']}\n{setup_config['card_expiration_month']}\n{setup_config['card_expiration_year']}")

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

def run_bots(setup = False):
    #* Amazon
    toast(
        'Setup is running the Amazon bot',
        'Amazon ID = Your Amazon Account\'s email address\nCredential File Password = A separate password to encrypt your password and ID (make sure to remember it)'
    )

    run_in_context(lambda: run_command_process('py -3.8 -m pipenv run py app.py amazon'), absPath + "\\fairgame-0.6.5")

    time.sleep(1)

    if setup:
        insert_command(setup_config['email'])
        insert_command(setup_config['password'])
        insert_command('test_pass')

    insert_command('test_pass')

    #* Newegg
    run_in_context(lambda: run_command_process('node newegg_bot.js'), absPath)
    #* EVGA
    run_in_context(lambda: run_command_process('py evga_bot.py'), absPath)

# ? Config
def setup_universal_config():
    config_keys = [
        'email', #? Bot should have the same email and password for each site
        'password',
        'card_holder_name', #? Use a virtual credit card
        'card_number',
        'card_expiration_month',
        'card_expiration_year',
        'cvv', #? The 3 digits number on the back of a credit card
        'price_limit' #? Max expense for a card
    ]
    config = {}

    for key in config_keys:
        inp = input(f'{key}: ')
        config[key] = inp

    return config

# ? Languages
# * Get NodeJS and packages
def setup_node():
    print(" ====== Setting up Node.js ====== ")

    create_folder('node-v14.16.1-win-x64')
    print('Downloading Node...')
    get_and_unzip('https://nodejs.org/dist/v14.16.1/node-v14.16.1-win-x64.zip', '.')
    os.system('.\\node-v14.16.1-win-x64\\npm install puppeteer -PUPPETEER_PRODUCT=firefox')

# * Setup python, packages and path
def setup_python():
    print(" ====== Setting up Python ====== ")

    # * Install python38
    request_and_write('https://www.python.org/ftp/python/3.8.9/python-3.8.9-amd64.exe', '.\\tmp\\python38_inst.exe')
    toast('Python Installation Required', 'You will need to go through the python installer to run the bot')
    time.sleep(2) #? To give people time to react
    os.system('.\\tmp\\python38_inst.exe')

    # * Refresh and modify path
    refresh_path()
    sys.path.append(f"{absPath}\\webdrivers\\")

    os.system('py -3.8 -m pip install selenium')

def windows_workflow():
    create_folder("tmp")

    setup_node()
    setup_python()

    # ? Setup bots
    setup_amazon()
    setup_newegg()
    setup_evga()

    run_bots(True)

if __name__ == '__main__':
    # ? Handle runtime args
    parser = argparse.ArgumentParser(description='Sets up and runs a bunch of different bots')
    parser.add_argument('--run', action='store_true', help='Runs the bots without setup')
    args = parser.parse_args()

    toaster = ToastNotifier()

    # ? Show startup warning
    startup_warning()

    # ? On setup (not run)
    if not args.run:
        setup_config = setup_universal_config()

    if os.name == 'nt':
        if args.run: # ? On run
            run_bots()
        else: # ? On setup
            windows_workflow()
    else:
        print('Currently only Windows is supported!')
