from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

login_url = "https://www.bestbuy.com/identity/global/signin"

def main(user: str, password: str) -> str:
    browser = webdriver.Firefox()
    wait = WebDriverWait(browser, 60)

    browser.get(login_url)

    username_field = wait.until(lambda browser: browser.find_element(By.XPATH, "//input[@type='email']"))
    password_field = wait.until(lambda browser: browser.find_element(By.XPATH, "//input[@type='password']"))

    username_field.send_keys(user)
    password_field.send_keys(password)

    signin_field = wait.until(lambda browser: browser.find_element(By.XPATH, "//button[@type='submit']"))
    signin_field.click()

    while not browser.current_url == "https://www.bestbuy.com/": pass

    cookie = browser.execute_script("return document.cookie.split(';').map(v => v.split('=')).reduce((acc, v) => {acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim()); return acc}, {})")

    browser.quit()
    return cookie['_abck']

if __name__ == '__main__':
    print(main('whydoiexist3812@gmail.com', 'UgeTpi4:kj2e:Dn'))
