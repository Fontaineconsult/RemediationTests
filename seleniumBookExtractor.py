from selenium import webdriver
import os
from os.path import join, dirname
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


browser_options = webdriver.ChromeOptions()

dotenv_path = join(dirname(__file__), '.env')
chrome_driver_path = join(dirname(__file__), 'chromedriver.exe')

browser_options.headless = False
browser_options.add_argument('--start-maximized')
browser_options.add_argument("user-data-dir=C:\\Users\\913678186\\AppData\\Local\\Google\\Chrome\\User Data\\Selenium")

prefs = {
    "download_restrictions": 3,  # disable downloads in browser
}
browser_options.add_experimental_option(
    "prefs", prefs
)
browser_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
browser_options.add_argument("--enable-javascript")

driver = webdriver.Chrome(chrome_driver_path, options=browser_options)

driver.get("https://accounts.mheducation.com/login?app=newconnect.mheducation.com")
time.sleep(5)
driver.implicitly_wait(5)

driver.find_element(By.XPATH, "/html/body/heclr-root/main/div/heclr-login/div/section/div/section/form/div[1]/input").send_keys("hnilsson@sfsu.edu")
driver.find_element(By.XPATH,'/html/body/heclr-root/main/div/heclr-login/div/section/div/section/form/div[2]/input').send_keys("Grodanboll12")
driver.find_element(By.XPATH,'/html/body/heclr-root/main/div/heclr-login/div/section/div/section/form/div[5]/button').click()

WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/app-root/page-connect/div[3]/container-iframe/section/div/iframe")))

time.sleep(5)
driver.implicitly_wait(5)

driver.find_element(By.XPATH,'/html/body/div/div/div/nav/div/div[1]/button').click()
time.sleep(2)
driver.implicitly_wait(2)

driver.find_element(By.XPATH,'/html/body/div/div/div/nav/div/div[2]/ul/li[4]/button').click()
time.sleep(2)
driver.implicitly_wait(2)

driver.find_element(By.XPATH,'/html/body/div/div/div/nav/div/div[2]/ul/li[4]/ul/li[1]/a').click()
time.sleep(5)
driver.implicitly_wait(5)



driver.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div[2]/div/div/div[2]/aside/div/div[2]/div[2]/div[2]/ul/li/a').click()

time.sleep(5)
driver.implicitly_wait(5)
print(driver.window_handles)

chld = driver.window_handles[1]
driver.switch_to.window(chld)


element = driver.find_element(By.XPATH, "/html/body/reader-ui-root/reader-ui-epub-viewer/reader-core-reader/mat-sidenav-container/mat-sidenav-content/div/div/reader-core-epub-viewer")
driver.implicitly_wait(3)

original_size = driver.get_window_size()

required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
print(required_height, required_width)
driver.set_window_size(required_width, required_height)

print(element.size)

driver.implicitly_wait(3)
# element.screenshot("shot11.png")



driver.quit()
# driver.get("https://prod.reader-ui.prod.mheducation.com/epub/sn_f8f6c/data-uuid-b61fd3a457104ed1925b93e3abbaac3f")