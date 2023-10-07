<template>
  <div class="login-container">
    <el-card shadow="always" class="login-form">
      <div class="top">
        <div class="header">
          <img alt="logo" class="logo" src="@/assets/login-icon.png">
          <span class="title">国自光伏MCS系统</span>
        </div>
        <div class="desc">让工作变得更高效、简单</div>
      </div>
      <h3 style="color:#0893ae">账户密码登录</h3>
      <el-form
        ref="loginForm"
        class="login"
        :model="loginForm"
        :rules="loginRules"
        auto-complete="on"
        label-position="left"
      >
        <el-form-item prop="username">
          <el-input
            ref="username"
            v-model="loginForm.username"
            placeholder="Username"
            name="username"
            type="text"
            tabindex="1"
            auto-complete="on"
          >
            <i slot="suffix" class="el-input__icon el-icon-user" />
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="Password"
            name="password"
            tabindex="2"
            auto-complete="on"
            @keyup.enter.native="handleLogin"
          >
            <i slot="suffix" class="el-input__icon el-icon-view" @click="showPwd" />
          </el-input>
          <!-- <span
            class="show-pwd"
            @click="showPwd"
          >
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span> -->
        </el-form-item>
        <div class="isRemember-class">
          <!-- <el-checkbox
            v-decorator="[
              'isRemember',
              {
                valuePropName: 'checked',
                initialValue: true,
              },
            ]"
          >
            记住账号
          </el-checkbox> -->
          <a style="color:#0893ae" @click="showForgetPwdHandler">忘记密码</a>
        </div>

        <div style="text-align:center">
          <el-button
            :loading="loading"
            type="primary"
            style="width:86%;margin-top:20px;"
            @click.native.prevent="handleLogin"
          >登 录</el-button>
        </div>
      </el-form>
    </el-card>

    <div class="bottom-text">
      <div style="font-size:50px;font-weight:600">动达天下 新见未来</div>
      <br>
      <span style="font-size:28px">致力于为人类社会创造智能、健康、安全的生产生活环境。</span>
    </div>
  </div>
</template>

<script>
// import { validUsername } from '@/utils/validate'

export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入用户名'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 3) {
        callback(new Error('密码长度大于3个'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(() => {
            // setCookie('password', this.loginForm.password, 9999)
            this.$router.push({
              path: '/',
              query: {
                // password: this.loginForm.password
              }})
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          return false
        }
      })
    },
    // 忘记密码
    showForgetPwdHandler() {
      const h = this.$createElement
      this.$msgbox({
        title: '忘记密码？',
        message: h('div', {}, [
          h('br'),
          h('p', '请联系管理员重置您的登录密码'),
          h('p', '重置密码不需要原密码')
        ]),
        onOk() {}
      })
    }
  }
}
// function setCookie(cName, value, expiredays) {
//   var exdate = new Date()
//   exdate.setDate(exdate.getDate() + expiredays)
//   document.cookie = cName + '=' + value + ((expiredays == null) ? '' : ';expires=' + exdate.toGMTString())
// }
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  // .login-container .el-input input {
    // color: $cursor;
  // }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 42px;
    width: 85%;
  }
}
</style>

<style lang="scss" scoped>
$bg:rgb(55, 58, 61);
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  background: linear-gradient(70deg,  $bg, #294a6aad);
  overflow: hidden;
  background: url('../../assets/login.png') no-repeat ;
    background-size:cover;
  .el-button{
    line-height: 1.5;
  }
  .login-form {
    text-align: center !important;
    position: absolute;
    height: 430px;
    top: -20px;
    bottom: 0;
    margin: auto;
    margin-left: 60%;
    width: 500px;
    background: #f0f2f5;
    z-index: 1;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color:#000;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
.el-card{
  background: #F0F2F5;
}
.el-card__body{
  padding:0;
}
.el-form-item{
  margin-bottom:22px;
}
.login {
    width: 440px;
    margin: 0 auto;
    @media screen and (max-width: 576px) {
      width: 95%;
    }
    @media screen and (max-width: 320px) {
      .captcha-button {
        font-size: 14px;
      }
    }
  }
  .top {
    padding-top: 5%;
    margin: 0 auto;
    width: 368px;
    text-align: center;
    padding-bottom: 10px;
    .header {
      height: 44px;
      line-height: 44px;
      a {
        text-decoration: none;
      }
      .logo {
        height: 44px;
        vertical-align: top;
        margin-right: 16px;
      }
      .title {
        font-size: 33px;
        color: #000;
        font-family: "Myriad Pro", "Helvetica Neue", Arial, Helvetica,
          sans-serif;
        font-weight: 600;
        position: relative;
        top: 2px;
      }
    }
    .desc {
      font-size: 14px;
      color: rgba(0, 0, 0, 0.45);
      margin-top: 12px;
      margin-bottom: 10px;
    }
  }
  .bottom-text{
    color:white;
    position: absolute;
    width: 100%;
    bottom:6%;
    text-align: center;
  }
  .isRemember-class{
    display: flex;
    justify-content:space-between;
    padding: 0 32px;
  }
}
</style>
