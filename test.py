import insyn
import json

# Read proxy settings from file 'proxies.txt'
# {
#     "http": "http://<ip>:<port>",
#     "https": "http://<ip>:<port>"
# }

with open('proxies.txt') as f:
    data = f.read()

proxies = json.loads(data)

id = "Axfood"

insyn = insyn.Insynsregistret(proxies=proxies)

print(insyn.getRecords(company=id
                       ,pubFromDate='2023-05-10'
                       ,pubToDate='2024-07-13'
                       ,transFromDate='2023-05-10'
                       ,transToDate='2024-07-13'))

#print(insyn.search(id))