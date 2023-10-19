import time
import datetime
import traceback
import json
import logging
import math
import functools
import requests
import asyncio 
import aiohttp

from sqlalchemy import text

import concurrent.futures
logger = logging.getLogger('dispatch_log')

from basics.management.utils import defines
from basics.management.utils.dbmanage import dbm

load_cnt= 0  
def timer(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        end_time = time.time()
        wralog = logging.getLogger('dispatch_log')
        wralog.info('{}:{}'.format(func.__name__,end_time-start_time))
        return result
    return wrapper

    

class mcs_dispatch():
    def __init__(self):
        self.__name = mcs_dispatch.get_name()
        self.cfg = mcs_dispatch.get_cfg()
        self.executor =  concurrent.futures.ThreadPoolExecutor(max_workers=1)

    @staticmethod
    def get_name():
        return __class__.__name__

    @staticmethod
    def get_cfg():
        return {'interval': '0m 0s 300ms', 'PROJECT_NO': 'mcs', 'desc': 'mcs_dispatch'}


    def get_mcs_con(self):
        con = dbm.get_con()
        return con
    
    def get_mcs_session(self):
        con = dbm.get_session()
        return con
    

    def db_get_agv_status(self):
        try:
            sql = '''SELECT created_time, tag,zz_info FROM public.dma_snap_shot 
	        where id in(SELECT id FROM public.dma_snap_shot order by id desc limit 1)'''
            active_platfrom = self.get_mcs_con().connect().execute(text(sql)).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None,400
        
        if len(active_platfrom) == 0:
            logger.error('db_get_agv_status error')
            return None,400
        
        return {'data':{'data':active_platfrom[0].zz_info}},200

    def http_get_agv_status(self):
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset':'utf-8',
        }
        try:
            RCS_URL_dict = self.get_db_config('rcs_url')
            RCS_URL = RCS_URL_dict['rcs_url']
            #RCS_URL = 'http://10.10.100.86:2000'
            #RCS_URL = 'http://127.0.0.1:8703'
            #RCS_URL='http://10.10.181.158:2000'
            url = RCS_URL + '/api/dispatch/agv-slots/'
            response = requests.request("GET",url, headers=headers, timeout=3)
        except (Exception) as e:
            
            return {"error":str(e)}, 400
        try:
            rdata = json.loads(response.text.encode('latin-1').decode('gbk'))
            #logger.info("restapi response data:（{}）,{}".format(rdata, response.status_code))
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return {"error": str(e)}, 400
        return rdata,response.status_code
    
    def http_apply_stack_ack(self,device_name,type):
        send_data = {
                "Request": {
                "deviceType": "mcs",
                "deviceName": device_name,
                "interfaceName": "LoadTask_MCSRequestStackReset" if type == 'out' else "UnloadTask_MCSRequestStackReset",
                "subInterfaceId": "",
                "control1": ""
                }
            }
        
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset':'utf-8',
        }
        logger.info(f"send ack:{send_data}")
        try:
            WCS_URL_dict = self.get_db_config('wcs_url')
            WCS_URL = WCS_URL_dict['wcs_url']
            #WCS_URL = 'http://10.10.100.18:9999'
            #WCS_URL = 'http://127.0.0.1:8702'
            #WCS_URL='http://10.10.181.158:2000'
            url = WCS_URL + f'/api/wcs/call_interface/?deviceName={device_name}'
            response = requests.request("POST",url,json= send_data,headers=headers, timeout=3)
        except (Exception) as e:    
            logger.error(traceback.format_exc())
            return False,{'error':'发送给WCS的请求失败'}
        
        rdata = json.loads(response.text.encode('latin-1').decode('gbk'))
        logger.info(f"recv ack:{rdata}")
        if 'Response' not in rdata or not rdata['Response']:
            return False,{'error':'WCS返回的复位数据解析失败,Response 不存在'}
        if 'Result' not in rdata['Response'] or not rdata['Response']['Result']:
            return False,{'error':'WCS返回的复位数据解析失败,Result 不存在'}
        
        if rdata['Response']['Result'] == 'False':
            return False,{'error':'WCS返回复位通讯失败Result 为 fasle'}

        return True,{}

    def http_apply_stack(self,device_name,device_id,group_no,order_no,layer,type):
        send_data = {
                "Request": {
                "deviceType": "mcs",
                "deviceName": device_name,
                "interfaceName": "LoadTask_MCSRequestStack" if type == 'out' else "UnloadTask_MCSRequestStack",
                "subInterfaceId": "",
                "control1": {
                    "machine_group": group_no,
                    "order_id": order_no[:9],
                    "layer": layer,
                    "request_stack": "2" if type == 'out' else "1"
                    }
                }
            }
        
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset':'utf-8',
        }
        logger.info(f"send request:{send_data}")
        try:
            WCS_URL_dict = self.get_db_config('wcs_url')
            WCS_URL = WCS_URL_dict['wcs_url']
            #WCS_URL = 'http://10.10.100.18:9999'
            #WCS_URL = 'http://127.0.0.1:8702'
            #WCS_URL='http://10.10.181.158:2000'
            url = WCS_URL + f'/api/wcs/call_interface/?deviceName={device_name}'
            response = requests.request("POST",url,json= send_data,headers=headers, timeout=3)
        except (Exception) as e:    
            logger.error(traceback.format_exc())
            return False,{'error':'发送给WCS的请求失败'}

        try:
            rdata = json.loads(response.text.encode('latin-1').decode('gbk'))
            logger.info(f"recv request:{rdata}")
            if 'Response' not in rdata or not rdata['Response']:
                return False,{'error':'WCS返回的数据解析失败,Response 不存在'}
            if 'Result' not in rdata['Response'] or not rdata['Response']['Result']:
                return False,{'error':'WCS返回的数据解析失败,Result 不存在'}
            
            if rdata['Response']['Result'] == 'False':
                return False,{'error':'WCS返回通讯失败Result 为 fasle'}
            
            if 'RecvData' not in rdata['Response'] or not rdata['Response']['RecvData']:
                return False,{'error':'WCS返回的数据解析失败,RecvData 不存在'}
            
            rst = rdata['Response']['RecvData'][-1]
            ''''
            	"content": {
					"stack_id": "1001",
					"machine_no": "2101",
					"cost_time": "240",
					"QTime": "3600",
					"stack_status": "1"
				},
            '''
            if 'content' not in rst or not rst['content']:
                return False,{'error':'WCS返回的数据解析失败,content 不存在'}     

            if 'stack_status' not in rst['content'] or not rst['content']['stack_status']:
                return False,{'error':'WCS返回的数据解析失败,stack_status 不存在'}
                '''
                0.等待堆栈处理
                1.允许
                2.不允许
                '''
            
            if rst['content']['stack_status'] != '1':
                if rst['content']['stack_status'] == '0':          
                    return False,{'error':'WCS返回等待堆栈处理','status':'pending'}
                else:
                    return False,{'error':'WCS返回不允许生成堆栈任务','status':'reack'}

            if type == 'out':
                if 'machine_no' not in rst['content'] or not rst['content']['machine_no'] or rst['content']['machine_no'] =='':
                    return False,{'error':'WCS返回的数据异常,machine_no字段为空','status':'reack'}
                if 'QTime' not in rst['content'] or not rst['content']['QTime'] or rst['content']['QTime'] =='':
                    return False,{'error':'WCS返回的数据异常,QTime字段为空','status':'reack'}
                return True,{'stack_id':rst['content']['stack_id'],'machine_no':rst['content']['machine_no'],'qtime':rst['content']['QTime']}
            else:
                return True,{'stack_id':rst['content']['stack_id']}
            
        except (Exception) as e:
            logger.error(traceback.format_exc())
            logger.info(f"recv data:{rdata}")
            return False,{'error':'WCS返回的数据解析失败，具体原因请查看日志'}


    async def async_get_stack(self,WCS_URL,data):
    # 协程任务逻辑
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset':'utf-8'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(WCS_URL,data=json.dumps(data),headers=headers) as response:
                result = await response.text()
                return result
            
    def http_get_mulit_stack(self,stack):
        requests_list = []
        redict = {}
        WCS_URL_dict = self.get_db_config('wcs_url')
        WCS_URL = WCS_URL_dict['wcs_url']
        #WCS_URL = 'http://10.10.100.18:9999'
        #WCS_URL = 'http://127.0.0.1:8702'
        #WCS_URL='http://10.10.181.158:2000'
        re_map = {}
        cnt  = 0
        for one_stack in stack:
            in_device_name = one_stack.in_location_name
            out_device_name = one_stack.out_location_name
            if in_device_name not in redict:
                redict[in_device_name] = 1
                url = WCS_URL + f'/api/wcs/call_interface/?deviceName={in_device_name}' 
                send_data = {
                    "Request": {
                    "deviceType": "mcs",
                    "deviceName": in_device_name,
                    "interfaceName": "GZ_StackRequestTask",
                    "subInterfaceId": "",
                    "control1": {
                        }
                    }
                }
                
                requests_list.append(self.async_get_stack(url,send_data))
                re_map[cnt] = in_device_name
                cnt = cnt+1

            if out_device_name not in redict:
                redict[out_device_name] = 1
                url = WCS_URL + f'/api/wcs/call_interface/?deviceName={out_device_name}' 
                send_data = {
                    "Request": {
                    "deviceType": "mcs",
                    "deviceName": out_device_name,
                    "interfaceName": "GZ_StackRequestTask",
                    "subInterfaceId": "",
                    "control1": {
                        }
                    }
                }
                requests_list.append(self.async_get_stack(url,send_data))
                re_map[cnt] = out_device_name
                cnt = cnt+1


        logger.info(f"send request:{requests_list}")
        if not requests_list:
            return False,{'error':'MCS堆栈配置数据异常'} 
        try:
            reslut = self.async_function(requests_list)
        except (Exception) as e:    
            logger.error(traceback.format_exc())
            return False,{'error':'发送给WCS的请求失败'}

        stack_loc_list = []
        for re_index,one_reslut in enumerate(reslut):
            loc_name = 'unknow' if re_index not in re_map else re_map[re_index]
            rdata = json.loads(one_reslut.encode('latin-1').decode('gbk'))
            logger.info(f"recv request:{rdata}")
            if 'Response' not in rdata or not rdata['Response']:
                self.set_alarm_log('error',f'{loc_name}: WCS返回的数据解析失败,Response 不存在，忽略恢复')
                logger.error(f'{loc_name}: WCS返回的数据解析失败,Response 不存在，忽略恢复')
                continue

            if 'Result' not in rdata['Response'] or not rdata['Response']['Result']:
                self.set_alarm_log('error',f'{loc_name}: WCS返回的数据解析失败,Result 不存在，忽略恢复')
                logger.error(f'{loc_name}: WCS返回的数据解析失败,Result 不存在，忽略恢复')
                continue

            if 'msg' not in rdata['Response'] or not rdata['Response']['msg']:
                self.set_alarm_log('error',f'{loc_name}: WCS返回的数据解析失败,msg 不存在，忽略恢复')
                logger.error(f'{loc_name}: WCS返回的数据解析失败,msg 不存在，忽略恢复')
                continue
            
            if rdata['Response']['Result'] == 'False':
                msg = rdata['Response']['msg']
                self.set_alarm_log('error',f'{loc_name}:{msg} 忽略恢复')
                logger.error(f'{loc_name}: {msg} 忽略恢复')
                continue

            if 'RecvData' not in rdata['Response'] or not rdata['Response']['RecvData']:
                self.set_alarm_log('error',f'{loc_name}:WCS返回的数据解析失败,RecvData 不存在 忽略恢复')
                logger.error(f'{loc_name}: WCS返回的数据解析失败,RecvData 不存在 忽略恢复')
                continue
            
            rst = rdata['Response']['RecvData'][-1]

            if 'content' not in rst or not rst['content']:
                self.set_alarm_log('error',f'{loc_name}:WCS返回的数据解析失败,content 不存在 忽略恢复')
                logger.error(f'{loc_name}: WCS返回的数据解析失败,content 不存在 忽略恢复')   
                continue 
            
            if rst['content'] == '1':
                stack_loc_list.append(loc_name)
                
        return True,stack_loc_list



    async def async_cancel_stack(self,WCS_URL,data):
    # 协程任务逻辑
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset':'utf-8'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(WCS_URL,data=json.dumps(data),headers=headers) as response:
                result = await response.text()
                return result
            
    def http_cancel_stack_task(self,cancel_task_dict):
        requests_list = []
        WCS_URL_dict = self.get_db_config('wcs_url')
        WCS_URL = WCS_URL_dict['wcs_url']
        #WCS_URL = 'http://10.10.100.18:9999'
        #WCS_URL = 'http://127.0.0.1:8702'
        #WCS_URL='http://10.10.181.158:2000'

        for loc_name,value in cancel_task_dict.items():

            url = WCS_URL + f'/api/wcs/call_interface/?deviceName={loc_name}' 
            type = value['type']
            group_no = value['group_no']
            send_data = {
                "Request": {
                "deviceType": "mcs",
                "deviceName": loc_name,
                "interfaceName": "UnloadTask_MCSRequestStack" if type == 'in' else "LoadTask_MCSRequestStack",
                "subInterfaceId": "",
                "control1": {
                    "machine_group":group_no,
                    "order_id":'0',
                    "layer": '0',
                    "request_stack": "3" if type == 'in' else "4"
                        }
                    }
                }

                
            requests_list.append(self.async_cancel_stack(url,send_data))
            logger.info('cancel_task:{}'.format(send_data))
        try:
            
            reslut = self.async_function(requests_list)
            logger.info('cancel_task:{}'.format(reslut))
        except (Exception) as e:    
            logger.error(traceback.format_exc())
            return False

        return True
       
    def get_active_platform(self):
        try:
            active_platfrom = self.get_mcs_con().connect().execute(text(defines.GET_ACTIVE_PLATFORM)).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None
        
        if len(active_platfrom) == 0:
            logger.error('not found active platfrom')
            return None
        
        return active_platfrom


    def get_roll_basket_ready_time(self,num,one_picth_time,changed_time):
        #num* 节拍
        newdatetime = changed_time + datetime.timedelta(seconds=one_picth_time*num)
        return  '' if one_picth_time == -1 else newdatetime.strftime('%Y-%m-%d %H:%M:%S')

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
        
    
    def get_active_tasks_by_platform_ID(self,platform_ID:tuple):
        try:
            active_tasks = self.get_mcs_con().connect().execute(text(defines.GET_ACTIVE_TASKS_BY_PLATFORM_ID), {'platform_ID':platform_ID}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return []
        return active_tasks
    
    def GET_ALL_ACTIVE_TASKS(self):
        try:
            active_tasks = self.get_mcs_con().connect().execute(text(defines.GET_ALL_ACTIVE_TASKS)).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None
        
        if len(active_tasks) == 0:
            return 0
        
        return active_tasks[0].cnt
    
    def get_last_tasks_by_platform_ID(self,platform_ID:tuple):
        try:
            active_tasks = self.get_mcs_con().connect().execute(text(defines.GET_LAST_TASKS_BY_PLATFORM_ID), {'platform_ID':platform_ID}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None
        
        if len(active_tasks) == 0:
            return None
        return active_tasks[0]
    
    def get_active_tasks_by_loc(self,loc:tuple):
        try:
            active_tasks = self.get_mcs_con().connect().execute(text(defines.GET_ACTIVE_TASKS_BY_LOC), {'loc':loc}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return []
        return active_tasks
    
    def get_platform_action(self,platform):
        try:
            platfrom_part = self.get_mcs_con().connect().execute(text(defines.GET_PLATFORM_PART_BY_PLATFROM_id), {'platform_info_id':platform.id}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return {}
        action = {}
        if len(platfrom_part) == 0:
            return {}
        for row in platfrom_part:
            
            action[row.axis_no] = row
        
        #要判断agv是否可以接其他工序的
        for key,value in {4:'G1A',3:'G1B',2:'G2A',1:'G2B'}.items():
            if key not in action:
                action[key] = {'part_type':0,'axis_no':key,'location_no':'','slot_no':value}

        return action
    
    def get_task_no(self,dst_loc,tag = None):
        if tag is None:
            now = datetime.datetime.now()
            formatted_date = now.strftime("%y%m%d%H%M%S")
            millisecond = now.microsecond /100000
            y = math.floor(millisecond)
            timesn = formatted_date + str(y)
            return  '{}{}'.format(dst_loc,timesn)
        else:
             return  '{}{}'.format(dst_loc,tag)
    
    def get_src_platfrom_by_process_and_route(self,process_id,route_schema_id):
        try:
            src_platfrom = self.get_mcs_con().connect().execute(text(defines.GET_PLATFORM_BY_PROCESS_AND_ROUTE), {'process_id':process_id, 'route_schema_id':route_schema_id}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return []
        return src_platfrom
    
    '''
    def get_active_src_platfrom_by_process_and_route(self,process_id,route_schema_id):
        try:
            src_platfrom = self.get_mcs_con().connect().execute(text(defines.GET_ACTIVE_PLATFORM_BY_PROCESS_AND_ROUTE), {'process_id':process_id, 'route_schema_id':route_schema_id}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return []
        return src_platfrom
    '''

    
    def get_src_platform_machine_list(self,platform):
        platform_list = []
        for row in platform:
            if row.platform_ID in platform_list:
                continue
            platform_list.append(row.platform_ID)
        return platform_list

    def get_stack_group_no_by_id(self,platform_id,route_schema_id,process_id):
        try:
            stack_group = self.get_mcs_con().connect().execute(text(defines.GET_STACK_GROUP_PLATFORM_ID), {'platform_id':platform_id,"route_schema_id":route_schema_id,"process_id":process_id}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return []
        return stack_group 
    

    def get_send_data(self,task_no,platform_ID,location_name,actionlist,task_type,agv_id='',agv_type =0):
        send_data = {
            "task_no": task_no,
            "dest_machine_no": platform_ID,
            "location_name": location_name,
            "agv_id":agv_id,
            "agv_type":agv_type,
            "action_list": json.dumps(actionlist),
            #"action_list": actionlist,
            "order_type": task_type
        }
        return send_data
    #def GET_ACTIVE_PLATFORM_BY_PROCESS_AND_ROUTE

    def create_action(self,opt,agv_slot,location_slot,roll_tasket_cost_time,basket_type=-1,machine_group_source=[],predicted_material=[],roll_basket_ready_time =-1,qtime = -1):
        return {'basket_type':basket_type,"agv_slot": agv_slot,"location_slot":location_slot,"opt": opt,"machine_group_source":machine_group_source,"predicted_material": predicted_material,"roll_basket_ready_time": roll_basket_ready_time,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": qtime}

    
    def create_task(self,platform,basket_num,task_type,changed_time,shunt_flag =False,tag =None,agv_id =''):
        task_no = self.get_task_no(platform.location_name,tag=tag)
        platform_action = self.get_platform_action(platform)
        if len(platform_action) == 0:
            logger.error("站台：{}，查不到站台动作".format(platform.location_name))
            self.set_alarm_log('error',"站台：{}，查不到站台动作".format(platform.location_name))
            return False
        
        if changed_time is None or platform.pitch_time is None:
            logger.error("站台：{}，节拍和plc数据变化时间是空".format(platform.location_name))
            self.set_alarm_log('error',"站台：{}，节拍和plc数据变化时间是空".format(platform.location_name))
            return False

        roll_basket_ready_time = self.get_roll_basket_ready_time(basket_num,platform.pitch_time/platform.slot_num,changed_time) 
        roll_tasket_cost_time_dict =  self.get_db_config('transfer_time')
        if  roll_tasket_cost_time_dict is None:
            roll_tasket_cost_time = 15
            logger.error("站台：{}，传篮时间找不到，使用默认15".format(platform.location_name))

        roll_tasket_cost_time = roll_tasket_cost_time_dict['transfer_time']
        q_time = platform.q_time
        src_platfrom = self.get_src_platfrom_by_process_and_route(platform.source_process_id,platform.route_schema_id)
        if len(src_platfrom) == 0:
            #空车
            pass
        '''
        1,None  上进
        2,None  上出
        1,2     上进下出
        2,1     上出下进
        None,1  下进
        None,2  下出
        
        '''
        #ps.upper_rail_type ,ps.upper_basket_type,ps.lower_rail_type
        tasktype = {(1,None):3,(2,None):2,(1,2):4,(2,1):4,(None,1):3,(None,2):2}
        #要处理取不到的情况
        actionlist = []
        task_ptr = {'task_no':task_no,
                    "platform_ID": platform.platform_ID,                   
                    'platform_name':platform.platform_name, 
                    'process_name':platform.process_name, 
                    'route_name':platform.route_name,
                    'task_location_type':1,
                    'task_type':1 if (platform.upper_rail_type,platform.lower_rail_type) not in tasktype else tasktype[(platform.upper_rail_type,platform.lower_rail_type)],
                    'loc':platform.location_name,
                    'priority':platform.task_priority,
                    'dz_group_no':None,
                    'G2B':None,'G2A':None, 'G1B':None, 'G1A':None, 
                    'G2B1':None, 'G2A2':None, 'G1B3':None, 'G1A4':None
                    }
        
        
        platform_action = {}
        actmap = {'G2B':1,'G2A':2, 'G1B':3, 'G1A':4}
        action_map = {'close':0,'put':2,'fetch':1}
        for row in platform.package:
            task_ptr[row['slot_no']] = action_map[row['opt']]
            if row['opt'] == 'close':
                action = self.create_action(opt = 'close',agv_slot = row['slot_no'],location_slot = row['location_ID'],roll_tasket_cost_time = roll_tasket_cost_time)
                task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = None
                actionlist.append(action)
            elif row['opt'] == 'put':               
                if platform.upper_rail_state == 1:
                    action = {'basket_type':row['basket_type'],"agv_slot": row['slot_no'],"location_slot":row['location_ID'],"opt": 'close',"machine_group_source": [],"predicted_material": [],"roll_basket_ready_time": -1,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": -1}
                    task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = None
                    actionlist.append(action)
                    continue
                
                machine_group_source = []
                if row['basket_type'] == 0:#空花篮上料
                    if shunt_flag == True:
                        machine_group_source = platform.shunt_from_platform
                        task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = platform.shunt_from_platform_name
                    else:
                        emppty_route = self.get_empty_route_by_dst(platform)
                        if len(emppty_route) != 0:
                            machine_group_source = self.get_src_platform_machine_list(emppty_route)  
                            task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = machine_group_source
                            #判断是否有空花篮定线
                            #堆栈定线pi.process_id,pg.route_schema_id,pi.id
                            stack_group = self.get_stack_group_no_by_id(platform.id,platform.route_schema_id,platform.source_process_id)
                            if platform.src_stack_gourp_no is not None and len(stack_group) != 0:
                                machine_group_source = machine_group_source + platform.src_stack_gourp_no 
                                task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = machine_group_source +  platform.src_stack_gourp_name                 
                        else:
                            logger.error("{}:不存在空花篮定线，不生成任务".format(platform.location_name))
                            self.set_alarm_log('error',"站台：{}，不存在空花篮定线，不生成任务".format(platform.location_name))
                            return False
                        
                    
                    action = {'basket_type':row['basket_type'],"agv_slot":row['slot_no'],"location_slot": row['location_ID'],"opt": row['opt'],"machine_group_source":machine_group_source,"predicted_material": [],"roll_basket_ready_time": roll_basket_ready_time,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": -1}
                    actionlist.append(action)
                else:
                    if len(src_platfrom) == 0:
                        #出错pass
                        logger.error('{}:配置错误，上料却没有来源工艺'.format(platform.location_name))
                        self.set_alarm_log('error',"站台：{}，配置错误，上料却没有来源工艺".format(platform.location_name))
                        return False
                    if shunt_flag == True:
                        machine_group_source = platform.shunt_from_platform
                        task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = platform.shunt_from_platform_name
                    else:
                        machine_group_source.append(src_platfrom[0].group_no)
                        if platform.src_stack_gourp_no is not None:
                            machine_group_source = machine_group_source + platform.src_stack_gourp_no 
                            task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = [src_platfrom[0].group_name] + platform.src_stack_gourp_name
                        else:
                            task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = [src_platfrom[0].group_name]
                    action = {'basket_type':row['basket_type'],"agv_slot": row['slot_no'],"location_slot": row['location_ID'],"opt": row['opt'],"machine_group_source": machine_group_source,"predicted_material": [],"roll_basket_ready_time": roll_basket_ready_time,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": -1}
                    actionlist.append(action)
            elif row['opt'] == 'fetch':
                if platform.lower_rail_state == 1:
                    action = {'basket_type':row['basket_type'],"agv_slot": row['slot_no'],"location_slot": row['location_ID'],"opt": 'close',"machine_group_source": [],"predicted_material": [],"roll_basket_ready_time": -1,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": -1}
                    task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = None
                    actionlist.append(action)
                    continue
                
                predicted_material = {
                    "machine_group": platform.group_no,
					"craft_id": platform.process_no,
                    "machine_no": platform.platform_ID,
                    "dest_machine_group_no": platform.group_no
                    }

                action = {'basket_type':row['basket_type'],"agv_slot": row['slot_no'],"location_slot": row['location_ID'],"opt": row['opt'],"machine_group_source": [],"predicted_material": [predicted_material],"roll_basket_ready_time": roll_basket_ready_time,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": q_time}
                actionlist.append(action)
                
            else:
                #要判断auto的情况
                action = {'basket_type':row['basket_type'],"agv_slot": row['slot_no'],"location_slot": row['location_ID'],"opt": row['opt'],"machine_group_source": [],"predicted_material": [],"roll_basket_ready_time": -1,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": -1}
                actionlist.append(action)
                task_ptr[row['slot_no']+str(actmap[row['slot_no']])] = None
        
        send_data = self.get_send_data(task_no,platform.platform_ID,platform.location_name,actionlist,task_type,str(agv_id),int(platform.agv_type_id))
        with self.get_mcs_session()() as session:
            id = session.execute(text(defines.ADD_ONE_TASK), task_ptr).one()
            session.execute(text(defines.ADD_ONE_TASK_COMMAND), {'task_id':id[0],'task_no':task_no,'task_delay_time':platform.task_delay_time,'send_data':json.dumps(send_data)})
            session.commit()          
        return True
    

    def get_platform_by_process_an_route(self,stack,task_type):
        sql = None
        if task_type == 'in':
            sql = defines.GET_IN_PLATFORM_BY_PROCESS_AND_ROUTE 
        else:
            sql = defines.GET_OUT_PLATFORM_BY_PROCESS_AND_ROUTE 
        
        try:
            platform = self.get_mcs_con().connect().execute(text(sql),{'process_id': stack.process_id,'route_schema_id':stack.route_schema_id}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None
        
        if len(platform) == 0:
            return None
        else:       
            return platform[0]

    def get_stack_loc(self,stack_id,task_type):
        sql = None
        if task_type == 'in':
            part_type = 2
        else:
            part_type = 1
        
        try:
            platform = self.get_mcs_con().connect().execute(text(defines.GET_STACK_LOC), {'stack_id': stack_id, 'part_type':part_type}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None
        
        stack_loc = {}
        for row in platform:
            stack_loc[row.slot_no] = row.loc_no

        if len(stack_loc) == 0:
            return None
        else:       
            return stack_loc
        
    def create_stack_task(self,stack,task_type,tag):
        
        if task_type == 'in':
            location_name =  stack.in_location_name
            type  =1
        else:
            location_name = stack.out_location_name
            type  =2
        

        #获取和堆栈动作一致的的机台，出站：当前工序，入栈，下游工序
        platform = self.get_platform_by_process_an_route(stack,task_type)
    
        platform_action = self.get_platform_action(platform)
        stack_location = self.get_stack_loc(stack.stack_id,task_type)

        roll_tasket_cost_time_dict =  self.get_db_config('transfer_time')
        if  roll_tasket_cost_time_dict is None:
            roll_tasket_cost_time = 15
            logger.error("站台：{}，传篮时间找不到，使用默认15".format(platform.location_name))
        else:
            roll_tasket_cost_time = roll_tasket_cost_time_dict['transfer_time']
       
        q_time = 20000

        src_platfrom = self.get_src_platfrom_by_process_and_route(platform.process_id,platform.route_schema_id)
        

        stack_task_eta_dict =  self.get_db_config('stack_task_eta')
        if  stack_task_eta_dict is None:
            stack_task_eta = 300
            logger.error("站台：{} stack_task_eta 找不到，默认300".format(platform.location_name))
        else:
            stack_task_eta = stack_task_eta_dict['stack_task_eta']

        newdatetime = datetime.datetime.now() +datetime.timedelta(seconds=stack_task_eta)
        roll_basket_ready_time = newdatetime.strftime('%Y-%m-%d %H:%M:%S')
        if len(src_platfrom) == 0:
            #空车
            pass
        agvopt = {2:'put',1:'fetch',0:'close'}
        task_no = self.get_task_no(stack.group_no+stack.device_ID+str(type))
        task_ptr = {'task_no':task_no,'task_type':3 if task_type =='in' else 2,
                    'loc':location_name,
                    'agv_id':'',
                    "platform_ID": stack.device_ID,                   
                    'platform_name':stack.device_name,
                    'process_name':stack.device_name, 
                    'task_location_type':2, 
                    'dz_group_no':stack.group_no,
                    'route_name':stack.route_name,'priority':stack.task_priority,
                    'G2B':None,'G2A':None, 'G1B':None, 'G1A':None, 
                    'G2B1':None, 'G2A2':None, 'G1B3':None, 'G1A4':None
                    }
        #要处理取不到的情况
        actionlist = []
        layer = '1'
        for key,value in platform_action.items():
            if task_type == 'in' and platform.upper_rail_type == 1 and value['slot_no'] in ('G2A','G2B'):
                layer = '2'
            elif task_type == 'in'  and platform.lower_rail_type == 1 and value['slot_no'] in ('G1A','G1B'):
                layer = '1'
            elif task_type == 'out'  and platform.lower_rail_type == 2 and value['slot_no'] in ('G1A','G1B'):
                layer = '1'
            elif task_type == 'out'  and platform.lower_rail_type == 2 and value['slot_no'] in ('G2A','G2B'):
                layer = '2'
            else:
                layer = layer
        
        

        
        while True:
            flag,data = self.http_apply_stack(location_name,stack.device_ID,stack.group_no,task_no,layer,task_type)
            machine_no = None
            if flag == False:           
                msg = data['error']
                logger.error(f'堆栈不允许，{msg}')
                self.set_alarm_log('error',f'堆栈不允许，{msg}')
                if 'status' in data:
                    if data['status'] == 'pending':
                        continue
                    elif data['status'] == 'reack':
                        self.loop_apply_stack_ack(location_name,task_type)
                else:
                    return False
            else:
                if 'machine_no' in data:
                    machine_no = data['machine_no']
                if 'qtime' in data:
                    q_time = int(data['qtime'])
                break
        

        

        for key,value in platform_action.items():
            task_ptr[value['slot_no']] = value['part_type']

            if agvopt[value['part_type']] == 'put' and task_type == 'in':#上料
                machine_group_source = []
                #要考虑upper_rail_type 和 轴的动作不一致的情况
                #upper_rail_type,ps.upper_basket_type,ps.lower_rail_type lower_basket_type in 3,5是空花篮

                if platform.upper_rail_type == 1 and value['slot_no'] in ('G2A','G2B') and platform.upper_basket_type in(1,3,5):#空花篮上层上料
                    #machine_group_source = self.get_src_platform_machine_list(src_platfrom)
                    #task_ptr[value['slot_no']+str(key)] = src_platfrom[0].group_name
                    machine_group_source = [stack.group_no]
                    task_ptr[value['slot_no']+str(key)] = stack.group_name
                    action = {'basket_type':0,"agv_slot": value['slot_no'],"location_slot":stack_location[value['slot_no']],"opt": agvopt[value['part_type']],"machine_group_source":machine_group_source,"predicted_material": [],"roll_basket_ready_time": roll_basket_ready_time,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": -1}
                    
                elif platform.lower_rail_type == 1 and value['slot_no'] in ('G1A','G1B') and platform.lower_basket_type in(1,3,5):#空花篮下层上料
                    #put 找源，fetch找目标，空花篮定线按空花篮定线来，没定线按定线处理
                    #machine_group_source = self.get_src_platform_machine_list(src_platfrom
                    machine_group_source = [stack.group_no]
                    task_ptr[value['slot_no']+str(key)] = stack.group_name
                    action = {'basket_type':0,"agv_slot": value['slot_no'],"location_slot": stack_location[value['slot_no']],"opt": agvopt[value['part_type']],"machine_group_source":machine_group_source,"predicted_material": [],"roll_basket_ready_time": roll_basket_ready_time,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": -1}
                    

                else: 
                    if len(src_platfrom) == 0:
                        #出错pass
                        logger.error('数据错误，src_platfrom为空，上料却没有来源工艺')
                        self.set_alarm_log('error','数据错误，src_platfrom为空，上料却没有来源工艺')
                        pass
                    else:
                        machine_group_source.append(src_platfrom[0].group_no)
                        task_ptr[value['slot_no']+str(key)] = src_platfrom[0].group_name
                    action = {'basket_type':1,"agv_slot": value['slot_no'],"location_slot": stack_location[value['slot_no']],"opt": agvopt[value['part_type']],"machine_group_source": machine_group_source,"predicted_material": [],"roll_basket_ready_time": roll_basket_ready_time,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": -1}
                actionlist.append(action)
            elif agvopt[value['part_type']] == 'fetch' and task_type == 'out':#下料:
                predicted_material = {
                    "machine_group": stack.stack_group_no,
					"craft_id": src_platfrom[0].process_no,
                    "machine_no":machine_no,
                    #"machine_no":stack.group_no,#agv交互获得，所以这边随意给个值
                    "dest_machine_group_no": src_platfrom[0].group_no
                    }
                if value['slot_no'] in ('G1A','G1B') and platform.lower_basket_type in(1,3,5) or value['slot_no'] in ('G2A','G2B') and platform.upper_basket_type in(1,3,5):
                    basket_type = 0
                    predicted_material = {
                    "machine_group": stack.stack_group_no,
					"craft_id": src_platfrom[0].process_no,
                    "machine_no":machine_no,
                    #"machine_no":stack.group_no,
                    "dest_machine_group_no": src_platfrom[0].group_no
                    } 
                else:
                    basket_type = 1
                action = {'basket_type':basket_type,"agv_slot": value['slot_no'],"location_slot": stack_location[value['slot_no']],"opt": agvopt[value['part_type']],"machine_group_source": [],"predicted_material": [predicted_material],"roll_basket_ready_time": roll_basket_ready_time,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": q_time}
                actionlist.append(action)
                #task_ptr[value['slot_no']+str(key)] = src_platfrom[0].group_name
            else:
                #要判断auto的情况
                action = {'basket_type':-1,"agv_slot": value['slot_no'],"location_slot": stack_location[value['slot_no']],"opt": 'close',"machine_group_source": [],"predicted_material": [],"roll_basket_ready_time": -1,"roll_tasket_cost_time": roll_tasket_cost_time,"qtime": -1}
                actionlist.append(action)
                task_ptr[value['slot_no']] = 0
                task_ptr[value['slot_no']+str(key)] = None
            

        send_data = self.get_send_data(task_no,stack.device_ID,location_name,actionlist,1,1005)   
        with self.get_mcs_session()() as session:
            id = session.execute(text(defines.ADD_ONE_TASK), task_ptr).one()
            session.execute(text(defines.ADD_ONE_TASK_COMMAND), {'task_id':id[0], 'task_no':task_no, 'task_delay_time':0,'send_data':json.dumps(send_data)})
            #"task_type = :type and traceback_state = 1 and tag =:tag returning id;
            session.execute(text(defines.SET_STACK_TASK_FINISHED), {'type':type,'tag':tag})          
            session.commit()

        self.loop_apply_stack_ack(location_name,task_type) 
        logger.info(f'堆栈({stack.device_ID})：生成{task_type}任务,物料：{stack.group_no}，任务号：{task_no}')
        return True

    def loop_apply_stack_ack(self,location_name,task_type):
        while True:
            flag,data = self.http_apply_stack_ack(location_name,task_type)
            if flag == False:
                msg = data['error']
                logger.error(f'堆栈确认数据异常,尝试重发{msg}')
                self.set_alarm_log('error',f'堆栈确认数据异常,尝试重发，{msg}')
            else:
                break  

    def get_empty_route_by_dst(self,platform):
        try:
            empty_route = self.get_mcs_con().connect().execute(text(defines.GET_EMPTY_ROUTE_BY_DST), {'platform_id':platform.id}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return []
        return empty_route

       
    def agv_count(self,agv_status_dict,slot_data,is_busy):
        if 'machine_group' in slot_data and slot_data["machine_group"] != '' and slot_data["machine_group"] is not None :
                key = slot_data["machine_group"] 
                if key in agv_status_dict:
                    if is_busy:
                        agv_status_dict[key]['busy'] = agv_status_dict[key]['busy'] + 1
                    else:
                        agv_status_dict[key]['free'] = agv_status_dict[key]['free'] + 1
                else:
                    if is_busy:
                        agv_status_dict[key] = {'free':0,'busy':1}
                    else:
                        agv_status_dict[key] = {'free':1,'busy':0}
                return True
        else:
            return False

 
    def get_agv_status(self):
        #要做参数检查

        data,code= self.http_get_agv_status()
        #data,code= self.db_get_agv_status()
        if "data" not in data or "data" not in data["data"] or len(data["data"]["data"]) == 0:
            return None,None,None
        # 要考虑如何处理 一个agv 取多个工艺的料
        agv_status_dict = {}
        process_pack_set = {}
        for row in data["data"]["data"]:
            G1A_data = row["G1A"]
            G1B_data = row["G1B"]
            G2A_data = row["G2A"]
            G2B_data = row["G2B"]
            process_pack = row['process_pack'] if 'process_pack' in row and row['process_pack'] !='' and 'process_pack' and row['process_pack'] is not None else None
            if process_pack is not None:
                process_pack_set[row['process_pack']] =  str(row['agv_id'])

            if self.agv_count(agv_status_dict,G1A_data,row["busy"]):
                continue
            if self.agv_count(agv_status_dict,G1B_data,row["busy"]):
                continue
            if self.agv_count(agv_status_dict,G2A_data,row["busy"]):
                continue
            if self.agv_count(agv_status_dict,G2B_data,row["busy"]):
                continue

        return agv_status_dict,process_pack_set,data["data"]["data"]
    
    #在制统计方式：0关闭，1带料agv，2带料空闲agv，3上游+下游+带料agv     
    def get_goup_map(self):
        try:
            group_list = self.get_mcs_con().connect().execute(text(defines.GET_GOURP_MAP)).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None

        if len(group_list) == 0:
            return None
        else:
            group_map = {}
            for row in group_list:
                group_map[row.b_group_no] = row
            return group_map

    def get_group_agv_cnt(self):
        try:
            group_list = self.get_mcs_con().connect().execute(text(defines.GET_GROUP_AGV_CNT)).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None

        if len(group_list) == 0:
            return None
        else:
            group_map = {}
            for row in group_list:
                group_map[row.group_no] = row.agv_num
            return group_map  

    def get_empty_agv_cnt(self):
        try:
            group_list = self.get_mcs_con().connect().execute(text(defines.GET_EMPTY_AGV_CNT)).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None

        if len(group_list) == 0:
            return None
        else:
            group_map = {}
            for row in group_list:
                group_map[row.group_no] = row.agv_num
            return group_map   
           
    def get_platfrom_group_agv_num(self):
        zz_sum_type_dict = self.get_db_config('zz_sum_type')
        if  zz_sum_type_dict is None:
            zz_sum_type = 0
        else:
            zz_sum_type = zz_sum_type_dict['zz_sum_type']
        
        if zz_sum_type not in [1,2,3]:
            zz_sum_type = 0
            logger.error('zz_sum_type[{}] 与预期的0关闭，1带料agv，2带料空闲agv，3上游+下游+带料agv不符'.format(zz_sum_type))

        if zz_sum_type == 0:
            return None,None,None
        

        agv_status_dict,process_pack_set,srcdata = self.get_agv_status()
        if agv_status_dict is None:
            return None,None,None
        agv_status ={}
        group_map = self.get_goup_map()
        
        if group_map is None:
            return None,None,None
        
        
        if zz_sum_type == 1:
            for key,value in agv_status_dict.items():
                if key in group_map:
                    auto_group = group_map[key].at_group_no
                else:
                    auto_group = key
                if auto_group in agv_status:
                    agv_status[auto_group] = agv_status[auto_group] + value['busy'] + value['free']
                else:
                    agv_status[auto_group] = value['busy'] + value['free']

        elif zz_sum_type == 2:
            for key,value in agv_status_dict.items():
                if key in group_map:
                    auto_group = group_map[key].at_group_no
                else:
                    auto_group = key
                if auto_group in agv_status:
                    agv_status[auto_group] =  agv_status[auto_group] + value['free']
                else:
                    agv_status[auto_group] = value['free']

        elif zz_sum_type == 3:
            empty_agv = self.get_empty_agv_cnt()
            group_agv = self.get_group_agv_cnt()

            for key,value in agv_status_dict.items():
                if key in group_map:
                    auto_group = group_map[key].at_group_no
                else:
                    auto_group = key
                
                if auto_group in empty_agv:
                    empty_agv_cnt = empty_agv[auto_group]
                    group_agv_cnt = 0
                else:
                    empty_agv_cnt = 0               
                    if auto_group in group_agv:
                        group_agv_cnt = empty_agv[auto_group]
                    else:
                        group_agv_cnt = 0
                if key in agv_status:
                    agv_status[key] = agv_status[key]+value['busy'] + value['free'] + empty_agv_cnt+group_agv_cnt 
                else:
                    agv_status[key] = value['busy'] + value['free'] + empty_agv_cnt + group_agv_cnt 
        else:
            return None,None,None
           
        return agv_status,process_pack_set,srcdata
    
    def get_cached_empty_loc(self):
        return 100

    def get_cached_count(self,group_no,stack):      
        try:
            count = self.get_mcs_con().connect().execute(text(defines.GET_STACK_GROUP_COUNT_BY_GROUP_STACK), {'stack_no':stack.device_name, 'group_no':group_no}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return 0
        if len(count) == 0:
            return 0 
        else:
            return count[0].cnt
 

    def get_all_stack(self):
        #对比阈值，是否需要创建任务,要一种料在多个堆栈中。
        try:
            stack_info = self.get_mcs_con().connect().execute(text(defines.GET_CACHE_DEVICE_INFO)).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return []

        return stack_info
    
    def get_cached_time_out_task(self,group_no,stack):
        try:
            stack_info = self.get_mcs_con().connect().execute(text(defines.GET_TIMEOUT_STACK_GROUP_COUNT_BY_GROUP_STACK),{'stack_no':stack.device_name, 'group_no':group_no}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return False
        if len(stack_info) == 0:
            return False
        #select equip_code,in_material_type_name as group_no,basket_num,output_time_consume,q_time
        logger.info('堆栈:[{},{}],[{},{}]生成超时出库任务'.format(stack_info[0].equip_code,stack_info[0].group_no,stack_info[0].output_time_consume,stack_info[0].q_time))
        return True

    
    def check_can_create_task(self,group,process_id,count):
        
        try:
            cached_info = self.get_mcs_con().connect().execute(text(defines.GET_CACHE_DEVICE_INFO_BY_GROUP_NAME), {'group_no':group, 'process_id':process_id}).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None,None
        
        if len(cached_info) ==0:
            return None,None
        for one_cached_info in cached_info:
            if one_cached_info.in_is_used:
                if count >one_cached_info.maximum:
                    active_task = self.get_active_tasks_by_loc(tuple([one_cached_info.in_location_name]))
                    if len(active_task) >= one_cached_info.allow_task_num:
                        pass
                    else:
                        return 'in',one_cached_info
                
            if one_cached_info.out_is_used:  
                active_task = self.get_active_tasks_by_loc(tuple([one_cached_info.out_location_name]))
                if len(active_task) >= one_cached_info.allow_task_num:
                    continue 
                if self.get_cached_time_out_task(group,one_cached_info):
                        logger.info('堆栈:[{},{}]MCS判定可生成超时出库任务'.format(one_cached_info.device_ID,group))
                        return 'out',one_cached_info
                
                if count < one_cached_info.minimum:
                    if self.get_cached_count(group,one_cached_info) <=0:
                        logger.error('堆栈:[{},{}]，没有料'.format(one_cached_info.device_ID,group))
                        self.set_alarm_log('error',"堆栈:{}，{}没有料".format(one_cached_info.device_ID,group))
                        continue
                    else:
                        logger.info('堆栈:[{},{}]MCS判定可生成出库任务'.format(one_cached_info.device_ID,group))
                        return 'out',one_cached_info
                            
        return None,None
    
    def get_wet_group_no_by_platform(self,platform_ID):
        try:
            wet_group = self.get_mcs_con().connect().execute(text(defines.GET_WET_GROUP_NO_BY_PLATFORM,{'platform_ID':platform_ID})).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return []
        if len(wet_group) == 0:
            return []
        return wet_group

    def can_create_task_by_wet_group_no(self,wet_group_threshold,wet_group,agv_count):
        if len(wet_group) ==0:
            return True
        cnt = 0
        for row in wet_group:
            if row in agv_count:
                cnt = cnt + agv_count[row]
                if cnt >= wet_group_threshold:
                    return False
        return True

    def get_tag(self):
        now = datetime.datetime.now()
        formatted_date = now.strftime("%y%m%d%H%M%S")
        millisecond = now.microsecond /100000
        y = math.floor(millisecond)
        timesn = formatted_date + str(y)
        return timesn
    

    #@timer
    def dispatch(self,agv_count,srcdata,tag =None):

        active_platfrom = self.get_active_platform()
        if active_platfrom is None:
            logger.error("所有站台禁用，请在界面上启用")
            self.set_alarm_log('error',"所有站台禁用，请在界面上启用")
            return
        self.set_data_snapshot(active_platfrom,agv_count,srcdata,tag)
        for one_platfrom in active_platfrom:
            #改进
            try:
                #机台是否屏蔽
                #尾料处理
                if one_platfrom.agv_type_id is None:
                    logger.info('{} 机台对应工作区的agv类型为空，请在页面配置'.format(one_platfrom.location_name))
                    self.set_alarm_log('error',"站台：{}，机台对应工作区的agv类型为空，请在页面配置".format(one_platfrom.location_name))
                    continue   

                if one_platfrom.agv_type_id.isdigit() == False:
                    logger.info('{} 机台对应工作区的agv类型只能为数字，请在页面配置'.format(one_platfrom.location_name))
                    self.set_alarm_log('error',"站台：{}，机台对应工作区的agv类型只能为数字，请在页面配置".format(one_platfrom.location_name))
                    continue   
                '''
                
                (1,2)#上进下出
                (2,1)#下进上出
                (1,1,0)#上进
                (1,0,1)#下进
                (1,2,0)#上出
                (1,0,2)#下出
                机台单层进出，如果机台屏蔽状态和界面配置状态不一致，退出
                '''
                can_do = (one_platfrom.upper_rail_state,one_platfrom.lower_rail_state,one_platfrom.upper_rail_type,one_platfrom.lower_rail_type)
                if  can_do ==(1,0,1,None) or can_do == (1,0,None,1):
                    logger.info('{} 实际机台上料屏蔽，和软件机台配置不一致'.format(one_platfrom.location_name))
                    self.set_alarm_log('error',"站台：{}，实际机台上料屏蔽，和软件机台配置不一致".format(one_platfrom.location_name))
                    continue
                if  can_do ==(0,1,2,None) or can_do == (0,1,None,2):
                    logger.info('{} 实际机台下料屏蔽，和软件机台配置不一致'.format(one_platfrom.location_name))
                    self.set_alarm_log('error',"站台：{}，实际机台下料屏蔽，和软件机台配置不一致".format(one_platfrom.location_name))
                    continue
                if one_platfrom.upper_rail_state == 1 and one_platfrom.lower_rail_state ==1:
                    logger.info('{} 实际机台上层和下层都屏蔽，不生成任务'.format(one_platfrom.location_name))
                    self.set_alarm_log('error',"站台：{}，上层和下层都屏蔽，不生成任务".format(one_platfrom.location_name))
                    continue   
                '''
                if one_platfrom.dock_status != 0:
                    #logger.info('{} 不满足下料条件'.format(one_platfrom.dock_status))
                    self.set_alarm_log('error',"站台：{}，dock_status不为空".format(one_platfrom.location_name))
                    continue
                '''
                #if one_platfrom.overed ==True:
                if False:
                    #机台花篮数据超过15s 过期退出
                    self.set_alarm_log('error',"站台：{}，机台花篮数据超过15s 过期退出".format(one_platfrom.location_name))
                    continue
                if one_platfrom.slot_num is None or one_platfrom.slot_num == 0:
                    #一车花篮数未配置或配置错误
                    self.set_alarm_log('error',"站台：{}，一车花篮数未配置或配置错误".format(one_platfrom.location_name))
                    continue

                if (one_platfrom.task_trigger_type == 1 and one_platfrom.upper_basket_num is not None and one_platfrom.up_task_trigger_threshold >= one_platfrom.upper_basket_num):
                    basket_num  = one_platfrom.upper_basket_num
                    changed_time = one_platfrom.upper_basket_changed_time
                elif (one_platfrom.task_trigger_type == 2 and one_platfrom.lower_basket_num is not None and one_platfrom.down_task_trigger_threshold <= one_platfrom.lower_basket_num):
                    #总数要计算，当前写死10个，one_roller_number * 上层或者下层轴数
                    basket_num  = one_platfrom.slot_num - one_platfrom.lower_basket_num
                    changed_time = one_platfrom.lower_basket_changed_time
                elif (one_platfrom.task_trigger_type is None):
                    #机台换液，根据实际轴的动作取阈值
                    continue
                else:
                    continue   

           
                last_task = self.get_last_tasks_by_platform_ID(one_platfrom.platform_ID)
                if last_task is not None and last_task.state in(1,2,3,4,5,6):
                    #已有活跃任务
                    continue
                if last_task is not None and last_task.end_time is not None and last_task.end_time >one_platfrom.last_updated_time and last_task.state in [7,8]:
                    logger.info("站台：{}上个任务完成但花篮数未更新，不生成任务。任务完成时间{}，花篮数更新时间{}".format(one_platfrom.location_name,last_task.end_time,one_platfrom.last_updated_time)) 
                    self.set_alarm_log('error',"站台：{}上个任务完成但花篮数未更新，不生成任务。任务完成时间{}，花篮数更新时间{}".format(one_platfrom.location_name,last_task.end_time,one_platfrom.last_updated_time))
                    continue

                #互斥判断
                if one_platfrom.rejected_to_platform is not None:
                    rejected_tasks = self.get_active_tasks_by_platform_ID(tuple(one_platfrom.rejected_to_platform))
                    if len(rejected_tasks) !=0:
                        #任务已存在互斥任务，退出
                        logger.info("站台：{},等待互斥站台{} 任务结束".format(one_platfrom.location_name,one_platfrom.rejected_to_platform)) 
                        self.set_alarm_log('error',"站台：{},等待互斥站台{} 任务结束".format(one_platfrom.location_name,one_platfrom.rejected_to_platform))    
                        continue
                    
                #要判断在制数量是否超过阈值maximum,minimum
                #platfrom_group_agv_num = self.get_platfrom_group_agv_num(one_platfrom)
                cur_platfrom_group_agv_num = agv_count.get(one_platfrom.group_no,0)
                shunt_cnt = 0
                shunt_flag = False
                if one_platfrom.shunt_from_platform is not None:
                    for row in one_platfrom.shunt_from_platform:
                        shunt_cnt = shunt_cnt + agv_count.get(row,0)

                if one_platfrom.shunt_threshold is not None and shunt_cnt > one_platfrom.shunt_threshold:
                    shunt_flag = True

                #如果只进空花篮，没有设备组
                '''
                1,None  上进
                2,None  上出
                1,2     上进下出
                2,1     上出下进
                None,1  下进
                None,2  下出           
                '''

                #ps.upper_rail_type ,ps.upper_basket_type(3,5),ps.lower_rail_type
                

                if one_platfrom.is_dry_type is False:
                    #湿区设备，获取配置设备组，不满足退出
                    wet_group = self.get_wet_group_no_by_platform(self,one_platfrom.platform_ID)
                    flag = self.can_create_task_by_wet_group_no(one_platfrom.wet_group_threshold,wet_group,agv_count)
                    if flag == False:
                        continue
                
                #只进空花栏没有组
                if one_platfrom.upper_basket_type in (1,3,5) and one_platfrom.upper_rail_type ==1 and one_platfrom.lower_rail_type is None:
                    self.create_task(one_platfrom,basket_num,0,changed_time,shunt_flag,tag=tag)
                    logger.info('(上层进空花篮)站台:{},触发条件：{}，阈值：{}，数量：{},tag:{},分流{}, 时间:{},数据时间{}'.format(one_platfrom.location_name,one_platfrom.task_trigger_type,[one_platfrom.up_task_trigger_threshold,one_platfrom.down_task_trigger_threshold], [one_platfrom.upper_basket_num,one_platfrom.lower_basket_num],tag,shunt_flag,changed_time,one_platfrom.last_updated_time)) 
                elif one_platfrom.lower_basket_type in (1,3,5) and one_platfrom.upper_rail_type is None and one_platfrom.lower_rail_type ==1:
                    self.create_task(one_platfrom,basket_num,0,changed_time,shunt_flag,tag=tag)
                    logger.info('(下层进空花篮)站台:{},触发条件：{}，阈值：{}，数量：{},tag:{},分流{}, 时间:{},数据时间{}'.format(one_platfrom.location_name,one_platfrom.task_trigger_type,[one_platfrom.up_task_trigger_threshold,one_platfrom.down_task_trigger_threshold], [one_platfrom.upper_basket_num,one_platfrom.lower_basket_num],tag,shunt_flag,changed_time,one_platfrom.last_updated_time))
                else:
                    if  cur_platfrom_group_agv_num<=one_platfrom.maximum:                
                        self.create_task(one_platfrom,basket_num,0,changed_time,shunt_flag,tag=tag)
                        logger.info('站台:{},触发条件：{}，阈值：{}，数量：{},tag:{},分流{}, 时间:{},数据时间{}'.format(one_platfrom.location_name,one_platfrom.task_trigger_type,[one_platfrom.up_task_trigger_threshold,one_platfrom.down_task_trigger_threshold], [one_platfrom.upper_basket_num,one_platfrom.lower_basket_num],tag,shunt_flag,changed_time,one_platfrom.last_updated_time)) 
                    else:
                        if one_platfrom.is_dry_type is None:
                            self.create_task(one_platfrom,basket_num,0,changed_time,shunt_flag,tag=tag)
                            logger.info('站台:{},触发条件：{}，阈值：{}，数量：{},tag:{},分流{}, 时间:{},数据时间{}'.format(one_platfrom.location_name,one_platfrom.task_trigger_type,[one_platfrom.up_task_trigger_threshold,one_platfrom.down_task_trigger_threshold], [one_platfrom.upper_basket_num,one_platfrom.lower_basket_num],tag,shunt_flag,changed_time,one_platfrom.last_updated_time))
                        elif one_platfrom.is_dry_type is True:
                            logger.info("站台：{}，干式设备满足阈值限制任务生成".format(one_platfrom.location_name)) 
                            self.set_alarm_log('info',"站台：{}，干氏设备满足阈值限制任务生成".format(one_platfrom.location_name))
                        else:
                            pass

            except (Exception) as e:
                logger.error(traceback.format_exc())
                self.set_alarm_log('error',"站台：{}，程序执行异常退出".format(one_platfrom.location_name))
                continue
            

    def add_stack_task(self,device_ID,group_no,task_no,type):
        try:#:device_ID, :group_no, :tag, :type
            self.get_mcs_con().connect().execute(text(defines.ADD_STACK_TASK,{'device_ID':device_ID,'group_no':group_no,'task_no':task_no,'type':type})).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return False
        return True

    def set_stack_task_state(self,device_ID,group_no,task_no,type):
        try:#:device_ID, :group_no, :tag, :type
            self.get_mcs_con().connect().execute(text(defines.ADD_STACK_TASK,{'device_ID':device_ID,'group_no':group_no,'task_no':task_no,'type':type})).fetchall()
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return False
        return True    

   
    #@timer       
    def stack(self,agv_count,tag='s'):
        #logger.info('agv_count:{}'.format(agv_count))
        tag = self.get_tag()
        stack_info = self.get_all_stack()
        
        group_no =None
        count = 0
        task_map ={}
        for one_stack in stack_info:
            if one_stack.group_no in agv_count:
                group_no = one_stack.group_no
                count = agv_count[one_stack.group_no]

            else:
                group_no = one_stack.group_no
                count = 0

            try:
                type, one_stack = self.check_can_create_task(group_no,one_stack.process_id,count)
                if type is None:
                    continue 
                if group_no in task_map:
                    continue
                task_map[group_no] = 1

                self.create_stack_task(one_stack,type,tag)
                
            except (Exception) as e:
                logger.error(traceback.format_exc())
                self.set_alarm_log('error','堆栈任务执行异常退出')
                continue

    async def run_coroutines(self,task_group):  
        results = await asyncio.gather(*task_group, return_exceptions=True)
        return results
    
    def async_function(self,coroutines):
        async_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(async_loop)
        results = async_loop.run_until_complete(self.run_coroutines(coroutines))
        async_loop.close()
        return results         

    def get_action_by_agv_cnt(self,data):
        roll_tasket_cost_time_dict =  self.get_db_config('transfer_time')
        if  roll_tasket_cost_time_dict is None:
            roll_tasket_cost_time = 15
        else:
            roll_tasket_cost_time = roll_tasket_cost_time_dict['transfer_time']

        act_list = []
        for row in data:
            row['roll_tasket_cost_time'] = roll_tasket_cost_time
            act_list.append(row)
        return act_list


    def retasks(self,retask_platfrom,agv_data,tag =None):
        logger.info("任务恢复开始")
        
        cnt = self.GET_ALL_ACTIVE_TASKS()  

        if cnt is None:
            logger.error("查询任务表异常，退出任务恢复逻辑")
            self.set_alarm_log('error',"查询任务表异常，退出任务恢复逻辑")
            return False
        if cnt !=0:
            logger.error("任务表存在数据，退出任务恢复逻辑")
            self.set_alarm_log('error',"任务表存在数据，退出任务恢复逻辑")
            return True
        
        if tag is None:
            tag = 're'
        else:
            tag = 're' + tag
        
        active_platfrom = self.get_active_platform()
    
        if active_platfrom is None:
            logger.error("无活跃站台")
            self.set_alarm_log('error',"配置异常,无活跃站台")

        stack_info = self.get_all_stack()
        if not stack_info:
            logger.error("堆栈数据获取异常或无堆栈配置，如无堆栈配置可忽略此告警")
            self.set_alarm_log('error',"堆栈数据获取异常或无堆栈配置，如无堆栈配置可忽略此告警")
        else:
            flag,advance_pre = self.http_get_mulit_stack(stack_info)
            


        stack_dict = {}
        for onestack in  stack_info:
            stack_dict[onestack.in_location_name] = {'type':'in','data':onestack}
            stack_dict[onestack.out_location_name] = {'type':'out','data':onestack}
        
        cancel_task_dict = {}    
        for row in advance_pre:
            if row in stack_dict and row not in retask_platfrom:
                if row not in cancel_task_dict:
                    cancel_task_dict[row] = {'type':stack_dict[row]['type'],'group_no':stack_dict[row]['data'].group_no}


        if cancel_task_dict:
            logger.info('待取消的备料请求:{}'.format(cancel_task_dict))
            flag = self.http_cancel_stack_task(cancel_task_dict)
            if flag ==False:
                self.set_alarm_log('error',"取消备料请求失败，忽略取消操作，具体原因查看日志")

        if len(retask_platfrom) ==0 and not advance_pre:
            return True
    
        
        platform_dict = {}

        for one_p in active_platfrom:
            if one_p.location_name in retask_platfrom:
                platform_dict[one_p.location_name] = one_p

    
        for row in agv_data:
            if 'process_pack' not in row or row["process_pack"] is None:
                continue

            platform_id = row["process_pack"]
            task_type = 0

            actionlist = []
            platform_ID =None
            location_name = None
            if platform_id in platform_dict:
                task_type = 1      #站台
                platform = platform_dict[platform_id]
                task_no = self.get_task_no(platform.location_name,tag=tag)
                taskopt = {(1,None):3,(2,None):2,(1,2):4,(2,1):4,(None,1):3,(None,2):2}

                task_ptr = {'task_no':task_no,
                            "platform_ID": platform.platform_ID,                   
                            'platform_name':platform.platform_name, 
                            'process_name':platform.process_name, 
                            'route_name':platform.route_name,
                            'task_location_type':task_type,
                            'task_type':1 if (platform.upper_rail_type,platform.lower_rail_type) not in taskopt else taskopt[(platform.upper_rail_type,platform.lower_rail_type)],
                            'loc':platform.location_name,
                            'priority':platform.task_priority,
                            'dz_group_no':None,
                            'G2B':None,'G2A':None, 'G1B':None, 'G1A':None, 
                            'G2B1':None, 'G2A2':None, 'G1B3':None, 'G1A4':None
                        }
                platform_ID = platform.platform_ID,
                location_name = platform.location_name 
                agv_type = int(platform.agv_type_id)
            elif platform_id in stack_dict:

                task_type = 2      #堆栈
                agv_type = 1005
                stack = stack_dict[platform_id]['data']
                #task_no = self.get_task_no(platform.location_name,tag=tag)
                task_no = self.get_task_no(stack.group_no+stack.device_ID+str(task_type))
                task_ptr = {'task_no':task_no,'task_type':3 if stack_dict[platform_id]['type'] =='in' else 2,
                    'loc':platform_id,
                    'agv_id':'',
                    "platform_ID": stack.device_ID,                   
                    'platform_name':stack.device_name,
                    'process_name':stack.process_name, 
                    'task_location_type':task_type, 
                    'dz_group_no':stack.group_no,
                    'route_name':stack.route_name,'priority':stack.task_priority,
                    'G2B':None,'G2A':None, 'G1B':None, 'G1A':None, 
                    'G2B1':None, 'G2A2':None, 'G1B3':None, 'G1A4':None
                    }
                platform_ID = stack.device_ID,
                location_name = platform_id
                    
            else:
                task_type = 0
                agv_type = 0
                logger.error("agv:{},rcs在制数据异常，站台id:{}，不存在mcs的活跃站台列表里（定线+启用)".format(row["agv_id"],platform_id))
                self.set_alarm_log('error',"agv:{},rcs在制数据异常，站台id:{}，不存在mcs的活跃站台列表里（定线+启用)".format(row["agv_id"],platform_id))
                continue

            agv_id = str(row["agv_id"])

            

            '''
            1,None  上进
            2,None  上出
            1,2     上进下出
            2,1     上出下进
            None,1  下进
            None,2  下出
            
        '''
            #ps.upper_rail_type ,ps.upper_basket_type,ps.lower_rail_type

            
            if "parameter_str_2" not in row or row["parameter_str_2"] is None:
                logger.error("rcs提供的在制数据异常，忽略agv:{}，站台id:{}的恢复，process_pack字段存在但是parameter_str_2不存在".format(row["agv_id"],platform_id))
                self.set_alarm_log('error',"rcs提供的在制数据异常，忽略agv:{}，站台id:{}的恢复，process_pack字段存在但是parameter_str_2不存在".format(row["agv_id"],platform_id))            
                continue
            
            actionlist = self.get_action_by_agv_cnt(json.loads(row["parameter_str_2"]))

            send_data = self.get_send_data(task_no,platform_ID,location_name,actionlist,task_type,str(agv_id),agv_type)
            with self.get_mcs_session()() as session:
                id = session.execute(text(defines.ADD_ONE_TASK), task_ptr).one()
                session.execute(text(defines.ADD_ONE_TASK_COMMAND), {'task_id':id[0],'task_no':task_no,'task_delay_time':0,'send_data':json.dumps(send_data)})
                session.commit()          

        return True
           
    @timer
    def execute(self):
        global load_cnt

        agv_count,process_pack_set,srcdata = self.get_platfrom_group_agv_num()
        tag = self.get_tag()
        
        if load_cnt == 0 and agv_count is None:
            logger.error('程序暂停，等待rcs返回在制信息')
            self.set_alarm_log('error',"程序暂停，等待rcs返回在制信息")
            return        
        
        if load_cnt == 0:
            self.set_data_snapshot({},agv_count,srcdata,tag)
            try:
                resend_task_dict = self.get_db_config('resend_task')
                resend_task = resend_task_dict['resend_task']
            except Exception:
                resend_task = 1
            if resend_task == 1:
                flag = self.retasks(process_pack_set,srcdata,tag)
            
                if flag == True:
                    load_cnt = 1 
                else:
                    return 
            else:
                load_cnt = 1 

        self.dispatch(agv_count,srcdata,tag)   
        if self.executor._work_queue.qsize() > 0:
            logger.info("堆栈任务正在执行")
            return

        # 提交函数b到线程池
        future = self.executor.submit(self.stack,agv_count)
        

        #self.stack(agv_count,tag=tag)

    def set_data_snapshot(self,active_platfrom,agv_count,srcdata,tag = 'new'):
        def __default(obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime('%Y-%m-%dT%H:%M:%S')
            else:
                raise TypeError('%r is not JSON serializable' % obj)
        json_data = json.dumps([dict(row) for row in active_platfrom],default=__default)
        try:
            sql = '''
                INSERT INTO public.dma_snap_shot(
                    stock_type, stock_info, zz_info, zz_summary_info, created_time,tag)
                    VALUES (1,:platfrom_info, :zr, :zz, now(),:tag);
            '''
            self.get_mcs_con().connect().execute(text(sql),{'platfrom_info':json_data ,'zr':json.dumps(srcdata),'zz':json.dumps(agv_count),'tag':tag})
        except (Exception) as e:
            logger.error(traceback.format_exc())
            return None

    def set_alarm_log(self,level,data,type =1):
        '''
        1. DEBUG
        2. INFO
        3. WARNING
        4. ERROR
        5. CRITICAL
        
        '''
        unused_time = 1 #小时
        level_map = {'info':2,'warning':3,'error':4,'critcal':5}
        ptr = {
            'type':type,
            'level':0 if level not in level_map else level_map[level],
            'data':data,
            't':unused_time

        }
        s_sql = '''select id,md5_data from dma_alarm_log as al
	    where md5_data = MD5(:data) and alarm_type =:type and level = :level
        '''
        i_sql = '''INSERT INTO public.dma_alarm_log(
	    alarm_type, level, alarm_desc, first_alarm_time, alarm_times, last_updated_time,md5_data)
	    VALUES (:type, :level, :data,now(),1,now(), MD5(:data));
        '''
        u_sql = '''
        update dma_alarm_log set alarm_times= alarm_times+1,last_updated_time = now(),
        first_alarm_time = (case when (now() - last_updated_time)< ':t hours' then first_alarm_time else now() end)
        where alarm_type =:type and level = :level and md5_data = MD5(:data)
        '''

        try:
            with self.get_mcs_session()()as session:
                data = session.execute(text(s_sql),ptr).fetchall()
                if len(data) != 0:
                    session.execute(text(u_sql),ptr)
                else:
                    session.execute(text(i_sql),ptr)
                session.commit()
        except (Exception) as e:
            logger.error("数据库操作异常{}".format(str(e)))
 
        
    def run(self):
        try:
            task_switch_dict = self.get_db_config('task_switch')
            task_switch = task_switch_dict['task_switch']
        except Exception:
            task_switch = 1
        if task_switch == 1:
            try:
                self.execute()
            except (Exception) as e:
                logger.error(traceback.format_exc())
                pass
        else:
            logger.info("任务生成功能关闭，请在全局配置开启")
            self.set_alarm_log('info','任务生成功能关闭，请在全局配置开启')


if __name__ == '__main__':
    do = mcs_dispatch()
    do.run()

#一个组两个堆栈，会生成两个任务