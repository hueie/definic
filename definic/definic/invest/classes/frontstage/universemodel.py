class PortfolioItem:
    def __init__(self,index,column,code,company):
        self.index = index
        self.column = column
        self.code = code
        self.company = company
        self.df = None
        self.score = 0

    def setData(self,df):
        self.df = df

class UniverseModel:
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


    def add(self,column,model,code,company):
        portfolio = self.find(model)
        if portfolio is None:
            self.items[model] = []

        a_item = PortfolioItem(self.countItem(model),column,code,company)
        self.items[model].append( a_item )
        pass

    def saveUniverse(self,column,model,stock_dict):
        for key in stock_dict.keys():
            self.add(column,model,key,stock_dict[key])
            
        pass

    def dump(self):
        print(">>> Portfolio.dump <<<")
        for key in self.items.keys():
            print("- model=%s" % (key))
            for a_item in self.items[key]:
                print("... column=%s : index=%s, code=%s" % (a_item.column, a_item.index, a_item.code))

        print("--- Done ---")
        pass
