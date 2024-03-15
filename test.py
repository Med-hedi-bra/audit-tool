from time import sleep
import requests


def has_mfa(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            mfa_keywords = ["multi-factor authentication", "MFA"]
            for keyword in mfa_keywords:
                if keyword in response.text:
                    return True
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False


def main():
    # Example usage
    # url = "https://www.facebook.com/login"
    # if has_mfa(url):
    #     print("This target has MFA enabled.")
    # else:
    #     print("This target does not have MFA enabled.")
    # vim test.py

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait


    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    URL = "http://aspnet.testsparker.com/administrator/Login.aspx?r=/Dashboard/"
    SUCCESS_LOGIN_URL = "https://defendtheweb.net/dashboard"
    USERNAME_PLACEHOLDER = 'Username'
    PASSWORD_PLACEHOLDER = 'Password'
    USERNAME = "vscodeonly"
    PASSWORD = "vscodeonly"
    driver.get(URL)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//input[@placeholder='{USERNAME_PLACEHOLDER}']"))
    )
    username_field = driver.find_element(By.XPATH, f"//input[@placeholder='{USERNAME_PLACEHOLDER}']")
    
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//input[contains(@placeholder, '{PASSWORD_PLACEHOLDER}')]"))
    )    
    password_field = driver.find_element(By.XPATH, f"//input[contains(@placeholder, '{PASSWORD_PLACEHOLDER}')]")
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Log')]"))
    )
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Log')]")
    login_button.click()
    
    try:
        WebDriverWait(driver, 10).until(EC.url_matches(SUCCESS_LOGIN_URL))
        print("Logged in successfully!")
    except:
        print("Unable to login.")
    
    sleep(5)
    return


main()
