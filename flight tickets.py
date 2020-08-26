from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time,datetime,pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart

browser = webdriver.Chrome("D:\chromedriver.exe")


#Setting ticket types paths
return_ticket = "//label@id='flight-type-roundtrip-label-hp-flight']"
one_way_ticket = "//label@id='flight-type-one-way-label-hp-flight']"
multi_ticket = "//label@id='flight-type-multi-dest-label-hp-flight']"


def pick_ticket(ticket):

    try:
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as e:
        pass


def pick_dep_country(dep_country):  # Departure country ticket
    fly_from = browser.find_element_by_xpath("//input[@id='flight-origin-hp-flight']")
    time.sleep(1)  # Giving the page's elements time to load
    fly_from.clear()  # Clear stuff that was recorded previously
    time.sleep(1.5)
    fly_from.send_keys('Malaysia')
    time.sleep(1.5)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")   # The first choice appears from drop-off menu
    time.sleep(1.5)
    first_item.click()


def pick_arriv_country(arriv_country):  # Arrival country ticket
    fly_to = browser.find_element_by_xpath("//input[@id='flight-destination-hp-flight']")
    time.sleep(1)
    fly_to.clear()
    time.sleep(1.5)
    fly_to.send_keys('Canada')
    time.sleep(1.5)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()


def pick_dep_country(month, day, year):   # Choosing the date

    dep_date_button = browser.find_element_by_xpath("//input[@id='flight-departing-hp-flight']")
    dep_date_button.clear()
    dep_date_button.send_keys('08' + '/' + '31' + '/' + '2019')


def pick_return_date(month, day, year):
    return_date_button = browser.find_element_by_xpath("//input[@id='flight-returning-hp-flight']")

    for i in range(11):
        return_date_button.send_keys(Keys.BACKSPACE)
    return_date_button.send_keys('09' + '/' + '07' + '/' + '2019')


def search():
    search = browser.find_element_by_xpath("//button[@class='btn-primary btn-action gcw-submit']")
    search.click()
    time.sleep(15)
    print('The results have been loaded.')
    


df = pd.DataFrame()
def compile_data():
    global df
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list


    #departure times
    dep_times = browser.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]


    #arrival times
    arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]


    #airline name
    airlines = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]


    #prices
    prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text for value in prices]


    #durations
    durations = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]


    #stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]


    #layovers
    layovers = browser.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
    layovers_list = [value.text for value in layovers]


    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'price' + '(' + current_date + '---' + current_time + ')'
    for i in range(len(dep_times_list)):
        try:
            df.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'airline'] = airlines_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'layovers'] = layovers_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, str(current_price)] = price_list[i]
        except Exception as e:
            pass

    print('Excel Sheet has been created')



#email credentials
username = 'kennytoong129@hotmail.com'
password = 'kennytoong131'

def mail(username, password):
    global server
    server = smtplib.SMTP('smtp.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)

    
#Create message template for email
def generate_msg():
    global msg
    msg = '\nCurrent Cheapest flight:\n\nDeparture time: {}\nArrival time: {}\nAirline: {}\nFlight duration: {}\nNo. of stops: {}\nPrice: {}\n'.format(cheapest_dep_time,
                       cheapest_arrival_time,
                       cheapest_airline,
                       cheapest_duration,
                       cheapest_stops,
                       cheapest_price)


def send_email(msg):
    global message
    message = MIMEMultipart()
    message['Subject'] = 'Current Best flight'
    message['From'] = 'kennytoong129@hotmail.com'
    message['to'] = 'kennytoong129@hotmail.com'
    server.sendmail('kennytoong129@hotmail.com', 'kennytoong129@hotmail.com', msg)


for i in range(8):    
    link = 'https://www.expedia.com/'
    browser.get(link)
    time.sleep(5)
    #choose flights only
    flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
    flights_only.click()
    ticket_chooser(return_ticket)
    dep_country_chooser('Malaysia')
    arrival_country_chooser('Canada')
    dep_date_chooser('31', '08', '2019')
    return_date_chooser('07', '09', '2019')
    search()
    compile_data()
    #save values for email
    current_values = df.iloc[0]
    cheapest_dep_time = current_values[0]
    cheapest_arrival_time = current_values[1]
    cheapest_airline = current_values[2]
    cheapest_duration = current_values[3]
    cheapest_stops = current_values[4]
    cheapest_price = current_values[-1]
    print('run {} completed!'.format(i))
    create_msg()
    connect_mail(username,password)
    send_email(msg)
    print('Email sent!')
    df.to_excel('flights.xlsx')
    time.sleep(3600)


