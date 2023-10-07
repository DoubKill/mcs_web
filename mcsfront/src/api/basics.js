import request from '@/utils/request'
import API from '@/api/url'

export function login(data) {
  return request({
    url: API.LoginUrl,
    method: 'post',
    data
  })
}
export function resetPassword(method, id, data = {}) {
  const obj = {
    url: id ? API.ResetPassword + id + '/' : API.ResetPassword,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}

export function personnelsUrl(method, id, data = {}) {
  const obj = {
    url: id ? API.PersonnelsUrl + id + '/' : API.PersonnelsUrl,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function planScheduleUrl(method, id, data = {}) {
  const obj = {
    url: id ? API.PlanScheduleUrl + id + '/' : API.PlanScheduleUrl,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function setSuperuser(method, id, data = {}) {
  const obj = {
    url: id ? API.SetSuperuser + id + '/' : API.SetSuperuser,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}

export function permissions(method, id, data = {}) {
  const obj = {
    url: id ? API.PermissionUrl + id + '/' : API.PermissionUrl,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}

// 公共代码
export function getGlobalTypes(params) {
  return request({
    url: API.GlobalTypesUrl,
    method: 'get',
    params
  })
}

export function postGlobalTypes(data) {
  return request({
    url: API.GlobalTypesUrl,
    method: 'post',
    data
  })
}

export function putGlobalTypes(data, id) {
  return request({
    url: API.GlobalTypesUrl + id + '/',
    method: 'put',
    data
  })
}

export function deleteGlobalTypes(id) {
  return request({
    url: API.GlobalTypesUrl + id + '/',
    method: 'delete'
  })
}

export function globalTypesUrlBatchDestroy(method, id, data = {}) {
  const obj = {
    url: id ? API.GlobalTypesUrlBatchDestroy + id + '/' : API.GlobalTypesUrlBatchDestroy,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}

export function getGlobalCodes(params) {
  return request({
    url: API.GlobalCodesUrl,
    method: 'get',
    params
  })
}
export function postGlobalCodes(data) {
  return request({
    url: API.GlobalCodesUrl,
    method: 'post',
    data
  })
}
export function putGlobalCodes(data, id) {
  return request({
    url: API.GlobalCodesUrl + id + '/',
    method: 'put',
    data
  })
}

export function globalCodesUrlBatchDestroy(method, id, data = {}) {
  const obj = {
    url: id ? API.GlobalCodesUrlBatchDestroy + id + '/' : API.GlobalCodesUrlBatchDestroy,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function commonCode(params) {
  return request({
    url: API.CommonCode,
    method: 'get',
    params
  })
}

