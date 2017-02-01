class StockCode:
    def __init__(self):
        self.items = {}

    def count(self):
        return len(self.items)

    def clear(self):
        self.items.clear()

    def add(self,market_type,code,full_code,company):
        a_item = StockCodeItem(market_type,code,full_code,company)
        self.items[code] = a_item

    def remove(self,stock_code):
        del self.items[stock_code]

    def find(self,stock_code):
        return self.items[stock_code]

    def iterItems(self):
        return self.items.iteritems()

    def dump(self):
        index = 0
        for key,value in self.items.iteritems():
            print("%s : %s - Code=%s, Full Code=%s, Company=%s" % (index, value.market_type, key, value.full_code, value.company))
            index += 1



class StockCodeItem:
    def __init__(self,market_type,code,full_code,company):
        self.market_type = market_type
        self.code = code
        self.full_code = full_code
        self.company = company
