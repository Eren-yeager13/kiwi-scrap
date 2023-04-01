from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv


dep_city = input("Enter The Depart City : ")
dest_city = input("Enter The Destination City : ")
print(f" >>> Searching Flights From : {dep_city} >>>> {dest_city}....")


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(3)
browser.get("https://www.kiwi.com")
browser.maximize_window()


close_button = browser.find_element(By.CSS_SELECTOR,".lmWXzV")
close_button.click()

# set destination country 
dest_class = '.eOBVBy .zyCxe .ewuZzw'
destination = browser.find_element(By.CSS_SELECTOR, dest_class)
destination.send_keys(Keys.BACKSPACE)
destination.send_keys(dest_city)

time.sleep(3)
dest_choice = browser.find_element(By.CSS_SELECTOR, '.fasyeN')
dest_choice.click()

# set depart country :
dep_class = '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div[2]/div/input'
depart = browser.find_element(By.XPATH, dep_class)
depart.send_keys(Keys.BACKSPACE)
depart.send_keys(dep_city)
time.sleep(3)
dep_choice = browser.find_element(By.CLASS_NAME, 'fasyeN')
dep_choice.click()

# uncheck booking
browser.find_element(By.CLASS_NAME,"fKLfkU").click()

# set one way flight
browser.find_element(By.CLASS_NAME,"drQcMO").click()

browser.find_element(By.LINK_TEXT,"One-way").click()

# search for flights
search_class = '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[2]/a'
search = browser.find_element(By.XPATH, search_class)

search.click()

# loading more pages
for i in range(4):
    
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    browser.find_element(By.CLASS_NAME,"hXJpFI").click()
    time.sleep(5)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

time.sleep(5)
prices = []
prices_elements = browser.find_elements(By.CSS_SELECTOR,".fTIQNZ span")
for i in prices_elements:
    prices.append(i.text.strip())

#Flight date
dates = browser.find_elements(By.CLASS_NAME,'dtRWuZ')
dates_list=[]
for date in dates:
      dates_list.append(date.text.strip())


depart_time=[]
Return_Time=[]
times=browser.find_elements(By.CLASS_NAME,'cVhCfK')
for i in range (0,len(times),2):
    depart_time.append(times[i].text.strip())
    
for i in range (1,len(times),2):
     Return_Time.append(times[i].text.strip())

depart_airport=[]
Return_airport=[]
airport=browser.find_elements(By.CLASS_NAME,'jZbDQV')

for i in range (0,len(airport),2):
     depart_airport.append(airport[i].text.strip())

for i in range (1,len(airport),2):
     Return_airport.append(airport[i].text.strip())

airline=browser.find_elements(By.CLASS_NAME,'hLDGBn')

airline_name=[]
for i in airline:
     airline_name.append(i.get_attribute('alt').strip())

flight_type = []
stops_elemets = browser.find_elements(By.CSS_SELECTOR,('.eJWIKy .hGicnp .jziOCR'))
for i in stops_elemets:
    flight_type.append(i.text.strip())

card_elements = browser.find_elements(By.CLASS_NAME,"bEUNMt")

element_number = []
for elements in card_elements:
    element_number.append(elements.get_attribute('innerHTML').count("eJWIKy"))

flight_duration=[]
duration=browser.find_elements(By.CSS_SELECTOR,'.bEUNMt .eJWIKy .dPpmfj .jziOCR')
for i in duration:
    flight_duration.append(i.text.strip())



# adding prices to file.txt
with open(f"{dep_city}-{dest_city}.csv","w",encoding="utf-8",newline="") as page:
    writer = csv.writer(page)
    page.truncate()
    header = ["Price","Date","Depart_Time","Arrive_Time","Depart_Airport","Return_Airport","Airline_Name","Flight_Type","flight_duration"]
    writer.writerow(header)
    with open(f"{dep_city}-{dest_city}.csv","a",encoding="utf-8",newline="") as page:
        air = iter(airline_name)
        for i in range(len(prices)+1):
            if element_number[i] == 3:
                writer.writerow([prices[i],dates_list[i],depart_time[i],Return_Time[i],depart_airport[i],Return_airport[i],next(air),flight_type[i],flight_duration[i]])
            elif element_number[i] == 4:
                writer.writerow([prices[i],dates_list[i],depart_time[i],Return_Time[i],depart_airport[i],Return_airport[i],f"{next(air)} > {next(air)}",flight_type[i],flight_duration[i]])
            elif element_number[i] == 5:
                writer.writerow([prices[i],dates_list[i],depart_time[i],Return_Time[i],depart_airport[i],Return_airport[i],f"{next(air)} > {next(air)} > {next(air)}",flight_type[i],flight_duration[i]])
print(">>>>>>>>>>> prices added successfuly <<<<<<<<<<<<<<<<")

browser.quit()