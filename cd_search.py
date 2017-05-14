from __future__ import print_function

import time
import datetime
import ujson
import pprint
import re
from grab import Grab


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
                "date": "15.05.2017",
                "time": "09:00",
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
            if 'var model = ' in line:
                print('found model')
                result = re.match(r'\s*var\s+model\s+=\s+(.*);', line).groups()
                json = ujson.loads(result[0])
                connection_result = []
                for connection in json['list']:
                    conn_dtime = None
                    conn_atime = None
                    for train in connection['trains']:
                        dTime = datetime.datetime.strptime(train['depDate']+train['depTime'],  '%d.%m.%Y%H:%M')
                        aTime = datetime.datetime.strptime(train['arrDate']+train['arrTime'],  '%d.%m.%Y%H:%M')
                        if conn_dtime is not None:
                            conn_dtime = min(conn_dtime, dTime)
                        else:
                            conn_dtime = dTime
                        if conn_atime is not None:
                            conn_atime = max(conn_atime, aTime)
                        else:
                            conn_atime = aTime
                    conn_price = connection['price']['price'] / 100.0
                    connection_result += [(conn_dtime, conn_atime, conn_price)]
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
