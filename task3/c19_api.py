import requests
import json

'''VACCOVID - coronavirus, vaccine and treatment tracker'''


class C19_info:
    basic_url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/europe"
    headers = {
        'x-rapidapi-key': "d43ed9a56amsh0937df41d04fa40p14ce4bjsn8973dcf26245",
        'x-rapidapi-host': "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
    }
    all_countries = {}

    def __init__(self):
        self.get_all_countries()

    def __repr__(self) -> str:
        return str(self.data)

    def get_all_countries(self):
        url_base = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/"
        regions = ['australia', 'southamerica',
                   'northamerica', 'europe', 'africa', 'asia']
        for region in regions:
            response = requests.request(
                "GET", url_base+region, headers=self.headers)
            data = json.loads(response.text)
            for country in data:
                self.all_countries[country["Country"].lower(
                )] = country["ThreeLetterSymbol"].lower()
                self.all_countries[country["TwoLetterSymbol"].lower(
                )] = country["ThreeLetterSymbol"].lower()
        pass

    def update_data_with(self, country=''):
        try:
            country = self.all_countries[country.lower()]
        except:
            pass
        self.url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/api-covid-data/reports/" + \
            country if country else self.basic_url
        response = requests.request("GET", self.url, headers=self.headers)
        self.data = json.loads(response.text)
        assert len(self.data) > 0, "Wrong country name"

    table_not_include = ["id", 
                         "rank", 
                         "Continent", 
                         "TwoLetterSymbol", 
                         "ThreeLetterSymbol",
                         "name", 
                         "iso", 
                         "Tests_1M_Pop", 
                         "TotCases_1M_Pop", 
                         "one_Testevery_X_ppl"]

    def get_table_colloms(self) -> dict:
        """Make dictionary like this
        data = {'col1':['1','2','3','4'],
                'col2':['1','2','1','3'],
                'col3':['1','1','2','1']}
        """
        table = {}
        for key in self.data[0].keys():
            if key in self.table_not_include:
                continue
            table[key] = []

        for country in self.data:
            for key in country.keys():
                if key in self.table_not_include:
                    continue
                table[key].append(str(country[key]))
        return table


if __name__ == '__main__':
    # basic = C19_info()
    # print(basic.response.text)
    country = C19_info()

    country.update_data_with('ua')
    table = country.get_table_colloms()
    for key in table.keys():
        print(key)
    # print(country)
