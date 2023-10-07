import enum

GET_ACTIVE_PLATFORM = '''
--全套配置查询，前后置关系，动作信息,任务生成判定条件
with rejected_info as(SELECT srpr.from_platforminfo_id as from_id,
	pit."platform_ID" as to_platform_id,pit.platform_name as to_platform_name,pit.id as to_id
	FROM public.shunt_reject_platform_relation as srpr
	inner join bdm_platform_info as pit on srpr.to_platforminfo_id = pit.id),
shunt_infro as(
	select  pgr.platforminfo_id,pg."group_ID" as group_no,pg.group_name from shunt_platform_group_relation as pgr
	inner join bdm_platform_group as pg on pg.id = pgr.platformgroup_id
),stack_info as(
	select rcdr.group_id,pgd.group_name,pgd."group_ID" as group_no,pgd.route_schema_id,pgd.process_id,cdi.out_is_used
	from bdm_cache_device_info  as cdi
	inner join bdm_route_cache_device_relation as rcdr on rcdr.cache_device_id = cdi.id
	inner join bdm_platform_group as pgd on pgd.id = rcdr.group_id
)
,platform as(
SELECT rs.route_name,rs."route_ID",pg.group_name,pg."group_ID" as group_no, ps.process_name,ps."process_ID" as process_no,
pi.platform_name,pi."platform_ID", pi.location_name,pi.is_dry_type,pi.wet_group_threshold,
pi.platform_type,ps.upper_rail_type ,ps.upper_basket_type,ps.lower_rail_type,ps.lower_basket_type,
pi.process_id,ps.source_process_id,ps.target_process_id,pg.route_schema_id,pi.id,ps.ordering, pi.task_priority,
(case when pi.q_time is NULL then ps.q_time else pi.q_time end) as q_time,ps.pitch_time,
pi.task_trigger_type,pri.dock_status,pi.up_task_trigger_threshold,pi.down_task_trigger_threshold,pri.upper_basket_num,pri.lower_basket_num,pri.upper_rail_state,pri.lower_rail_state,
(case when now() - pri.last_updated_time >= '15 s' then true else false end) as past_due,pri.upper_basket_changed_time,pri.lower_basket_changed_time,
exists(select end_location from dma_tasks where end_location =  pi.location_name and state in(1,2,3,4,5,6)) as has_active_task,
pg.maximum,pg.minimum,pi.delete_flag,pi.is_used,rs.is_used as route_is_used,pi.task_delay_time,
pi.shunt_threshold,
ps.single_slot_num*((SELECT count(part_type) from bdm_platform_part where bdm_platform_part.platform_info_id = pi.id)/ (select count(upper_rail_type)+count(lower_rail_type) from  bdm_process_section where id = pi.process_id)) as slot_num,
pri.last_updated_time,(case when now() - pri.last_updated_time >= '15 s' then true else false end) as overed,
(select array_to_json(array_agg(rejected_info.to_platform_id)) from rejected_info where rejected_info.from_id = pi.id) as rejected_to_platform,
(select array_to_json(array_agg(shunt_infro.group_no)) from shunt_infro where shunt_infro.platforminfo_id = pi.id) as shunt_from_platform,
(select array_to_json(array_agg(shunt_infro.group_name)) from shunt_infro where shunt_infro.platforminfo_id = pi.id) as shunt_from_platform_name,
(select array_to_json(array_agg(distinct stack_info.group_no)) from stack_info where stack_info.route_schema_id = rs.id and stack_info.process_id = ps.source_process_id) as src_stack_gourp_no,
(select array_to_json(array_agg(distinct stack_info.group_name)) from stack_info where stack_info.route_schema_id = rs.id and stack_info.process_id = ps.source_process_id) as src_stack_gourp_name
from bdm_platform_info as pi
left join bdm_platform_group as pg on pg.id = pi.group_id
inner join bdm_process_section as ps on ps.id = pi.process_id
left join bdm_route_schema as rs on rs.id = pg.route_schema_id
left join bdm_platform_real_info as pri on pri.platform_info_id = pi.id)
select p.*,
(select platform.group_no from platform where platform.process_id = p.source_process_id and platform.route_schema_id = p.route_schema_id limit 1) as "上工艺设备组",
--(select array_to_json(array_agg(platform."platform_ID")) from platform where platform.process_id = p.source_process_id and platform.route_schema_id = p.route_schema_id) as "上工艺机台",
(select platform.group_no from platform where platform.process_id = p.target_process_id and platform.route_schema_id = p.route_schema_id limit 1) as "下工艺设备组",
--(select array_to_json(array_agg(platform."platform_ID")) from platform where platform.process_id = p.target_process_id and platform.route_schema_id = p.route_schema_id) as "下工艺机台",
(select array_to_json(array_agg(t)) from(
select (case when part_type =2 then 'put' when part_type = 1 then 'fetch'  else 'close' end) as opt,
	(case when p.upper_basket_type in (3,5) and slot_no in ('G2A','G2B') then 0 
	 when p.upper_basket_type is NULL and slot_no in ('G2A','G2B') then -1 
	 when p.lower_basket_type in (3,5) and slot_no in ('G1A','G1B') then 0 
	 when p.lower_basket_type is NULL and slot_no in ('G1A','G1B') then -1  
	 else 1 end) as basket_type,"location_ID",slot_no ,
	(select case when (p.upper_rail_type =2 or p.upper_rail_type is NULL) and slot_no in ('G2A','G2B') then '' 
	 when (p.lower_rail_type =2 or p.lower_rail_type is NULL) and slot_no in ('G1A','G1B') then '' 
	 else (select platform.group_no from platform where platform.process_id = p.source_process_id and platform.route_schema_id = p.route_schema_id limit 1) 
	 end )
from bdm_platform_part where  platform_info_id =  p.id
	) as t ) as package
from platform as p
where p.is_used = true and p.route_is_used = true;
'''

