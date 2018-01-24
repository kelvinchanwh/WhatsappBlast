# Requires Chrome, webdriver, Selenium, Pandas, time, json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Replace below path with the absolute path
# to chromedriver in your computer
driver = webdriver.Chrome('./chromedriver')

driver.get("https://web.whatsapp.com/")
waits = WebDriverWait(driver, 5)
waitl = WebDriverWait(driver, 60)

# Insert link to CSV file
df = pd.read_csv("./Contacts.csv")
# First column should be named 'Names' with list of contacts
contacts = df['Names']


# Defining how to send a message
def send_message(target):
    # Look for search bar
    y_arg = '//*[@id="side"]/div[2]/div/label/input'
    input_y = waitl.until(EC.presence_of_element_located((By.XPATH, y_arg)))
    # Enter contact into search bar
    input_y.send_keys(target + Keys.ENTER)
    time.sleep(1)

    # Number of times the message should be sent
    for i in range(1):
        try:
            # Check that correct contact choosen
            check_xpath = "//*[@id='main']/header/div[2]/div/div/span[text() = '%s']" % target
            waits.until(EC.presence_of_element_located((By.XPATH, check_xpath)))
            # Looks for input box
            inp_xpath = "//div[@contenteditable='true']"
            input_box = waits.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
            input_box.send_keys(Keys.SHIFT, Keys.INSERT)
            time.sleep(0.5)
            # Sends Message
            send_xpath = "//*[@id='main']/footer/div[1]/button"
            send_button = waits.until(EC.presence_of_element_located((By.XPATH, send_xpath)))
            send_button.click()
            # Clears search bar for next contact
            y_arg = '//*[@id="side"]/div[2]/div/label/input'
            input_y = waits.until(EC.presence_of_element_located((By.XPATH, y_arg)))
            input_y.clear()
            # Confirmation of message sent
            print ('Sucessfully sent message to ' + target)

        except TimeoutException:
            # Clears search bar for next contact
            y_arg = '//*[@id="side"]/div[2]/div/label/input'
            input_y = waitl.until(EC.presence_of_element_located((By.XPATH, y_arg)))
            input_y.clear()
            # Notification of failure
            print ('Failed to send message to ' + target)

start = time.time()
# For loop to cycle through all contacts in CSV file
for contact in contacts:
    send_message(contact)

end = time.time()

Elapsed = end - start
print('Time taken = ', Elapsed)

print('Logging Out... This process will take 6 seconds. Please be patient.')
time.sleep(4)

# Logout
menu_xpath = "//*[@id='side']/header/div[2]/div/span/div[3]/div"
menu_button = waits.until(EC.presence_of_element_located((By.XPATH, menu_xpath)))
menu_button.click()
logout_xpath = "//*[@id='side']/header/div[2]/div/span/div[3]/span/div/ul/li[6]"
logout_button = waits.until(EC.presence_of_element_located((By.XPATH, logout_xpath)))
time.sleep(1)
logout_button.click()
time.sleep(1)

driver.quit()

print('Task Completed')


