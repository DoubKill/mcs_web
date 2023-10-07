<template>
  <div v-loading="loading" class="card-container">
    <table

      border="1"
      bordercolor="black"
      class="info-table"
    >
      <tbody>
        <tr>
          <td colspan="5" class="title-style"><span v-if="testData.emergency_release_flag" class="xx-style">☆</span>胶料信息卡</td>
        </tr>
        <tr>
          <td colspan="4">{{ testData.product_no }}</td>
          <!-- <td rowspan="14" style="transform:rotate(-90deg); width: 150px; max-width: 150px;">
            <img class="barcode" style="margin-left: -120px">
          </td> -->
          <td rowspan="14" style="width:200px;position:relative">
            <img
              class="barcode"
              style="max-width:540px;position:absolute;top:50%;left:50%;
              transform:translateX(-50%) translateY(-50%) rotate(-90deg)"
            >
          </td>
        </tr>
        <tr>
          <td>工厂日期</td>
          <td>{{ testData.day_time }}</td>
          <td>生产班次</td>
          <td>{{ testData.classes_group }}</td>
        </tr>
        <tr>
          <td>生产机台</td>
          <td>{{ testData.equip_no }}</td>
          <td>生产车次</td>
          <td>{{ testData.actual_trains }}</td>
        </tr>
        <tr>
          <td>收皮重量</td>
          <td>{{ testData.actual_weight }}</td>
          <td>余量</td>
          <td>{{ testData.residual_weight }}</td>
        </tr>
        <tr>
          <td>生产时间</td>
          <td colspan="3">{{ testData.production_factory_date }}</td>
        </tr>
        <tr>
          <td>有效时间</td>
          <td colspan="3">{{ testData.valid_time }}</td>
        </tr>
        <tr>
          <td>收皮员</td>
          <td>{{ testData.operation_user }}</td>
          <td>托盘号</td>
          <td>{{ testData.test ? testData.test.pallet_no : '' }}</td>
        </tr>
        <tr>
          <td colspan="4">质量信息卡</td>
        </tr>
        <tr>
          <td>检测时间</td>
          <td colspan="3">{{ testData.test ? testData.test.test_factory_date : '' }}</td>
        </tr>
        <tr>
          <td>打印时间</td>
          <td colspan="3">{{ testData.print_time }}</td>
        </tr>
        <tr>
          <td>检测员</td>
          <td>{{ testData.test ? testData.test.test_user : '' }}</td>
          <td>检测班次</td>
          <td>{{ testData.test ? testData.test.test_class : '' }}</td>
        </tr>
        <tr>
          <td>检测结果</td>
          <td>{{ testData.test_result }}</td>
          <!-- <td>备注</td>
          <td>{{ testData.test ? testData.test.test_note : '' }}</td> -->
          <td>处理人</td>
          <td>{{ testData.deal_user }}</td>
        </tr>
        <tr>
          <td>处理时间</td>
          <td colspan="3">{{ testData.deal_time }}</td>
        </tr>
        <tr>
          <td>处理意见</td>
          <td colspan="3">{{ testData.deal_suggestion }}</td>
        </tr>
      </tbody>
    </table>
    <table
      border="2"
      bordercolor="black"
    >
      <tr>
        <th style="width:100px">车次</th>
        <th v-for="(value, key) in mtrListHead" :key="key">{{ value }}</th>
        <th style="width:100px">综合判级</th>
      </tr>
      <!-- <tr>
        <th v-for="(subHead, index) in testData.mtr_list.sub_head" :key="index">{{ subHead }}</th>
      </tr> -->
      <tr v-for="(row,i) in mtrListRow" :key="i">
        <td>{{ row.trains }}</td>
        <td v-for="(item, index) in mtrListHead" :key="index">
          <div v-if="row[item]">
            {{ row[item].value }}
            <div v-if="row[item].value > mtrListRow[0][item].value">+</div>
            <div v-if="row[item].value < mtrListRow[1][item].value">-</div>
          </div>
        </td>
        <td>{{ row.status }}</td>
        <!-- <td v-for="(item, index) in testData.mtr_list[row]" :key="index">
          {{ index !== testData.mtr_list[row].length - 1 ? item.value : '' }}
          {{
            index !== testData.mtr_list[row].length - 1 ? item.add_subtract : item.status
          }}

          <div>{{ setGraph(index !== testData.mtr_list[row].length - 1 ? item.result : '') }}</div>
        </td> -->
      </tr>
    </table>
    <img class="barcode" style="max-width:600px">

    <div v-if="testData.test_result&&testData.test_result!=='三等品'" class="seal-style">{{ testData.test_result }}</div>
  </div>