GET_PLATFORM_BY_PROCESS_AND_ROUTE = '''
SELECT pi.id,pi."platform_ID", pi.platform_name, pi.platform_type, pi.pitch_time, pi.location_name, 
pi.rejected_threshold, pi.is_dry_type, pi.shunt_threshold, pi.task_trigger_type, 
pi.up_task_trigger_threshold,pi.down_task_trigger_threshold, pri.upper_basket_num, pri.lower_basket_num, pi.task_priority, pi.task_delay_time, 
pi.process_id, pg.id as group_id,pg.group_name, pg.maximum,pg.minimum,
ps."process_ID" as process_no,ps.process_name,ps.ordering,ps.upper_rail_type,ps.upper_basket_type,ps.lower_rail_type,ps.lower_basket_type,ps.source_process_id,
ps.pitch_time,pg.route_schema_id,pg."group_ID" as group_no,(case when pi.q_time is NULL then ps.q_time else pi.q_time end) as q_time,
pri.upper_rail_state,pri.lower_rail_state,now() as upper_basket_changed_time,now() as lower_basket_changed_time,pri.dock_status,ps.single_slot_num,
pri.last_updated_time,(case when now() - pri.last_updated_time >= '15 s' then true else false end) as overed
from bdm_platform_info as pi
inner join bdm_platform_group as pg on pg.id = pi.group_id
inner join bdm_process_section as ps on ps.id = pi.process_id
inner join bdm_platform_real_info as pri on pri.platform_info_id = pi.id
--left join  bdm_process_section as pss on pss.id = ps.source_process_id
and pg.process_id =:process_id AND pg.route_schema_id =:route_schema_id;
'''

GET_PLATFORM_PART_BY_PLATFROM_id ='''
select (case when part_type is NULL then 0 else part_type end)as part_type,axis_no,"location_ID" as location_no,slot_no from public.bdm_platform_part
where platform_info_id = :platform_info_id
'''

GET_ALL_CONFIGURATION  = '''
select key,value from bdm_configuration;
'''
 
GET_ONE_CONFIGURATION = '''
select key,value,value_type from bdm_configuration
where key =:key_id;
'''

GET_ACTIVE_TASKS_BY_PLATFORM_ID = '''
SELECT task_no, task_type, end_location,"platform_ID", priority, state, rcs_order_id, agv_no
FROM public.dma_tasks 
where "platform_ID" in :platform_ID and state in(1,2,3,4,5,6)
'''

GET_ALL_ACTIVE_TASKS = '''
SELECT count(*) as cnt FROM public.dma_tasks where state in(1,2,3,4,5,6)
'''

GET_LAST_TASKS_BY_PLATFORM_ID = '''
SELECT task_no, task_type, end_location,"platform_ID", priority, state, rcs_order_id, agv_no,end_time
FROM public.dma_tasks 
where "platform_ID" = :platform_ID
order by id desc limit 1
'''


