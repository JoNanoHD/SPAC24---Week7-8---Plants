import numpy as np
import string
import copy
import random
from faker import Faker
from datetime import datetime
import sqlalchemy
import sqlalchemy_utils
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from sqlalchemy import inspect
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
#metadata_obj = 
#dialect+driver://username:password@host:port/database
#engine = create_engine("mysql+mysqlconnector://Jonas:j19732381@localhost:3306/Week7+8")
#if not database_exists(engine.url):
#    create_database(engine.url)
#engine.connect()
#sqlalchemy_utils.functions.drop_database("mysql+mysqlconnector://Jonas:j19732381@localhost:3306/Week7+8")


class Base(DeclarativeBase):
    pass


class MySQLSetup:
   def __init__(self, user, password):
        #setup server (if doesn't exist) and connect.
        self.engine = create_engine("mysql+mysqlconnector://"+str(user)+":"+str(password)+"@localhost:3306/Week7+8")
        if not database_exists(self.engine.url):
            self.db = create_database(self.engine.url)
        self.connection = self.engine.connect()
        self.session = Session(self.engine)
        #create sheets w necessary columns
        
            # Ware sheet; ID,name,description,category,price,stock...
            
            # Category sheet; ID,name,description...
            
            # Transaction sheet; trsc_ID,ware_ID,time,quantity,type...

   def ClearSQLData():
       
        # What it says in the name
        
        pass
   pass


_engine = MySQLSetup('root', 'j19732381')
# print(_engine.engine)
# print(type(_engine.connection))
# print(_engine.session)
# #_engine.db.drop()
# #print(dir(sqlalchemy))
# print(_engine.engine.url.database)

#Base.metadata.drop_all(_engine.engine)


def ClearSQLData(engine):
    
     # What it says in the name
     
     
     Base.metadata.drop_all(bind=engine)



class SQLUserLogin:
    #in
    pass


class ware(Base):
    
    __tablename__ = "Wares"
    #__table_args__ = {'extend_existing': True}
    _id: Mapped[int]  = mapped_column(primary_key=True,)
    
    
    name:     Mapped[str]            = mapped_column(String(30))
    descr:    Mapped[Optional[str]]  = mapped_column(String(60))
    category: Mapped[str]            = mapped_column(String(30))
    price:    Mapped[float]
    stock:    Mapped[int]
    def __init__(self, name,descr,category,price,stock, session):
        _id = random.randint(0, 9999)
        while session.execute(select(ware).where(ware._id==self._id)).scalar() != None:
            _id = random.randint(0, 9999)
        self._id      = _id
        self.name     = name
        self.descr    = descr
        self.category = category
        self.price    = price
        self.stock    = stock
        if session.execute(select(ware).where(ware.name==self.name)).scalar() == None:
            session.add(self)
            session.commit()
        

Base.metadata.create_all(_engine.engine)
orchid = ware('Orchid','A lovely flower','Plants',20,10,_engine.session)
monstera = ware('Monstera','Green houseplant','Plants','40','5',_engine.session)
monstera = ware('Ficus','Green houseplant','Plants','60','5',_engine.session)
monstera = ware('Birds of Paradise','Green houseplant','Plants','60','5',_engine.session)

_engine.session.commit()
#print(_engine.session.execute(select(ware).where(ware.name=='Orchid')).scalar().__dict__)#.scalar().__dict__)


class transaction(Base):
    __tablename__ = "Transaction"
    __table_args__ = {'extend_existing': True}

    transaction_id: Mapped[int]  = mapped_column(primary_key=True)
    ware_id: Mapped[int]
    time: Mapped[datetime]
    quantity: Mapped[int]
    value: Mapped[float]
    item: Mapped[str] = mapped_column(String(30))
    _type: Mapped[str] = mapped_column(String(30))
    def __init__(self, ware_id,time,quantity,_type, session):
        transaction_id  = random.randint(0, 9999)
        while session.execute(select(transaction).where(transaction.transaction_id==self.transaction_id)).scalar() != None:
            transaction_id = random.randint(0, 9999)
        self.transaction_id = transaction_id
        self.ware_id  =  ware_id
        self.time  =  time
        self.quantity  =  quantity
        self._type  =  _type
        self.item = session.execute(select(ware).where(ware._id==self.ware_id)).scalar().__dict__['name']
        self.value = session.execute(select(ware).where(ware._id==self.ware_id)).scalar().__dict__['price'] * self.quantity
        if session.execute(select(transaction).where(transaction.transaction_id==self.transaction_id)).scalar() == None:
            session.add(self)
            session.commit()

