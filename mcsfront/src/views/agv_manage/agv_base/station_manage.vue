<template>
  <div class="sation-style">
    <!-- 站台管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="站台信息">
          <el-input
            v-model="getParams.search"
            size="small"
            clearable
            placeholder="请输入站台编号或名称"
          />
        </el-form-item>
        <el-form-item label="启用标志">
          <el-select
            v-model="getParams.is_used"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{id:true,name:'启用'},{id:false,name:'禁用'}]"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="归属设备">
          <el-select
            v-model="getParams.equip"
            clearable
            size="small"
            placeholder="请选择归属设备"
            @visible-change="visibleChange"
          >
            <el-option
              v-for="item in equip_list"
              :key="item.equip_name"
              :label="item.equip_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="工序">
          <el-select
            v-model="getParams.equip__process"
            clearable
            size="small"
            placeholder="请选择工序"
            @visible-change="visibleChange1"
          >
            <el-option
              v-for="item in process_list"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="站台类型">
          <el-select
            v-model="getParams.platform_type"
            clearable
            size="small"
            placeholder="请选择站台类型"
          >
            <el-option
              v-for="item in type_list"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="进站物料类型">
          <el-select
            v-model="getParams.in_port_material_type"
            filterable
            clearable
            size="small"
            placeholder="请选择"
            @visible-change="visibleChange2"
          >
            <el-option
              v-for="item in material_list"
              :key="item.port_material_type_name"
              :label="item.port_material_type_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="出站物料类型"
        >
          <el-select
            v-model="getParams.out_port_material_type"
            filterable
            clearable
            size="small"
            placeholder="请选择"
            @visible-change="visibleChange2"
          >
            <el-option
              v-for="item in material_list"
              :key="item.port_material_type_name"
              :label="item.port_material_type_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="工艺所处循环"
        >
          <el-select
            v-model="getParams.cycle_location"
            filterable
            clearable
            size="small"
            placeholder="请选择"
            @visible-change="visibleChange3"
          >
            <el-option
              v-for="item in cycle_location_list"
              :key="item.id"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <!-- <el-button type="success" size="small" @click="clearSearch">重置查询条件</el-button> -->
          <el-button
            type="success"
            icon="el-icon-search"
            size="small"
            @click="changeList"
          >搜索</el-button>
        </el-form-item>
        <el-form-item label="">
          <el-checkbox v-model="left_time" @change="getList">仅显示断产剩余时间为0的数据</el-checkbox>
        </el-form-item>
      </el-form>
    </div>
    <div
      v-loading="loading"
      class="center-box"
    >
      <div class="botton-box" style="margin-bottom: 0px">
        <span style="font-weight: 700;color: #606266">选择显示列:</span>
        <el-select
          v-model="headerData"
          collapse-tags
          style="margin-left: 10px;width:300px"
          multiple
          clearable
          size="small"
          placeholder="请选择"
        >
          <el-option
            v-for="item in pickData"
            :key="item.label"
            :label="item.label"
            :value="item.label"
          />
        </el-select>
        <el-button
          v-permission="['platform_info','add']"
          style="margin-left: 10px;"
          type="blue"
          icon="el-icon-plus"
          size="small"
          @click="addFun"
        >新增</el-button>
        <el-button
          v-permission="['platform_info','update']"
          type="danger"
          icon="el-icon-turn-off"
          size="small"
          @click="useFun('禁用',1)"
        >禁用</el-button>
        <el-button
          v-permission="['platform_info','update']"
          type="danger"
          icon="el-icon-open"
          size="small"
          @click="useFun('启用',1)"
        >启用</el-button>
        <el-button
          v-permission="['platform_info','delete']"
          type="danger"
          icon="el-icon-delete"
          size="small"
          @click="deleteFun"
        >删除</el-button>

      </div>
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          type="selection"
          width="40"
        />
        <el-table-column
          v-for="(herder,index) in headerData"
          :key="index"
          :prop="pickData.find(d=>d.label===herder).prop"
          :label="herder"
          min-width="110"
        >
          <template slot-scope="scope">
            <el-link
              v-if="herder==='缓存位组'"
              type="primary"
              @click="editGroup(scope.row,1)"
            >{{ scope.row.cache_groups }}</el-link>
            <el-tag
              v-if="herder==='启用标志'"
              size="mini"
              style="border-radius: 20px"
              effect="dark"
              :type="scope.row.is_used?'success':'info'"
            >{{ scope.row.is_used?'启用':'禁用' }}</el-tag>
            <el-tag
              v-if="herder==='能否混用'"
              size="mini"
              style="border-radius: 20px"
              effect="dark"
              :type="scope.row.is_mixed?'success':'info'"
            >{{ scope.row.is_mixed?'是':'否' }}</el-tag>
            <span v-if="herder!=='缓存位组'&&herder!=='启用标志'&&herder!=='能否混用'">{{ scope.row[pickData.find(d=>d.label===herder).prop] }} </span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="140"
        >
          <template slot-scope="{row}">
            <el-button
              v-permission="['platform_info','change']"
              size="small"
              type="text"
              @click="editShow(row)"
            >修改</el-button>
            <el-button
              v-permission="['platform_info','change']"
              size="small"
              type="text"
              @click="editGroup(row,2)"
            >缓存位组设置</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page
        :old-page="false"
        :total="total"
        :current-page="getParams.page"
        @currentChange="currentChange"
      />
    </el-footer>

    <el-dialog
      :title="(currentObj.id?'编辑':'新建')+'站台信息'"
      :visible.sync="dialogVisible"
      width="1200px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form
        ref="ruleForm"
        :model="currentObj"
        :rules="rules"
        label-width="280px"
        inline
        class="dialog-style"
      >
        <el-form-item
          label="站台编号"
          prop="platform_code"
        >
          <el-input
            v-model="currentObj.platform_code"
            size="small"
            :disabled="currentObj.id?true:false"
          />
        </el-form-item>
        <el-form-item
          label="站台名称"
          prop="platform_name"
        >
          <el-input
            v-model="currentObj.platform_name"
            size="small"
            :disabled="currentObj.id?true:false"
          />
        </el-form-item><br>
        <el-form-item
          label="设备"
          prop="equip"
        >
          <el-select
            v-model="currentObj.equip"
            clearable
            size="small"
            placeholder="请选择设备"
            @change="changeEquipType"
            @visible-change="visibleChange"
          >
            <el-option
              v-for="item in equip_list"
              :key="item.id"
              :label="item.equip_name"
              :value="item.id"
              :disabled="!item.is_used"
            >
              <span style="float: left">{{ item.equip_name }}</span>
              <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px">已禁用</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="站台类型"
          prop="platform_type"
        >
          <el-select
            v-model="currentObj.platform_type"
            clearable
            size="small"
            placeholder="请选择站台类型"
          >
            <el-option
              v-for="item in type_list"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item><br>
        <el-form-item
          label="能否混用"
          prop="is_mixed"
        >
          <el-select
            v-model="currentObj.is_mixed"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{value:true,label:'是'},{value:false,label:'否'}]"
              :key="item.label"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="位置点"
          prop="location"
        >
          <el-select
            v-model="currentObj.location"
            filterable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in cache_list"
              :key="item.location_code"
              :label="item.location_code"
              :value="item.id"
              :disabled="!item.is_used"
            >
              <span style="float: left">{{ item.location_code }}</span>
              <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px">已禁用</span>
            </el-option>
          </el-select>
        </el-form-item><br>
        <el-form-item
          label="进站物料类型"
          prop="in_port_material_type"
        >
          <el-select
            v-model="currentObj.in_port_material_type"
            filterable
            size="small"
            placeholder="请选择"
            @visible-change="visibleChange2"
          >
            <el-option
              v-for="item in material_list"
              :key="item.port_material_type_name"
              :label="item.port_material_type_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="出站物料类型"
          prop="out_port_material_type"
        >
          <el-select
            v-model="currentObj.out_port_material_type"
            filterable
            size="small"
            placeholder="请选择"
            @visible-change="visibleChange2"
          >
            <el-option
              v-for="item in material_list"
              :key="item.port_material_type_name"
              :label="item.port_material_type_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item><br>
        <!-- <el-form-item
          label="进站调度开关"
          prop="in_is_opened"
        >
          <el-select
            v-model="currentObj.in_is_opened"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{value:true,label:'开启'},{value:false,label:'关闭'}]"
              :key="item.label"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="出站调度开关"
          prop="out_is_opened"
        >
          <el-select
            v-model="currentObj.out_is_opened"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{value:true,label:'开启'},{value:false,label:'关闭'}]"
              :key="item.label"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item><br> -->
        <el-form-item
          label="进站台策略组"
          prop="sl_strategy_group"
        >
          <el-select
            v-model="currentObj.sl_strategy_group"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in strateg_list"
              :key="item.id"
              :label="item.strategy_group_name"
              :value="item.id"
            />
          </el-select>
          <el-button type="blue" size="small" @click="showStrategy(currentObj.sl_strategy_group)">决策</el-button>
        </el-form-item>
        <el-form-item
          label="出站台策略组"
          prop="xl_strategy_group"
          class="xl_strategy_group_class"
        >
          <el-select
            v-model="currentObj.xl_strategy_group"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in strateg_list"
              :key="item.id"
              :label="item.strategy_group_name"
              :value="item.id"
            />
          </el-select>
          <el-button type="blue" size="small" @click="showStrategy(currentObj.xl_strategy_group)">决策</el-button>
        </el-form-item><br>
        <!-- <el-form-item
          label="站台上次进料完成时间"
          prop="last_feed_finish_time"
        >
          <el-date-picker
            v-model="currentObj.last_feed_finish_time"
            size="small"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
          />
        </el-form-item> -->
        <el-form-item label="调度站台类型" prop="dispatch_type">
          <el-select
            v-model="currentObj.dispatch_type"
            size="small"
            placeholder="请选择调度站台类型"
          >
            <el-option
              v-for="item in (currentObj.equip_type===1?station_list:station_list1)"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="工艺所处循环"
          prop="cycle_location"
        >
          <el-select
            v-model="currentObj.cycle_location"
            filterable
            size="small"
            placeholder="请选择"
            @visible-change="visibleChange3"
          >
            <el-option
              v-for="item in cycle_location_list"
              :key="item.id"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <br>
        <!-- <el-form-item
          label="站台缓存支撑时间(秒)"
          prop="cache_time"
        >
          <el-input-number
            v-model="currentObj.cache_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
        <el-form-item
          label="站台消耗一车料的时间(秒)"
          prop="production_time"
        >
          <el-input-number
            v-model="currentObj.production_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item><br> -->
        <el-form-item
          label="进站台使用公共缓存断产剩余时间(秒)"
          prop="in_common_cache_left_time"
        >
          <el-input-number
            v-model="currentObj.in_common_cache_left_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
        <el-form-item
          label="出站台使用公共缓存断产剩余时间(秒)"
          prop="out_common_cache_left_time"
        >
          <el-input-number
            v-model="currentObj.out_common_cache_left_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item><br>
        <el-form-item
          label="进站台使用专属缓存断产剩余时间(秒)"
          prop="in_private_cache_left_time"
        >
          <el-input-number
            v-model="currentObj.in_private_cache_left_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
        <el-form-item
          label="出站台使用专属缓存断产剩余时间(秒)"
          prop="out_private_cache_left_time"
        >
          <el-input-number
            v-model="currentObj.out_private_cache_left_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item><br>
        <!-- <el-form-item
          label="出站台预调度断产时间(秒)"
          prop="out_pre_time"
        >
          <el-input-number
            v-model="currentObj.out_pre_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
        <el-form-item
          label="进站台预调度断产时间(秒)"
          prop="in_pre_time"
        >
          <el-input-number
            v-model="currentObj.in_pre_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item><br> -->
        <el-form-item
          label="进站台生成任务断产剩余时间(秒)"
          prop="in_task_time"
        >
          <el-input-number
            v-model="currentObj.in_task_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
        <el-form-item
          label="出站台生成任务断产剩余时间(秒)"
          prop="out_task_time"
        >
          <el-input-number
            v-model="currentObj.out_task_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item><br>
        <el-form-item
          label="变更在途最大距离(米)"
          prop="max_change_distance"
        >
          <el-input-number
            v-model="currentObj.max_change_distance"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
        <el-form-item
          label="直达站台"
          prop="direct_plat_form"
        >
          <el-select
            v-model="currentObj.direct_plat_form"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in platform_list"
              :key="item.platform_name"
              :label="item.platform_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item><br>
        <el-form-item
          label="节拍(秒)"
          prop="pitch_time"
        >
          <el-input-number
            v-model="currentObj.pitch_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
        <el-form-item
          label="站台断产剩余时间(秒)"
          prop="left_time"
        >
          <el-input-number
            v-model="currentObj.left_time"
            style="width:auto"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
        <!-- <el-form-item label="是否启用" prop="is_used">
          <el-radio v-model="currentObj.is_used" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_used" :label="false">否</el-radio>
        </el-form-item> -->

      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button
          type="primary"
          :loading="btnLoading"
          @click="submitFun(true)"
        >确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="'缓存位组'+(currentObj.id?'设定':'')"
      :visible.sync="dialogVisibleGroup"
      width="1200px"
      :before-close="handleCloseGroup"
      class="dialog-style"
    >
      <el-form
        ref="ruleForm"
        :model="currentObj"
        :rules="rules"
        label-width="150px"
        inline
      >
        <el-form-item label="站台编号">
          <el-input
            v-model="currentObj.platform_code"
            size="small"
            disabled
          />
        </el-form-item>
        <el-form-item label="站台名称">
          <el-input
            v-model="currentObj.platform_name"
            size="small"
            disabled
          />
        </el-form-item>
        <!-- <el-form-item label="区域">
          <el-input v-model="currentObj.material_name" size="small" disabled />
        </el-form-item><br> -->
        <el-form-item label="机台专属位组">
          <el-select
            v-model="currentObj.private_group"
            :disabled="type===1?true:false"
            clearable
            size="small"
            placeholder=""
            @change="changeText(currentObj.private_group,1)"
          >
            <el-option
              v-for="item in locations_list1"
              :key="item.id"
              :label="item.location_group_code"
              :value="item.id"
              :disabled="!item.is_used"
            >
              <span style="float: left">{{ item.location_group_code }}</span>
              <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px">已禁用</span>
            </el-option>
          </el-select>
          &nbsp;&nbsp;&nbsp;
          <el-input
            v-model="currentObj.private_group_detail"
            disabled
            size="small"
          />
        </el-form-item><br>
        <el-form-item label="公共缓存位组">
          <el-select
            v-model="currentObj.public_group"
            :disabled="type===1?true:false"
            clearable
            size="small"
            placeholder=""
            @change="changeText(currentObj.public_group,2)"
          >
            <el-option
              v-for="item in locations_list2"
              :key="item.id"
              :label="item.location_group_code"
              :value="item.id"
              :disabled="!item.is_used"
            >
              <span style="float: left">{{ item.location_group_code }}</span>
              <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px">已禁用</span>
            </el-option>
          </el-select>
          &nbsp;&nbsp;&nbsp;
          <el-input
            v-model="currentObj.public_group_detail"
            disabled
            size="small"
          />
        </el-form-item><br>
        <el-form-item label="缓存接力组">
          <el-select
            v-model="currentObj.cache_relay_group"
            :disabled="type===1?true:false"
            clearable
            size="small"
            placeholder=""
            @change="changeText(currentObj.cache_relay_group,3)"
          >
            <el-option
              v-for="item in locations_list3"
              :key="item.id"
              :label="item.location_group_code"
              :value="item.id"
              :disabled="!item.is_used"
            >
              <span style="float: left">{{ item.location_group_code }}</span>
              <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px">已禁用</span>
            </el-option>
          </el-select>
          &nbsp;&nbsp;&nbsp;
          <el-input
            v-model="currentObj.cache_relay_group_detail"
            disabled
            size="small"
          />
        </el-form-item><br>
        <el-form-item label="决策缓存位组">
          <el-select
            v-model="currentObj.decision_relay_group"
            :disabled="type===1?true:false"
            clearable
            size="small"
            placeholder=""
            @change="changeText(currentObj.decision_relay_group,4)"
          >
            <el-option
              v-for="item in locations_list4"
              :key="item.id"
              :label="item.location_group_code"
              :value="item.id"
              :disabled="!item.is_used"
            >
              <span style="float: left">{{ item.location_group_code }}</span>
              <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px">已禁用</span>
            </el-option>
          </el-select>
          &nbsp;&nbsp;&nbsp;
          <el-input
            v-model="currentObj.decision_relay_group_detail"
            disabled
            size="small"
          />
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="handleCloseGroup(false)">取 消</el-button>
        <el-button
          v-if="type===2"
          type="primary"
          :loading="btnLoading"
          @click="submitFun(false)"
        >确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="'策略组'"
      :visible.sync="dialogVisible1"
      width="600px"
      class="dialog-style"
    >
      <el-table
        :data="tableData1"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
      >
        <el-table-column
          label="顺序"
          type="index"
          width="50"
        />
        <el-table-column
          label="搬运策略"
          min-width="30"
          prop="strategy_name"
        />
        <el-table-column
          label="是否模拟运行"
          min-width="20"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.is_debug?'是':'否' }}</span>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible1=false">关 闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script lang="js">
