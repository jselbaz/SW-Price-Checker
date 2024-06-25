# SW Price Checker

## Summary
Now that Southwest has their prices listed on google flights this script allows you to scrape and compare prices to a manually set baseline. If the price drops you can either email or text yourself an alert so you can rebook at the lower price.

## Installation
Recommend installing pip to manage dependencies
pip install -r /path/to/requirements.txt

This requires an App Password if using gmail which can be created [here](https://myaccount.google.com/apppasswords)

## Cell Phone Details to enable text notifications
|Provider|Gateway|
|--------|-------|
|AT&T|@txt.att.net|
|Sprint|@messaging.sprintpcs.com or @pm .sprint.com|
|T-Mobile|@tmomail.net|
|Verizon|@vtext.com|
|Boost Mobile|@myboostmobile.com|
|Cricket|@sms.mycricket.com|
|Metro PCS|@mymetropcs.com|
|Tracfone|@mmst5.tracfone.com|
|U.S. Cellular|@email.uscc.net|
|Virgin Mobile|@vmobl.com|

## Automation
I recommend making a cron job or scheduling a batch file to run this every few hours