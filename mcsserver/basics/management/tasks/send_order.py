import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand
import json
import traceback

from sqlalchemy import text

import logging

from mcs import settings

logger = logging.getLogger('send_log')

from basics.management.utils import defines
from basics.management.utils.dbmanage import dbm
#from mcs.settings import RCS_URL




import functools

def ttimer(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        end_time = time.time()
        wralog = logging.getLogger('send_log')
        wralog.info('{}:{}'.format(func.__name__,end_time-start_time))
        return result
    return wrapper

def default_dead_line():
    s = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    return s


class send_order():
    def __init__(self):
        self.__name = send_order.get_name()
        self.cfg = send_order.get_cfg()

    @staticmethod
    def get_name():
        return __class__.__name__

    @staticmethod
    def get_cfg():
        return {'interval': '0m 5s 0ms', 'PROJECT_NO': 'mcs', 'desc': "给rcs发送订单",'task_lock_time':1000,'ts_name':'loadact'}

    
    def get_mcs_con(self):
        con = dbm.get_con()
        return con
    
    def get_mcs_session(self):
        con = dbm.get_session()
        return con

    def get_dll_cfg(self,key,default =None):
        value = send_order.get_cfg()
        if value is None and default is not None:
            return default
        else:
            return value
    
    def get_db_config(self,key=None):
        config = None
        try:
            if key is None:
                config = self.get_mcs_con().connect().execute(text(defines.GET_ALL_CONFIGURATION)).fetchall()
                return None
            else:
                config = self.get_mcs_con().connect().execute(text(defines.GET_ONE_CONFIGURATION), {'key_id':key}).fetchall()
                if config is None or len(config) == 0:
                    return None
                else:
                    if config[0].value_type == 'str':
                        return {key:config[0].value}
                    elif config[0].value_type == 'int':
                        return {key:int(config[0].value)}
                    elif config[0].value_type == 'choices':
                        return {key:int(config[0].value)}   
                    elif config[0].value_type == 'bool':
                        return {key:False if int(config[0].value)== 0  else True}
                    else:
                        pass 
                    return {key:config[0].value}

        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None 

    def send_order_nouid(self,data):
        import requests
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset':'utf-8',
        }
        order_json = {
            "order_name": data["task_no"],
            "priority": data["priority"] if "priority" in data  else 0,
            "dead_line": default_dead_line() if 'dead_line' not in data else data["dead_line"],
            "ts_name": data["ts_name"],
            "parameters": data["parameters"]
            }

        try:
            RCS_URL_dict = self.get_db_config('rcs_url')
            RCS_URL = RCS_URL_dict['rcs_url']
            url = RCS_URL + '/api/om/order/'
            response = requests.request("POST",url, json=order_json, headers=headers, timeout=3)
        except (Exception) as e:
            
            return {"error":str(e)}, 400
        return response.text.encode('latin-1').decode('gbk'),response.status_code    
    
    def get_mcs_active_task_info(self):
        try:           
            with self.get_mcs_session()() as session:            
                cursor = session.execute(defines.GET_ALL_CREATED_TASKS)
                orderinfo = cursor.fetchall()
                session.commit()
        except (Exception) as e:
            logger.error("get_mcs_active_task_info数据库操作异常{}".format(str(e)))
            return None
        return orderinfo

    #@ttimer
    def create_order(self,order_name,ts_name,ptr,pr= 0):
        ptrjson = json.dumps(ptr)
        order_json = {
            "task_no": order_name,
            "priority": pr,
            "ts_name": ts_name,
            "parameters": ptrjson
            }
        redata, recode = self.send_order_nouid(order_json)
        if recode == 200:
            return True,redata
        else:
            logger.info("任务[{}]发送om失败，稍后继续重发{}".format(order_name, redata))
            return False,redata
    

    def get_ts_ptr(self,command):              
        stay_time = self.get_dll_cfg('task_lock_time',10000)
        #1空花篮，2满花篮 0空车
        typemao = {3:1,4:2,5:1,6:2,7:0}
        try:
            mtype = typemao[command.basket_type]
        except Exception as e:
            logger.info(f"获取mtype数据错误{str(e)}")
            return None
        slotmap ={
            (None,None,None,None):{'act':[],'slot':[],'goods':[mtype,mtype,mtype,mtype]},#导航
            (2,2,None,None):{'act':['fetch','fetch'],'slot':['G2A','G2B'],'goods':[0,0,0,0]},#上取
            (1,1,None,None):{'act':['put','put'],'slot':['G2A','G2B'],'goods':[0,0,mtype,mtype]},#上卸
            (None,None,2,2):{'act':['fetch','fetch'],'slot':['G1A','G1B'],'goods':[0,0,0,0]},#下取
            (None,None,1,1):{'act':['put','put'],'slot':['G1A','G1B'],'goods':[mtype,mtype,0,0]},#下卸
            (1,1,2,2):{'act':['fetch','fetch','put','put'],'slot':['G1A','G1B','G2A','G2B'],'goods':[0,0,mtype,mtype]},#上卸下取
            (2,2,1,1):{'act':['put','put','fetch','fetch'],'slot':['G1A','G1B','G2A','G2B'],'goods':[mtype,mtype,0,0]},#上取下卸
        }
        try:
            ptr = slotmap[command.axis1_action, command.axis2_action, command.axis3_action, command.axis4_action]
            # 判断是否能取到，异常记录，并把param返回空。
            param = {
                'type': command['task_type'],
                'agv': command['rack_id'],
                'src': command['start_location'],
                'location': command['end_location'],
                'roller_goods_list': ptr['goods'],
                'act_list': ptr['act'],
                'roller_slot_list': ptr['slot'],
                'stay_time': stay_time
            }
        except Exception as e:
            param = None
            logger.info("查找ts_ptr失败")
        return param
    
    def get_db_config(self,key=None):
        config = None
        try:
            if key is None:
                config = self.get_mcs_con().connect().execute(text(defines.GET_ALL_CONFIGURATION)).fetchall()
                return None
            else:
                config = self.get_mcs_con().connect().execute(text(defines.GET_ONE_CONFIGURATION), {'key_id':key}).fetchall()
                if config is None or len(config) == 0:
                    return None
                else:
                    if config[0].value_type == 'str':
                        return {key:config[0].value}
                    elif config[0].value_type == 'int':
                        return {key:int(config[0].value)}
                    elif config[0].value_type == 'choices':
                        return {key:int(config[0].value)}   
                    elif config[0].value_type == 'bool':
                        return {key:False if int(config[0].value)== 0  else True}
                    else:
                        pass 
                    return {key:config[0].value}

        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None
    
    def process_command_create_goto(self, command) -> None:
        
        ts_name_dict = self.get_db_config('ts_name')
        ts_name = 'roller_ts' if ts_name_dict is None else ts_name_dict['ts_name']
        param = command['send_data']

        logger.info("begin send:{}".format(command))
        flag,rst = self.create_order(command['task_no'], ts_name, param, command.priority)

        if flag ==True:
            resp  = json.loads(rst)
            code = resp['code']
            message = resp['msg']
            data = resp['data']
            order_id = resp['data'][0]['in_order_id']
            if 0 == resp['code']:
                logger.info(f'set_command_goto_create_success. command: {command}. order_id: {order_id}.')
                order_id = resp['data'][0]['in_order_id']
                self.set_command_goto_create_success(command,order_id)

            else:
                e = f'MCS create order error. order: {command}. Get error data {resp}.'
                self.set_command_goto_create_failure(command,message)
                logger.error(e)              
        else:
            message = rst['error']
            self.set_command_goto_create_failure(command,message)
            # logger.error(e)
    
    def set_command_goto_create_failure(self,command,msg) -> None:

        '''
        设置command状态
        '''
        try:
            with self.get_mcs_session()()as session:
                session.execute(text(defines.SET_COMMAND_CONSUMED), {'cmd_id':command['cmd_id'], 'error_reason':msg})
                session.commit()
        except (Exception) as e:
            logger.error("数据库操作异常{}".format(str(e)))
            
            return False  
    
    def set_command_goto_create_success(self,command,order_id) -> None:

        '''
        设置location起点解锁
        设置订单状态
        设置command状态
        '''
        try:
            with self.get_mcs_session()()as session:
                session.execute(text(defines.SET_TASK_RUNNING), {'task_id':command['task_id'], 'rcs_order_id':order_id})
                session.commit()
        except (Exception) as e:
            logger.error("数据库操作异常{}".format(str(e)))
            
            return False  
    def m_order(self):

        # 获取活跃MCS任务
        mcs_active_task = self.get_mcs_active_task_info()
        if mcs_active_task is None:
            logger.error("MCS无活跃任务")
            return
    

        for row in mcs_active_task:
            self.process_command_create_goto(row)
            logger.info("任务编号为[{}]已发送".format(row.task_no)) 
             

    # @catch_exception
    def run(self):
        try:
            self.m_order()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            pass


if __name__ == '__main__':
    do = send_order()
    do.run()