def printColumn(session, table):
    for item in session.execute(select(table)).scalars().all():
        print('- - - - - - - -')
        for key in sorted(item.__dict__.keys()):
            if key != '_sa_instance_state':
                print(str(key)+':  '+ str(item.__dict__[key])) 


Base.metadata.create_all(_engine.engine)


class depotManager:
    # access and manipulate SQL data, should call other classes, particularly transaction
    # to do this.
    def __init__(self, engine):
        self.engine = engine
    # should have attributes keeping track of stock value, total sales etc
 
    def selectCell(self, table, column, selection):
        stmt = select(table).where(column==selection)
        return self.engine.session.execute(stmt)
    
    def editCell(self, table, columnSearch, columnTarget, selection, newInput):
        if columnTarget == 'name':
            stmt = (
                update(table).
                where(columnSearch == selection).
                values(name=newInput)
                )
            self.engine.session.execute(stmt)
            
        elif columnTarget == 'descr':
            stmt = (
                update(table).
                where(columnSearch == selection).
                values(descr=newInput)
                )
            self.engine.session.execute(stmt)
            
        elif columnTarget == 'price':
            stmt = (
                update(table).
                where(columnSearch == selection).
                values(price=newInput)
                )
            self.engine.session.execute(stmt)
            
        elif columnTarget == 'category':
            stmt = (
                update(table).
                where(columnSearch == selection).
                values(category=newInput)
                )
            self.engine.session.execute(stmt)
        
        elif columnTarget == 'stock':
            stmt = (
                update(table).
                where(columnSearch == selection).
                values(stock=newInput)
                )
            self.engine.session.execute(stmt)
        else:
            print('Invalid target column selected in editCell')
        
        # row = self.selectCell(table, columnSearch, selection)
        # print(newInput)
        # row.price = newInput
        # print(row.scalar().__dict__)
        # self.selectCell(table, columnSearch, selection)
        self.engine.session.commit()
        pass
    
    def addToValue(self, table, columnSearch, columnTarget, selection, delta):
        # print(table)
        # print(columnSearch)
        # print(columnTarget)
        print(self.engine.session.execute(select(table).where(columnSearch==selection)).scalar().__dict__['stock'])#.__dict__[columnTarget] )
        newVal = delta + self.engine.session.execute(select(table).where(columnSearch==selection)).scalar().__dict__[columnTarget] 
        #print(newVal)
        self.editCell(table, columnSearch, columnTarget, selection, newVal)
        self.engine.session.commit()
        pass
        
    
    #### ADD ITEM: call ware class to add row to Wares SQL datasheet
    
    
    def addItem(self, name, descr, category, price, stock):
        item = ware(name, descr, category, price, stock, self.engine.session)
        # self.engine.session.add(item)
        # self.engine.session.commit()
        pass
 
    #### EDIT ITEM: use session.execute to edit info in SQL sheet, ie change price, stock, name
    ####### - CHANGE PRICE
    ####### - ADD/REMOVE STOCK
    ####### - CHANGE NAME/CATEGORY/DESCRIPTION    

    def changePrice(self, itemName, newPrice):
        self.editCell(ware, ware.name, 'price', itemName, newPrice)
        pass
    
    def changeStock(self, itemName, stockDelta):
        self.addToValue(ware, ware.name, 'stock', itemName, stockDelta)
        pass
    def changeStockID(self, _id, stockDelta):
        self.addToValue(ware, ware._id, 'stock', _id, stockDelta)
        pass
    
    def editItemString(self, itemName, columnTarget, newInput):
        self.editCell(ware, ware.name, columnTarget, itemName, newInput)
        pass

    
    #### TRANSACTION: call transaction class to add new transation to SQL DATA sheet.
    ####### - SALE: remove stock from aproppriate item in Wares SQL sheet.
    ####### - RETURN: basically opposite of above.
    ####### - RESTOCK: Add stock to appropriate Ware (basically same code as RETURN?)
    
    
    def addTransaction(self, ware_id, time, quantity, _type):
        transac = transaction(ware_id, time, quantity, _type, self.engine.session)
        # self.engine.session.add(transac)
        # self.engine.session.commit()
        pass
    
    
    def newSale(self,  ware_id, time, quantity):
        self.addTransaction(ware_id, time, quantity, 'Sale')
        self.changeStockID(ware_id, -quantity)
        #self.addToValue(ware,  ware.stock, ware_id, -quantity)
        pass
    
    def newReturn(self, ware_id, time, quantity):
        self.addTransaction(ware_id, time, quantity, 'Return')
        self.changeStockID(ware_id, quantity)
        #self.addToValue(ware, ware._id, ware.stock, ware_id, quantity)
        pass
    
    def restockItem(self, ware_id, time, quantity):
        self.addTransaction(ware_id, time, quantity, 'Restock')
        self.changeStockID(ware_id, quantity)
        #self.addToValue(ware, ware._id, ware.stock, ware_id, quantity)
        pass
    
    #### REPORTS: print a statement with some stats for the depot
    ####### SALES: total value of sales, breakdown by category, best selling item.
    ####### LOWSTOCK: print all Wares with stock below a certain threshold (eg 5) as well as current stock
    ####### OVERVIEW: print overview of all wares in depot
    ########## - BY_CATEGORY: same as above but only for given category.
    ###### TRANSACTION LOG
    
    #### SEARCH: search one of the SQL data-sheets with different criteria (use STRATEGY pattern here)
    ####### - SEARCH_WARES
    ####### - SEARCH_TRANSACTIONS
    
    def search(self, table, columnSearch, query):
        return self.selectCell(table, columnSearch, query)

    def wSearchbyID(self,query):
        return self.selectCell(ware, ware._id, query)
    
    def wSearchbyName(self,query):
        return self.selectCell(ware, ware.name, query)

    def wSearchbyCat(self,query):
        return self.selectCell(ware, ware.category, query)

    def wSearchbyDescr(self,query):
        return self.selectCell(ware, ware.descr, query)

    def tSearchbyTID(self,query):
        return self.selectCell(transaction, transaction.transaction_id, query)

    def tSearchbyWID(self,query):
        return self.selectCell(transaction, transaction.ware_id, query)

    def tSearchbyType(self,query):
        return self.selectCell(transaction, transaction._type, query)

    def tSearchbyTime(self,query):
        return self.selectCell(transaction, transaction.time, query)
    
    def printColumn(self, table):
        for item in self.engine.session.execute(select(table)).scalars().all():
            print('- - - - - - - -')
            for key in item.__dict__.keys():
                if key != '_sa_instance_state':
                    print(str(key)+': '+ str(item.__dict__[key])) 
    
    
    pass

