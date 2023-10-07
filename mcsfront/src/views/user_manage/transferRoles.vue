<template>
  <div>
    <el-input v-model="text" style="margin-bottom:5px" type="text" placeholder="请输入角色" @input="changeInput" />
    <el-transfer
      v-model="userGroups"
      :render-content="renderFunc"
      :titles="['可用 角色', '选中的 角色']"
      :data="groupList"
      @change="changeTransferGroup"
    />
  </div>
</template>

<script>
export default {
  props: {
    groups: {
      type: Array,
      default: () => {
        return []
      }
    },
    defaultGroups: {
      type: Array,
      default: () => {
        return []
      }
    }
  },
  data() {
    return {
      text: '',
      groupList: this.groups
    }
  },
  computed: {
    userGroups: {
      // eslint-disable-next-line vue/return-in-computed-property
      get() {
        if (this.defaultGroups.length > 0) {
          return this.defaultGroups || []
        }
      },
      set() { }
    }
  },
  watch: {
    groups(arr) {
      this.groupList = arr
    }
  },
  methods: {
    renderFunc(h, option) {
      return <span title={option.name}>{option.name}</span>
    },
    changeTransferGroup(val) {
      this.$emit('changeTransferGroup', val)
    },
    changeInput(val) {
      var restaurants = this.groups
      var results = val ? restaurants.filter(this.createStateFilter(val)) : restaurants
      this.$set(this, 'groupList', results)
    },
    createStateFilter(queryString) {
      return (state) => {
        return (state.name.toLowerCase().indexOf(queryString.toLowerCase()) > -1)
      }
    }
  }
}
</script>

<style>

</style>
