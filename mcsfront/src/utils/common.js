// 公用数据
export default {
  formLabelWidth: '120px',
  normalOutboundSwitch: true,
  statusList: [
    { id: 1, name: '完成' },
    { id: 2, name: '执行中' },
    { id: 3, name: '失败' },
    { id: 4, name: '新建' },
    { id: 5, name: '关闭' }
  ],
  rubberStateList: [
    {
      value: 1, label: '编辑'
    }, {
      value: 2, label: '提交'
    }, {
      value: 3, label: '校对'
    }, {
      value: 4, label: '启用'
    }, {
      value: 5, label: '驳回'
    }, {
      value: 6, label: '废弃'
    }, {
      value: 7, label: '停用'
    }
  ],
  echartColor: ['#FC7213', '#73c0de', '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'],
  workTypeList: ['巡检', '保养', '润滑', '标定', '维修'],
  basketTypeList: [
    { id: 1, name: '空叠片盒' },
    { id: 2, name: '满叠片盒' },
    { id: 3, name: '空湿花篮' },
    { id: 4, name: '满湿花篮' },
    { id: 5, name: '空干花篮' },
    { id: 6, name: '满干花篮' },
    { id: 7, name: '空车' }
  ],
  FOREIGN_KEY: {
    source_process_name: 'source_process',
    working_area_name: 'working_area',
    target_process_name: 'target_process',
    upper_rail_type_name: 'upper_rail_type',
    upper_basket_type_name: 'upper_basket_type',
    lower_rail_type_name: 'lower_rail_type',
    lower_basket_type_name: 'lower_basket_type',

    processes_name: 'processes'
  }
}
