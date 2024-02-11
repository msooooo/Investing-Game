import tkinter
import tkinter.ttk
from tkinter import scrolledtext
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import stock_storage.stock as stock
import stock_storage.stock_1 as s001
import stock_storage.stock_2 as s002
import stock_storage.stock_3 as s003
import stock_storage.stock_4 as s004
import stock_storage.stock_5 as s005
import stock_storage.stock_6 as s006
import stock_storage.stock_7 as s007
import stock_storage.stock_8 as s008
import stock_storage.stock_9 as s009
import stock_storage.stock_10 as s010
import stock_storage.stock_11 as s011
import stock_storage.stock_12 as s012
import virtual_time


vt = virtual_time.Time(8,0)
root = tkinter.Tk()

class GameGUI:

# 01
    def __init__(self,master):
        self.master = master
        self.master.title("Investing Game")

        self.code = stock.player_1.code

        for code in self.code:
                setattr(self,code,getattr(globals()[code],'Invest')())
        
        self.timeRate = 5
        self.previousPrice_List=[]
        self.dailyChangeRate()

        self.marketStatus = 'Closure'
        self.selectedBannerCode = 's001'
        self.candleTick = 0
        self.candleTurn = 0
        self.candleDay = 0

        self.graphGenerator()




# ------------------------------------------------------------------------------------------------------------------ #

        self.buy_stock = tkinter.Button(master,text="Buy", command=lambda:self.trading('s001','buy'))
        self.buy_stock.place(relx=0.75,rely=0.9,relheight=0.05,relwidth=0.1)

        self.sell_stock = tkinter.Button(master,text="Sell", command=lambda:self.trading('s001','sell'))
        self.sell_stock.place(relx=0.875,rely=0.9,relheight=0.05,relwidth=0.1)

# ------------------------------------------------------------------------------------------------------------------ #

        self.selectedBanner_name = tkinter.Label(root,text='None',font=("Helvetica",15,'bold'),anchor='w')
        self.selectedBanner_price = tkinter.Label(root,text='None',font=("Helvetica",30,'bold'),anchor='w')
        self.selectedBanner_change = tkinter.Label(root,text='None',font=("Helvetica",20,'bold'),anchor='w')

        self.selectedBanner_name.place(relx=0.175,rely=0.05,relheight=0.03,relwidth=0.20)
        self.selectedBanner_price.place(relx=0.175,rely=0.10,relheight=0.03,relwidth=0.10)
        self.selectedBanner_change.place(relx=0.275,rely=0.105,relheight=0.03,relwidth=0.10)

# ------------------------------------------------------------------------------------------------------------------ #

        self.stockStatTable = []
        for code in self.code:
            name = getattr(getattr(self,code),'stock')['name']
            price = getattr(getattr(self,code),'stock')['price']
            change = getattr(getattr(self,code),'stock')['change']
            if change >= 0:
                self.stockStatTable.append((name,price,f'+{change} %'))
            else:
                self.stockStatTable.append((name,price,f'-{abs(change)} %'))


        self.stockStat = tkinter.ttk.Treeview(master,columns=("Stock","Price","Change"),show="headings")

        self.stockStat.column("Stock",width=60)
        self.stockStat.column("Price",width=40)
        self.stockStat.column("Change",width=50)

        self.stockStat.heading("Stock",text="Name")
        self.stockStat.heading("Price",text="Price")
        self.stockStat.heading("Change",text="Change")

        for row in self.stockStatTable:
            self.stockStat.insert("","end",values=row)

        self.stockStat.bind("<<TreeviewSelect>>", self.tradingStock)

        self.stockStat.place(relx=0.025,rely=0.16,relheight=0.5,relwidth=0.1)

# ------------------------------------------------------------------------------------------------------------------ #

        self.playerStatTable = [('Cash',stock.player_1.player['cash'],''),
                                ('Sum',stock.player_1.player['sum'],'')]

        self.playerStat = tkinter.ttk.Treeview(master,columns=("Status","Number1","Number2"),show="headings")

        self.playerStat.column("Status",width=50)
        self.playerStat.column("Number1",width=50)
        self.playerStat.column("Number2",width=50)

        self.playerStat.heading("Status",text="Clock")
        self.playerStat.heading("Number1",text=vt.getTimeString()[0:5])
        self.playerStat.heading("Number2",text=self.marketStatus)

        for row in self.playerStatTable:
            self.playerStat.insert("","end",values=row)

        self.playerStat.place(relx=0.875,rely=0.04,relheight=0.1,relwidth=0.1)

