import API

p = API.PinnacleAPI()

#sportsJSON = p.get(p.endpoints['sports'])
#sportsArr = sportsJSON['sports']

activeMarkets = p.getActiveMarkets()

#for am in activeMarkets:
#    print am
#    print p.getOdds(am['id'])
#
#for am in activeMarkets:
#    print am
#    print p.getOdds(am['id'])

SID = 29
o = p.getOdds(SID)
print o
o = p.getOdds(SID)
print o


#o = p.getOdds(22)
#OR = Pinnacle.OddsResponse(o)
#l = OR.leagues[0]
#L = Pinnacle.League(l)
#e = l.events[0]
#E = Pinnacle.Event(e)
