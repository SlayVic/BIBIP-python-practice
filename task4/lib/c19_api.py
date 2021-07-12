import requests
import json

"""VACCOVID - coronavirus, vaccine and treatment tracker"""

# * Library class
class C19_info:

    # * EU api url
    url_base = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/"
    regions = [
        "australia",
        "southamerica",
        "northamerica",
        "europe",
        "africa",
        "asia",
    ]

    # * request headers
    headers = {
        "x-rapidapi-key": "d43ed9a56amsh0937df41d04fa40p14ce4bjsn8973dcf26245",
        "x-rapidapi-host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com",
    }

    # * all country dict to provide search not only by 3 laters, because API support only 3
    all_countries = {}

    def __init__(self):
        self.data = []

    def __repr__(self) -> str:
        return str(self.data)

    @classmethod
    def get_all_countries(cls):
        """Get all countries from all regions"""

        for region in cls.regions:
            response = requests.request(
                "GET", cls.url_base + region, headers=cls.headers
            )
            data = json.loads(response.text)
            # print(str(data))
            for country in data:
                cls.all_countries[country["Country"].lower()] = country[
                    "ThreeLetterSymbol"
                ].lower()
                cls.all_countries[country["TwoLetterSymbol"].lower()] = country[
                    "ThreeLetterSymbol"
                ].lower()
        pass

    def update_data_with(self, country="europe"):
        """Update data variable with required data

        Args:
            country (str, optional): get full, 3 or 2 letters name variant.
            Or use 2 letter region name like europe.
            Defaults to "europe".
        """

        country = country.lower()
        # print(country)

        try:  # * try use dict, in case user use 2/full name variant
            country = self.all_countries[country]
        except:  # * if key not found, continue with user input
            pass

        # * generate get request link
        self.url = (
            (self.url_base + country)
            if country in self.regions
            else (
                "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/api-covid-data/reports/"
                + country
            )
        )

        response = requests.request("GET", self.url, headers=self.headers)
        self.data = json.loads(response.text)

        # * Err if data is void
        assert len(self.data) > 0, "Wrong country name"

    # * json keys that commonty used by user
    common_keys = [
        "TotalCases",
        "TotalDeaths",
        "NewCases",
        "NewDeaths",
        "TotalRecovered",
        "NewRecovered",
        "ActiveCases",
        "confirmed",
        "recovered",
        "deaths",
    ]

    def get_valid_keys(self):
        """Get keys that user can use for current data

        Yields:
            str: key
        """
        for key in self.common_keys:
            if key in self.data[0]:
                yield key

    def get_sorted_data(self, key):
        """Get sorted data by key ↓ from hight to low

        Args:
            key (str): key to sort by

        Returns:
            json(list of dicts): data that sort by key
        """

        data = self.data
        data.sort(key=lambda i: int(i[key]), reverse=True)
        return data

    def get_cool_text(self, key):
        """Get line of cool styled text

        Args:
            key (str): key to sort

        Yields:
            str: line of cool styled text
        """

        data = self.get_sorted_data(key)

        # chose it country or province
        place_key = "Country" if "Country" in data[0] else "province"
        yield place_key + " " * (36 - len(place_key + key)) + key + "\n" # ret first line
        for item in data:
            # return each line of statistic
            yield (
                item[place_key]
                + " " * (36 - len(item[place_key] + key))
                + str(item[key])
                + "\n"
            )


# * get all countries when start this file or import
C19_info.get_all_countries()

# * debug and tests
if __name__ == "__main__":
    # "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/australia"
    pass
