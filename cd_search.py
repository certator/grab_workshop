from __future__ import print_function

import time
import datetime
import ujson
import pprint
import re
from grab import Grab


my_date = "20.05.2017"
my_datetime = datetime.datetime.strptime(my_date,  '%d.%m.%Y')


def fill_connection_result(json):
    connection_result = []
    for connection in json['list']:
        conn_id = connection['id']
        conn_dtime = []
        conn_atime = []
        for train in connection['trains']:
            dTime = datetime.datetime.strptime(train['depDate']+train['depTime'],  '%d.%m.%Y%H:%M')
            aTime = datetime.datetime.strptime(train['arrDate']+train['arrTime'],  '%d.%m.%Y%H:%M')
            conn_dtime = [min(conn_dtime + [dTime])]
            conn_atime = [max(conn_atime + [aTime])]
        conn_price = connection['price']['price'] / 100.0
        if my_datetime.date() == conn_dtime[0].date():
            connection_result += [(conn_id, conn_dtime[0], conn_atime[0], conn_price)]
    return connection_result


def search_brno_ostrava():
    g = Grab()
    g.setup(
        timeout=60,
        post={'data': ujson.dumps(
            {
                "from": {
                    "listId": 1,
                    "name": "Brno"
                },
                "to": {
                    "listId": 1,
                    "name": "Ostrava"
                },
                "date": my_date,
                "time": "00:00",
                "isAdvanced": False,
                "doSearch": True,
                "passengers": []
            }
        )}
    )
    g.go('https://www.cd.cz/spojeni-a-jizdenka/api-hp/')

    for script in g.doc.select('//script'):
        if script.node().text is None:
            continue
        text = script.node().text.replace('\r', '')
        if 'ConnectionList' not in text:
            continue

        for line in text.splitlines():
            if 'var model = ' not in line:
                continue

            print('found model')
            result = re.match(r'\s*var\s+model\s+=\s+(.*);', line).groups()
            json = ujson.loads(result[0])

            connection_result = fill_connection_result(json)

            current_result = None

            while (current_result != []):
                g.setup(post={
                  'guid': json['guid'],
                  'SearchType': '2',
                  'pageType': '0',
                  'refreshID': json['list'][0]['id'],
                  'prevID': json['list'][1]['id'],
                  'nextID': json['list'][-2]['id'],
                  'priceType': '0',
                  'sortType': '0'
                })
                g.go('https://www.cd.cz/spojeni-a-jizdenka/getconnectionlist/')
                json = g.response.json
                current_result = fill_connection_result(json)
                connection_result += current_result

    list(set(connection_result))

    return connection_result


                    # print(g.response.json['searchId'])
    # searchId = g.response.json['searchId']
    # g.setup(headers={})
    # g.go('https://www.goeuro.co.uk/GoEuroAPI/rest/api/v5/searches/{}'.format(searchId))
    # g.go('https://www.goeuro.co.uk/GoEuroAPI/rest/api/v5/results?price_from=1'
    #      + '&stops=0%7C1%7C2%3B-1&travel_mode=train&limit=10&offset=0'
    #      + '&position_report_enabled=true&all_positions=true&sort_by=price'
    #      + '&sort_variants=price&use_stats=true&search_id={}&ts={}'.format(
    #     searchId, int(time.time()*1000.0)
    # ))
    # result = []
    # for outbound_key, outbound in g.response.json['outbounds'].items():
    #     dtime = datetime.datetime.strptime(outbound['departureTime'][:-10], '%Y-%m-%dT%H:%M:%S')
    #     atime = datetime.datetime.strptime(outbound['arrivalTime'][:-10], '%Y-%m-%dT%H:%M:%S')
    #     price = outbound['price'] / 100.0
    #     result += [(dtime, atime, price)]
    # return result


if __name__ == '__main__':
    pprint.pprint((search_brno_ostrava()))