# ------------------------------------------------------------------------------------------------------------------ #

        self.playerStockTable = []
        c = -2
        for code in self.code:
            c += 2
            name = getattr(getattr(self, code),'stock')['name']
            share = stock.player_1.player[code][0]
            profit = stock.player_1.player['profits'][0+c]
            profit_percentage = stock.player_1.player['profits'][1+c]
            if stock.player_1.player['profits'][0+c] >= 0 and stock.player_1.player[code][0] >= 1:
                self.playerStockTable.append((name,share,f'+{profit}',f'+{float(profit_percentage)} %'))
            elif stock.player_1.player[code][0] >= 1:
                self.playerStockTable.append((name,share,f'-{abs(profit)}',f'-{abs(profit_percentage)} %'))

        self.playerStock = tkinter.ttk.Treeview(master,columns=("Stock","Share","Profit",'Profit_Percentage'),show="headings")

        self.playerStock.column("Stock",width=135)
        self.playerStock.column("Share",width=40)
        self.playerStock.column("Profit",width=50)
        self.playerStock.column("Profit_Percentage",width=50)

        self.playerStock.heading("Stock",text="Name")
        self.playerStock.heading("Share",text="Share")
        self.playerStock.heading("Profit",text="Profit")
        self.playerStock.heading("Profit_Percentage",text="Percentage")

        for row in self.playerStockTable:
            self.playerStock.insert("","end",values=row)

        self.playerStock.place(relx=0.75,rely=0.16,relheight=0.5,relwidth=0.225)

# ------------------------------------------------------------------------------------------------------------------ #
        
        self.chat = scrolledtext.ScrolledText(root, width=40, height=10, state=tkinter.DISABLED)
        self.chat.place(relx=0.025,rely=0.73,relheight=0.2,relwidth=0.5)

        self.entry = tkinter.Entry(root, width=30)
        self.entry.place(relx=0.025,rely=0.93,relheight=0.02,relwidth=0.5)

        self.entry.bind("<Return>", self.send_message)

        self.send_button = tkinter.Button(root, text="Send", command=self.send_message)
        self.send_button.place(relx=0.5,rely=0.93,relheight=0.02,relwidth=0.025)

# ------------------------------------------------------------------------------------------------------------------ #

        self.master.after(self.timeRate,self.main_stat)
        self.master.after(self.timeRate,self.sub_stat)

# ================================================================================================================== #

# 02
    def tradingStock(self,event=None):
        clicked = self.stockStat.selection()
        if clicked:
            selection = self.stockStat.item(clicked,"values")[0]
            for code in self.code:
                if selection == getattr(getattr(self,code),'stock')['name']:
                    self.tradingStock_Button(code)
                    self.selectedBannerCode = code
                    self.graphData = getattr(getattr(self,code),'priceHistory')


# 02-1
    def tradingStock_Button(self,code):
        self.buy_stock.config(text="Buy",command=lambda:self.trading(code,'buy'))
        self.sell_stock.config(text="Sell",command=lambda:self.trading(code,'sell'))


# 02-3
    def sumCalculator(self):
        um = 0

        for code in self.code:
            um += stock.player_1.player[code][0]*getattr(getattr(self,code),'stock')['price']

        stock.player_1.player['sum'] = um + stock.player_1.player['cash']

# 02-4
    def topBanner(self,code):
        selectedBannerComponents = [getattr(getattr(self,code),'stock')['name'],getattr(getattr(self,code),'stock')['price'],getattr(getattr(self,code),'stock')['change']]
        
        self.selectedBanner_name.config(text=selectedBannerComponents[0])
        self.selectedBanner_price.config(text=selectedBannerComponents[1])

        if selectedBannerComponents[2] > 0:
            self.selectedBanner_change.config(text=f'+{selectedBannerComponents[2]} %',foreground='red')
        elif selectedBannerComponents[2] == 0:
            self.selectedBanner_change.config(text=f'{selectedBannerComponents[2]} %',foreground='gray')
        else:
            self.selectedBanner_change.config(text=f'-{abs(selectedBannerComponents[2])} %',foreground='blue')

# ================================================================================================================== #

