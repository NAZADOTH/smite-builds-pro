import sys
import pprint

from selenium import webdriver

import updater

phase = 'just a phase'
month = 9
day = 9
match_id = sys.argv[1] if len(sys.argv) > 1 else 2455
match_url = f'{updater.spl_matches_url}/{match_id}'
builds = []
with webdriver.Firefox() as driver:
    driver.implicitly_wait(3)
    builds = updater.scrape_match(driver, phase, month, day, match_url, match_id)
    pprint.pprint(builds)