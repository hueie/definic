
'''
if __name__ == '__main__':
    import sys,os
    sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
    from common.dbhandler import DBHandler
    print((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
elif __name__ == '__django__':
    from ..common.dbhandler import DBHandler
    
'''
