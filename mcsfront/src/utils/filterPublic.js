import Vue from 'vue'

Vue.filter('setTimeMin', function(value) {
  if (value < 0) return value
  if (!value) return 0
  const a = (parseFloat(value / 60)).toString()
  let num
  if (a.lastIndexOf('.') > -1) {
    num = a.substring(0, a.lastIndexOf('.') + 2)
  } else {
    num = a
  }
  return Number(num)
})
