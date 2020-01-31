import gspread
import sys
import time
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.support.wait import WebDriverWait


###################################################
### Chrome Options / Login Details
###################################################

chrome_options = Options()
#chrome_options.add_argument("--headless")

###################################################
### Global Methods
###################################################
def error(error, exception):
    print(exception)
    sys.exit(error)
def ask_continue():
    option = input("would you like to continue? (search again?): ")
    if option.lower() == "yes":
        Google.search()
    elif option.lower() == "no":
        browser.close()

###################################################
### Variables:
###################################################
group_name =  input("frat/sorierty name: ")
college_name = input("college name: ")
social_type = input("social name: ")

# declare browser for global use
browser = webdriver.Chrome(chrome_options= chrome_options, executable_path= '/Users/carsonrhodes/Documents/SeleniumDrivers/chromedriver')  # comment out to remove browser if isolating

###################################################
### Classes:
###################################################

class Google: # handles tasks involving the use of Google for search queries.
    def __init__(self):
        # variables

        # self.group_name = input("type in the group/frat/soriority you'd like to search: ")
        # self.college_name = input("type in the college to search: ")  # <- change to google another ig
        # self.social_type = input("type in the social to search: ")  # <- change to switch social your googling

        self.error = "[!] There was a critical error that broke the program!"

    def search(self): # a function made for the purpose sending a query to Google.
        print("searching...")
        url = "http://www.google.com/"
        browser.get(url)
        xpath = "//input[@name='q']"
        google_search_box = browser.find_element_by_xpath(xpath)
        search_term = college_name + " " + group_name + " " + social_type
        google_search_box.send_keys(search_term, Keys.ENTER)

    def locate_instagram(self): # a function made for the purpose of locating an instagram result.
        try:
            print("locating instagram page...")
            #instagram = browser.find_element_by_xpath(xpath= "//div[contains(text(),'Instagram photos and videos')]")
            instagram = WebDriverWait(browser, 10).until(lambda x: x.find_element_by_xpath(xpath= "//div[contains(text(),'Instagram photos and videos')]"))
            instagram.click()
            time.sleep(2)
            print(browser.current_url)

        except:
            print("the program was unable to find instagram page from Google query.")
            exception = Exception(self.error)
            error(self.error, exception)


class InputData:
    def __init__(self):
        # use creds to create a client to interact with the Google Drive API
        self.scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open("College Bookings itslit.org").sheet1
        self.error = "[!] There was a critical error that broke the program!"
        self.colleges = ""

    def import_sheet(self): # checks data on sheet and saves it to the init function.
        print("checking data...")
        try:
            print(self.sheet.col_values(1))
            self.colleges = self.sheet.col_values(1)
        except:
            print(self.error)
            print("there was an error when trying to connect to Google.")


    def check_if_college_exists(self): # checks if college already exists on college columun
        matched =  "no"
        college_name_formatted = college_name.lower()
        college_name_formatted = college_name_formatted.capitalize()
        print(self.sheet.col_values(1))
        count_of_colleges = 0
        for college in self.sheet.col_values(1):
            self.count_of_colleges = count_of_colleges + 1
            if college == college_name_formatted:
                matched = "yes"
                print("match")
            elif college != college_name_formatted:
                print("no match")
        if matched == "yes":
            print("college exists!")
            print("moving sheets...")
            InputData.navigate_sheet()
        if matched == "no":
            print("college was not found!")
            print("adding college to list...")
            InputData.add_college()

    def navigate_sheet(self):
        worksheet_list = self.sheet.worksheets()
        print(worksheet_list)

    def add_college(self):
            cell = "a" + str(self.count_of_colleges)
            print(self.count_of_colleges)
            val = self.sheet.acell(cell).value
            print(val)


###################################################
###         CODE STARTS HERE:
###################################################
#Google = Google()
#Google.search()
#Google.locate_instagram()

InputData = InputData()
InputData.import_sheet()
InputData.check_if_college_exists()
#ask_continue()
