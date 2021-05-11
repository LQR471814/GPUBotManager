import json
import os
import time
import keyboard

# import win10toast

import get_bestbuy_cookie as BBCookie
from shared_context import *
from utils import *

amazon_repo_name = 'fairgame-master'
bestbuy_repo_name = 'Nvidia3080_BB_bot-master'

# def toast(title: str, message: str):
#     toaster.show_toast(title, message, duration=10, threaded=True)

# ? Setup functions
def setup_newegg():
    request_and_write('https://raw.githubusercontent.com/Ataraksia/NeweggBot/master/NeweggBot.js', '.\\newegg_bot.js')
    f = open('config.json', 'w')
    # TODO: Change in future
    f.write(
        json.dumps({
            "email": setup_config['email'],
            "password": setup_config['password'],
            "cv2": setup_config['card_cvv'],
            "refresh_time": "5",
            "item_number": "N82E16814137595,N82E16814126455",
            "auto_submit": "true",
            "price_limit": setup_config['price_limit']
        })
    )
    f.close()

def setup_amazon():
    # * Get fairgame bot
    create_folder(amazon_repo_name)
    get_and_unzip('https://github.com/Hari-Nagarajan/fairgame/archive/refs/heads/master.zip', '.')

    def setup():
        # * Setup pipenv
        os.system('py -3.8 -m pip install pipenv')
        os.system('py -3.8 -m pipenv install')

        amazonConfig['reserve_max_1'] = int(setup_config['price_limit'])

        # * Modify settings
        with open('.\\config\\amazon_config.json', 'w') as f: f.write(json.dumps(amazonConfig))

        os.rename('.\\config\\apprise.conf_template', 'apprise.conf')

    run_in_context(setup, f'.\\{amazon_repo_name}')

def setup_evga():
    with open('evga.key', 'w') as f: f.write(f"{setup_config['email']}\n{setup_config['password']}")
    with open('payment.key', 'w') as f: f.write(f"{setup_config['firstname']} {setup_config['lastname']}\n{setup_config['password']}\n{setup_config['card_cvv']}\n{setup_config['card_expiration_month']}\n{setup_config['card_expiration_year']}")

    # request_and_write('https://raw.githubusercontent.com/jarodschneider/evga-bot/master/evga_bot.py', '.\\evga_bot.py')

def setup_bestbuy():
    def setup():
        with open('.\\data\\sensor_data_cookie.txt', 'w') as f: f.write(cookie)
        with open('.\\data\\tasks.json', 'w') as f:
            linksObj = []
            for i in range(len(bestbuy_links)):
                linksObj.append(
                    {
                        'task_id': str(i + 1),
                        'site': 'Bestbuy',
                        'product': bestbuy_links[i],
                        'profile': 'BotManager',
                        'proxies': 'None',
                        'monitor_delay': '5.0',
                        'error_delay': '5.0',
                        'max_price': '750'
                    }
                )
            f.write(json.dumps(linksObj))
        with open('.\\data\\profiles.json', 'w') as f:
            profilesObj = []
            profilesObj.append({
                'profile_name': 'BotManager',
                'shipping_fname': setup_config['firstname'], #? Shipping info
                'shipping_lname': setup_config['lastname'],
                'shipping_email': setup_config['email'],
                'shipping_phone': setup_config['phone_number'],
                'shipping_a1': setup_config['shipping_address'],
                'shipping_a2': setup_config['shipping_address'],
                'shipping_city': setup_config['shipping_city'],
                'shipping_zipcode': setup_config['shipping_zip'],
                'shipping_state': setup_config['shipping_state'],
                'shipping_county': setup_config['shipping_county'],
                'billing_fname': setup_config['firstname'], #? Billing info (same as shipping info)
                'billing_lname': setup_config['lastname'],
                'billing_email': setup_config['email'],
                'billing_phone': setup_config['phone_number'],
                'billing_a1': setup_config['shipping_address'],
                'billing_a2': setup_config['shipping_address'],
                'billing_city': setup_config['shipping_city'],
                'billing_zipcode': setup_config['shipping_zip'],
                'billing_state': setup_config['shipping_state'],
                'billing_county': setup_config['shipping_county'],
                'card_number': setup_config['card_number'], #? Card info
                'card_month': setup_config['card_expiration_month'],
                'card_year': setup_config['card_expiration_year'],
                'card_type': setup_config['card_expiration_year'],
                'card_cvv': setup_config['card_cvv'],
            })
            f.write(json.dumps(profilesObj))

        run_command_process('py -3.8 -m pip install -r requirements.txt')

    create_folder(bestbuy_repo_name)
    get_and_unzip('https://github.com/alexxsalazar/Nvidia3080_BB_bot/archive/refs/heads/master.zip', '.')

    cookie = BBCookie.main(setup_config['email'], setup_config['password'])
    run_in_context(setup, f'.\\{bestbuy_repo_name}')

