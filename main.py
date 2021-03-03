from bs4 import BeautifulSoup
import os
import requests
import lxml
from twilio.rest import Client

website = "https://www.amazon.ca/Premium-Aluminum-Adjustable-Articulating-STAND-V001Q/dp/B01LYVCEIB/ref" \
          "=pd_ys_c_rfy_6369487011_0?_encoding=UTF8&pd_rd_i=B01LYVCEIB&pd_rd_r=6S2M24NJPH3YK1GV6QBB&pd_rd_w=NND14" \
          "&pd_rd_wg=thZYt&pf_rd_p=459cc93f-7985-4874-99f3-2b78ddf7306e&psc=1&refRID=HVH4172D715B2X288QWC "
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81",
    "Accept-Language": "en-US,en;q=0.9"
}
response = requests.get(url=website, headers=headers)
webpage = response.text

soup = BeautifulSoup(webpage, "lxml")
price = float(soup.find(name="span", id="priceblock_ourprice").text[5:])

ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
TWILIO_PHONE = os.environ.get('TWILIO_PHONE')
PHONE_OUT = os.environ.get('PHONE_OUT')

threshold = 80

if price < threshold:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        body=f"The price has fallen below the threshold of ${threshold}, it is now {price}",
        from_=TWILIO_PHONE,
        to=PHONE_OUT
    )
    print(message.status)
else:
    print(f"Sorry the price is too high, sitting at ${price}")
