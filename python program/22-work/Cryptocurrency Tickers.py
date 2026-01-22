import requests

url = "https://api.coinlore.net/api/tickers/"
response = requests.get(url).json()

data = response["data"]
#1
# for coin in data:
#     print(coin)
#
# print("======================================")
# #2
# for coin in data:
#     print(coin["name"])
#
# print("=======================================")
# #3
# for index, coin in enumerate(data):
#     print(index, coin["name"])
#
# print("========================================")
# #4
# for coin in data:
#     print(coin["name"], "-", coin["symbol"])
#
# print("=========================================")
# #5
# for coin in data:
#     print(coin["name"], ":", coin["price_usd"])
#
# print("===========================================")
#6
# count = 0
# for coin in data:
#     if count == 5:
#         break
#     print(coin["name"])
#     count += 1
#
# print("===========================================")
#7
# length = len(data)
# for i in range(length - 5, length):
#     print(data[i]["name"])
#
# print("===========================================")
#8
# for coin in data:
#     print(coin["name"], "Rank:", coin["rank"])
#
# print("============================================")
# #9
# for index, coin in enumerate(data):
#     print(index, coin["name"], coin["symbol"], coin["price_usd"])
#
# print("=============================================")
#10
# for index, coin in enumerate(data):
#     if index % 2 == 0:
#         print(index, coin["name"])
#
# print("==============================================")
# #11
# for index, coin in enumerate(data):
#     if index % 2 != 0:
#         print(index, coin["name"])
#
# print("================================================")
#12
# first = None
# last = None
#
# for coin in data:
#     if first is None:
#         first = coin
#     last = coin
#
# print("First Coin:", first)
# print("Last Coin:", last)
# #13
# for index, coin in enumerate(data):
#     if 5 <= index <= 10:
#         print(coin["name"])
# print("==============================")
# #14
# for coin in data:
#     print("===================================")
#     print(coin)
#     print("===================================")
#15
for coin in data:
    print("Keys:")
    for key in coin.keys():
        print(key)
    print("-------------------------")
