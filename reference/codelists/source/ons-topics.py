from json.decoder import JSONDecodeError
from queue import Queue

from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from cachecontrol.heuristics import ExpiresAfter
from requests import Session
import csv

with open('../ons-topics.csv', 'w') as topics_file:
    topics = csv.DictWriter(topics_file, fieldnames=['Label', 'Path', 'Parent', 'Summary'])
    topics.writeheader()
    session = CacheControl(Session(), cache=FileCache('.cache'), heuristic=ExpiresAfter(days=1))
    to_visit = Queue()
    visited = set()
    for top in ['/businessindustryandtrade', '/economy', '/employmentandlabourmarket', '/peoplepopulationandcommunity']:
        to_visit.put((top, None))
    while not to_visit.empty():
        (section, parent) = to_visit.get()
        visited.add(section)
        try:
            to_fetch = f'https://www.ons.gov.uk{section}/data'
            taxon = session.get(to_fetch).json()
        except JSONDecodeError as e:
            print(f'Error fetching {to_fetch}')
            print(e)
            continue
        topics.writerow({
            'Label': taxon['description']['title'],
            'Path': taxon['uri'],
            'Parent': parent,
            'Summary': taxon['description']['summary'].strip(),
        })
        for subsection in taxon.get('sections', []):
            if subsection['uri'] not in visited:
                to_visit.put((subsection['uri'], section))
