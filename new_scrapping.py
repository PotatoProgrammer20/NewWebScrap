from unicodedata import name
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import ast
import time
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()  

###################################### loading env variables ##############################

DRIVER_PATH = os.environ.get('driver_path')
main_url = os.environ.get('main_url')
file_save_path = os.environ.get('file_save_path')
departments = ast.literal_eval(os.environ.get('departments'))

departments_list = list(departments.keys())
departments_values = list(departments.values())

#######################################  set up driver ####################################

def main():

    for i in range(len(departments_list)):
            
        options = webdriver.ChromeOptions()
        MYDIR = file_save_path + '/' + departments_list[i]
        CHECK_FOLDER = os.path.isdir(MYDIR)

        # If folder doesn't exist, then create it.
        if not CHECK_FOLDER:
            os.makedirs(MYDIR)

        prefs = {"download.default_directory" : MYDIR}
        #example: prefs = {"download.default_directory" : "C:\Tutorial\down"};
        options.add_experimental_option("prefs",prefs)

        driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)

        #######################################  main function ####################################

        driver.get(main_url)

        web_element = driver.find_element_by_link_text("IT Portfolio")
        web_element.click()

        time.sleep(1)

        department = Select(driver.find_element_by_id('agency-select'))      ###find_element_by_id
        department.select_by_value(departments_values[i])

        page=driver.page_source
        page = BeautifulSoup(page, 'html.parser')
        time.sleep(5)                                                 ########## sleep to let website open ############
        spendings = page.find("div", "it-spending")
        time.sleep(5)
        spending_value = spendings.find("p")
        spending_value = spending_value.text.strip()

        investments_value = page.find("div", "major-spending")
        time.sleep(4)
        investments_value = investments_value.find("p")
        investments_value = investments_value.text.strip()

        df  = pd.DataFrame(data = [[departments_list[i], investments_value , spending_value]], columns=['Department' , 'FY 2022 IT Spending', 'Spending on Major Investments'])
        df.to_csv(MYDIR + '/scraped_data.csv', index=False)

        list_of_document_to_download = ['IT Spending Source Data']

        for i in range(len(list_of_document_to_download)):

            csv_download = driver.find_element_by_link_text(list_of_document_to_download[i])
            csv_download.click()
        
        time.sleep(3)
    
if __name__== "__main__":

    main()