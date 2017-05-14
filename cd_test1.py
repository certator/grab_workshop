from __future__ import print_function
from grab import Grab


def get_cd_number():
    g = Grab()
    g.go('https://www.cd.cz/default.htm')
    number = g.doc.select('//*[@class="helpdesknum"]').text()
    return number


if __name__ == '__main__':
    print('cd number', get_cd_number())