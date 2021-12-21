from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import plotly.express as px
from pprint import pprint
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

username = 'your username here'
api_key = 'Your key here'

chart_studio.tools.set_credentials_file(username=username,
                                        api_key=api_key)


symbol_list = ["BTC", "ETH", "SOL", "LUNA", "NEAR", "AVAX"]
mkt_cap_list = []

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  "symbol": "BTC,ETH,SOL,LUNA,NEAR,AVAX",
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'a1330e1e-8e84-4c06-af10-771d050574c4',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    pprint(data["data"]["BTC"]["quote"]["USD"]["market_cap"])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

for symbol in symbol_list:
    mkt_cap = data["data"][symbol]["quote"]["USD"]["market_cap"]
    mkt_cap_list.append(mkt_cap)
    #print(mkt_cap)

df = pd.read_csv("coins.csv")


df.insert(2, 'Market Cap', mkt_cap_list, True)
df["K Value"] = round(df["Market Cap"]/df["Wallets"] ** 2, 4)
print(df)

#--------- Plotting the Graph ------#

fig = px.scatter(df, x="Wallets", y="Market Cap", size="K Value",
                 hover_name="Coin", text="Coin", log_x=True, log_y=True, size_max=100, template="plotly_dark")

fig.update_xaxes(title_text="Number of Wallet in millions as of 11/22/21 (Proxy of Users)")

fig.update_yaxes(title_text="Market Cap")


fig.update_layout(title_text="Relative Valuation By Metcalfe's Law",
                  title_font_size=25,
                  title_yanchor="top",
                  title_pad_t=20)
fig.show()

fig.write_html("ML-test.html")
py.plot(fig, filename="Metcalfe", auto_open=True)
