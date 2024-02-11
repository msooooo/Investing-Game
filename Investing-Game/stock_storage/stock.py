import math
import random
class Player:

# 01
    def __init__(self):

# Stock Settings
        self.code = ['s001','s002','s003','s004','s005','s006','s007','s008','s009','s010','s011','s012','s013','s014','s015','s016','s017','s018','s019','s020']
        
        self.name = ['QuantumWorks',
                     'NovaCorp',
                     'ElysianTech',
                     'HorizonX',
                     'StellarEdge',
                     'Ultilife',
                     'Vertex',
                     'UASP',
                     'WaveTech',
                     'Copley',
                     'Aperture',
                     'Arasaka',
                     'CloudMap',
                     'IOP',
                     'AstralTech',
                     '16 Lab',
                     'SoPI',
                     'SDEX Daily Stock Market ETF',
                     'SDEX Daily Stock Market Inverse ETF',
                     'SDEX Daily Basic-Advance Science ETF']
        self.start = [1650,
                      3040,
                      1940,
                      2030,
                      2450,
                      1340,
                      1570,
                      1200,
                      1930,
                      2530,
                      2780,
                      2100,
                      1560,
                      1040,
                      3100,
                      3150,
                      2890,
                      1000,
                      1000,
                      1000
                      ]
        
        self.vari = [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
        self.weight = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
        profits_List = []
        self.position = []
        for code in self.code:
            position = random.randrange(0,2)
            if position == 1:
                self.position.append('long')
            elif position == 0:
                self.position.append('short')
        self.const = [7,3,5,7,3,2,7,9,3,6,7,3,4,5,9,7,8,2,0,0,0]

# Player Settings
        self.player = {}
        self.player['cash'] = 10000
        self.player['sum'] = 0
        self.player['profits'] = profits_List
        self.player['code'] = 'p001'

        for code in self.code:
            self.player[code] = [0,0.0]
            profits_List.append(0.0)
            profits_List.append(0.0)

# Market Settings                       # Start Time
        self.marketStatus = ['23:30',   # Regular
                             '06:00',   # After
                             '08:00',   # Closure   -   Daily Change Rate Calculation Point
                             '08:01',   # Day
                             '17:50',   # Closure
                             '18:00']   # Pre







player_1 = Player()
