import requests
import sys

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
    # initialization methods
    def __init__(self):
        API.__init__(self)
        self.sports = {}
        self.marketTypeIds = {
            'Live' : 0,
            'Today' : 1,
            'Early' : 2
        }

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

        print("Message from AO: %s" % reg_rsp['Result']['TextMessage'])
        if (reg_rsp['Code'] == 0 and reg_rsp['Result']['Success'] == True):
            self._auth_headers = init_headers
            del self._auth_headers['AOKey']

            self.init_sports()
            print("success: AsianOdds API setup")
            return
        else:
            sys.stderr.write(str(reg_rsp) + "\n")
            sys.exit("Error setting up AsianOdds API")

    def init_sports(self):
        self.sports = {}
        sports_rsp = self.getSports()
        if sports_rsp['Code'] == 0:
            sports = sports_rsp['Data']
            for sport in sports:
                self.sports[sport['Name']] = sport
            print("success: AsianOdds sports codes setup")
        else:
            sys.stderr.write(str(sports_rsp) + "\n")
            sys.exit("Error setting up AsianOdds sports codes")

    # straight AsianOdds API methods

        # 2. Bet Details
    def getBets(self):
        return self.get('/GetBets')

    def getBetByReference(self):
        pass

    def getRunningBets(self):
        pass

    def getNonRunningBets(self):
        pass

        # 3. Account Summary
    def getAccountSummary(self):
        return self.get('/GetAccountSummary')

    def getHistoryStatement(self):
        pass

            # ...

        # 4. Betting Methods
    def getLeagues(self,
     sportsType=None, marketTypeId=None, bookies=None, since=None,
     sportName=None, marketTimeName=None):

        if sportsType == None:
            if sportName == None:
                raise Exception("sports type or sports name is required")
            else:
                sportsType = self.sports[sportName]['Id']

        if marketTypeId == None and marketTimeName:
            marketTypeId = self.marketTypeIds[marketTimeName]

        optionals = ''
        if marketTypeId:
            optionals += '&marketTypeId=%s' % marketTypeId

        if bookies:
            optionals += '&bookies=%s' % bookies

        if since:
            optionals += '&since=%s' % since

        print("Getting: %s" % '/GetLeagues?sportsType=%s'%sportsType + optionals)
        return self.get('/GetLeagues?sportsType=%s'%sportsType + optionals)


    def getSports(self):
        return self.get('/GetSports')

    # additional helper methods
    def getOdds():
        pass

    def getPosition():
        pass
