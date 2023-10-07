import axios from 'axios'
import router from '@/router'
import {
  Message
} from 'element-ui'
import store from '@/store'
import Cookies from 'js-cookie'
// import {
//   getToken
// } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  // 合到dev的时候手动改一下 改成线上地址
  baseURL: Cookies.get('zc-url'),
  // 'http://124.160.19.254:60001/',
  // baseURL: 'http://10.4.24.25:8169/',
  timeout: 10000000000
})

// request interceptor
service.interceptors.request.use(
  config => {
    if (Cookies.get('zc-userId')) {
      config.headers['TenantNumber'] = 1
      // config.headers['UserId'] = Cookies.get('zc-userId')
    }
    if (Cookies.get('zc-url')) {
      config.baseURL = Cookies.get('zc-url') || ''
      // config.baseURL = 'http://10.4.24.25:8169/'
    }
    return config
  },
  error => {
    // do something with request error
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  response => {
    if (response.status < 300) {
      if (response.data.state === 0) {
        // Message({
        //   message: response.data.datas,
        //   type: 'error',
        //   duration: 3 * 1000
        // })

        // if (response.data.msg === `对象名 't_stock_out_task' 无效。`) {
        //   store.dispatch('user/logout')
        //   router.push('/login')
        //   return Promise.reject()
        // }
        const res = response.data
        return Promise.resolve(res)
      } else {
        const res = response.data
        return Promise.resolve(res)
      }
    } else {
      // Message({
      //   message: '请求失败' + response.status,
      //   type: 'error',
      //   duration: 3 * 1000
      // })
      return Promise.reject(response)
    }
  },
  error => {
    if (error.response.status && error.response.status === 403 ||
      error.response.status === 401) {
      Message({
        message: '登录过期',
        type: 'error',
        duration: 3 * 1000
      })
      store.dispatch('user/logout')
      router.push('/login')
      return Promise.reject()
    }
    // if (Object.prototype.toString.call(error.response.data) === '[object Object]') {
    //   const obj = error.response.data
    //   let str = ''
    //   if (obj && Object.prototype.hasOwnProperty.call(obj, 'batching_details')) {
    //     obj.batching_details.forEach(details => {
    //       for (const key in details) {
    //         str += details[key]
    //       }
    //     })
    //   } else {
    //     for (const key in obj) {
    //       if (!(obj[key] instanceof Array)) {
    //         str += obj[key]
    //       } else {
    //         obj[key].forEach(element => {
    //           if (Object.prototype.toString.call(element) === '[object Object]') {
    //             for (const key in element) {
    //               str += element[key]
    //             }
    //           } else {
    //             str += element
    //           }
    //         })
    //       }
    //     }
    //   }

    //   Message({
    //     message: str,
    //     type: 'error',
    //     duration: 3 * 1000
    //   })
    //   return Promise.reject(error.response.data)
    // } else if (Object.prototype.toString.call(error.response.data) === '[object Array]') {
    //   let str = ''
    //   error.response.data.forEach(errorData => {
    //     let obj = null
    //     if (errorData) {
    //       try {
    //         obj = JSON.parse(errorData)
    //       } catch (e) {
    //         obj = errorData
    //       }
    //     }

    //     if (errorData && Object.prototype.hasOwnProperty.call(obj, 'non_field_errors')) {
    //       str += (`${obj.non_field_errors.join(',')}\n`)
    //     } else if (Object.prototype.hasOwnProperty.call(obj, 'batching_details')) {
    //       obj.batching_details.forEach(details => {
    //         if (details && Object.prototype.hasOwnProperty.call(details, 'non_field_errors')) {
    //           str += (`${details.non_field_errors.join(',')}\n`) + ';'
    //         } else {
    //           str += details
    //         }
    //       })
    //     } else {
    //       str += errorData
    //     }
    //     //  else if (Object.prototype.toString.call(error.response.data) === '[object Object]') {
    //     //   for (const key in obj) {
    //     //     if (!(obj[key] instanceof Array)) {
    //     //       str += obj[key]
    //     //     } else {
    //     //       obj[key].forEach(element => {
    //     //         str += element
    //     //       })
    //     //     }
    //     //   }
    //     // }
    //   })
    //   Message({
    //     message: str,
    //     type: 'error',
    //     duration: 3 * 1000
    //   })
    //   return Promise.reject(error.response.data)
    // } else if (typeof error.message === 'string') {
    //   Message({
    //     message: error.message,
    //     type: 'error',
    //     duration: 3 * 1000
    //   })
    //   return Promise.reject(error)
    // } else {
    Message({
      message: '操作错误',
      type: 'error',
      duration: 3 * 1000
    })
    return Promise.reject(error)
    // }
  }
)

export default service
