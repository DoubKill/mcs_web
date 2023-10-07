import request from '@/utils/request'
import API from '@/api/url'

export function permissions(method, id, data = {}) {
  const obj = {
    url: id ? API.PermissionUrl + id + '/' : API.PermissionUrl,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