# ? Bot functions
def startup_warning():
    print('WARNING: Do NOT use this config with a normal credit card, instead, one should opt for a virtual private card WITH spending limits (otherwise some of the bots might end up buying cards at exorbitant prices)\nInsert \'ok\' and press [ENTER] to continue (Note: If you want to exit at any time, press CTRL + C)')
    if input(' > ') != 'ok':
        quit()

def run_bots(setup = False):
    #* Amazon
    def run_amazon():
        amazonBotProc = run_in_context(lambda: run_command_process("py -3.8 -m pipenv run py app.py amazon --p test_pass --headless", shell=False), f'.\\{amazon_repo_name}')

        time.sleep(5)

        if setup:
            insert_line_to_process(amazonBotProc, setup_config['email'])
            keyboard.write(setup_config['password'] + '\n')
            keyboard.write('test_pass' + '\n')
            keyboard.write('test_pass' + '\n')

        amazonBotProc

    # #* Newegg
    # def run_newegg():
    #     run_in_context(lambda: run_command_process('node newegg_bot.js'), absPath)

    # #* EVGA
    # def run_evga():
    #     pass
    #     # evgaBotProc = run_in_context(lambda: run_command_process('py -3.8 evga_bot.py', shell=False), absPath)
    #     # insert_line_to_process(evgaBotProc, 'RTX 3080 FTW3 GAMING')
    #     # evga_bot.main([])

    #* Best Buy
    def run_bestbuy():
        run_in_context(lambda: run_command_process('py -3.8 app.py', shell=False), f'.\\{bestbuy_repo_name}')

    run_amazon()
    if setup:
        time.sleep(10)
    run_bestbuy()

    print('Close this window to stop bots')

    while True: pass

# ? Config
def setup_universal_config():
    config = dict.fromkeys([
        'email', #? Bot should have the same email and password for each site
        'password',
        'firstname',
        'lastname',
        'phone_number',
        'shipping_address',
        'shipping_city',
        'shipping_zip',
        'shipping_state',
        'shipping_county',
        'card_number',
        'card_expiration_month',
        'card_expiration_year',
        'card_cvv', #? The 3 digits number on the back of a credit card
        'price_limit' #? Max expense for a card
    ])

    for key in config:
        inp = input(f'{key}: ')
        config[key] = inp

    return config

# ? Webdrivers
def setup_webdrivers():
    get_and_unzip('https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-win64.zip', '.')

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

    print('Downloading the Python Installer...')
    # * Install python38
    request_and_write('https://www.python.org/ftp/python/3.8.9/python-3.8.9-amd64.exe', '.\\tmp\\python38_inst.exe')
    print('Launching python installer, you will need to go through it manually')
    # toast('Python Installation Required', 'You will need to go through the python installer to run the bot')
    time.sleep(2) #? To give people time to react
    os.system('.\\tmp\\python38_inst.exe')

    # * Refresh and modify path
    refresh_path()

    os.system('py -3.8 -m pip install selenium')

def windows_workflow():
    create_folder("tmp")

    # setup_node()
    setup_python()
    setup_webdrivers()

    # ? Setup bots
    setup_amazon()
    setup_bestbuy()

    open('SETUP_FINISHED', 'w').close()

    run_bots(True)

if __name__ == '__main__':
    # ? Handle runtime args
    # toaster = win10toast.ToastNotifier()

    # ? Show startup warning
    startup_warning()

    setup = not os.path.isfile(f'.\\SETUP_FINISHED')
    cfg_test = os.path.isfile(f'.\\USE_TEST_CONFIG')

    # ? On setup (and not test)
    if setup and not cfg_test:
        setup_config = setup_universal_config()
    else: # ? On test
        setup_config = {
            'email': 'whydoiexist3812@gmail.com',
            'password': '3z8QV&/_.)AjpQU',
            'firstname': 'Test',
            'lastname': 'User',
            'phone_number': '6692348106',
            'shipping_address': 'address',
            'shipping_city': 'city',
            'shipping_zip': 'zip',
            'shipping_state': 'state',
            'shipping_county': 'county',
            'card_number': '123456789',
            'card_expiration_month': 'June',
            'card_expiration_year': '2021',
            'card_cvv': '321',
            'price_limit': '750',
        }

    if os.name == 'nt':
        if setup:
            windows_workflow()
        else:
            run_bots()
    else:
        print('Currently only Windows is supported!')
