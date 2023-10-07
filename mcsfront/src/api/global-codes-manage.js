import request from '@/utils/request'
import API from '@/api/url'

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
export function deleteGlobalCodes(id) {
  return request({
    url: API.GlobalCodesUrl + id + '/',
    method: 'delete'
  })
}
export function commonCode(params) {
  return request({
    url: API.CommonCode,
    method: 'get',
    params
  })
}
