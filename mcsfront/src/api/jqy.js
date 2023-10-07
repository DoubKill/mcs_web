import request from '@/utils/request'
import API from '@/api/url'

export function personnelsUrl(method, id, data = {}) {
  const obj = {
    url: id ? API.PersonnelsUrl + id + '/' : API.PersonnelsUrl,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function personnelsUrlDel(method, id, data = {}) {
  const obj = {
    url: id ? API.PersonnelsUrlDel + id + '/' : API.PersonnelsUrlDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function materialIdentifies(method, id, data = {}) {
  const obj = {
    url: id ? API.MaterialIdentifies + id + '/' : API.MaterialIdentifies,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function materialIdentifiesDel(method, id, data = {}) {
  const obj = {
    url: id ? API.MaterialIdentifiesBatchDestroy + id + '/' : API.MaterialIdentifiesBatchDestroy,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function districtInfos(method, id, data = {}) {
  const obj = {
    url: id ? API.DistrictInfos + id + '/' : API.DistrictInfos,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function vehicleInfos(method, id, data = {}) {
  const obj = {
    url: id ? API.VehicleInfos + id + '/' : API.VehicleInfos,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function vehicleInfosDel(method, id, data = {}) {
  const obj = {
    url: id ? API.VehicleInfosBatchDestroy + id + '/' : API.VehicleInfosBatchDestroy,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function vehicleInfosUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.VehicleInfosBatchUpdate + id + '/' : API.VehicleInfosBatchUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function shuntConf(method, id, data = {}) {
  const obj = {
    url: id ? API.ShuntConf + id + '/' : API.ShuntConf,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function shuntConfUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.ShuntConfUpdate + id + '/' : API.ShuntConfUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function shuntConfDel(method, id, data = {}) {
  const obj = {
    url: id ? API.ShuntConfDel + id + '/' : API.ShuntConfDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function viewPath(method, id, data = {}) {
  const obj = {
    url: id ? API.ViewPath + id + '/' : API.ViewPath,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function productionProcessesUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.ProductionProcessesUpdate + id + '/' : API.ProductionProcessesUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheLocations(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheLocations + id + '/' : API.CacheLocations,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheLocationsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheLocationsDel + id + '/' : API.CacheLocationsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheLocationsUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheLocationsUpdate + id + '/' : API.CacheLocationsUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheLocationsGroup(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheLocationsGroup + id + '/' : API.CacheLocationsGroup,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheLocationsGroupDel(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheLocationsGroupDel + id + '/' : API.CacheLocationsGroupDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheLocationsGroupUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheLocationsGroupUpdate + id + '/' : API.CacheLocationsGroupUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function receiveAlarm(method, id, data = {}) {
  const obj = {
    url: id ? API.ReceiveAlarm + id + '/' : API.ReceiveAlarm,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function receiveAlarmDel(method, id, data = {}) {
  const obj = {
    url: id ? API.ReceiveAlarmDel + id + '/' : API.ReceiveAlarmDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function receiveAlarmUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.ReceiveAlarmUpdate + id + '/' : API.ReceiveAlarmUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function processesChangeSequence(method, id, data = {}) {
  const obj = {
    url: id ? API.ProcessesChangeSequence + id + '/' : API.ProcessesChangeSequence,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function platformInfo(method, id, data = {}) {
  const obj = {
    url: id ? API.PlatformInfo + id + '/' : API.PlatformInfo,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function platformInfoUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.PlatformInfoUpdate + id + '/' : API.PlatformInfoUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function platformInfoDel(method, id, data = {}) {
  const obj = {
    url: id ? API.PlatformInfoDel + id + '/' : API.PlatformInfoDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function equipParts(method, id, data = {}) {
  const obj = {
    url: id ? API.EquipParts + id + '/' : API.EquipParts,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function equipPartsUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.EquipPartsUpdate + id + '/' : API.EquipPartsUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function equipPartsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.EquipPartsDel + id + '/' : API.EquipPartsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function stockInfo(method, id, data = {}) {
  const obj = {
    url: id ? API.StockInfo + id + '/' : API.StockInfo,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function stockInfoDel(method, id, data = {}) {
  const obj = {
    url: id ? API.StockInfoDel + id + '/' : API.StockInfoDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function stockInfoUnderway(method, id, data = {}) {
  const obj = {
    url: id ? API.StockInfoUnderway + id + '/' : API.StockInfoUnderway,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function taskMonitor(method, id, data = {}) {
  const obj = {
    url: id ? API.TaskMonitor + id + '/' : API.TaskMonitor,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function stockMonitor(method, id, data = {}) {
  const obj = {
    url: id ? API.StockMonitor + id + '/' : API.StockMonitor,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function abnormalMonitor(method, id, data = {}) {
  const obj = {
    url: id ? API.AbnormalMonitor + id + '/' : API.AbnormalMonitor,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function strategyGroups(method, id, data = {}) {
  const obj = {
    url: id ? API.StrategyGroups + id + '/' : API.StrategyGroups,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function basketTransport(method, id, data = {}) {
  const obj = {
    url: id ? API.BasketTransport + id + '/' : API.BasketTransport,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function agvMonitor(method, id, data = {}) {
  const obj = {
    url: id ? API.AgvMonitor + id + '/' : API.AgvMonitor,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function agvDetailMonitor(method, id, data = {}) {
  const obj = {
    url: id ? API.AgvDetailMonitor + id + '/' : API.AgvDetailMonitor,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheLocation(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheLocation + id + '/' : API.CacheLocation,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheLocationDetail(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheLocationDetail + id + '/' : API.CacheLocationDetail,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function userImport(method, id, data = {}) {
  const obj = {
    url: id ? API.UserImport + id + '/' : API.UserImport,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function delUser(method, id, data = {}) {
  const obj = {
    url: id ? API.DelUser + id + '/' : API.DelUser,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function portMaterialType(method, id, data = {}) {
  const obj = {
    url: id ? API.PortMaterialType + id + '/' : API.PortMaterialType,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function portMaterialTypeDel(method, id, data = {}) {
  const obj = {
    url: id ? API.PortMaterialTypeDel + id + '/' : API.PortMaterialTypeDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function rackType(method, id, data = {}) {
  const obj = {
    url: id ? API.RackType + id + '/' : API.RackType,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function rackTypeDel(method, id, data = {}) {
  const obj = {
    url: id ? API.RackTypeDel + id + '/' : API.RackTypeDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function sectionTree(method, id, data = {}) {
  const obj = {
    url: id ? API.SectionTree + id + '/' : API.SectionTree,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function roles(method, id, data = {}) {
  const obj = {
    url: id ? API.GroupUrl + id + '/' : API.GroupUrl,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function rolesUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.GroupUrlUpdate + id + '/' : API.GroupUrlUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function rolesDel(method, id, data = {}) {
  const obj = {
    url: id ? API.GroupUrlDel + id + '/' : API.GroupUrlDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function userOperationLog(method, id, data = {}) {
  const obj = {
    url: id ? API.UserOperationLog + id + '/' : API.UserOperationLog,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function orderHistory(method, id, data = {}) {
  const obj = {
    url: id ? API.OrderHistory + id + '/' : API.OrderHistory,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheStation(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheStation + id + '/' : API.CacheStation,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheStationDetail(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheStationDetail + id + '/' : API.CacheStationDetail,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function rcsAgvInfo(method, id, data = {}) {
  const obj = {
    url: id ? API.RcsAgvInfo + id + '/' : API.RcsAgvInfo,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function syncLocations(method, id, data = {}) {
  const obj = {
    url: id ? API.SyncLocations + id + '/' : API.SyncLocations,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function agvCapacityStatistics(method, id, data = {}) {
  const obj = {
    url: id ? API.AgvCapacityStatistics + id + '/' : API.AgvCapacityStatistics,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function agvErrorLog(method, id, data = {}) {
  const obj = {
    url: id ? API.AgvErrorLog + id + '/' : API.AgvErrorLog,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheDeviceErrorLog(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheDeviceErrorLog + id + '/' : API.CacheDeviceErrorLog,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function processSections(method, id, data = {}) {
  const obj = {
    url: id ? API.ProcessSections + id + '/' : API.ProcessSections,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function processSectionsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.ProcessSectionsDel + id + '/' : API.ProcessSectionsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function processSectionsImport(method, id, data = {}) {
  const obj = {
    url: id ? API.ProcessSectionsImport + id + '/' : API.ProcessSectionsImport,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function platformInfoNew(method, id, data = {}) {
  const obj = {
    url: id ? API.PlatformInfoNew + id + '/' : API.PlatformInfoNew,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function platformInfoNewDel(method, id, data = {}) {
  const obj = {
    url: id ? API.PlatformInfoNewDel + id + '/' : API.PlatformInfoNewDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function platformInfoNewUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.PlatformInfoNewUpdate + id + '/' : API.PlatformInfoNewUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function restLocations(method, id, data = {}) {
  const obj = {
    url: id ? API.RestLocations + id + '/' : API.RestLocations,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function restLocationsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.RestLocationsDel + id + '/' : API.RestLocationsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function restLocationsUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.RestLocationsUpdate + id + '/' : API.RestLocationsUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheDeviceInfo(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheDeviceInfo + id + '/' : API.CacheDeviceInfo,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheDeviceInfoDel(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheDeviceInfoDel + id + '/' : API.CacheDeviceInfoDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheDeviceInfoUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheDeviceInfoUpdate + id + '/' : API.CacheDeviceInfoUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function equipLocations(method, id, data = {}) {
  const obj = {
    url: id ? API.EquipLocations + id + '/' : API.EquipLocations,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function realTimeMonitor(method, id, data = {}) {
  const obj = {
    url: id ? API.RealTimeMonitor + id + '/' : API.RealTimeMonitor,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function locationsSyncLocation(method, id, data = {}) {
  const obj = {
    url: id ? API.LocationsSyncLocation + id + '/' : API.LocationsSyncLocation,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function locations(method, id, data = {}) {
  const obj = {
    url: id ? API.Locations + id + '/' : API.Locations,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function locationsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.LocationsDel + id + '/' : API.LocationsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function locationsUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.LocationsUpdate + id + '/' : API.LocationsUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function locationGroups(method, id, data = {}) {
  const obj = {
    url: id ? API.LocationGroups + id + '/' : API.LocationGroups,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function locationGroupsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.LocationGroupsDel + id + '/' : API.LocationGroupsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function productStatic(method, id, data = {}) {
  const obj = {
    url: id ? API.ProductStatic + id + '/' : API.ProductStatic,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}

export function downloadTemplate(params) {
  return request({
    url: API.DownloadTemplate,
    method: 'get',
    params,
    responseType: 'blob'
  })
}
export function platformInfoImport(method, id, data = {}) {
  const obj = {
    url: id ? API.PlatformInfoImport + id + '/' : API.PlatformInfoImport,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