import { getGlobalCodes } from '@/api/basics'
import { basicsEquips, productionProcesses } from '@/api/base_w'
import { platformInfo, platformInfoUpdate, platformInfoDel, portMaterialType, cacheLocationsGroup, cacheLocations, strategyGroups } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'StationManage',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      type: 0,
      material_list: [],
      headerData: [
        '站台编号', '站台名称', '设备名称', '站台类型', '位置点', '断产剩余时间(秒)',
        '节拍(秒)', '进站物料类型', '出站物料类型', '进站台策略组', '出站台策略组', '缓存位组', '启用标志'],
      pickData: [
        { prop: 'platform_code', label: '站台编号' },
        { prop: 'platform_name', label: '站台名称' },
        { prop: 'equip_name', label: '设备名称' },
        { prop: 'platform_type_name', label: '站台类型' },
        { prop: 'is_mixed', label: '能否混用' },
        { prop: 'location_name', label: '位置点' },
        { prop: 'left_time', label: '断产剩余时间(秒)' },
        { prop: 'in_port_material_type_name', label: '进站物料类型' },
        { prop: 'out_port_material_type_name', label: '出站物料类型' },
        { prop: 'sl_strategy_group_name', label: '进站台策略组' },
        { prop: 'xl_strategy_group_name', label: '出站台策略组' },
        { prop: 'dispatch_type_name', label: '调度站台类型' },
        { prop: 'cache_groups', label: '缓存位组' },
        { prop: 'cycle_location_name', label: '工艺所处循环' },
        { prop: 'is_used', label: '启用标志' },
        { prop: 'in_common_cache_left_time', label: '进站公共缓存断产剩余时间(秒)' },
        { prop: 'out_common_cache_left_time', label: '出站公共缓存断产剩余时间(秒)' },
        { prop: 'in_private_cache_left_time', label: '进站专属缓存断产剩余时间(秒)' },
        { prop: 'out_private_cache_left_time', label: '出站专属缓存断产剩余时间(秒)' },
        { prop: 'in_task_time', label: '进站任务断产剩余时间(秒)' },
        { prop: 'out_task_time', label: '出站任务断产剩余时间(秒)' },
        { prop: 'max_change_distance', label: '变更在途最大距离(米)' },
        { prop: 'direct_plat_form_name', label: '直达站台' },
        { prop: 'pitch_time', label: '节拍(秒)' }
      ],
      process_list: [],
      type_list: [{ name: '进料', id: 1 }, { name: '出料', id: 2 }, { name: '进出一体', id: 3 }],
      station_list: [{ name: '工艺站台', id: 1 }],
      station_list1: [{ name: '进堆栈站台', id: 2 }, { name: '出堆栈站台', id: 3 }],
      btnExportLoad: false,
      left_time: false,
      dialogVisible: false,
      dialogVisibleGroup: false,
      rules: {
        platform_code: [
          { required: true, message: '请填写站台编号', trigger: 'blur' }
        ],
        platform_name: [
          { required: true, message: '请填写站台名称', trigger: 'blur' }
        ],
        dispatch_type: [
          { required: true, message: '请选择调度站台类型', trigger: 'change' }
        ],
        equip: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        platform_type: [
          { required: true, message: '请选择站台类型', trigger: 'change' }
        ],
        location: [
          { required: true, message: '请选择位置点', trigger: 'change' }
        ],
        in_port_material_type: [
          { required: true, message: '请选择进站物料类型', trigger: 'change' }
        ],
        out_port_material_type: [
          { required: true, message: '请选择出站物料类型', trigger: 'change' }
        ],
        cycle_location: [
          { required: true, message: '请选择工艺所处循环', trigger: 'change' }
        ],
        // in_is_opened: [
        //   { required: true, message: '请选择进站调度开关', trigger: 'change' }
        // ],
        // out_is_opened: [
        //   { required: true, message: '请选择出站调度开关', trigger: 'change' }
        // ],
        in_common_cache_left_time: [
          { required: true, message: '请填写进站台公共缓存断产剩余时间', trigger: 'change' }
        ],
        in_private_cache_left_time: [
          { required: true, message: '请填写进站台专属缓存断产剩余时间', trigger: 'change' }
        ],
        out_common_cache_left_time: [
          { required: true, message: '请填写出站台公共缓存断产剩余时间', trigger: 'change' }
        ],
        out_private_cache_left_time: [
          { required: true, message: '请填写出站台专属缓存断产剩余时间', trigger: 'change' }
        ],
        out_pre_time: [
          { required: true, message: '请填写出站台预调度断产时间', trigger: 'change' }
        ],
        in_pre_time: [
          { required: true, message: '请填写进站台预调度断产时间', trigger: 'change' }
        ],
        out_task_time: [
          { required: true, message: '请填写出站台生成任务断产剩余时间', trigger: 'change' }
        ],
        in_task_time: [
          { required: true, message: '请填写进站台生成任务断产剩余时间', trigger: 'change' }
        ],
        is_mixed: [
          { required: true, message: '请选择能否混用', trigger: 'change' }
        ]
      },
      locations_list: [],
      locations_list1: [],
      locations_list2: [],
      locations_list3: [],
      locations_list4: [],
      equip_list: [],
      platform_list: [],
      cache_list: [],
      strateg_list: [],
      currentVal: [],
      btnLoading: false,
      loading: true,
      dialogVisible1: false,
      loading1: false,
      tableData1: [],
      cycle_location_list: []
    }
  },
  created() {
    this.getList()
  },
  mounted() {
  },
  methods: {
    changeEquipType() {
      this.$set(this.currentObj, 'equip_type', this.equip_list.find(d => d.id === this.currentObj.equip).equip_type)
      if (this.currentObj.dispatch_type) {
        this.currentObj.dispatch_type = null
      }
    },
    async getType() {
      try {
        // const data = await getGlobalCodes({ all: 1, type_name: '站台类型' })
        const data1 = await cacheLocations('get', null, { params: { all: 1, location_type: 2 }})
        const data2 = await platformInfo('get', null, { params: { all: 1, is_used: true }})
        const data3 = await strategyGroups('get', null, { params: { all: 1, is_used: true }})
        // this.type_list = data || []
        this.cache_list = data1 || []
        this.platform_list = data2 || []
        this.strateg_list = data3 || []
      } catch (e) {
        //
      }
    },
    async getCacheGroup() {
      try {
        const data = await cacheLocationsGroup('get', null, { params: { all: 1 }})
        this.locations_list = data || []
        this.locations_list1 = data.filter(d => d.location_group_type === 1)
        this.locations_list2 = data.filter(d => d.location_group_type === 2)
        this.locations_list3 = data.filter(d => d.location_group_type === 3)
        this.locations_list4 = data.filter(d => d.location_group_type === 4)
      } catch (e) {
        //
      }
    },
    visibleChange1(bool) {
      if (bool) {
        this.getProcessList()
      }
    },
    async getProcessList() {
      try {
        const data = await productionProcesses('get', null, { params: { all: 1, is_used: true }})
        this.process_list = data || []
      } catch (e) {
        //
      }
    },
    visibleChange(bool) {
      if (bool) {
        this.getEquip()
      }
    },
    async getEquip() {
      try {
        const data = await basicsEquips('get', null, { params: { all: 1 }})
        this.equip_list = data
      } catch (e) {
        //
      }
    },
    visibleChange2(bool) {
      if (bool) {
        this.getMaterialList()
      }
    },
    visibleChange3(bool) {
      if (bool) {
        this.getCycleLocationList()
      }
    },
    async getCycleLocationList() {
      try {
        const data = await getGlobalCodes({ type_name: '工艺循环' })
        this.cycle_location_list = data || []
      } catch (e) {
        //
      }
    },
    async getMaterialList() {
      try {
        const data = await portMaterialType('get', null, { params: { all: 1 }})
        this.material_list = data || []
      } catch (e) {
        //
      }
    },
    async getList() {
      try {
        this.getParams.left_time = this.left_time ? 0 : ''
        this.loading = true
        const data = await platformInfo('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async changeText(gruop, val) {
      const data = await cacheLocationsGroup('get', gruop, { params: {}})
      if (val === 1) {
        this.$set(this.currentObj, 'private_group_detail', data.choice_locations)
      } else if (val === 2) {
        this.$set(this.currentObj, 'public_group_detail', data.choice_locations)
      } else if (val === 3) {
        this.$set(this.currentObj, 'cache_relay_group_detail', data.choice_locations)
      } else {
        this.$set(this.currentObj, 'decision_relay_group_detail', data.choice_locations)
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.dialogVisible = true
      this.currentObj = {
        in_is_opened: true,
        out_is_opened: true,
        is_mixed: true,
        left_time: 0,
        cache_time: 0,
        production_time: 0,
        in_common_cache_left_time: 0,
        in_private_cache_left_time: 0,
        out_common_cache_left_time: 0,
        out_private_cache_left_time: 0,
        out_pre_time: 0,
        in_pre_time: 0,
        out_task_time: 0,
        in_task_time: 0,
        pitch_time: 0,
        max_change_distance: 1000
      }
      if (this.$refs.ruleForm) {
        this.$refs.ruleForm.resetFields()
      }
      this.getType()
    },
    editShow(row) {
      this.currentObj = Object.assign({}, row)
      this.dialogVisible = true
      this.getEquip()
      this.getProcessList()
      this.getCacheGroup()
      this.getMaterialList()
      this.getCycleLocationList()
      this.getType()
    },
    editGroup(row, val) {
      this.type = val
      this.currentObj = Object.assign({}, row)
      this.dialogVisibleGroup = true
      this.getCacheGroup()
    },
    clearSearch() {
      this.getParams = { page: 1 }
      this.getList()
    },
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {}
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    handleCloseGroup(done) {
      this.dialogVisibleGroup = false
      this.currentObj = {}
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    deleteFun() {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      this.currentVal.forEach(d => {
        arr.push(d.id)
      })
      this.$confirm('此操作删除不可逆, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('settings/operateTypeSetting', '删除')
        platformInfoDel('post', null, { data: { obj_ids: arr }})
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.changeList()
          }).catch(() => {
          })
      }).catch(() => {
      })
    },
    useFun(val, bool) {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      this.currentVal.forEach(d => {
        if (val === '禁用' && d.is_used) {
          arr.push(d.id)
        } else if (val === '启用' && !d.is_used) {
          arr.push(d.id)
        }
      })
      this.$confirm(`此操作${val}, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('settings/operateTypeSetting', val)
        platformInfoUpdate('post', null, { data: { 'obj_ids': arr }})
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.getList()
          }).catch(() => {
          })
      }).catch(() => {
      })
    },
    submitFun(val) {
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await platformInfo(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            if (val) { this.handleClose(null) } else {
              this.handleCloseGroup(null)
            }
            this.getList()
            this.btnLoading = false
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = platformInfo
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.btnExportLoad = false
        }).catch(e => {
          this.btnExportLoad = false
        })
    },
    showStrategy(id) {
      this.dialogVisible1 = true
      this.getStrategyList(id)
    },
    async getStrategyList(id) {
      try {
        this.tableData1 = []
        this.loading1 = true
        const data = await strategyGroups('get', id, { params: {}})
        this.tableData1 = data.group_strategies || []
        this.loading1 = false
      } catch (e) {
        this.loading1 = false
      }
    }
  }
}
</script>

<style lang="scss">
.sation-style{
  .dialog-style{
  .el-input__inner{
  width: 200px;
}}
.xl_strategy_group_class{
  label{
    width: 223px !important;
  }
}
}

</style>

