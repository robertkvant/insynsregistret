import requests
import unicodedata
import json

class Insynsregistret:
    """
    A class to fetch data from Insynsregistret 
    (The Swedish transparency register for share trading).

    Attributes:
        proxies (dict): A dictionary of proxies to use for requests.
    """

    def __init__(self, proxies):
        """
        Initialize the Insynsregistret class with proxies.

        Args:
            proxies (dict): A dictionary of proxies to use for requests.
        """
        self.proxies = proxies

    def getRecords(self, company, pubFromDate, pubToDate, transFromDate, transToDate):
        """
        Retrieve records from Insynsregistret.

        Args:
            company (str): The company to search for.
            pubFromDate (str): The publication start date (YYYY-MM-DD).
            pubToDate (str): The publication end date (YYYY-MM-DD).
            transFromDate (str): The transaction start date (YYYY-MM-DD).
            transToDate (str): The transaction end date (YYYY-MM-DD).

        Returns:
            list: A list object containing the retrieved records.
        """
        # Define the URL, payload, and headers for the request
        headers = {
            'accepts': "text/csv; charset=utf-8"
        }
        payload = {
            'SearchFunctionType': 'Insyn',
            'Utgivare': company,
            'Transaktionsdatum.From': transFromDate,
            'Transaktionsdatum.To': transToDate,
            'Publiceringsdatum.From': pubFromDate,
            'Publiceringsdatum.To': pubToDate,
            'button': 'export',
            'Page': '1',
        }
        url = "https://marknadssok.fi.se/Publiceringsklient/sv-SE/Search/Search"

        # Send the GET request with proxies and headers
        response = requests.get(
            url=url,
            proxies=self.proxies,
            headers=headers,
            params=payload
        )

        # Ensure the response is encoded properly
        response.encoding = response.apparent_encoding

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Process the response
        data = self.__processResponse(response)

        # Return response data as a list object
        return data

    def search(self, keyword):
        """
        Search for a company using a keyword.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: The search results as a list object.
        """
        # Define the URL and headers for the request
        headers = {
            'accepts': "application/json, text/javascript, */*; q=0.01"
        }
        payload = {
            'sokfunktion': 'Insyn',
            'sokterm': keyword,
            'falt': 'Utgivare'
        }
        url = ("https://marknadssok.fi.se/Publiceringsklient/sv-SE/AutoComplete/"
               "H%C3%A4mtaAutoCompleteListaFull")

        # Send the GET request with proxies and headers
        response = requests.get(
            url=url,
            proxies=self.proxies,
            headers=headers,
            params=payload
        )

        # Ensure the response is encoded properly
        response.encoding = response.apparent_encoding

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Return the response as a list object
        return json.loads(response.text)

    def __processResponse(self, response):
        """
        Process the response received by splitting all the lines,
        separating the headers and remove empty values.

        Args:
            response (requests.Response): The response object to process.

        Returns:
            list: A list of dictionaries containing the processed data.
        """
        # Normalize Unicode data
        csv_data = self.__normalizeEncoding(response.text)

        # Split the CSV data into lines
        lines = csv_data.splitlines()

        # Extract headers from the first line
        headers = lines[0].split(';')

        # Initialize an empty list to store the output
        output = []

        # Iterate over the remaining lines and process each row
        for line in lines[1:]:
            row = line.split(';')
            # Create a dictionary for the row, excluding empty values
            d = {k: v for k, v in dict(zip(headers, row)).items() if v}
            # Append the dictionary to the output list
            output.append(d)

        return output

    def __normalizeEncoding(self, data):
        """
        Normalize the encoding of the given data to NFKD form.

        Args:
            data (str): The data to normalize.

        Returns:
            str: The normalized data.
        """
        return unicodedata.normalize("NFKD", data)
