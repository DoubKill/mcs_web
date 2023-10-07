
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging
logger = logging.getLogger('sql')
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcs.settings")
django.setup()
from mcs.settings import DATABASES
def tran(src):
    if src == None:
        return None
    dst = None
    codemap= {' ':'%20','"':'%22','#':'%23','%':'%25',
    '&':'%26',
    '(':'%28',
    ')':'%29',
    '+':'%2B',
    ',':'%2C',
    '/':'%2F',
    ':':' %3A',
    ';':'%3B',
    '<':'%3C',
    '=':'%3D',
    '>':'%3E',
    '?':'%3F',
    '@':'%40',
    '\\':'%5C',
    '|':'%7C'}
    for row in range(len(src)):

        if src[row] in codemap.keys():
            #src[row] = codemap[src[row]]
            dst =dst + codemap[src[row]]
        else:
            if dst ==None:
                dst = src[row]
            else:
                dst =dst + src[row]
    return dst    

'''
'ENGINE': os.getenv('MES_ENGINE', 'django.db.backends.postgresql_psycopg2'),  # 数据库引擎
'NAME': os.getenv('MES_DATABASE_NAME', 'mcs_test'),  # 数据库名称
'USER': os.getenv('MES_DATABASE_USERNAME', 'postgres'),  # 用户名
'PASSWORD': os.getenv('MES_DATABASE_PASSWORD', 'gz@admin'),  # 密码
'HOST': os.getenv('MES_DATABASE_HOSTNAME', '10.10.120.40'),  # HOST
'PORT': os.getenv('MES_MONOCLE_API_PORT', '5432'),  # 端口
'''

class dbman:
    def __init__(self):
        self.condict = {}
    
    def create(self,no='pg'):
        USERNAME = DATABASES.get('default').get('USER')
        PASSWORD = DATABASES.get('default').get('PASSWORD')
        HOST = DATABASES.get('default').get('HOST')
        PORT = DATABASES.get('default').get('PORT')
        DATABASE = DATABASES.get('default').get('NAME')
        DB_URI = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}".format(username=tran(USERNAME),password=tran(PASSWORD), host=HOST,port=PORT, db=DATABASE)
        echo_pool = True
        size = 10 
        time_out = 5 
        
        engine = create_engine(DB_URI, echo=False, echo_pool=echo_pool, pool_size=size, pool_timeout=time_out)
        SessionFactory = sessionmaker(bind=engine)

        self.condict[no] = {"s":SessionFactory,"c":engine}
    
    def getcon(self,no='pg'):
        #如果文件被删要创建

        if no in self.condict:
            return self.condict[no]["s"]
        else:
            self.create(no)
            return self.condict[no]["s"]

    def get_session(self, no='pg'):
        if no in self.condict:
            return self.condict[no]["s"]
        else:
            self.create( no)
            return self.condict[no]["s"]

    def get_con(self, no='pg'):
        if no in self.condict:
            return self.condict[no]["c"]
        else:
            self.create(no)
            return self.condict[no]["c"]


dbm = dbman() 