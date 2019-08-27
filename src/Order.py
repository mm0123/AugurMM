class Order(object):
    def __init__(self, party, action, size, oType, price=None):
        # party: party placing the trade
        # action: BUY or SELL
        # size: quantity of shares specified in order
        # oType: market or limit
        # price: needed for limit orders
        self.party = party
        self.action = action
        self.size = size
        self.type = oType
        self.price = price
