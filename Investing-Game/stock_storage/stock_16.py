import random
import math
import stock_storage.stock as stock

class Invest:

# 01
    def __init__(self):
        self.stock = {'name':stock.player_1.name[15],'code':'s016','price':stock.player_1.start[15],'change':0}
        self.msg = ''
        self.priceHistory = [self.stock['price']]
        self.position = stock.player_1.position[15]
        self.UpDownRange = 2
        self.const = 0
        self.term = 0
        self.termo = 0
        self.limit = 0
        self.parameterRoulette()
    
# 02
    def priceManager(self):
        self.primaryPriceManager(self.termo,self.const,self.limit)
        self.UpDownRange = self.const
        self.Variation = 0
        self.UpDown = random.randrange(0,self.UpDownRange)
        self.Varient = random.randrange(0,math.ceil(self.stock['price']*stock.player_1.vari[15]))

        if self.position == 'long' and self.UpDown >= (self.UpDownRange/2) - self.UpDown*stock.player_1.weight[15] :
            self.Variation += self.Varient
        elif self.position == 'long' and self.UpDown < (self.UpDownRange/2) - self.UpDown*stock.player_1.weight[15] :
            self.Variation -= self.Varient
        if self.position == 'short' and self.UpDown >= (self.UpDownRange/2) + self.UpDown*stock.player_1.weight[15] :
            self.Variation += self.Varient
        elif self.position == 'short' and self.UpDown < (self.UpDownRange/2) + self.UpDown*stock.player_1.weight[15] :
            self.Variation -= self.Varient

        
        self.stock['price'] += self.Variation
        
        self.term += 1

    
    def primaryPriceManager(self,term,const,limit):
        if self.term >= len(self.priceHistory):
            self.term = len(self.priceHistory)-1
        
        elif self.stock['change'] < -self.const/10:
            self.position = 'long'
        elif self.stock['change'] > self.const/10:
            self.position = 'short'

        else:
            if self.position == 'long':
                if abs(self.priceHistory[0] - self.priceHistory[self.term]) > limit:
                    self.position = 'short'
                    self.parameterRoulette()
                    self.UpDownRange = const
                    self.term = 0
                elif self.term > term:
                    self.term = 0
                    self.position = 'short'
                    self.parameterRoulette()
                    self.UpDownRange = const

            elif self.position == 'short':
                if abs(self.priceHistory[0] - self.priceHistory[self.term]) > limit:
                    self.position = 'long'
                    self.parameterRoulette()
                    self.UpDownRange = const
                    self.term = 0
                elif self.term > term:
                    self.term = 0
                    self.position = 'long'
                    self.parameterRoulette()
                    self.UpDownRange = const

    def parameterRoulette(self):
        self.const = random.randrange(10,stock.player_1.const[15]*10)
        self.limit = round(stock.player_1.start[15]/10,0)
        self.termo = random.randrange(2,round(stock.player_1.start[15]/(self.const)))


# 03
    def buyStock(self):
        if stock.player_1.player['cash'] >= self.stock['price']:
            stock.player_1.player['s016'][1] += self.stock['price']
            stock.player_1.player['s016'][0] += 1
            stock.player_1.player['cash'] -= self.stock['price']
            self.msg = 'Stock Buy for ' + str(self.stock['price'])
        else:
            self.msg = 'Not Enough Cash!'
        
# 04
    def sellStock(self):
        if stock.player_1.player['s016'][0] >= 1:
            stock.player_1.player['s016'][1] -= stock.player_1.player['s016'][1]/stock.player_1.player['s016'][0]
            stock.player_1.player['s016'][0] -= 1
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
        
















    
    