# 03
    def main_stat(self):
        if self.marketStatus != 'Closure':
            for code in self.code:
                getattr(self,code).priceManager()

        self.playerStat.heading("Number1",text=vt.getTimeString()[0:5])

        if vt.getTimeString() == stock.player_1.marketStatus[0]:
            self.marketStatus = 'Regular'
        elif vt.getTimeString() == stock.player_1.marketStatus[1]:
            self.marketStatus = 'After'
        elif vt.getTimeString() == stock.player_1.marketStatus[2]:
            self.marketStatus = 'Closure'
        elif vt.getTimeString() == stock.player_1.marketStatus[3]:
            self.marketStatus = 'Day'
        elif vt.getTimeString() == stock.player_1.marketStatus[4]:
            self.marketStatus = 'Closure'
        elif vt.getTimeString() == stock.player_1.marketStatus[5]:
            self.marketStatus = 'Pre'

        if vt.getTimeString() == stock.player_1.marketStatus[0] or stock.player_1.marketStatus[1] or stock.player_1.marketStatus[2] or stock.player_1.marketStatus[3] or stock.player_1.marketStatus[4] or stock.player_1.marketStatus[5]:
            self.playerStat.heading("Number2",text=self.marketStatus)

        vt.timeFlow(1)
        if self.marketStatus != 'Closure':
            self.candleTick += 1
        if self.candleTick >= 2:
            self.candleTick = 0
            self.candleTurn += 1
            self.priceRecord()
            print(self.s001.position)
        if vt.getTimeString() == stock.player_1.marketStatus[2]:
            self.candleTurn = 0
            self.candleDay += 1
            self.s011.initialPrice = self.s011.priceHistory[-1]
            self.s012.initialPrice = self.s012.priceHistory[-1]
            self.priceRecord()
            print(self.candleDay)
        
        self.sumCalculator()

        self.profitCalculator()
        self.dailyChangeRate()

        self.graphUpdator()

        for code in self.code:
            if getattr(getattr(self,code),'stock')['price'] <= 0:
                self.stockKiller(code)

        # Semiconductor Index 3x Leverage
        self.s011.ratio = 1 + ((self.s003.stock['change'] + self.s004.stock['change'] + self.s005.stock['change'] + self.s006.stock['change'])*3/400)
        self.s012.ratio = 1 - ((self.s003.stock['change'] + self.s004.stock['change'] + self.s005.stock['change'] + self.s006.stock['change'])*3/400)
        
        
        self.master.after(self.timeRate*5,self.main_stat)

# ------------------------------------------------------------------------------------------------------------------ #

    def sub_stat(self):
        self.update_table()
        self.topBanner(self.selectedBannerCode)


        self.master.after(int(self.timeRate/5),self.sub_stat)

# ================================================================================================================== #

# 04
    def update_table(self):
        self.stockStatTable = []
        for code in self.code:
            name = getattr(getattr(self,code),'stock')['name']
            price = getattr(getattr(self,code),'stock')['price']
            change = getattr(getattr(self,code),'stock')['change']
            if change >= 0:
                self.stockStatTable.append((name,price,f'+{change} %'))
            else:
                self.stockStatTable.append((name,price,f'-{abs(change)} %'))

        for item in self.stockStat.get_children():
            self.stockStat.delete(item)

        for row in self.stockStatTable:
            self.stockStat.insert("","end",values=row)


        self.playerStatTable = [('Cash',stock.player_1.player['cash'],''),
                                ('Sum',stock.player_1.player['sum'],'')]

        for item in self.playerStat.get_children():
            self.playerStat.delete(item)

        for row in self.playerStatTable:
            self.playerStat.insert("","end",values=row)


        self.playerStockTable = []
        c = -2
        for code in self.code:
            c += 2
            name = getattr(getattr(self,code),'stock')['name']
            share = stock.player_1.player[code][0]
            profit = stock.player_1.player['profits'][0+c]
            profit_percentage = stock.player_1.player['profits'][1+c]
            if stock.player_1.player['profits'][0+c] >= 0 and stock.player_1.player[code][0] >= 1:
                self.playerStockTable.append((name,share,f'+{profit}',f'+{float(profit_percentage)} %'))
            elif stock.player_1.player[code][0] >= 1:
                self.playerStockTable.append((name,share,f'-{abs(profit)}',f'-{abs(profit_percentage)} %'))


        for item in self.playerStock.get_children():
            self.playerStock.delete(item)

        for row in self.playerStockTable:
            self.playerStock.insert("","end",values=row)

# ================================================================================================================== #

# 05
    def send_message(self,event=None):
        user_input = self.entry.get()
        if user_input:
            self.chat.config(state=tkinter.NORMAL)
            self.chat.insert(tkinter.END, f"{vt.getTimeString()} - Msoo: {user_input}\n")
            self.chat.config(state=tkinter.DISABLED)
            self.entry.delete(0, tkinter.END)

            self.chat.yview(tkinter.END)

    def console_message(self,msg,event=None):
        self.chat.config(state=tkinter.NORMAL)
        self.chat.insert(tkinter.END, f"{vt.getTimeString()} - Console: {msg}\n")
        self.chat.config(state=tkinter.DISABLED)
        self.entry.delete(0, tkinter.END)

        self.chat.yview(tkinter.END)

