from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import smtplib
import boto3
import os

client = boto3.client('ssm')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('flight_pricing')

def lambda_handler(event, context):

    #get parameters from SSM and store them in variables
    response = client.get_parameters(
        Names = [
            'RecipientCell', #cell number to text alerts to
            'RecipientEmail', #email to send alerts to
            'SenderEmail', #email to send alerts from
            'SenderEmailAppPassword' #app password for sender email
            ],
            WithDecryption=True
        )
        
    response = response.get('Parameters')

    for item in response:
        if item['Name'] == 'RecipientCell':
            RecipientCell = item['Value']
        elif item['Name'] == 'RecipientEmail':
            RecipientEmail = item['Value']
        elif item['Name'] == 'SenderEmail':
            SenderEmail = item['Value']
        elif item['Name'] == 'SenderEmailAppPassword':
            SenderEmailAppPassword = item['Value']

    def initialise_driver():
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_argument("--no-zygote")
        chrome_options.add_argument("--single-process")
        chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

        service = Service(
            executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
            service_log_path="/tmp/chromedriver.log"
        )

        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )

        return driver
    
    driver = initialise_driver()

    dict_builder = []
    
    #flight number and google flights URL stored as env vars in lambda as FLIGHT1, FLIGHT2, URL1, URL2, etc
    for name in os.environ.keys():
        if ("FLIGHT" in name) or ("URL" in name):
            dict_builder.append(name)

    dict_builder = sorted(dict_builder)

    length = (len(dict_builder)//2)

    flights = []

    for i in range(length):
        ref_dict_i = {}
        ref_dict_i["flight"] = int(os.environ[dict_builder[i]])
        ref_dict_i["url"] = os.environ[dict_builder[i+length]]
        flights.append(ref_dict_i)

    def check_price(flight_num):
        response =  table.get_item(Key={
            'flight': flight_num
        })
        current_price = response.get('Item')['price']

        return current_price

    # Create an App Password for gmail here https://myaccount.google.com/apppasswords
    def notify(flight_num, current_price, price):
        email_message = f"Subject: Price Drop for Flight " + str(flight_num) + "\n\nFlight " + str(flight_num) + " has dropped from $" + str(current_price) + " to $" + str(price) 
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls() # Encrypts the email
        s.login(SenderEmail, SenderEmailAppPassword)
        s.sendmail(SenderEmail, RecipientEmail, email_message)  # This sends you an email
        s.sendmail(SenderEmail, RecipientCell, email_message)  # This sends you a text
        s.quit()

    for flight in flights:
        driver.get(flight['url'])
        driver.implicitly_wait(15)
        price = driver.find_element(By.CLASS_NAME, "tZe0ff").text
        price = price[1:]
        price = int(price)

        check=table.get_item(Key={'flight': flight['flight']})
        if check.get('Item') == None:
            table.put_item(Item={
                'flight': flight['flight'],
                'price': price
            })
            current_price=price
        else:
            current_price=check_price(flight['flight']) 

        
        if price < current_price:
            # Send the notifications
            notify(flight['flight'], current_price, price)
            table.put_item(Item={
                'flight': flight['flight'],
                'price': price
            })

    driver.close()
    driver.quit()

    return {
        "statusCode": 200,
        "body": "Prices checked!"
    }
