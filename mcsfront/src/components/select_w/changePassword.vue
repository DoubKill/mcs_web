<template>
  <div>
    <el-dialog
      title="修改密码"
      :visible.sync="dialogTableVisible"
      :before-close="beforeClose"
    >
      <el-form
        ref="ruleForm"
        :model="userForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item
          label="原密码"
          prop="old_password"
        >
          <el-input
            v-model="userForm.old_password"
            type="password"
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item
          label="新密码"
          prop="new_password"
        >
          <el-input
            v-model="userForm.new_password"
            type="password"
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item
          label="确认新密码"
          prop="checkPass"
        >
          <el-input
            v-model="userForm.checkPass"
            type="password"
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="submitForm('ruleForm')"
          >提 交</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { validPassword, validCheckPass } from '@/utils/validate'
import { changePassword } from '@/api/basics'
export default {
  props: {
    tableVisible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      dialogTableVisible: false,
      loading: false,
      userForm: {
        old_password: '',
        new_password: '',
        checkPass: ''
      },
      rules: {
        old_password: [
          { required: true, validator: (rule, value, callback) => { validPassword(rule, value, callback, this) }, trigger: 'blur' }
        ],
        new_password: [
          { required: true, validator: (rule, value, callback) => { validPassword(rule, value, callback, this) }, trigger: 'blur' }
        ],
        checkPass: [
          { required: true, validator: (rule, value, callback) => { validCheckPass(rule, value, callback, this) }, trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    tableVisible(bool) {
      if (bool) {
        this.dialogTableVisible = bool
      }
    }
  },
  methods: {
    async submitForm(formName) {
      // eslint-disable-next-line space-before-function-paren
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          try {
            this.loading = true
            await changePassword('post', { data: this.userForm })
            this.$message.success('密码修改成功')
            this.dialogTableVisible = false
            this.beforeClose()
          } catch (e) {
            this.loading = false
          }
        } else {
          return false
        }
      })
    },
    beforeClose(done) {
      this.loading = false
      this.$refs.ruleForm.resetFields()
      this.$emit('dialogTableVisible')
      done()
    }
  }
}
</script>

<style>

</style>