# ================================================================================================================== #

# 06
    def trading(self,code,type):
        if type == 'buy':
            getattr(self,code).buyStock()
            self.console_message(getattr(getattr(self,code),'msg'))
        
        elif type == 'sell':
            getattr(self,code).sellStock()
            self.console_message(getattr(getattr(self,code),'msg'))

# ================================================================================================================== #

# 07
    def profitCalculator(self):
        c = -2
        for code in self.code:
            self.profit = round(stock.player_1.player[code][0] * getattr(getattr(self,code),'stock')['price'] - stock.player_1.player[code][1],1)

            if stock.player_1.player[code][1] != 0:
                self.profit_percentage = round((self.profit / stock.player_1.player[code][1])*100,1)
            else:
                self.profit_percentage = 0

            c += 2
            stock.player_1.player['profits'][0+c] = self.profit
            stock.player_1.player['profits'][1+c] = self.profit_percentage

# ================================================================================================================== #

# 08
    def dailyChangeRate(self):
        if vt.getTimeString() == stock.player_1.marketStatus[2]:
            self.previousPrice_List = []
            for code in self.code:
                self.previousPrice_List.append(getattr(getattr(self,code),'stock')['price'])


        if vt.getTimeString():
            c = -1
            dailyChangeRate_List = []
            for code in self.code:
                c += 1
                if self.previousPrice_List[c] != 0:
                    dailyChangeRate_List.append(round(((getattr(getattr(self,code),'stock')['price'] - self.previousPrice_List[c]) / self.previousPrice_List[c]) * 100,1))
                else:
                    dailyChangeRate_List.append(0.0)


            for code in self.code:
                value = getattr(getattr(self,code),'stock')
                value['change'] = dailyChangeRate_List[self.code.index(code)]

# ================================================================================================================== #

# 09
    def priceRecord(self):
        for code in self.code:
            getattr(getattr(self,code),'priceHistory').append(getattr(getattr(self,code),'stock')['price'])
        if self.candleDay >= 1:
            for code in self.code:
                getattr(getattr(self,code),'priceHistory').pop(0)

# ================================================================================================================== #

# 10
    def stockKiller(self,code):
        getattr(getattr(self,code),'stock')['price'] = 0
        stock.player_1.player[code][0] = 0

# ================================================================================================================== #
        
# 11
    def graphUpdate(self):
        data = getattr(getattr(self,self.selectedBannerCode),'priceHistory')
        rate = getattr(getattr(self,self.selectedBannerCode),'stock')['change']
        buffer = max(data) - min(data)
        if buffer == 0:
            buffer = 1

        self.ax.clear()

        if rate > 0:
            self.ax.plot((data),'r-')
            self.ax.fill_between(range(len(data)), data, color='lightcoral', alpha=0.5)
        elif rate == 0:
            self.ax.plot((data),'k-')
            self.ax.fill_between(range(len(data)), data, color='lightgray', alpha=0.5)
        elif rate < 0:
            self.ax.plot((data),'b-')
            self.ax.fill_between(range(len(data)), data, color='skyblue', alpha=0.5)

        self.ax.axis('off')
        self.ax.set_facecolor('none')

        if len(data) == 1:
            self.ax.set_xlim(0,1)
        else:
            self.ax.set_xlim(0,len(data)-1)
        self.ax.set_ylim(min(data)-buffer*0.1,max(data)+buffer*0.1)

        self.ax.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)

        if len(data) == 0:
            current_value = getattr(getattr(self,self.selectedBannerCode),'stock')['price']
            self.ax.plot([0,1],[current_value,current_value], 'k-')
        else:
            current_value = data[-1]
            self.ax.plot([0,len(data)],[current_value,current_value], 'k-')


        self.canvas.draw()

    
    def graphGenerator(self):
        fig = Figure(figsize=(5,4),dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Value')
        self.canvas = FigureCanvasTkAgg(fig, master=root)
        self.canvas.get_tk_widget().place(relx=0.15,rely=0.16,relheight=0.5,relwidth=0.50)
        self.canvasd = tkinter.Canvas(root,width=0,height=0,background='gray',bd=1,highlightthickness=1,highlightbackground="gray")

    def graphUpdator(self):
        update_thread = threading.Thread(target=self.graphUpdate)
        update_thread.daemon = True
        update_thread.start()













app = GameGUI(root)
root.geometry("1800x480")




root.minsize(300,480)
root.maxsize(1920,1080)
root.mainloop()