#print(_engine.session.execute(select(ware)).scalar().__dict__.keys())
mngr = depotManager(_engine)

# mngr.addItem('Croton', 'Multicolored house plant', 'Plants', 70, 8)
# mngr.editCell(ware, ware.name, 'stock', 'Orchid', 500)
# mngr.newSale(8399, datetime.now(), 2)
# mngr.restockItem(8399, datetime.now(), 10)
# mngr.newReturn(8399, datetime.now(), 2)

print()

printColumn(_engine.session, ware)
print('# # # # # ')
printColumn(_engine.session, transaction)

depotsum = 0
for item in _engine.session.execute(select(ware)).scalars().all(): 
    # print( item.__dict__['price'] , item.__dict__['stock'])
    # print( item.__dict__['price'] * item.__dict__['stock'])
    depotsum += item.__dict__['price'] * item.__dict__['stock']
print(depotsum)

def depotSetup():
     # create a bunch of wares and transactions to fill out the database
    
    pass

def ManagementUI():
    
    # Run everything in the terminal
    ### LOGIN with mySQL credentials  --> MySQLSetup class
    
    ### depotSetup to create data
    
    ## Start screen
    # - search
    # - overview
    # - add/edit
    
    #
    #
    #
    #  Access functions from depotManager class
    #
    #
    #
    #
    
    
    ### LOGOUT/QUIT
    
    pass



#ClearSQLData(_engine.engine)


