import time
import requests
from binascii import hexlify
from beemgraphenebase.ecdsasig import sign_message
from beem import Hive
import os
from hiveengine.api import Api
from pycoingecko import CoinGeckoAPI
from beem.instance import set_shared_blockchain_instance

cg = CoinGeckoAPI()

delay = 60
delaymins = round(delay/60, 0)
posting_key = '5xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
username = 'your-user-name'
mytoken = 'SPS'
version = 1.2

# Enables ANSI colors to be used on Wintel platform
os.system("")

nodes = ['https://api.hive.blog', 'https://api.deathwing.me', 'https://anyx.io']
hive = Hive(node=nodes, keys=[posting_key])
set_shared_blockchain_instance(hive)
api = Api()

# Kept due to HE issues occasionally, uncomment (below) if the default node gives errors
# enginenode = ['https://engine.rishipanthee.com/']
# api = Api(enginenode)

# --------------------------------------------------------------------
# StdOut console colour definitions


class Bcolors:

    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    VIOLET = '\033[35m'
    END = '\033[0m'

# --------------------------------------------------------------------


def compute_sig(string_to_sign: str, priv_key: str):
    bytestring_signature = sign_message(string_to_sign, priv_key)
    sig = hexlify(bytestring_signature).decode("ascii")
    return sig


def login(private_key: str, username: str):
    login_endpoint = "https://api2.splinterlands.com/players/login"
    ts = int(time.time() * 1000)
    sig = compute_sig(username + str(ts), private_key)
    login_endpoint += "?name=" + username + "&ts=" + str(ts) + "&sig=" + sig
    return requests.get(login_endpoint)


def stake_sps(hive: Hive, user: str, qty: float):
    hive_id: str = "sm_stake_tokens"
    request = {"token": "SPS", "qty": qty}
    hive.custom_json(hive_id, json_data=request, required_posting_auths=[user])


def get_balance(login_resp: dict, currency_token: str):
    balance: float = 0
    try:
        for entry in login_resp.get("balances"):
            if currency_token == entry.get("token"):
                balance = entry.get("balance")
                break
    except TypeError:
        print(Bcolors.RED + f"Node error getting balance, pausing for {delay} seconds.." + Bcolors.END)
        return 0
    return balance

# --------------------------------------------------------------------
# Returns the Highest Offer from the Buybook for Token


def gethighoffer(strtoken):

    book = (api.find("market", "buyBook", query={"symbol": strtoken}))
    fprice = 0
    for high in book:
        if float(high['price']) > fprice:
            fprice = float(high['price'])

    return fprice

# --------------------------------------------------------------------


print(Bcolors.GREEN + f'SPS Auto-Staker v.{version} is starting up...' + Bcolors.END)
estimated = 0

while True:
    # Get SPS High BuyBook Price.
    price = gethighoffer(mytoken)

    hiveprice = cg.get_price(ids='hive', vs_currencies='usd', include_market_cap='true')
    usdhiveprice = hiveprice['hive']['usd']

    spsprice = cg.get_price(ids='splinterlands', vs_currencies='usd', include_market_cap='true')
    usdspsprice = spsprice['splinterlands']['usd']

    login_response = login(posting_key, username).json()
    spsp_balance = get_balance(login_response, "SPSP")
    sps_balance = get_balance(login_response, "SPS")

    totalvalue = round(spsp_balance*price, 2)
    usdspstotalvalue = round(usdspsprice * spsp_balance, 2)

    print(Bcolors.CYAN + f'Unstaked {mytoken} Balance is {sps_balance}, Staked {mytoken} Balance is {spsp_balance:,}'
                         f' SPS (${usdspstotalvalue:,}) USD' + Bcolors.END)
    print(Bcolors.VIOLET + f'Staking {sps_balance}..' + Bcolors.END)
    stake_sps(hive, username, sps_balance)
    dailyincome = round(price * sps_balance * (24*delay), 2)
    usddailyincome = round(dailyincome * usdhiveprice, 2)

    if estimated > 1:
        print(Bcolors.GREEN + f'Current Estimated Daily SPS Staking is valued at {dailyincome} HIVE'
                              f' (${usddailyincome:,}) USD' + Bcolors.END)
    else:
        print(Bcolors.GREEN + f'Current Estimated Daily SPS Staking is currently undetermined...' + Bcolors.END)

    estimated += 1
    print(f' - Waiting {delaymins} minutes before staking again...')
    print()
    time.sleep(delay)
