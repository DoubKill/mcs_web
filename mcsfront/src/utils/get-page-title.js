import defaultSettings from '@/settings'
// import i18n from '@/lang'
// 头部title显示

const title = defaultSettings.title || 'Vue Admin Template'

export default function getPageTitle(key) {
  // const hasKey = i18n.te(`route.${key}`)
  // if (hasKey) {
  //   const pageName = i18n.t(`route.${key}`)
  //   return `${pageName} - ${title}`
  // }
  // return `${title}`
  if (key) {
    return `${key} - ${title}`
  }
  return `${title}`
}