GET_ACTIVE_TASKS_BY_LOC = '''
SELECT task_no, task_type, end_location,"platform_ID", priority, state, rcs_order_id, agv_no
FROM public.dma_tasks 
where end_location in :loc and state in(1,2,3,4,5,6)
'''

GET_EMPTY_ROUTE_BY_DST= '''  
    SELECT ers.platform_info_id as target_platform_info_id,rpr.platforminfo_id as src_platform_info_id,pi."platform_ID"
	FROM public.bdm_empty_route_schema as ers
	inner join bdm_route_platform_relation as rpr on rpr.emptybasketrouteschema_id = ers.id
    inner join bdm_platform_info as pi on pi.id = ers.platform_info_id
	where rpr.platforminfo_id = :platform_id
	--and  pi.is_used = true and pi.delete_flag = false;
'''



ADD_ONE_TASK= '''
INSERT INTO public.dma_tasks(
	task_no, task_type, end_location, priority, state, created_time, last_updated_time,axis1_action, axis2_action, axis3_action, axis4_action,  axis1_package_name, axis2_package_name, axis3_package_name, axis4_package_name,"platform_ID", platform_name, route_name,process_name,task_location_type,dz_group_no)
	VALUES (:task_no,:task_type,:loc,:priority,1,now(),now(),:G2B,:G2A,:G1B,:G1A,:G2B1,:G2A2,:G1B3,:G1A4,:platform_ID, :platform_name, :route_name,:process_name,:task_location_type,:dz_group_no) returning id;
'''

ADD_ONE_TASK_COMMAND ='''
	INSERT INTO public.dma_tasks_command(
	task_id,task_no, command_type, current_retry_times, last_retry_time, created_time, last_updated_time, send_data,task_delay_time)
	VALUES (:task_id, :task_no,1,0,now(), now(), now(), :send_data,:task_delay_time);
'''

GET_ALL_CREATED_TASKS = '''
select t.id  as task_id,t.task_no,t.priority, tc.id as cmd_id,(select send_data from dma_tasks_command where task_id = t.id) as send_data 
from dma_tasks as t
inner join dma_tasks_command as tc on tc.task_id = t.id
where state  in (1,2) and now() - t.created_time >= interval '1 second' * tc.task_delay_time
'''

SET_TASK_RUNNING = f'''
    UPDATE
        dma_tasks
    SET
        state = 3,
        last_updated_time = now(),
        rcs_order_id = :rcs_order_id
    WHERE
        id = :task_id
    ;
'''

SET_COMMAND_CONSUMED = '''
    UPDATE
        dma_tasks_command
    SET
        current_retry_times = current_retry_times+1,
        last_retry_time = now(),
        error_reason = :error_reason
    WHERE
        id = :cmd_id
    ;
'''




#堆栈
GET_CACHE_DEVICE_INFO = '''
select cdi.id as stack_id,cdi."device_ID",cdi.device_name,cdi.in_location_name, cdi.out_location_name,
cdi.allow_task_num,rcdr.group_id,pg.group_name,pg."group_ID" as group_no,pg.route_schema_id,pg.process_id,rs.route_name,
pgd.group_name as stack_group_name,pgd."group_ID" as stack_group_no,ps.process_name,
cdi.storage_num,pgd.maximum,pgd.minimum,cdi.in_is_used,cdi.out_is_used,cdi.task_priority
from bdm_cache_device_info  as cdi
inner join bdm_route_cache_device_relation as rcdr on rcdr.cache_device_id = cdi.id
inner join bdm_platform_group as pgd on pgd.id = rcdr.group_id
inner join bdm_platform_group as pg on pg.process_id = pgd.process_id and pg.route_schema_id = pgd.route_schema_id and pg.group_type =1
inner join bdm_route_schema as rs on rs.id = pg.route_schema_id
inner join bdm_process_section as ps on ps.id = pg.process_id
'''

GET_STACK_GROUP_PLATFORM_ID = '''
select distinct
rcdr.group_id,pg.group_name,pg."group_ID" as group_no,pg.route_schema_id,pg.process_id,rs.route_name,
pgd.group_name as stack_group_name,pgd."group_ID" as stack_group_no
from bdm_cache_device_info  as cdi
inner join bdm_route_cache_device_relation as rcdr on rcdr.cache_device_id = cdi.id
inner join bdm_platform_group as pgd on pgd.id = rcdr.group_id
inner join bdm_platform_group as pg on pg.process_id = pgd.process_id and pg.route_schema_id = pgd.route_schema_id and pg.group_type =1
inner join bdm_route_schema as rs on rs.id = pg.route_schema_id 
inner join bdm_empty_cache_route_schema as ecrs on cdi.id = ecrs.cache_info_id
inner join bdm_cache_route_platform_relation as crpr on crpr.emptycacherouteschema_id = ecrs.id
where crpr.platforminfo_id = :platform_id and pg.route_schema_id = :route_schema_id and pg.process_id = :process_id
'''

