class Time:

# 1
    def __init__(self,h,m):
        if h >= 0 and m >= 0 and h < 24 and m < 60:
            self.h = h
            self.m = m
        else:
            self.h = 0
            self.m = 0

# 2
    def getTimeTuple(self):
        return (self.h,self.m)

# 3
    def getTimeString(self):
        if self.h < 10:
            h = '0' + str(self.h)
        else:
            h = str(self.h)
        if self.m < 10:
            m = '0' + str(self.m)
        else:
            m = str(self.m)

        return h + ':' + m

# 03-2
    def timeFlow(self,flowRate):
        self.m += flowRate
        if self.h != 23 and self.m == 60:
            self.m = 0
            self.h += 1
        elif self.h == 23 and self.m == 60:
            self.h = 0
            self.m = 0

# 4
class Time_24_View(Time):
    def getViewString(self):
        if self.h < 10:
            h = '0' + str(self.h)
        else:
            h = str(self.h)
        if self.m < 10:
            m = '0' + str(self.m)
        else:
            m = str(self.m)

        return h + ':' + m
    
# 5
    def __str__(self):
        return self.getTimeString()
    
# 6
class Time_12_View(Time):
    def getViewString(self):
        if self.h < 10:
            h = '0' + str(self.h)
        else:
            h = str(self.h)
        if self.m < 10:
            m = '0' + str(self.m)
        else:
            m = str(self.m)
        if self.h < 12:
            return h + ':' + m + ' AM'
        else:
            return h + ':' + m + ' PM'
        
# 7
    def __str__(self):
        return self.getViewString()

# 8
class Clock:

    def __init__(self,givenObject):
        if isinstance(givenObject,Time_12_View) or isinstance(givenObject,Time_24_View):
            self.time = givenObject
        else:
            self.time = Time_24_View(0,0)
        self.alarmList = []

# 9
    def getClockTime(self):
        if isinstance(self.time,Time_12_View):
            return Time_12_View.getViewString(self.time)
        else:
            return Time_24_View.getViewString(self.time)

# 10
    def changeClockTimeMode(self):
        if isinstance(self.time,Time_12_View):
            h,m = self.time.getTimeTuple()
            self.time = Time_24_View(h,m)
        else:
            h,m = self.time.getTimeTuple()
            self.time = Time_12_View(h,m)         
        return self.getClockTime()
    
# 11
    def setClockTime(self,givenString):
        h,m = int(givenString[0:2]),int(givenString[3:5])
        if len(givenString) == 11:
            setTime = Time_12_View(h,m)
        else:
            setTime = Time_24_View(h,m)
        self.time = setTime
        return self.getClockTime()

# 12
    def addAlarm(self,givenObject):
        if isinstance(givenObject,Time_12_View) or isinstance(givenObject,Time_24_View):
            self.alarmList.append(str(givenObject))
        return len(self.alarmList)

# 13
    def getAlarmRemainsInSecondList(self):
        subList = []

        h,m = self.time.getTimeTuple()
        timeInSecond = int(h) * 3600 + int(m)

        for alarm in self.alarmList:
            h,m = int(alarm[0:2]),int(alarm[3:5])
            alarmInSecond = h * 3600 + m * 60
            alarmInSecond -= timeInSecond
            if alarmInSecond < 0:
                alarmInSecond += 86400
                subList.append(alarmInSecond)
            else:
                subList.append(alarmInSecond)
        return subList