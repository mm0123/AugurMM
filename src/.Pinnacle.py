class Response(object):
    pass

class OddsResponse(Response):
    def __init__(self, json):
        self.sportId = json['sportId'] # "Same as requested sport Id"
        self.last = json['last'] # Use this value for subsequent requests (since paramter)
        _leagues = json['leagues'] # "Contains a list of Leagues"
        self.leagues = map(lambda l: League(l), _leagues)

    def update(self, json):
        print "UPDATING. given: %s" % json

    def __repr__(self):
        return "OddsResponse id:%s\tlast:%s\n\tleagues:%s" % (self.sportId,
         self.last, self.leagues)

class League(object):
    def __init__(self, json):
        self.id = json['id'] # "League ID"
        _events = json['events'] # "Contains a list of events"
        self.events = map(lambda e: Event(e), _events)

    def __repr__(self):
        return "League id:%s\n\t\tevents:%s" % (self.id, self.events)

class Event(object):
    def __init__(self, json):
        self.id = json['id'] # "Event ID"
        _periods = json['periods'] # "Contains a list of period"
        self.periods = map(lambda p: Period(p), _periods)
        self.awayScore = json.get('awayScore') # "Away team score. Only for live soccer events"
        self.homeScore = json.get('homeScore') # "Home team score. Only for live soccer events"
        self.awayRedCards = json.get('awayRedCards') # "Home team red cards. Only for live soccer events"
        self.homeRedCards = json.get('homeRedCards') # "Home team red cards. Only for live soccer events"

    def __repr__(self):
        spc = "\n\t\t\t"
        return "Event id:%s%s%s%s%s%s" % (self.id,
         '' if self.awayScore is None else "%sawayScore: %s" % ('\t', self.awayScore),
         '' if self.homeScore is None else "%shomeScore: %s" % ('\t', self.homeScore),
         '' if self.awayRedCards is None else "%sawayRedCards: %s" % ('\t', self.awayRedCards),
         '' if self.homeRedCards is None else "%shomeRedCards: %s" % ('\t', self.homeRedCards),
         spc + str(self.periods))


class Period(object):
    def __init__(self, json):
        self.lineId = json['lineId'] # "Line ID"
        self.number = json['number'] # "Period of the match. eg. 0=Game 1=1stHalf 2=2ndHalf"
        self.cutoff = json['cutoff'] # "Period's wagering cut-off date"

        _spreads = json.get('spreads') # "Container for spread odds"
        self.spreads = None if _spreads is None else map(lambda s: Spread(s), _spreads)

        _totals = json.get('totals') # "Container for total odds"
        self.totals = None if _totals is None else map(lambda t: TotalPoints(t), _totals)

        self.moneyLine = json.get('moneyLine') # "Container for moneyLine odds"
        self.teamTotal = json.get('teamTotal') # "Container for team total points"
        self.maxSpread = json.get('maxSpread') # "Maximum spread bet. Only in straight odds response."
        self.maxTotal = json.get('maxTotal') # "Maximum total points bet.  ..."
        self.maxMoneyLine = json.get('maxMoneyLine') # "Maximum moneyline bet. ..."
        self.maxTeamTotal = json.get('maxTeamTotal') # "Maximum team total points bet. ..."

    def __repr__(self):
        spc = "\n\t\t\t\t"
        return "%sLine id:%s\tNumber:%s\tCutoff:%s%s%s%s%s%s%s%s%s" % (
         spc, self.lineId, self.number, self.cutoff,
         '' if self.spreads is None else "%sspreads: %s" % (spc, self.spreads),
         '' if self.totals is None else "%stotals: %s" % (spc, self.totals),
         '' if self.moneyLine is None else "%smoneyLine: %s" % (spc, self.moneyLine),
         '' if self.teamTotal is None else "%steamTotal: %s" % (spc, self.teamTotal),
         '' if self.maxSpread is None else "%smaxSpread: %s" % (spc, self.maxSpread),
         '' if self.maxTotal is None else "%smaxTotal: %s" % (spc, self.maxTotal),
         '' if self.maxMoneyLine is None else "%smaxMoneyLine: %s" % (spc, self.maxMoneyLine),
         '' if self.maxTeamTotal is None else "%smaxTeamTotal: %s" % (spc, self.maxTeamTotal))

class Spread(object):
    def __init__(self, json):
        self.altLineId = json.get('altLineId') # "This is present only if it's alternative line."
        self.hdp = json['hdp'] # "Home team handicap"
        self.away = json['away'] # "Away team price"
        self.home = json['home'] # "Home team price"

    def __repr__(self):
        return "%s hdp: %s\tawayPrice: %s\thomePrice: %s\n\t\t\t\t\t" % (
         "" if self.altLineId is None else "altLineId: " + str(self.altLineId),
         self.hdp, self.away, self.home)

class MoneyLine(object):
    def __init__(self, json):
        self.away = json['away'] # "Away team price"
        self.home = json['home'] # "Home team price"
        self.draw = json['draw'] # "Draw price. This is present only for events we offer price for draw."

class TotalPoints(object):
    def __init__(self, json):
        self.altLineId = json.get('altLineId') # "This is present only if it's alternative line"
        self.points = json['points'] # "Total points"
        self.over = json['over'] # "Over price"
        self.under = json['under'] # "Under price"

    def __repr__(self):
        spc = "\n\t\t\t\t\t"
        return "%s%sPoint: %s\tover: %s\tunder: %s" % (spc, 
         '' if self.altLineId is None else "altLineId: %s\t" % self.altLineId,
         self.points, self.over, self.under)

class TeamTotalPoints(object):
    def __init__(self, json):
        self.away = json.get('away') # "Away team total points"
        self.home = json.get('home') # "Home team total points"
