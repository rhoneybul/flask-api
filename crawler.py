from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import json

profile = webdriver.FirefoxProfile()
profile.set_preference("webdriver.load.strategy", "unstable")

driver = webdriver.Firefox(firefox_profile=profile) 

# driver = webdriver.Firefox()

driver.get("http://web.csse.uwa.edu.au/contact/profiles")

staff_names = []
while len(staff_names) == 0:
    staff_names = driver.find_elements_by_css_selector('td:nth-child(1) a')

staff_names_array = []
staff_pages_array = []
for staff_name in staff_names:
    staff_names_array.append(staff_name.text)
    staff_pages_array.append(staff_name.get_attribute("href"))

staff_dict = {}
total_length = len(staff_pages_array)
for i, (staff_page, staff_name) in enumerate(zip(staff_pages_array, staff_names_array)):
    sys.stdout.write("%.2f %% Completed\r" % (float(i) * 100 / total_length))
    sys.stdout.flush()
    name = staff_name.encode('ascii', 'ignore')
    staff_image = None
    positions_array = []
    if staff_page is not None:
        staff_dict[name] = {}
        driver.get(staff_page)
        time.sleep(1)
        positions = driver.find_elements_by_css_selector('.cdl-profile-position')
        for j, pos in enumerate(positions):
            positions_array.append(pos.text.split('\n')[0].encode('ascii', 'ignore') + ": " + pos.text.split('\n')[1].encode('ascii', 'ignore'))
        image = driver.find_elements_by_css_selector('img.imgright.border')
        if(len(image) > 0):
            staff_image = image[0].get_attribute("src").encode('ascii', 'ignore')
        if staff_image is not None:
            staff_dict[name]["Image"] = staff_image
        if len(positions_array) > 0:
            staff_dict[name]["Positions"] = positions_array
        staff_dict[name]['Profile'] = staff_page
        staff_dict[name]['id'] = i
        staff_dict[name]['Name'] = name

with open("staff_data.json", 'w') as f:
    json.dump(staff_dict, f, indent = 2)

sys.stdout.write("Completed!                                 \n")
    
driver.close()