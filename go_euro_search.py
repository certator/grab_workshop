from __future__ import print_function

import time
import datetime
import ujson
import pprint
from grab import Grab


def search_prague_berlin():
    g = Grab()
    g.setup(
        timeout=60,
        headers={'Content-Type': 'application/json'},
        post=ujson.dumps({
        "searchOptions": {
            "departurePosition": {"id": 375859},
            "arrivalPosition": {"id": 376217},
            "travelModes": ["Flight", "Train", "Bus"],
            "departureDate": "2017-05-22",
            "passengers": [{"age": 12, "discountCards": []}],
            "userInfo": {
                "identifier": "0.wi76ilky8xt",
                "domain": ".co.uk",
                "locale": "en",
                "currency": "EUR"},
            "abTestParameters": ["", "APIV5_TRIGGER", "main_index"]}}

    ))
    g.go('https://www.goeuro.co.uk/GoEuroAPI/rest/api/v5/searches')
    print(g.response.json['searchId'])
    searchId = g.response.json['searchId']
    g.setup(headers={})
    g.go('https://www.goeuro.co.uk/GoEuroAPI/rest/api/v5/searches/{}'.format(searchId))
    g.go('https://www.goeuro.co.uk/GoEuroAPI/rest/api/v5/results?price_from=1'
         + '&stops=0%7C1%7C2%3B-1&travel_mode=train&limit=10&offset=0'
         + '&position_report_enabled=true&all_positions=true&sort_by=price'
         + '&sort_variants=price&use_stats=true&search_id={}&ts={}'.format(
        searchId, int(time.time()*1000.0)
    ))
    result = []
    for outbound_key, outbound in g.response.json['outbounds'].items():
        dtime = datetime.datetime.strptime(outbound['departureTime'][:-10], '%Y-%m-%dT%H:%M:%S')
        atime = datetime.datetime.strptime(outbound['arrivalTime'][:-10], '%Y-%m-%dT%H:%M:%S')
        price = outbound['price'] / 100.0
        result += [(dtime, atime, price)]
    return result


if __name__ == '__main__':
    pprint.pprint((search_prague_berlin()))
