from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import pyautogui as py
import time as t

chrome_driver_path = "C:/Users/rahul/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Create a Chrome service
chrome_service = Service(chrome_driver_path)

# Create a new instance of the Chrome driver with the service
driver = webdriver.Chrome(service=chrome_service)

start_day = "08012020"
current_day = "08012020"
end_day = "12132023"

url = "https://jansoochna.rajasthan.gov.in/Services/GetMoreData?q=JCACQCaD+3Xh5jYLcSTzwdXguzXcq4gdfeqrpvU0qNY="

out_file = "outfile.txt" # change to .csv if you want



driver.get(url)

t.sleep(5)

loader = driver.find_element(By.ID,"AjaxLoader")

class loader_visible(object):
  def __init__(self,locater):
      self.locater = locater

  def __call__(self, driver):
    if loader.is_displayed():
        return False
    else:
        return driver.find_element(*(self.locater))

districts = Select(driver.find_element(By.ID,"जिला"))


for district in districts.options[1:]:
    district.click()
    wait = WebDriverWait(driver, 10)
    ulbs = Select(wait.until(loader_visible((By.ID,"यूएलबी_का_चयन_करें"))))
    # ulbs = Select(driver.find_element(By.ID,"यूएलबी_का_चयन_करें"))
    for ulb in ulbs.options[1:]:
        ulb.click()
        rasois=Select(wait.until(loader_visible((By.ID,"रसोई_नंबर_का_चयन_करें"))))
        # rasois = Select(driver.find_element(By.ID,"रसोई_नंबर_का_चयन_करें"))
        # print("found")
        for rasoi in rasois.options[1:]:
            print("found")
            rasoi.click()
            date_input = driver.find_element(By.XPATH,"//input[@type='date']")
            submit_button = driver.find_element(By.ID,"btnSubmit")
            current_date = start_day
            if current_day == end_day:
                current_day = start_day
            
            while current_day != end_day:
                date_input = driver.find_element(By.XPATH,"//*[@id='data_1']//input")
                date_input.clear()
                date_input.send_keys(current_day)
                elem = wait.until(loader_visible((By.ID,"seeAll")))
                submit_button.click()
                

                t_elems = driver.find_elements(By.XPATH,"//*[@id='tblResult_0']/tbody/tr/td")
                current_date = datetime.strptime(current_day, "%m%d%Y")
                with open(out_file,"a",encoding="utf-8") as f:
                    f.write(current_date.strftime("%m/%d/%Y")+",")
                    for i in t_elems:
                        f.write(i.text+",")
                    f.write("\n")

                # Perform any additional actions you need to do on the page with the selected date

                next_date = current_date + timedelta(days=1)
                current_day = next_date.strftime("%m%d%Y")

# Find an element by its ID and interact with it
# element = driver.find_element("id", "some_element_id")
# element.click()

# Get the page title
print("Page title:", driver.title)

# Close the browser
t.sleep(100000)
driver.quit()
