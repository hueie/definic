# -*- coding: utf-8 -*-
import numpy as np
from ..common.const import *

class PortfolioItem:
    def __init__(self,model,code,row_index,position):
        self.model = model
        self.code = code
        self.row_index = row_index
        self.position = position

    def setData(self,df):
        self.df = df


class TradingSystem():
    def __init__(self):
        self.items = {}

    def clear(self):
        self.items.clear()
    
    def count(self):
        return len(self.items.key())

    def countItem(self,column):
        return len(self.items[column])


    def find(self,column):
        if self.items.has_key(column):
            return self.items[column]
        return None

    def iterItems(self):
        return self.items.iterItems()
    
    def setData(self,df):
        self.df = df
    
    def findCode(self,model,code):
        model = self.find(model)
        if model is None:
            return None

        for a_item in self.items[model]:
            if a_item.code == code:
                return a_item

        return None


    def saveUniverse(self,column,model,stock_dict):
        for key in stock_dict.keys():
            self.add(column,model,key,stock_dict[key])
            
        pass

    
    def setPortfolio(self, portfolio):
        self.portfolio = portfolio

    def add(self,model,code,row_index,position):
        if self.find(code) is None:
            self.items[code] = []

        a_item = PortfolioItem(model,code,row_index,position)

        self.items[code].append( a_item )


    def assessSignal(self,column,df,row_index,position):
        #print "row=%s, len=%s" % (row_index,df.shape[0])
        if (row_index)>=(df.shape[0]-1):
            return None

        current_price = df.loc[row_index,column]
        next_price = df.loc[row_index+1,column]
        diff = next_price - current_price

        #print "row_index=%s, position=%s, price=%s, next=%s, diff=%s" % (row_index,position,current_price,next_price,diff)

        if np.sign(diff)>0:
            if position==LONG:
                return True
        elif np.sign(diff)<0:
            if position==SHORT:
                return True
        else:
            return True

        return False


    def simulate(self):
        result = {}

        self.portfolio.dump()

        for model in self.portfolio.items.keys():
            for a_item in self.portfolio.items[model]:
                #for key in self.items.keys():

                count_correct = 0

                for a_trade in self.items[a_item.code]:
                    result = self.assessSignal(a_item.column,a_item.df,a_trade.row_index,a_trade.position)
                    if result is not None:
                        if result:
                            count_correct += 1

                a_item.hit_ratio = count_correct/(a_item.df.shape[0])

                print("model=%s, code=%s , count_correct=%s, hit_ratio=%0.2f" % (model,a_item.code,count_correct,a_item.hit_ratio))


    def dump(self):
        print(">>> Portfolio.dump <<<")
        for key in self.items.keys():
            for a_item in self.items[key]:
                print("... model=%s, code=%s, row_index=%s, position=%s" % (a_item.model,a_item.code,a_item.row_index,a_item.position))

        print("--- Done ---")
