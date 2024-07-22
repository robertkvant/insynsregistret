# MIT License

# Copyright (c) 2024 Robert Kvant

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import insyn
import json
import datetime
from fastapi import FastAPI

app = FastAPI()

# Read proxy settings from file 'proxies.txt'
# The proxies.txt file should contain JSON data in the following format:
# {
#     "http": "http://<ip>:<port>",
#     "https": "http://<ip>:<port>"
# }

# Open the proxies.txt file and read its content
with open('proxies.txt') as f:
    data = f.read()

# Load the content as JSON to get the proxy settings
proxies = json.loads(data)

# Initialize the Insynsregistret class with the proxy settings
insyn = insyn.Insynsregistret(proxies=proxies)

@app.get("/getrecords/{company}/{startDate}/{endDate}")
def read_item(company: str, startDate: datetime.date, endDate: datetime.date):
    """
    Endpoint to get records for a specific company between given start and end dates.
    (Currently uses the same start and end dates for publication and transaction dates)
    
    :param company: The name of the company.
    :param startDate: The start date for records in the format YYYY-MM-DD.
    :param endDate: The end date for records in the format YYYY-MM-DD.
    :return: JSON response with the records.
    """
    return insyn.getRecords(
        company=company,
        pubFromDate=startDate,
        pubToDate=endDate,
        transFromDate=startDate,
        transToDate=endDate
    )

@app.get("/search/{company}")
def read_item(company: str):
    """
    Endpoint to search for a specific company.
        
    :param company: The name of the company.
    :return: JSON response with the search results.
    """
    return insyn.search(company)
