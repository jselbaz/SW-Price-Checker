from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PyMessenger.PyMessenger import Email, SMS, Messenger

# Set this URL for the price you want to track
URL = 'https://www.google.com/travel/flights/booking?tfs=CBwQAho_EgoyMDI0LTA3LTA2Ih8KA01EVxIKMjAyNC0wNy0wNhoDTEdBKgJXTjIDNTY1agcIARIDTURXcgcIARIDTEdBQAFIAXABggELCP___________wGYAQI&tfu=CmhDalJJU0hGTk1XTnRhRVZ4VFhkQlJraDVTM2RDUnkwdExTMHRMUzB0TFhaMGRXWXhPVUZCUVVGQlIxcHpaSGMwUTB4MmVWZEJFZ1ZYVGpVMk5Sb0tDUHdxRUFJYUExVlRSRGdkY1B3cRICCAAiAA&hl=en-US&gl=US'
# Enter your gmail creds here - email address and app password in single quotes.
my_messenger = Messenger('emailaddress@gmail.com', 'apppassword')
# Set comparison price
current_price=500 #change this

# Create an App Password for gmail here https://myaccount.google.com/apppasswords
to      = 'youremail@gmail.com'
subject = 'Price Drop for Flight'
body    = 'Flight has dropped in price!'
email_msg     = Email(to, subject, body, is_HTML=False)

# Text notifications
number    = 'yourphonenumber' # Example US phone number and it must include the country code 
gateway   = '@tmomail.net' # For a Tmobile number
subject   = 'Flight Price Drop'
body      = 'Flight has dropped in price!\n'
txt_msg       = SMS(number, gateway, subject, body)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--enable-javascript")
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
driver.implicitly_wait(2)
price = driver.find_element(By.CLASS_NAME, "tZe0ff").text
price = price[1:]
price = int(price)
driver.quit()
if price < current_price:
    # Send the notifications
    my_messenger.send_email(email_msg, one_time=True) 
    my_messenger.send_sms(txt_msg, one_time=True)
