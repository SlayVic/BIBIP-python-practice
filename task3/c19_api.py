import requests
import json

"""VACCOVID - coronavirus, vaccine and treatment tracker"""


# * Library class
class C19_info:

    # * EU api url
    basic_url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/europe"

    # * request headers
    headers = {
        "x-rapidapi-key": "d43ed9a56amsh0937df41d04fa40p14ce4bjsn8973dcf26245",
        "x-rapidapi-host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com",
    }

    # * all country dict to provide search not only by 3 laters, because API support only 3
    all_countries = {}

    def __init__(self):
        pass

    def __repr__(self) -> str:
        return str(self.data)

    @classmethod
    def get_all_countries(cls):
        """Get all countries from all regions"""

        url_base = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/"
        regions = [
            "australia",
            "southamerica",
            "northamerica",
            "europe",
            "africa",
            "asia",
        ]
        for region in regions:
            response = requests.request("GET", url_base + region, headers=cls.headers)
            data = json.loads(response.text)
            for country in data:
                cls.all_countries[country["Country"].lower()] = country[
                    "ThreeLetterSymbol"
                ].lower()
                cls.all_countries[country["TwoLetterSymbol"].lower()] = country[
                    "ThreeLetterSymbol"
                ].lower()
        pass

    def update_data_with(self, country=""):
        """Update data variable with required data

        Args:
            country (str, optional): get full, 3 or 2 letters name variant.
            if void make update with EU data.
            Defaults to "".
        """
        try:  # * try use dict, in case user use 2/full name variant
            country = self.all_countries[country.lower()]
        except:  # * if key not found, continue with user input
            pass

        # * generate get request link
        self.url = (
            "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/api-covid-data/reports/"
            + country
            if country
            else self.basic_url
        )

        response = requests.request("GET", self.url, headers=self.headers)
        self.data = json.loads(response.text)

        # * Err if data is void
        assert len(self.data) > 0, "Wrong country name"

    # * json keys that will not include to the table
    table_not_include = [
        "id",
        "rank",
        "Continent",
        "TwoLetterSymbol",
        "ThreeLetterSymbol",
        "name",
        "iso",
        "Tests_1M_Pop",
        "TotCases_1M_Pop",
        "one_Testevery_X_ppl",
    ]

    def get_table_columns(self) -> dict:
        """Make dictionary like this
        data = {'col1':['1','2','3','4'],
                'col2':['1','2','1','3'],
                'col3':['1','1','2','1']}
        """
        table = {}
        # * make void table with needed keys(columns) 
        for key in self.data[0].keys():
            # * skip keys from exceptions
            if key in self.table_not_include:
                continue
            table[key] = []

        # * fill keys(columns)
        for country in self.data:
            for key in country.keys():
                # * skip keys from exceptions
                if key in self.table_not_include:
                    continue
                table[key].append(str(country[key]))
        return table

# * get all countries when start this file or import
C19_info.get_all_countries()

# * debug and tests
if __name__ == "__main__":
    country = C19_info()

    country.update_data_with("ua")
    table = country.get_table_columns()
    for key in table.keys():
        print(key)
