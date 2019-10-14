import requests
import sys

import Pinnacle

# Encapsulates API connection details (authorization, url, etc)
class API(object):
    def __init__(self):
        self._base_url = None
        self._auth_headers = None

    # returns JSON object which is preferable to text which is the default
    def get(self, endpoint):
        rsp = requests.get(self._base_url + endpoint,
                           headers=self._auth_headers)
        try:
            return rsp.json()
        except ValueError as error:
            print >> sys.stderr, "endpoint: %s" % endpoint
            print >> sys.stderr, "status=%s, text=%s" % (rsp.status_code, rsp.text)
            print >> sys.stderr, "%s" % error
            return {}

    def getOdds():
        pass #should return an OddsResponse object

    def getPosition():
        pass

class AsianOddsAPI(API):
    def __init__(self):
        API.__init__(self)
        init_url = 'http://webapi.asianodds88.com/AsianOddsService'
        init_headers = {'accept': 'application/json'}
        user = 'webapiuser46'
        _pass = '734a564318d673471041efd1c8799da6' # FIXME security

        auth_url = init_url + '/Login?username=%s&password=%s' % (user, _pass)
        auth_rsp = requests.get(auth_url, headers = init_headers).json()
        auth_res = auth_rsp['Result']

        self._base_url = auth_res['Url']
        init_headers['AOKey'] = auth_res['Key']
        init_headers['AOToken'] = auth_res['Token']

        register_url = self._base_url + ('/Register?username=%s' % user)
        reg_rsp = requests.get(register_url, headers = init_headers).json()

        if (reg_rsp['Code'] == 0 and reg_rsp['Result']['Success'] == True):
            self._auth_headers = init_headers
            del self._auth_headers['AOKey']
            print("AsianOdds API Setup Successful")
            return
        else:
            sys.stderr.write(str(reg_rsp) + "\n")
            sys.exit("Error setting up AsianOdds API")

    def getAccountSummary(self):
        return self.get('/GetAccountSummary')

    def getOdds():
        pass

    def getPosition():
        pass

### not using this for now, using the AsianOdds API instead ###
#class PinnacleAPI(API):
#    def __init__(self):
#        self._base_url = 'http://api.ps3838.com'
#        self._key = 'QUM4ODBCUzYwMTpwIW5uQGNMMw==' # FIXME security
#        self._auth_headers = {'Authorization': 'Basic %s' % self._key}
#        self.endpoints = {
#            'sports': '/v2/sports',
#            'odds': '/v1/odds',
#            'bets': '/v1/bets',
#        }
#        self._lastOddsUpdateFor = {}
#        self._oddsCache = {}
#
#    def getActiveMarkets(self):
#        sportsArr = self.get(self.endpoints['sports'])['sports'] # pinnacle only has sports markets (i think)
#        return filter(lambda s: s['hasOfferings'], sportsArr) # 'hasOfferings' = "Whether the sport currently has event"
#
#    def getOdds(self, sportId, isLive=0, oddsFormat="AMERICAN"):
#        url = self.endpoints['odds'] + "?sportId=%s" % sportId
#        url += "&isLive=%s" % isLive
#        url += "&oddsFormat=%s" % oddsFormat
#
#        if (self._oddsCache.get(sportId) is None): # no saved data, must request
#            print "NEW"
#            oddsJSON = self.get(url)
#            self._oddsCache[sportId] = None if oddsJSON == {} else Pinnacle.OddsResponse(oddsJSON)
#        else: # use the "since" parameter and update current record
#            print "OLD"
#            odds = self._oddsCache[sportId]
#            recentOdds = self.get(url + "&since=%s" % odds.last)
#            odds.update(recentOdds)
#
#        return self._oddsCache[sportId]
#
#    def getPosition(self):
#        url = self.endpoints['bets']
#        url += "?betlist=running&fromDate=2019-07-29&toDate=2019-08-15"
#        return self.get(url)
