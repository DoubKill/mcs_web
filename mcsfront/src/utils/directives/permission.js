import store from '@/store'

function checkPermission(el, binding) {
  const { value } = binding
  const permissionObj = store.getters && store.getters.permission

  if (value && value instanceof Array) {
    if (value.length > 0) {
      const permissionArr = permissionObj[value[0]]
      if (!permissionArr || permissionArr.length === 0) {
        return
      }
      const hasPermission = permissionArr.some(D => {
        return D === value[1]
      })

      if (!hasPermission) {
        el.parentNode && el.parentNode.removeChild(el)
      }
    }
  } else {
    throw new Error(`need roles! Like v-permission="['admin','editor']"`)
  }
}

export default {
  inserted(el, binding) {
    checkPermission(el, binding)
  },
  update(el, binding) {
    checkPermission(el, binding)
  }
}
