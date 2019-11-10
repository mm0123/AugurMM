import API

import pprint
pprint = pprint.pprint

ao = API.AsianOddsAPI()

pprint(ao.getAccountSummary())

pprint(ao.getLeagues(sportName='Football'))
pprint(ao.getLeagues(sportName='Football', marketTimeName='Early'))

#TODO: make asianodds methods that are similar to below
#sportsJSON = p.get(p.endpoints['sports'])
#sportsArr = sportsJSON['sports']

#activeMarkets = p.getActiveMarkets()

#for am in activeMarkets:
#    print am
#    print p.getOdds(am['id'])
#
#for am in activeMarkets:
#    print am
#    print p.getOdds(am['id'])

#SID = 29
#o = p.getOdds(SID)
#pos = p.getPosition()
#print pos
#print o
#o = p.getOdds(SID)
#print o


#o = p.getOdds(22)
#OR = Pinnacle.OddsResponse(o)
#l = OR.leagues[0]
#L = Pinnacle.League(l)
#e = l.events[0]
#E = Pinnacle.Event(e)
