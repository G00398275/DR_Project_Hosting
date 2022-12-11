'''Data Representation - Winter 2022
Big Project: nflDAO.py
Author: Ross Downey (G00398275)
Lecturer: Andrew Beatty'''

import mysql.connector

from dbconfig import config as cfg

class NFL_DAO:
    host =""
    user = ""
    password =""
    database =""

    connection = ""
    cursor =""
    
    def __init__(self):
        self.host=       cfg['host']
        self.user=       cfg['user']
        self.password=   cfg['password']
        self.database=   cfg['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()

    def createDatabase(self):
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password   
        )
        self.cursor = self.connection.cursor()
        sql="create database "+ self.database
        self.cursor.execute(sql)

        self.connection.commit()
        self.closeAll()   

    def createtableQBs(self):
        cursor = self.getcursor()
        sql="create table QBTable (id int AUTO_INCREMENT NOT NULL PRIMARY KEY, Name varchar(250), Team varchar(250), Yards int(5), TDs int(3), INTs int(3))"
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll() 

    def createtableRBs(self):
        cursor = self.getcursor()
        sql="create table RBTable (id int AUTO_INCREMENT NOT NULL PRIMARY KEY, Name varchar(250), Team varchar(250), Yards int(5), ATTs int(3), TDs int(3))"
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll() 
         
    def createQBs(self, values):
        
       cursor = self.getcursor()
       sql="insert into QBTable (Name, Team, Yards, TDs, INTs) values (%s,%s,%s,%s,%s)"
       cursor.execute(sql, values)
       self.connection.commit()
       newid = cursor.lastrowid
       self.closeAll()
       return newid

    def createRBs(self, values):
        
       cursor = self.getcursor()
       sql="insert into RBTable (Name, Team, Yards, ATTs, TDs) values (%s,%s,%s,%s,%s)"
       cursor.execute(sql, values)
       self.connection.commit()
       newid = cursor.lastrowid
       self.closeAll()
       return newid
        
    def convertQBToDictionary(self, result):
        colnames=['id','Name','Team','Yards', "TDs", "INTs"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
       
    def getAllQBs(self):
        cursor = self.getcursor()
        sql="select * from QBTable"
        cursor.execute(sql)
        result = cursor.fetchall()
        arr = []
        for x in result:
            arr.append(self.convertQBToDictionary(x)) 
        self.closeAll()
        return arr

    def convertRBToDictionary(self, result):
        colnames=['id','Name','Team','Yards', "ATTs", "TDs"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item

    def getAllRBs(self):
        cursor = self.getcursor()
        sql="select * from RBTable"
        cursor.execute(sql)
        result = cursor.fetchall()
        arr = []
        for x in result:
            arr.append(self.convertRBToDictionary(x)) 
        self.closeAll()
        return arr

    def findQBByID(self, id):
        cursor = self.getcursor()
        sql="select * from QBTable where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        for x in result:
            print(x)
        self.closeAll()
        return self.convertQBToDictionary(result)

    def findRBByID(self, id):
        cursor = self.getcursor()
        sql="select * from RBTable where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        for x in result:
            print(x)
        self.closeAll()
        return self.convertRBToDictionary(result)

    def updateQBs(self, values):
        cursor = self.getcursor()
        sql="update QBTable set Name= %s, Team=%s, Yards=%s, TDs=%s, INTs=%s where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def updateRBs(self, values):
        cursor = self.getcursor()
        sql="update RBTable set Name= %s, Team=%s, Yards=%s, ATTs=%s, TDs=%s where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def deleteQB(self, id):
        cursor = self.getcursor()
        sql="delete from QBTable where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll

    def deleteRB(self, id):
        cursor = self.getcursor()
        sql="delete from RBTable where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll
        
nflDAO = NFL_DAO()

if __name__ == "__main__":
    
    nflDAO.createDatabase()
    print("Database created!")

    nflDAO.createtableQBs()
    print("QB Table created!")

    nflDAO.createtableRBs()
    print("RB Table created!")

# Quarterback data, 10 added
    data = ("Patrick Mahomes", "Kansas City Chiefs", 3585, 29, 8)
    nflDAO.createQBs(data)
    
    data2 = ("Josh Allen", "Buffalo Bills", 3183, 23, 11)
    nflDAO.createQBs(data2)
    
    data3 = ("Joe Burrow", "Cincinnati Bengals", 3160, 23, 8)
    nflDAO.createQBs(data3)
    
    data4 = ("Tom Brady", "Tampa Bay Buccaneers", 3051, 14, 2)
    nflDAO.createQBs(data4)
    
    data5 = ("Justin Herbert", "Los Angeles Chargers", 3004, 19, 7)
    nflDAO.createQBs(data5)
    
    data6 = ("Geno Smith", "Seattle Seahawks", 2802, 19, 5)
    nflDAO.createQBs(data6)
    
    data7 = ("Kirk Cousins", "Minnesota Vikings", 2760, 17, 9)
    nflDAO.createQBs(data7)

    data8 = ("Derek Carr", "Las Vegas Raiders", 2730, 18, 7)
    nflDAO.createQBs(data8)

    data9 = ("Jared Goff", "Detroit Lions", 2682, 17, 7)
    nflDAO.createQBs(data9)

    data10 = ("Aaron Rodgers", "Green Bay Packers", 2682, 21, 9)
    nflDAO.createQBs(data10)
    print ("QBs Added to table!")

    nflDAO.getAllQBs()
    print ("All QBs in table are listed above")

# Running Back Data, 10 added
    data11 = ("Josh Jacobs", "Las Vegas Raiders", 1159, 216, 9)
    nflDAO.createRBs(data11)

    data12 = ("Derrick Henry", "Tennessee Titans", 1048, 247, 10)
    nflDAO.createRBs(data12)

    data13 = ("Nick Chubb", "Cleveland Browns", 1039, 200, 12)
    nflDAO.createRBs(data13)

    data14 = ("Saquon Barkley", "New York Giants", 992, 224, 7)
    nflDAO.createRBs(data14)
    
    data15 = ("Miles Sanders", "Philadelphia Eagles", 900, 177, 8)
    nflDAO.createRBs(data15)

    data16 = ("Dalvin Cook", "Minnesota Vikings", 841, 178, 6)
    nflDAO.createRBs(data16)

    data17 = ("Justin Fields", "Chicago Bears", 834, 122, 7)
    nflDAO.createRBs(data17)

    data18 = ("Aaron Jones", "Green Bay Packers", 821, 155, 2)
    nflDAO.createRBs(data18)

    data19 = ("Dameon Pierce", "Houston Texans", 788, 180, 3)
    nflDAO.createRBs(data19)

    data20 = ("Jonathan Taylor", "Indianapolis Colts", 761, 136, 4)
    nflDAO.createRBs(data20)
    print ("RBs added to table!")

    nflDAO.getAllRBs()
    print ("All RBs in table are listed above")
    
    nflDAO.findQBByID(1)
    print ("The QB with id number given is listed")
    
    '''
    values = ("Josh Allen", "Buffalo Bills", 4000, 30, 20, 2)
    nflDAO.updateQBs(values)
    print ("The QB with id number given has been updated with the values given")
    
    nflDAO.deleteQB(2)
    print ("The QB with the id number given has been deleted")
    '''
    print("(In)sanity!!")