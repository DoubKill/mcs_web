import request from '@/utils/request'
import API from '@/api/url'

export function productionProcesses(method, id, data = {}) {
  const obj = {
    url: id ? API.ProductionProcesses + id + '/' : API.ProductionProcesses,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function productionProcessesDel(method, id, data = {}) {
  const obj = { // obj_ids
    url: id ? API.ProductionProcessesDel + id + '/' : API.ProductionProcessesDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function deviceTypes(method, id, data = {}) {
  const obj = {
    url: id ? API.DeviceTypes + id + '/' : API.DeviceTypes,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function deviceTypesDel(method, id, data = {}) {
  const obj = {
    url: id ? API.DeviceTypesDel + id + '/' : API.DeviceTypesDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function processSummary(method, id, data = {}) {
  const obj = {
    url: id ? API.ProcessSummary + id + '/' : API.ProcessSummary,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function equipLines(method, id, data = {}) {
  const obj = {
    url: id ? API.EquipLines + id + '/' : API.EquipLines,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function equipLinesDel(method, id, data = {}) {
  const obj = {
    url: id ? API.EquipLinesDel + id + '/' : API.EquipLinesDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function deviceTypeSummary(method, id, data = {}) {
  const obj = {
    url: id ? API.DeviceTypeSummary + id + '/' : API.DeviceTypeSummary,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function deviceInfos(method, id, data = {}) {
  const obj = {
    url: id ? API.DeviceInfos + id + '/' : API.DeviceInfos,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function deviceInfosDel(method, id, data = {}) {
  const obj = {
    url: id ? API.DeviceInfosDel + id + '/' : API.DeviceInfosDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function alarmDefinitions(method, id, data = {}) {
  const obj = {
    url: id ? API.AlarmDefinitions + id + '/' : API.AlarmDefinitions,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function alarmDefinitionsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.AlarmDefinitionsDel + id + '/' : API.AlarmDefinitionsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function batchReset(method, id, data = {}) {
  const obj = {
    url: id ? API.BatchReset + id + '/' : API.BatchReset,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function lineInfos(method, id, data = {}) {
  const obj = {
    url: id ? API.LineInfos + id + '/' : API.LineInfos,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function setLines(method, id, data = {}) {
  const obj = {
    url: id ? API.SetLines + id + '/' : API.SetLines,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function shelvesInfos(method, id, data = {}) {
  const obj = {
    url: id ? API.ShelvesInfos + id + '/' : API.ShelvesInfos,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function shelvesInfosImportXlsx(method, id, data = {}) {
  const obj = {
    url: id ? API.ShelvesInfosImportXlsx + id + '/' : API.ShelvesInfosImportXlsx,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function restArea(method, id, data = {}) {
  const obj = {
    url: id ? API.RestArea + id + '/' : API.RestArea,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function restAreaImportXlsx(method, id, data = {}) {
  const obj = {
    url: id ? API.RestAreaImportXlsx + id + '/' : API.RestAreaImportXlsx,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function batchUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.BatchUpdate + id + '/' : API.BatchUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function deviceInfoSettings(method, id, data = {}) {
  const obj = {
    url: id ? API.DeviceInfoSettings + id + '/' : API.DeviceInfoSettings,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}

export function deviceInfoSettingsBatchUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.DeviceInfoSettingsBatchUpdate + id + '/' : API.DeviceInfoSettingsBatchUpdate,
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

export function districtInfosDel(method, id, data = {}) {
  const obj = {
    url: id ? API.DistrictInfosDel + id + '/' : API.DistrictInfosDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}

export function errorCodes(method, id, data = {}) {
  const obj = {
    url: id ? API.ErrorCodes + id + '/' : API.ErrorCodes,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}

export function errorCodesDel(method, id, data = {}) {
  const obj = {
    url: id ? API.ErrorCodesDel + id + '/' : API.ErrorCodesDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}

export function cacheDeviceConf(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheDeviceConf + id + '/' : API.CacheDeviceConf,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheDeviceConfUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheDeviceConfUpdate + id + '/' : API.CacheDeviceConfUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheDeviceConfDel(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheDeviceConfDel + id + '/' : API.CacheDeviceConfDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function craftManagements(method, id, data = {}) {
  const obj = {
    url: id ? API.CraftManagements + id + '/' : API.CraftManagements,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function craftManagementsUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.CraftManagementsUpdate + id + '/' : API.CraftManagementsUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function craftManagementsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.CraftManagementsDel + id + '/' : API.CraftManagementsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function basicsEquips(method, id, data = {}) {
  const obj = {
    url: id ? API.BasicsEquips + id + '/' : API.BasicsEquips,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function basicsEquipsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.BasicsEquipsDel + id + '/' : API.BasicsEquipsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function basicsEquipsUpdate(method, id, data = {}) {
  const obj = {
    url: id ? API.BasicsEquipsUpdate + id + '/' : API.BasicsEquipsUpdate,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function agvTasks(method, id, data = {}) {
  const obj = {
    url: id ? API.AgvTasks + id + '/' : API.AgvTasks,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function cacheStationTasks(method, id, data = {}) {
  const obj = {
    url: id ? API.CacheStationTasks + id + '/' : API.CacheStationTasks,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function monitorPlatform(method, id, data = {}) {
  const obj = {
    url: id ? API.MonitorPlatform + id + '/' : API.MonitorPlatform,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function monitorPlatformDetail(method, id, data = {}) {
  const obj = {
    url: id ? API.MonitorPlatformDetail + id + '/' : API.MonitorPlatformDetail,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function monitorAgvTask(method, id, data = {}) {
  const obj = {
    url: id ? API.MonitorAgvTask + id + '/' : API.MonitorAgvTask,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function rackInfo(method, id, data = {}) {
  const obj = {
    url: id ? API.RackInfo + id + '/' : API.RackInfo,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function rackInfoDel(method, id, data = {}) {
  const obj = {
    url: id ? API.RackInfoDel + id + '/' : API.RackInfoDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function strategyGroupsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.StrategyGroupsDel + id + '/' : API.StrategyGroupsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function processRoute(method, id, data = {}) {
  const obj = {
    url: id ? API.ProcessRoute + id + '/' : API.ProcessRoute,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function taskCapacityAnalysis(method, id, data = {}) {
  const obj = {
    url: id ? API.TaskCapacityAnalysis + id + '/' : API.TaskCapacityAnalysis,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function dataBoard(method, id, data = {}) {
  const obj = {
    url: id ? API.DataBoard + id + '/' : API.DataBoard,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function routingSchema(method, id, data = {}) {
  const obj = {
    url: id ? API.RoutingSchema + id + '/' : API.RoutingSchema,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function currentRoute(method, id, data = {}) {
  const obj = {
    url: id ? API.CurrentRoute + id + '/' : API.CurrentRoute,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function platformGroup(method, id, data = {}) {
  const obj = {
    url: id ? API.PlatformGroup + id + '/' : API.PlatformGroup,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function emptyRoutingSchema(method, id, data = {}) {
  const obj = {
    url: id ? API.EmptyRoutingSchema + id + '/' : API.EmptyRoutingSchema,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function equipStatus(method, id, data = {}) {
  const obj = {
    url: id ? API.EquipStatus + id + '/' : API.EquipStatus,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function workAreas(method, id, data = {}) {
  const obj = {
    url: id ? API.WorkAreas + id + '/' : API.WorkAreas,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function workAreasDel(method, id, data = {}) {
  const obj = {
    url: id ? API.WorkAreasDel + id + '/' : API.WorkAreasDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function globalSettings(method, id, data = {}) {
  const obj = {
    url: id ? API.GlobalSettings + id + '/' : API.GlobalSettings,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function processCyclicGraph(method, id, data = {}) {
  const obj = {
    url: id ? API.ProcessCyclicGraph + id + '/' : API.ProcessCyclicGraph,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function inProcessMonitor(method, id, data = {}) {
  const obj = {
    url: id ? API.InProcessMonitor + id + '/' : API.InProcessMonitor,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function agvPackage(method, id, data = {}) {
  const obj = {
    url: id ? API.AgvPackage + id + '/' : API.AgvPackage,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function thresholdDisplay(method, id, data = {}) {
  const obj = {
    url: id ? API.ThresholdDisplay + id + '/' : API.ThresholdDisplay,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function agvInProcess(method, id, data = {}) {
  const obj = {
    url: id ? API.AgvInProcess + id + '/' : API.AgvInProcess,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function inProcessTrend(method, id, data = {}) {
  const obj = {
    url: id ? API.InProcessTrend + id + '/' : API.InProcessTrend,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function monitorAlarm(method, id, data = {}) {
  const obj = {
    url: id ? API.MonitorAlarm + id + '/' : API.MonitorAlarm,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function qtimeReport(method, id, data = {}) {
  const obj = {
    url: id ? API.QtimeReport + id + '/' : API.QtimeReport,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function stationTaskTrack(method, id, data = {}) {
  const obj = {
    url: id ? API.StationTaskTrack + id + '/' : API.StationTaskTrack,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function taskDurationReport(method, id, data = {}) {
  const obj = {
    url: id ? API.TaskDurationReport + id + '/' : API.TaskDurationReport,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function checkConf(method, id, data = {}) {
  const obj = {
    url: id ? API.CheckConf + id + '/' : API.CheckConf,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function envIndicators(method, id, data = {}) {
  const obj = {
    url: id ? API.EnvIndicators + id + '/' : API.EnvIndicators,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function envCheckLocations(method, id, data = {}) {
  const obj = {
    url: id ? API.EnvCheckLocations + id + '/' : API.EnvCheckLocations,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function envCheckLocationsDel(method, id, data = {}) {
  const obj = {
    url: id ? API.EnvCheckLocationsDel + id + '/' : API.EnvCheckLocationsDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function issudTask(method, id, data = {}) {
  const obj = {
    url: id ? API.IssudTask + id + '/' : API.IssudTask,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function envCheckTasks(method, id, data = {}) {
  const obj = {
    url: id ? API.EnvCheckTasks + id + '/' : API.EnvCheckTasks,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function envCheckTasksDel(method, id, data = {}) {
  const obj = {
    url: id ? API.EnvCheckTasksDel + id + '/' : API.EnvCheckTasksDel,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
export function envLocationCheckHistory(method, id, data = {}) {
  const obj = {
    url: id ? API.EnvLocationCheckHistory + id + '/' : API.EnvLocationCheckHistory,
    method: method
  }
  Object.assign(obj, data)
  return request(obj)
}
