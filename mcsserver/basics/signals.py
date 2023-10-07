# import logging
#
# import requests
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from basics.models import PlatformGroup, RestLocationRouteRelation, PlatFormInfo, Configuration
# from mcs import settings
# from mcs.settings import DEBUG
#
# send_log = logging.getLogger('api_log')
#
#
# def rest_location_push(rcs_url, data):
#     headers = {
#         'Content-Type': "application/json",
#         'cache-control': "no-cache",
#         'charset': 'utf-8',
#     }
#     try:
#         url = rcs_url + '/api/dispatch/universal/basic-data/locations/group_status/'
#         response = requests.post(url, json={'data': data}, headers=headers, timeout=3)
#         response.raise_for_status()  # 检查请求是否成功
#     except requests.exceptions.RequestException as e:
#         send_log.error('推送失败，info:{}'.format(e))
#     else:
#         send_log.info('休息位推送成功，info:{}'.format(response.text))
#
# # @receiver(post_save, sender=PlatformGroup)
# # def group_post_save(sender, instance=None, created=False, update_fields=None, **kwargs):
# #     if instance.group_type == 3:
# #         # [
# #         #     {
# #         #         'location_name': 'zrkd01',
# #         #         'fit_group': [
# #         #             {'machine_no': '1011', 'priority': 1}
# #         #         ],
# #         #         'if_relay': False,
# #         #         'if_active': True
# #         #     }
# #         # ]
# #         ret = {}
# #         location_relations = RestLocationRouteRelation.objects.filter(
# #             rest_location_id__in=list(instance.r_rls.values_list('rest_location_id', flat=True)))
# #         for location_relation in location_relations:
# #             location_name = location_relation.rest_location.location_name
# #             priority = location_relation.group.priority
# #             location_plts = PlatFormInfo.objects.filter(
# #                 group__route_schema=location_relation.group.route_schema,
# #                 process=location_relation.group.process
# #             ).values_list('platform_code', flat=True)
# #             if_active = location_relation.rest_location.is_used
# #             fit_group = []
# #             for plt in location_plts:
# #                 fit_group.append({'machine_no': plt, 'priority': priority})
# #             if location_name in ret:
# #                 ret[location_name]['fit_group'].extend(fit_group)
# #             else:
# #                 ret[location_name] = {
# #                     'location_name': location_name,
# #                     'fit_group': fit_group,
# #                     'if_relay': False,
# #                     'if_active': if_active
# #                 }
# #         rest_location_push(list(ret.values()))
#
#
# @receiver(post_save, sender=PlatformGroup)
# def group_post_save(sender, instance=None, created=False, update_fields=None, **kwargs):
#     if instance.group_type == 3 and not DEBUG:
#         location_relations = RestLocationRouteRelation.objects.filter(
#             rest_location_id__in=instance.r_rls.values('rest_location_id')
#         )
#         ret = {}
#         rcs_url = Configuration.objects.get(key='rcs_url').value
#         for location_relation in location_relations:
#             location_name = location_relation.rest_location.location_name
#             priority = location_relation.group.priority
#             location_plts = PlatFormInfo.objects.filter(
#                 group__route_schema=location_relation.group.route_schema,
#                 process=location_relation.group.process
#             ).values_list('platform_ID', flat=True)
#             fit_group = [{'machine_no': plt, 'priority': priority} for plt in location_plts]
#             ret.setdefault(location_name, {
#                 'location_name': location_name,
#                 'fit_group': [],
#                 'if_relay': False,
#                 'if_active': location_relation.rest_location.is_used
#             })
#             ret[location_name]['fit_group'].extend(fit_group)
#         rest_location_push(rcs_url, list(ret.values()))