import requests
import sys

import Pinnacle

# Encapsulates API connection details (authorization, url, etc)
class API(object):
    def __init__(self):
        self._base_url = None
        self._key = None
        self._auth_header = None

    # returns JSON object which is preferable to text which is the default
    def get(self, endpoint):
        rsp = requests.get(self._base_url + endpoint,
                           headers=self._auth_header)
        try:
            return rsp.json()
        except ValueError as error:
            print >> sys.stderr, "%s: for endpoint: %s" % (error, endpoint)
            return {}

class PinnacleAPI(API):
    def __init__(self):
        self._base_url = 'http://api.ps3838.com'
        self._key = 'QUM4ODBCUzYwMTpwIW5uQGNMMw=='
        self._auth_header = {'Authorization': 'Basic %s' % self._key}
        self.endpoints = {
            'sports': '/v2/sports',
            'odds': '/v1/odds' 
        }
        self._lastOddsUpdateFor = {}
        self._oddsCache = {}

    def getActiveMarkets(self):
        sportsArr = self.get(self.endpoints['sports'])['sports'] # pinnacle only has sports markets as far as i can tell
        return filter(lambda s: s['hasOfferings'], sportsArr) # 'hasOfferings' = "Whether the sport currently has event"

    def getOdds(self, sportId, isLive=0, oddsFormat="AMERICAN"):
        url = self.endpoints['odds'] + "?sportId=%s" % sportId
        url += "&isLive=%s" % isLive
        url += "&oddsFormat=%s" % oddsFormat

        if (self._oddsCache.get(sportId) is None): # no saved data, must request
            print "NEW"
            oddsJSON = self.get(url)
            self._oddsCache[sportId] = None if oddsJSON == {} else Pinnacle.OddsResponse(oddsJSON)
        else: # use the "since" parameter and update current record
            print "OLD"
            odds = self._oddsCache[sportId]
            recentOdds = self.get(url + "&since=%s" % odds.last)
            odds.update(recentOdds)

        return self._oddsCache[sportId]
