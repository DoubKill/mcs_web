export const optionAbnormal = {
  tooltip: {
    trigger: 'axis'
  },
  color: ['#59A0F7'],
  //   legend: {
  //     data: ['今天', '昨天'],
  //     top: 'bottom',
  //     left: 'center'
  //   },
  title: {
    left: 'left',
    text: '异常任务比例统计',
    textStyle: { color: '#000' }
  },
  grid: {
    left: '5%',
    right: '4%',
    // top: '3%',
    // bottom: '12%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: []
  },
  yAxis: {
    type: 'value',
    max: 1
    // nameGap: '35',
    // name: '产量(百片)',
    // nameLocation: 'middle'
  },
  series: [
    {
      name: '异常任务比例',
      type: 'line',
      data: []
    }
  ]
}
export const optionSW = {
  tooltip: {
    trigger: 'axis'
  },
  color: ['#71C87C'],
  title: {
    left: 'left',
    text: 'SW产能统计(万片)',
    textStyle: { color: '#000' }
  },
  grid: {
    left: '5%',
    right: '4%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: []
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'SW产能统计(万片)',
      type: 'line',
      data: []
    }
  ]
}