GET_CACHE_DEVICE_INFO_BY_GROUP_NAME = '''
select cdi.id as stack_id,cdi."device_ID",cdi.device_name,cdi.in_location_name, cdi.out_location_name,
cdi.allow_task_num,rcdr.group_id,pg.group_name,pg."group_ID" as group_no,pg.route_schema_id,pg.process_id,ps.process_name,rs.route_name,
pgd.group_name as stack_group_name,pgd."group_ID" as stack_group_no,
cdi.storage_num,pgd.maximum,pgd.minimum,cdi.in_is_used,cdi.out_is_used,cdi.task_priority
from bdm_cache_device_info  as cdi
inner join bdm_route_cache_device_relation as rcdr on rcdr.cache_device_id = cdi.id
inner join bdm_platform_group as pgd on pgd.id = rcdr.group_id
inner join bdm_platform_group as pg on pg.process_id = pgd.process_id and pg.route_schema_id = pgd.route_schema_id and pg.group_type =1
inner join bdm_route_schema as rs on rs.id = pg.route_schema_id 
inner join bdm_process_section as ps on ps.id = pg.process_id
where pg."group_ID" = :group_no and  pg.process_id = :process_id
'''


GET_IN_PLATFORM_BY_PROCESS_AND_ROUTE = '''
SELECT pi.id,ps.id as process_id,pg.route_schema_id,ps.process_name,ps."process_ID" as process_no,
pg."group_ID" as group_no,
pss.upper_rail_type,pss.upper_basket_type,pss.lower_rail_type,pss.lower_basket_type
from bdm_process_section as ps
inner join bdm_platform_info as pi on pi.process_id = ps.target_process_id
left join bdm_platform_group as pg on pg.id = pi.group_id 
inner join bdm_process_section as pss on pss.id = ps.target_process_id
where ps.id = :process_id  and pg.route_schema_id =:route_schema_id limit 1;
'''

GET_OUT_PLATFORM_BY_PROCESS_AND_ROUTE = '''
SELECT pi.id,ps.id as process_id,pg.route_schema_id,ps.process_name,ps."process_ID" as process_no,
pg."group_ID" as group_no,
ps.upper_rail_type,ps.upper_basket_type,ps.lower_rail_type,ps.lower_basket_type
from bdm_process_section as ps
inner join bdm_platform_info as pi on pi.process_id = ps.id
inner join bdm_platform_group as pg on pg.id = pi.group_id 
where ps.id = :process_id and pg.route_schema_id = :route_schema_id limit 1;
'''

GET_STACK_LOC = '''
SELECT part_type,axis_no-((part_type-1)*4),"location_ID" as loc_no,slot_no FROM public.bdm_cache_device_part
where cache_device_id=:stack_id and part_type=:part_type
'''

GET_STACK_GROUP_COUNT_BY_GROUP_STACK= '''
select equip_code,in_material_type_name as group_no,
sum(basket_num)/10  as cnt
from dam_cache_device_stock
where equip_code = :stack_no and in_material_type_name =:group_no
 group by equip_code,in_material_type_name
'''

GET_TIMEOUT_STACK_GROUP_COUNT_BY_GROUP_STACK ='''
select equip_code,in_material_type_name as group_no,basket_num,output_time_consume,storge_time,q_time
from dam_cache_device_stock
where  equip_code = :stack_no and in_material_type_name =:group_no and output_time_consume+storge_time >= q_time
'''

GET_GOURP_MAP = '''
select pgauto."group_ID" as at_group_no,pgauto.group_name as at_group_name,pgb."group_ID" as b_group_no,pgb.group_name as b_group_name
from bdm_platform_group as pgauto
inner join bdm_platform_group as pgb on pgauto.process_id = pgb.process_id and pgauto.route_schema_id =pgb.route_schema_id 
and pgb.group_type=2 and pgauto.group_type=1'''


