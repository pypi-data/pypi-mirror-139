from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import sys

if len(sys.argv) < 4:
    print("Usage: python jenkinsautoupdater.py <URL> <username> <password> [autorestart]")
    print("Example: python jenkinsautoupdater.py http://example.org admin password true")

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

driver.maximize_window()

# Login to Jenkins
driver.get(sys.argv[1] + "/login")

driver.find_element(By.NAME, "j_username").send_keys(sys.argv[2])
driver.find_element(By.NAME, "j_password").send_keys(sys.argv[3])
driver.find_element(By.NAME, "Submit").click()

driver.implicitly_wait(10)

# Go to the Jenkins Update Center
driver.get(sys.argv[1] + "/pluginManager")

# Click all the checkboxes
checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")

for current in checkboxes:
    try:
        current.click()
        driver.execute_script("window.scrollBy(0, 150);")
    except ElementClickInterceptedException:
        driver.execute_script("window.scrollBy(0, 150);")

driver.find_element(By.ID, "yui-gen1-button").click()

# Click the restart on download if the user asked, otherwise just close the browser
if sys.argv[4] and sys.argv[4] == "True" or sys.argv[4] == "true":
    driver.find_element(By.XPATH, "//input[@type='checkbox']").click()

driver.close()

if sys.argv[4] and sys.argv[4] == "True" or sys.argv[4] == "true":
    print("Done, Jenkins is now restarting, so please wait a few minutes.")
else:
    print("Done, plugins should be installing now. Check the progress on Jenkins.")

print("If you liked this, please consider starring the repo on GitHub.")

sys.exit(0)
