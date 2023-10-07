import Cookies from 'js-cookie'
// 登录凭证处理

const TokenKey = 'vue_admin_template_token_MCS'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