#一车花篮数临时写死
GET_GROUP_AGV_CNT = '''
with group_cnt as(
SELECT rs.route_name,rs."route_ID",pg.group_name,pg."group_ID" as group_no, ps.process_name,ps."process_ID" as process_no,pg.process_id,rs.id,
sum((case when pri.upper_rail_state is NULL or pri.upper_rail_state = 1 or pi.is_used = false then 0 else pri.upper_basket_num end)) as upper_basket_num,
sum((case when pri.lower_rail_state is NULL or pri.lower_rail_state = 1 or pi.is_used = false then 0 else pri.lower_basket_num end)) as lower_basket_num
from bdm_platform_info as pi
left join bdm_platform_group as pg on pg.id = pi.group_id
inner join bdm_process_section as ps on ps.id = pi.process_id
left join bdm_route_schema as rs on rs.id = pg.route_schema_id
left join bdm_platform_real_info as pri on pri.platform_info_id = pi.id
group by rs.route_name,rs."route_ID",pg.group_name,pg."group_ID", ps.process_name,ps."process_ID",pg.process_id,rs.id
)
select gc.route_name,gc."route_ID",gc.group_name,gc.group_no, gc.process_name,gc.process_no,gc.upper_basket_num,gc.lower_basket_num,
(select group_cnt.group_name from group_cnt where group_cnt.process_id = ps.target_process_id and gc.id = group_cnt.id),
gc.lower_basket_num,
(select group_cnt.upper_basket_num from group_cnt where group_cnt.process_id = ps.target_process_id and gc.id = group_cnt.id),
ceil((gc.lower_basket_num+(select group_cnt.upper_basket_num from group_cnt where group_cnt.process_id = ps.target_process_id and gc.id = group_cnt.id))::double precision /(ps.single_slot_num*2)) as agv_num
from group_cnt as gc
inner join bdm_process_section as ps on ps.id = gc.process_id
'''

#一车花篮数临时写死
GET_EMPTY_AGV_CNT = '''
select t.group_name, t.group_no,ceil((t.upper_basket_num)::double precision /(5*2)) as agv_num
 from(
SELECT
pg.group_name,pg."group_ID" as group_no,
sum((case when pri.upper_rail_state is NULL or pri.upper_rail_state = 1 or pi.is_used = false then 0 else pri.upper_basket_num end)) as upper_basket_num
--sum((case when pri.lower_rail_state is NULL or pri.lower_rail_state = 1 or pi.is_used = false then 0 else pri.lower_basket_num end)) as lower_basket_num
FROM public.bdm_empty_route_schema as ers
inner join bdm_route_platform_relation as rpr on rpr.emptybasketrouteschema_id = ers.id
inner join bdm_platform_info as pi on pi.id = rpr.platforminfo_id
inner join bdm_platform_info as pis on pis.id = ers.platform_info_id
inner join bdm_platform_group as pg on pg.id = pis.group_id
left join bdm_platform_real_info as pri on pri.platform_info_id = pi.id
group by pg.group_name,pg."group_ID")
as t
'''


GET_WET_GROUP_NO_BY_PLATFORM ='''
SELECT pg."group_ID" as group_no,pi."platform_ID" FROM public.wet_platform_group_relation as wpgr
inner join bdm_platform_group as pg on pg.id = wpgr.platformgroup_id
inner join bdm_platform_info as pi on pi.id = wpgr.platforminfo_id
where pi."platform_ID" = :platform_ID
'''


GET_STACK_TASK = '''
SELECT "device_ID", material_type, tag, task_type, task_state, traceback_state, request_allowed, created_time, end_time
FROM public.dam_cache_device_tasks
where "device_ID" = :device_ID and material_type=:group_no and task_state = 0 and task_type = :type
'''

ADD_STACK_TASK ='''
INSERT INTO public.dam_cache_device_tasks(
	"device_ID", material_type, tag, task_type, task_state, traceback_state, request_allowed, created_time)
	VALUES (:device_ID, :group_no, :task_no, :type, 0, 0, 0, now()) returning id;
    
'''
SET_STACK_TASK ='''
UPDATE public.dam_cache_device_tasks
	SET tag=:tag
	WHERE "device_ID" = :device_ID and material_type=:group_no and task_state = 0 and task_type = :type returning id;
    
'''

SET_STACK_TASK_FINISHED ='''
UPDATE public.dam_cache_device_tasks
	SET task_state = 2
	WHERE task_type = :type and traceback_state = 1 and tag =:tag;
'''


