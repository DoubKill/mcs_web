<template>
  <div class="TopNavber">
    <hamburger
      :is-active="sidebar.opened"
      class="hamburger-container"
      @toggleClick="toggleSideBar"
    />

    <breadcrumb class="breadcrumb-container" />
    <!-- <el-menu
      :default-active="activeMenu"
      background-color="#3e4553"
      text-color="#fff"
      class="el-menu-demo"
      mode="horizontal"
      active-text-color="#0bbd0b"
      @select="handleSelect"
    >
      <div
        v-for="route in routes"
        :key="route.path"
        style="display:inline-block"
      >
        <app-link
          v-if="hasOneShowingChild(route.children,route)"
          :to="resolvePath(onlyOneChild.path)"
        >
          <el-menu-item
            v-if="route.meta"
            :index="route.meta.title"
          >
            {{ generateTitle(route.meta.title) }}
          </el-menu-item>
        </app-link>
      </div>
    </el-menu> -->

    <div class="right-menu">
      <el-dropdown
        class="avatar-container"
        trigger="click"
      >
        <div class="avatar-wrapper">
          <span>
            <el-button type="text" icon="el-icon-s-custom" style="color:#fff;margin-right:6px" /></span>
          {{ name_MCS }}
          <i class="el-icon-caret-bottom" />
        </div>
        <el-dropdown-menu
          slot="dropdown"
          class="user-dropdown"
        >
          <router-link to="/">
            <el-dropdown-item>
              {{ $t('navbar.dashboard') }}
            </el-dropdown-item>
          </router-link>
          <el-dropdown-item
            divided
            @click.native="changePassword"
          >
            <span style="display:block;">{{ $t('navbar.cipher') }}</span>
          </el-dropdown-item>
          <el-dropdown-item
            divided
            @click.native="logout"
          >
            <span style="display:block;">{{ $t('navbar.logOut') }}</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>

    <!-- <div class="right-menu">
      <el-dropdown
        class="avatar-container"
        trigger="click"
      >
        <div class="avatar-wrapper">
          {{ lang==='zh'?'中文':lang==='en'?'English':'' }}
          <i class="el-icon-caret-bottom" />
        </div>
        <el-dropdown-menu
          slot="dropdown"
          class="i18n-dropdown"
        >
          <el-dropdown-item
            divided
            @click.native="setI18n('zh')"
          >
            <span style="display:block;">中文</span>
          </el-dropdown-item>
          <el-dropdown-item
            divided
            @click.native="setI18n('en')"
          >
            <span style="display:block;">English</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div> -->

    <el-dialog
      title="修改密码"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      append-to-body
    >
      <el-form
        ref="loginForm"
        :model="loginForm"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item prop="old_password" label="原密码">
          <el-input
            v-model="loginForm.old_password"
            placeholder="原密码"
            type="password"
            auto-complete="on"
            style="width:250px"
          />
        </el-form-item>
        <el-form-item
          label="新密码"
          prop="new_password"
        >
          <el-input
            v-model="loginForm.new_password"
            type="password"
            placeholder="新密码"
            style="width:250px"
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item
          label="确认密码"
          prop="checkPass"
          :rules="{required: true, validator: validatePass2, trigger: 'blur'}"
        >
          <el-input
            v-model="loginForm.checkPass"
            style="width:250px"
            placeholder="确认密码"
            type="password"
            autocomplete="off"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitChangePassword">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import path from 'path'
