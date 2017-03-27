# -*- coding: utf-8 -*-
import sys,os
'''
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from backstage.datawarehouse import DataWareHouse
'''
from ..backstage.datawarehouse import DataWareHouse

import copy
import numpy as np
     
class Inventory:
    def __init__(self):
        self.model = None
        pass

if __name__ == '__main__':
    datawarehouse = DataWareHouse()
    data = datawarehouse.selectInventoryFromDB("All")
    print(data)
    pass
