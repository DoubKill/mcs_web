export default {
  LoginUrl: '/api/v1/user/login/',
  ResetPassword: 'api/v1/user/reset-password/',
  GlobalTypesUrl: '/api/v1/basics/global-types/',
  GlobalTypesUrlBatchDestroy: '/api/v1/basics/global-types/batch-destroy/',
  GlobalCodesUrl: '/api/v1/basics/global-codes/',
  GlobalCodesUrlBatchDestroy: '/api/v1/basics/global-codes/batch-destroy/',
  CommonCode: '/api/v1/basics/common-code/',
  ProductionProcesses: '/api/v1/basics/production-processes/',
  ProductionProcessesDel: '/api/v1/basics/production-processes/batch-destroy/',
  ProductionProcessesUpdate: '/api/v1/basics/production-processes/batch-update/',
  DeviceTypes: '/api/v1/agv/device-types/',
  DeviceTypesDel: '/api/v1/agv/device-types/batch-destroy/',
  ProcessSummary: '/api/v1/agv/equip-lines/process-summary/',
  EquipLines: '/api/v1/agv/equip-lines/',
  EquipLinesDel: '/api/v1/agv/equip-lines/batch-destroy/',
  DeviceTypeSummary: '/api/v1/agv/device-infos/device-type-summary/',
  DeviceInfos: '/api/v1/agv/device-infos/',
  DeviceInfosDel: '/api/v1/agv/device-infos/batch-destroy/',
  MaterialIdentifies: '/api/v1/basics/material-identifies/',
  MaterialIdentifiesBatchDestroy: '/api/v1/basics/material-identifies/batch-destroy/',
  AlarmDefinitions: '/api/v1/basics/alarm-definitions/',
  AlarmDefinitionsDel: '/api/v1/basics/alarm-definitions/batch-destroy/',
  BatchReset: '/api/v1/basics/alarm-definitions/batch-reset/',
  LineInfos: '/api/v1/agv/device-infos/line-infos/',
  SetLines: '/api/v1/agv/device-infos/set-lines/',
  ShelvesInfos: '/api/v1/agv/shelves-infos/',
  ShelvesInfosImportXlsx: '/api/v1/agv/shelves-infos/import-xlsx/',
  RestArea: '/api/v1/agv/rest-areas/',
  RestAreaImportXlsx: '/api/v1/agv/rest-areas/import-xlsx/',
  BatchUpdate: '/api/v1/agv/rest-areas/batch-update/',
  DeviceInfoSettings: '/api/v1/agv/device-info-settings/',
  DeviceInfoSettingsBatchUpdate: '/api/v1/agv/device-info-settings/batch-update/',
  DistrictInfos: '/api/v1/basics/district-infos/',
  DistrictInfosDel: '/api/v1/basics/district-infos/batch-destroy/',
  VehicleInfos: '/api/v1/basics/vehicle-infos/',
  VehicleInfosBatchDestroy: '/api/v1/basics/vehicle-infos/batch-destroy/',
  VehicleInfosBatchUpdate: '/api/v1/basics/vehicle-infos/batch-update/',
  ErrorCodes: '/api/v1/basics/error-codes/',
  ErrorCodesDel: '/api/v1/basics/error-codes/batch-destroy/',
  // CacheDeviceConf: '/api/v1/basics/cache-device-conf/',
  // CacheDeviceConfUpdate: '/api/v1/basics/cache-device-conf/batch-update/',
  // CacheDeviceConfDel: '/api/v1/basics/cache-device-conf/batch-destroy/',
  CraftManagements: '/api/v1/agv/craft-managements/',
  CraftManagementsUpdate: '/api/v1/agv/craft-managements/batch-update/',
  CraftManagementsDel: '/api/v1/agv/craft-managements/batch-destroy/',
  ShuntConf: '/api/v1/agv/shunt-conf/',
  ShuntConfUpdate: '/api/v1/agv/shunt-conf/batch-update/',
  ShuntConfDel: '/api/v1/agv/shunt-conf/batch-destroy/',
  ViewPath: '/api/v1/agv/craft-managements/view-path/',

  BasicsEquips: '/api/v1/basics/equips/',
  BasicsEquipsDel: '/api/v1/basics/equips/batch-destroy/',
  BasicsEquipsUpdate: '/api/v1/basics/equips/batch-update/',
  CacheLocations: '/api/v1/basics/cache-locations/',
  CacheLocationsDel: '/api/v1/basics/cache-locations/batch-destroy/',
  CacheLocationsUpdate: '/api/v1/basics/cache-locations/batch-update/',
  ReceiveAlarm: '/api/v1/basics/receive-alarm/',
  ReceiveAlarmDel: '/api/v1/basics/receive-alarm/batch-destroy/',
  ReceiveAlarmUpdate: '/api/v1/basics/receive-alarm/batch-update/',
  CacheLocationsGroup: '/api/v1/basics/cache-locations-group/',
  CacheLocationsGroupDel: '/api/v1/basics/cache-locations-group/batch-destroy/',
  CacheLocationsGroupUpdate: '/api/v1/basics/cache-locations-group/batch-update/',
  ProcessesChangeSequence: '/api/v1/basics/production-processes/change-sequence/',
  CacheDeviceConf: '/api/v1/agv/cache-device-conf/',
  CacheDeviceConfUpdate: '/api/v1/agv/cache-device-conf/batch-update/',
  CacheDeviceConfDel: '/api/v1/agv/cache-device-conf/batch-destroy/',
  PlatformInfo: '/api/v1/basics/platform-info/',
  PlatformInfoUpdate: '/api/v1/basics/platform-info/batch-update/',
  PlatformInfoDel: '/api/v1/basics/platform-info/batch-destroy/',
  AgvTasks: '/api/v1/agv/agv-tasks/',
  CacheStationTasks: '/api/v1/agv/cache-station-tasks/',
  EquipParts: '/api/v1/basics/equip-parts/',
  EquipPartsUpdate: '/api/v1/basics/equip-parts/batch-update/',
  EquipPartsDel: '/api/v1/basics/equip-parts/batch-destroy/',
  StockInfo: '/api/v1/agv/stock-info/',
  StockInfoDel: '/api/v1/agv/stock-info/batch-destroy/',
  StockInfoUnderway: '/api/v1/agv/stock-info/underway/',
  TaskMonitor: '/api/v1/monitor/task-monitor/',
  StockMonitor: '/api/v1/monitor/inventory-in-process/',
  AbnormalMonitor: '/api/v1/monitor/error-warning/',
  StrategyGroups: '/api/v1/basics/strategy-groups/',
  StrategyGroupsDel: '/api/v1/basics/strategy-groups/batch-destroy/',
  BasketTransport: '/api/v1/monitor/basket-transport/',
  AgvMonitor: '/api/v1/monitor/agv/',
  AgvDetailMonitor: '/api/v1/monitor/agv-detail/',
  CacheLocation: '/api/v1/monitor/cache-location/',
  CacheLocationDetail: '/api/v1/monitor/cache-location-detail/',
  MonitorPlatform: '/api/v1/monitor/platform/',
  MonitorPlatformDetail: '/api/v1/monitor/platform-detail/',
  MonitorAgvTask: '/api/v1/monitor/agv-task/',
  PersonnelsUrl: '/api/v1/user/personnels/',
  PersonnelsUrlUpdate: '/api/v1/user/personnels/batch-update/',
  PersonnelsUrlDel: '/api/v1/user/personnels/batch-destroy/',
  SectionTree: '/api/v1/user/department/',
  GroupUrl: '/api/v1/user/group_extension/',
  GroupUrlUpdate: '/api/v1/user/group_extension/batch-update/',
  GroupUrlDel: '/api/v1/user/group_extension/batch-destroy/',
  PermissionUrl: '/api/v1/user/group-permissions/',
  UserOperationLog: '/api/v1/user/user-operation-log/',
  UserImport: '/api/v1/user/personnels/import_xlsx/',
  DelUser: '/api/v1/user/personnels/del-user/',
  PortMaterialType: '/api/v1/basics/port-material-type/',
  PortMaterialTypeDel: '/api/v1/basics/port-material-type/batch-destroy/',
  RackType: '/api/v1/basics/rack-type/',
  RackTypeDel: '/api/v1/basics/rack-type/batch-destroy/',
  RackInfo: '/api/v1/basics/rack-info/',
  RackInfoDel: '/api/v1/basics/rack-info/batch-destroy/',
  ProcessRoute: '/api/v1/basics/process-route/',
  OrderHistory: '/api/v1/monitor/order-history/',
  CacheStation: '/api/v1/monitor/cache-station/',
  CacheStationDetail: '/api/v1/monitor/cache-station-detail/',
  RcsAgvInfo: '/api/v1/basics/rcs-agv-info/',
  SyncLocations: '/api/v1/basics/cache-locations/sync-locations/',
  TaskCapacityAnalysis: '/api/v1/agv/task-capacity-analysis/',
  AgvCapacityStatistics: '/api/v1/agv/agv-capacity-statistics/',
  AgvErrorLog: '/api/v1/agv/agv-error-log/',
  CacheDeviceErrorLog: '/api/v1/agv/cache-device-error-log/',
  DataBoard: '/api/v1/agv/data-board/',
  ProcessSections: '/api/v1/basics/process-sections/',
  ProcessSectionsDel: '/api/v1/basics/process-sections/batch-destroy/',
  ProcessSectionsImport: '/api/v1/basics/process-sections/import_xlsx/',
  PlatformInfoNew: '/api/v1/basics/platform-info/',
  PlatformInfoNewDel: 'api/v1/basics/platform-info/batch-destroy/',
  PlatformInfoNewUpdate: '/api/v1/basics/platform-info/batch-update/',
  RoutingSchema: '/api/v1/basics/routing-schema/',
  RestLocations: '/api/v1/basics/rest-locations/',
  RestLocationsDel: '/api/v1/basics/rest-locations/batch-destroy/',
  RestLocationsUpdate: '/api/v1/basics/rest-locations/batch-update/',
  CacheDeviceInfo: '/api/v1/basics/cache-device-info/',
  CacheDeviceInfoDel: '/api/v1/basics/cache-device-info/batch-destroy/',
  CacheDeviceInfoUpdate: '/api/v1/basics/cache-device-info/batch-update/',
  PlatformGroup: '/api/v1/basics/platform-group/',
  EmptyRoutingSchema: '/api/v1/basics/empty-routing-schema/',
  EquipLocations: '/api/v1/basics/equip-locations/',
  EquipStatus: '/api/v1/monitor/equip-status/',

  WorkAreas: '/api/v1/basics/work-areas/',
  WorkAreasDel: '/api/v1/basics/work-areas/batch-destroy/',
  GlobalSettings: '/api/v1/basics/global-settings/',
  ProcessCyclicGraph: '/api/v1/basics/process-sections/process-cyclic-graph/',
  RealTimeMonitor: '/api/v1/monitor/real-time-monitor/',
  Locations: '/api/v1/basics/locations/',
  LocationsDel: '/api/v1/basics/locations/batch-destroy/',
  LocationsUpdate: '/api/v1/basics/locations/batch-update/',
  LocationGroups: '/api/v1/basics/location-groups/',
  LocationGroupsDel: '/api/v1/basics/location-groups/batch-destroy/',
  CurrentRoute: '/api/v1/basics/routing-schema/current-route/',
  InProcessMonitor: '/api/v1/monitor/in-process-monitor/',
  ProductStatic: '/api/v1/agv/product-static/',
  DownloadTemplate: '/api/v1/basics/platform-info/download-template/',
  PlatformInfoImport: '/api/v1/basics/platform-info/import-xlsx/',
  AgvPackage: '/api/v1/monitor/agv-package/',
  LocationsSyncLocation: '/api/v1/basics/locations/sync-location/',

  ThresholdDisplay: '/api/v1/basics/threshold-display/',
  AgvInProcess: '/api/v1/monitor/agv-in-process/',
  InProcessTrend: '/api/v1/monitor/in-process-trend/',
  MonitorAlarm: '/api/v1/monitor/alarm/',
  QtimeReport: '/api/v1/monitor/qtime-report/',
  StationTaskTrack: '/api/v1/agv/station-task-track/',
  TaskDurationReport: '/api/v1/monitor/task-duration-report/',
  CheckConf: '/api/v1/basics/check-conf/',

  EnvIndicators: '/api/v1/agv/env-indicators/',
  EnvCheckLocations: '/api/v1/agv/env-check-locations/',
  EnvCheckLocationsDel: '/api/v1/agv/env-check-locations/batch-destroy/',
  IssudTask: '/api/v1/agv/env-check-tasks/issue-task/',
  EnvCheckTasks: '/api/v1/agv/env-check-tasks/',
  EnvCheckTasksDel: '/api/v1/agv/env-check-tasks/batch-destroy/',
  EnvLocationCheckHistory: '/api/v1/agv/env-location-check-history/'
}