import { mapGetters } from 'vuex'
import Hamburger from '@/components/Hamburger'
import { isExternal } from '@/utils/validate'
// import AppLink from './Sidebar/Link'
import { resetPassword } from '@/api/basics'
import { generateTitle } from '@/utils/i18n'
import { encrypt } from '@/utils'
import Breadcrumb from '@/components/Breadcrumb'
export default {
  components: {
    Hamburger,
    Breadcrumb
    // AppLink
  },
  data() {
    var validatePass = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (this.loginForm.old_password === this.loginForm.new_password) {
        callback(new Error('新密码和原密码相同!'))
      } else if (value && (value.length < 3 || value.length > 16)) {
        callback(new Error('请输入3~16位长度的密码'))
      } else {
        callback()
      }
    }
    var validatePass1 = (rule, value, callback) => {
      var reg = /(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).{8,}/
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (this.loginForm.old_password === this.loginForm.new_password) {
        callback(new Error('新密码和原密码相同!'))
      } else if (value && !reg.test(value)) {
        // callback(new Error('密码必须同时包含大写英文,小写英文,数字,符号,且不少于8位'))
        callback()
      } else {
        callback()
      }
    }
    this.validatePass2 = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请确认密码'))
      } else if (value !== this.loginForm.new_password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      basePath: '',
      dialogVisible: false,
      loginForm: {},
      btnLoading: false,
      rules: {
        old_password: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        new_password: [
          { required: true, validator: validatePass1, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters([
      'sidebar',
      'name_MCS'
    ]),
    routes() {
      return this.$router.options.routes
    },
    activeMenu: {
      get() {
        const route = this.$route
        const { meta, matched } = route
        if (meta.activeMenu) {
          return meta.activeMenu
        }
        return matched[0].meta.title
      },
      set(val) {
        return val
      }
    },
    lang: {
      get() {
        return this.$store.state.app.language
      },
      set(lang) {
        this.$i18n.locale = lang
        this.$store.dispatch('app/setLanguage', lang)
      }
    }
  },
  watch: {
    $route(to, from) {
    },
    lang() {
    }
  },
  created() {
    // var reg = /(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).{8,}/
    // if (getCookie('password') && !reg.test(getCookie('password'))) {
    //   this.$message('密码强度低，请修改密码后再重新登录')
    //   this.dialogVisible = true
    // } else {
    //   this.dialogVisible = false
    // }
  },
  methods: {
    generateTitle,
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/login`)
    },
    changePassword() {
      this.dialogVisible = true
    },
    handleClose(done) {
      // var reg = /(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).{8,}/
      // if (getCookie('password') && !reg.test(getCookie('password'))) {
      //   this.logout()
      // } else {
      this.loginForm = {}
      this.$refs.loginForm.clearValidate()
      this.dialogVisible = false
      if (done) {
        done()
      }
      // }
    },
    submitChangePassword() {
      this.$refs.loginForm.validate(async(valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            const obj = Object.assign({}, this.loginForm)
            obj.checkPass = encrypt(obj.checkPass)
            obj.new_password = encrypt(obj.new_password)
            obj.old_password = encrypt(obj.old_password)
            await resetPassword('post', null, { data: obj })
            this.btnLoading = false
            this.$message.success('修改成功,请重新登录')
            setTimeout(async d => {
              await this.$store.dispatch('user/logout')
              this.$router.push(`/login`)
            }, 2000)
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    handleSelect(val) {
      this.activeMenu = val
    },
    hasOneShowingChild(children = [], parent) {
      if (Object.prototype.hasOwnProperty.call(parent, 'hidden') && parent.hidden) {
        return false
      } else {
        const showingChildren = children.filter(item => {
          if (item.hidden) {
            // 过滤掉hidden 要隐藏的
            return false
          } else {
            return true
          }
        })
        this.onlyOneChild = a(showingChildren, parent)
        return true
      }
    },
    resolvePath(routePath) {
      if (isExternal(routePath)) {
        return routePath
      }
      if (isExternal(this.basePath)) {
        return this.basePath
      }
      return path.resolve(this.basePath, routePath)
    },
    setI18n(val) {
      this.lang = val
    }
  }
}
function a(childrenVal = [], val) {
  let obj

  if (childrenVal.length > 0) {
    let _childrenObj = {}
    _childrenObj = childrenVal.find(D => D.path === val.redirect)

    if (JSON.stringify(_childrenObj) === '{}' || !_childrenObj) {
      obj = a(childrenVal[0].children, childrenVal[0])
      return obj
    } else {
      return _childrenObj
    }
  } else {
    return val
  }
}
// function getCookie(cName) {
//   if (document.cookie.length > 0) {
//     var cStart = document.cookie.indexOf(cName + '=')
//     if (cStart !== -1) {
//       cStart = cStart + cName.length + 1
//       var cEnd = document.cookie.indexOf(';', cStart)
//       if (cEnd === -1) cEnd = document.cookie.length
//       return document.cookie.substring(cStart, cEnd)
//     }
//   }
//   return ''
// }
</script>

<style lang="scss" scoped>
  @import "~@/styles/variables.scss";

.TopNavber {
//   height: 60px;
  overflow: hidden;
  position: relative;
  color:#fff !important;
  background: $menuBg;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  .el-menu.el-menu--horizontal{
      border-bottom: none;
  }
  .el-menu--horizontal .el-menu-item:not(.is-disabled):hover{
    background-color: rgba(0, 0, 0,.2) !important;
  }

  .el-menu-item{
    //  background-color: rgb(48, 65, 86) !important;
     background-color: rgb(62, 69, 83) !important;
  }
  .is-active{
      border-bottom: 3px solid;
  }
  .el-menu-demo{
      display: inline-block;
  }
  .right-menu .avatar-container .avatar-wrapper{
    margin-top: 0 !important;
  }
  .hamburger-container {
    line-height: 42px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background .3s;
    -webkit-tap-highlight-color:transparent;

    &:hover {
      background: rgba(0, 0, 0, .025)
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 42px;
    margin-bottom:4px;
    cursor: pointer;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background .3s;

        &:hover {
          background: rgba(0, 0, 0, .025)
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;
        color:#fff;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 15px;
          font-size: 12px;
        }
      }
    }
  }
  .el-menu-item, .el-submenu__title{
    height: 42px;
    line-height: 42px;
  }
}

.i18n-dropdown{
    .el-dropdown-menu__item--divided{
      border-top: none !important;
      margin-top: 0px;
    }
  }
</style>
