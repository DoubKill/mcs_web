<template>
  <el-select
    v-model="planScheduleId"
    clearable
    filterable
    placeholder="倒班规则"
    @change="selectChanged"
  >
    <el-option
      v-for="planSchedule in planSchedules"
      :key="planSchedule.id"
      :label="planSchedule.work_schedule__schedule_name"
      :value="planSchedule.id"
    />
  </el-select>
</template>

<script>
import { planScheduleUrl } from '@/api/base_w'

export default {
  props: {
    dayTime: {
      type: String
      // required: true
    }
  },
  data() {
    return {
      planScheduleId: null,
      planSchedules: []
    }
  },
  watch: {
    dayTime(val) {
      this.planScheduleId = null
      this.getPlanSchedules()
    }
  },
  created() {
    this.getPlanSchedules()
  },
  methods: {
    async getPlanSchedules() {
      this.planSchedules = []
      if (this.dayTime) {
        try {
          const planSchedulesData = await planScheduleUrl('get', null, {
            params: {
              all: 1,
              day_time: this.dayTime
            }
          })
          this.planSchedules = planSchedulesData.results
          // eslint-disable-next-line no-empty
        } catch (e) { }
      }
    },
    selectChanged() {
      this.$emit('planScheduleSelected', this.planScheduleId)
    }
  }
}
</script>
