from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import shutil

USERNAME    = os.environ.get("PME_USER")
PASSWORD    = os.environ.get("PME_PASS")

download_dir = "/app/downloads"
final_path   = "/app/PME_Disponibilita_Clean.xlsx"
driver_path  = "/usr/bin/chromedriver"

options = Options()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-features=TranslateUI")
options.page_load_strategy = 'eager'

driver  = webdriver.Chrome(service=Service(driver_path), options=options)
wait    = WebDriverWait(driver, 30)

driver.get("https://www.planningpme.fr/?cli=intech#/planning")
wait.until(EC.visibility_of_element_located((By.ID, "inputLoginUserName")))
driver.find_element(By.ID, "inputLoginUserName").send_keys(USERNAME)
driver.find_element(By.ID, "inputLoginPassword").send_keys(PASSWORD)
wait.until(EC.element_to_be_clickable((By.ID, "loginSignOn"))).click()

wait.until(EC.url_contains("/planning"))
wait.until(EC.element_to_be_clickable((By.ID, "btnSettings"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Rapporti")]'))).click()
time.sleep(2)

ActionChains(driver).click(wait.until(EC.element_to_be_clickable((By.NAME, "dateFrom")))).perform()
time.sleep(1)
driver.find_element(By.XPATH, '//button[contains(text(),"Oggi")]').click()
ActionChains(driver).click(wait.until(EC.element_to_be_clickable((By.NAME, "dateTo")))).perform()
time.sleep(1)
for _ in range(6):
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-icon-circle-triangle-e"))).click()
    time.sleep(0.5)
try:
    wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="15"]'))).click()
except:
    driver.find_element(By.XPATH, '//a[@class="ui-state-default"]').click()
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Convalida")]'))).click()

time.sleep(10)
latest = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)
shutil.copy(latest, final_path)
print("::PME_EXPORT_SUCCESS::")
exit(0)
