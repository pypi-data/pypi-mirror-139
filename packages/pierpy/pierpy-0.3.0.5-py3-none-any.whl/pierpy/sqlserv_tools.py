import sqlalchemy
import pandas as pd
import os
from tqdm import tqdm
from getpass import getpass

def conn(db_name, user = None, password = None, db_address = 'ier-db-d1', user_profile_path = None):
        '''
        db_name
        user
        password
        db_address
        user_profile_path
        '''
        #assert that user/password of user_profile_path has been provided
        #assert((user == None and password == None and user_profile_path != None) or (user != None and password != None))

        #get user/password from user profile
        if user_profile_path != None:
            f = open(user_profile_path,'r')
            user = f.readline().rstrip()
            password = f.readline().rstrip()
            f.close()
        elif user != None and password != None:
            user = user
            password = password        
        elif password == None:
            if user == None:
                print('User : ?')
                user = input()                
            print('Password : ?')
            password = getpass()
        

        db_address = db_address
        db_name = db_name
        conn_str = 'mssql+pyodbc://{}:{}@{}/{}?driver=SQL+Server'.format(user, password, db_address, db_name)
        conn = sqlalchemy.create_engine(conn_str,echo=False)    
        return conn

