from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#plain text passwords probably not a good practice
url = 'postgresql://bets_rw:Footer123!@bets-1.ckbpeclcmqau.ca-central-1.rds.amazonaws.com:5432/bets'
Engine = create_engine(url, echo=True)
Base = declarative_base()

class Bet(Base):
    __tablename__ = 'BetsTable'

    id = Column(Integer, primary_key=True)
    sport_id = Column(String)
    sell_put = Column(Integer)
    buy_put = Column(Integer)
    create_date = Column(String)
    start_date = Column(String)
    end_date = Column(String)

    def __repr__(self):
        return "<Bet(sport_id='%s', sell_put='%s', buy_put='%s'" % (
            self.sport_id, self.sell_put, self.buy_put
        )

class BetDAO(object):
    sessionmaker = sessionmaker(bind=Engine)

    @staticmethod
    def insertBets(bets):
        if BetDAO.sessionmaker is None:
            print >> sys.stderr, "Tried to insert inset BetsTable without creating session."
            return
        elif not bets:
            return
        else:
            session = BetDAO.sessionmaker()
            session.add_all(bets)
            session.commit()

    @staticmethod
    def queryBetsBySportId(sportId):
        if BetDAO.sessionmaker is None:
            print >> sys.stderr, "Tried to insert inset BetsTable without creating session."
            return None
        else:
            session = BetDAO.sessionmaker()
            return session.query(Bet).filter_by(sport_id=sportId)


#Initialize table, run once
#Base.metadata.create_all(Engine)

#Create Dummy Bet
dummy_bet = Bet(sport_id='123', sell_put=10, buy_put=10, create_date="01/01/2019", start_date="01/03/2019", end_date="01/04/2019")

#Insert into Database
BetDAO.insertBets([dummy_bet])

#Iterate over bets
for bet in BetDAO.queryBetsBySportId('123'):
    print bet.id


# import API
#
# class Odds(object):
#     def __init__(self, odds, fmt):
#         if (fmt == "American"):
#             if odds[0] == '+':
#                 n = float(odds[1:])
#                 self.percent = 100 / (100 + n)
#             elif odds[0] == '-':
#                 n = float(odds[1:])
#                 self.percent = n / (n + 100)
#             else:
#                 raise Exception("Asked to convert American odds but odds not\
#                  given in American format")


#p = API.PinnacleAPI()

#this file should have some classes for database / interfacing with a database

#using the pinnacle API, store data about active markets in a database
