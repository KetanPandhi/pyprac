#!/usr/bin/python3.5

"""smeagol is a dirty crawler"""

import urllib.request

def get_data(url):
    """get data from url"""

    with urllib.request.urlopen(url) as page:
        for line in page:
            print(line)