</template>

<script>
import jsbarcode from 'jsbarcode'

export default {

  data() {
    return {
      mtrListHead: [],
      mtrListRow: [],
      loading: true,
      testData: {}
    }
  },
  methods: {
    setGraph(result) {
      if (result === 'pass') {
        return '⚪'
      } else if (result === '不合格') {
        return '∆'
      } else {
        return ''
      }
    },
    setTestData(data) {
      this.testData = data
      jsbarcode(
        '.barcode',
        this.testData.lot_no, {
          displayValue: true
        }
      )

      this.mtrListRow = []
      this.mtrListHead = []
      this.testData.mtr_list.trains.forEach(D => {
        const obj = {
          trains: D.train
        }
        D.content.forEach(d => {
          obj[d.data_point_name] = { ...d }
          obj.status = d.status
        })
        this.mtrListRow.push(obj)
      })
      const obj1 = {
        trains: '上区间'
      }
      const obj2 = {
        trains: '下区间'
      }
      this.testData.mtr_list.table_head.forEach(D => {
        D.point_head.forEach(d => {
          this.mtrListHead.push(d.point)
          obj1[d.point] = {
            value: d.upper_limit
          }
          obj2[d.point] = {
            value: d.lower_limit
          }
        })
      })
      this.mtrListRow.unshift(obj2)
      this.mtrListRow.unshift(obj1)
      this.loading = false
      /** for (const key in this.testData.mtr_list) {
        if (key !== 'table_head' && key !== 'rows' && key !== 'sub_head') {
          this.testData.mtr_list.rows.push(key)
          const dataPointItems = []
          for (const head in this.testData.mtr_list.table_head) {
            this.testData.mtr_list.table_head[head].forEach(subHead => {
              const dataPointItem =
              this.testData.mtr_list[key].find(item => {
                return item.test_indicator_name === head && item.data_point_name === subHead
              })
              dataPointItems.push(dataPointItem || {})
            })
          }
          let max_test_times = 0
          let maxTestTimesItem = null
          for (let i = 0; i < dataPointItems.length; i++) {
            if (dataPointItems[i].max_test_times > max_test_times) {
              max_test_times = dataPointItems[i].max_test_times
              maxTestTimesItem = dataPointItems[i]
            }
          }
          if (maxTestTimesItem) {
            dataPointItems.push(maxTestTimesItem)
          }
          this.testData.mtr_list[key] = dataPointItems
        }
      }
      this.testData.mtr_list.sub_head = []
      for (const key in this.testData.mtr_list.table_head) {
        this.testData.mtr_list.sub_head = this.testData.mtr_list.sub_head.concat(
          this.testData.mtr_list.table_head[key])
      }**/
    }
  }
}
</script>

<style lang="scss">
  .card-container {
    width: 600px;
    margin: 0 auto;
    text-align: center;
    font-size: 14px;
    position: relative;
    table {
      width: 100%;
      border-collapse: collapse
    }

   .info-table {
      td {
        min-width: 100px;
        padding-top: 10px;
        padding-bottom: 10px;
      }
    }
    .seal-style{
      position:absolute;
      top:0;
      right:0;
      border:1px solid rgb(59, 59, 59);
      width:300px;
      height:300px;
      border-radius: 50%;
      font-size:60px;
      line-height: 300px;
    }
    .title-style{
      position: relative;
    }
    .xx-style{
      font-size: 40px;
      position: absolute;
      left: 10px;
      top:-3px;
    }
  }
</style>
