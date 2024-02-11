import stock_storage.stock as stock


class Invest:

# 01
    def __init__(self):
        self.stock = {'name':stock.player_1.name[19],'code':'s020','price':stock.player_1.start[19],'change':0}
        self.msg = ''
        self.priceHistory = [self.stock['price']]
        self.ratio = 1
        self.initialPrice = self.stock['price']
    
# 02
    def priceManager(self):
        self.stock['price'] = int(self.initialPrice * self.ratio)

# 03
    def buyStock(self):
        if stock.player_1.player['cash'] >= self.stock['price']:
            stock.player_1.player['s020'][1] += self.stock['price']
            stock.player_1.player['s020'][0] += 1
            stock.player_1.player['cash'] -= self.stock['price']
            self.msg = 'Stock Buy for ' + str(self.stock['price'])
        else:
            self.msg = 'Not Enough Cash!'
        
# 04
    def sellStock(self):
        if stock.player_1.player['s020'][0] >= 1:
            stock.player_1.player['s020'][1] -= stock.player_1.player['s020'][1]/stock.player_1.player['s020'][0]
            stock.player_1.player['s020'][0] -= 1
            stock.player_1.player['cash'] += self.stock['price']
            self.msg = 'Stock Sell for ' + str(self.stock['price'])
        else:
            self.msg = 'Not Enough Stock!'

# 05
    def infoMessage(self):
        return self.msg
    
# 06
    def resetMessage(self):
        self.msg = ''
        
















    
    
