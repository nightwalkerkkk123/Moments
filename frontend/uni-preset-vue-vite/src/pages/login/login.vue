<template>
  <view class="login-container" :style="{ paddingTop: statusBarHeight + 'px' }">
    <!-- Logo区域 -->
    <view class="logo-section">
      <view class="logo-circle">
        <text class="logo-icon">👤</text>
      </view>
      <text class="title">欢迎回来</text>
      <text class="subtitle">请登录您的账户</text>
    </view>

    <!-- 成功提示 -->
    <view class="success-message" v-if="showSuccess">登录成功！</view>

    <!-- 登录表单 -->
    <view class="form-container">
      <view class="form-group" :class="{ error: errors.username }">
        <text class="label">账号</text>
        <view class="input-wrapper">
          <input
            type="text"
            v-model.trim="formData.username"
            class="form-input"
            placeholder="请输入账号"
            placeholder-style="color:#b2b2b2;"
            @blur="validateUsername"
            @input="clearError('username')"
            confirm-type="next"
          />
          <text class="input-icon">👤</text>
        </view>
        <text class="error-message" v-if="errors.username">{{ errors.username }}</text>
      </view>

      <view class="form-group" :class="{ error: errors.password }">
        <text class="label">密码</text>
        <view class="input-wrapper">
          <input
            type="text"
            :password="!showPassword"
            v-model="formData.password"
            class="form-input"
            placeholder="请输入密码"
            placeholder-style="color:#b2b2b2;"
            @blur="validatePassword"
            @input="clearError('password')"
            confirm-type="done"
          />
          <text class="toggle-password" @click="togglePassword">
            {{ showPassword ? '🙈' : '👁️' }}
          </text>
        </view>
        <text class="error-message" v-if="errors.password">{{ errors.password }}</text>
      </view>

      <view class="form-options">
        <label class="remember-me">
          <checkbox :checked="formData.rememberMe" @tap="toggleRememberMe" />
          <text>记住密码</text>
        </label>
        <text class="forgot-password" @click="handleForgotPassword">忘记密码？</text>
      </view>

      <button 
        class="login-button" 
        :disabled="loading"
        @click="handleLogin"
      >
        <text v-if="loading" class="button-loading">登录中...</text>
        <text v-else>登录</text>
      </button>
    </view>

    <!-- 跳转到注册页面 -->
    <view class="register-link">
      <text>还没有账户？</text>
      <text class="link" @click="goToRegister">立即注册</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      statusBarHeight: 0,
      formData: {
        username: '',
        password: '',
        rememberMe: false
      },
      showPassword: false,
      loading: false,
      showSuccess: false,
      errors: {
        username: '',
        password: ''
      }
    }
  },
  onLoad() {
    this.setStatusBar()
    // 页面加载时，可以检查是否有保存的登录信息
    this.loadSavedCredentials()
  },
  onShow() {
    this.setStatusBar()
  },
  methods: {
    // 切换密码显示/隐藏
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    
    // 切换记住密码
    toggleRememberMe() {
      this.formData.rememberMe = !this.formData.rememberMe
    },
    
    // 验证账号
    validateUsername() {
      if (!this.formData.username.trim()) {
        this.errors.username = '请输入账号'
        return false
      }
      if (this.formData.username.trim().length < 3) {
        this.errors.username = '账号长度至少3位'
        return false
      }
      this.errors.username = ''
      return true
    },
    
    // 验证密码
    validatePassword() {
      if (!this.formData.password) {
        this.errors.password = '请输入密码'
        return false
      }
      if (this.formData.password.length < 6) {
        this.errors.password = '密码长度至少6位'
        return false
      }
      this.errors.password = ''
      return true
    },
    
    // 清除错误
    clearError(field) {
      this.errors[field] = ''
    },
    
    // 表单验证
    validateForm() {
      const usernameValid = this.validateUsername()
      const passwordValid = this.validatePassword()
      return usernameValid && passwordValid
    },
    
    // 处理登录
    handleLogin() {
      if (!this.validateForm()) {
        return
      }
      
      this.loading = true
      
      // 模拟登录请求
      setTimeout(() => {
        this.loading = false
        this.showSuccess = true
        
        // 如果选择了记住密码，保存登录信息
        if (this.formData.rememberMe) {
          this.saveCredentials()
        }
        
        // 这里可以添加实际的登录逻辑
        console.log('登录信息:', {
          username: this.formData.username,
          password: this.formData.password,
          rememberMe: this.formData.rememberMe
        })
        
        // 3秒后隐藏成功消息
        setTimeout(() => {
          this.showSuccess = false
          // 可以在这里跳转到首页
          // uni.switchTab({ url: '/pages/index/index' })
        }, 3000)
      }, 1500)
    },
    
    // 保存登录信息
    saveCredentials() {
      try {
        uni.setStorageSync('username', this.formData.username)
        uni.setStorageSync('rememberMe', true)
      } catch (e) {
        console.error('保存登录信息失败', e)
      }
    },
    
    // 加载保存的登录信息
    loadSavedCredentials() {
      try {
        const rememberMe = uni.getStorageSync('rememberMe')
        if (rememberMe) {
          const username = uni.getStorageSync('username')
          if (username) {
            this.formData.username = username
            this.formData.rememberMe = true
          }
        }
      } catch (e) {
        console.error('加载登录信息失败', e)
      }
    },
    
    // 忘记密码
    handleForgotPassword() {
      uni.showToast({
        title: '忘记密码功能待实现',
        icon: 'none'
      })
    },
    
    // 跳转到注册页面
    goToRegister() {
      uni.navigateTo({
        url: '/pages/register/register'
      })
    },
    setStatusBar() {
      try {
        const info = uni.getSystemInfoSync()
        this.statusBarHeight = info.statusBarHeight || 0
      } catch (e) {
        this.statusBarHeight = 0
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: #f6f6f6;
  padding: 60rpx 40rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}

/* Logo区域 */
.logo-section {
  text-align: center;
  margin: 40rpx 0 50rpx;
}

.logo-circle {
  width: 140rpx;
  height: 140rpx;
  background: #07c160;
  border-radius: 50%;
  margin: 0 auto 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12rpx 30rpx rgba(7, 193, 96, 0.25);
}

.logo-icon {
  font-size: 70rpx;
  color: #fff;
}

.title {
  display: block;
  color: #111;
  font-size: 48rpx;
  font-weight: 600;
  margin-bottom: 10rpx;
}

.subtitle {
  display: block;
  color: #808080;
  font-size: 26rpx;
}

/* 表单容器 */
.form-container {
  width: 100%;
  max-width: 820rpx;
  background: #fff;
  border-radius: 20rpx;
  padding: 50rpx 36rpx;
  box-shadow: 0 12rpx 40rpx rgba(0, 0, 0, 0.06);
  box-sizing: border-box;
}

/* 表单样式 */
.form-group {
  margin-bottom: 32rpx;
  position: relative;
}

.form-group.error .form-input {
  border-color: #fa5151;
  background: #fff7f7;
}

.label {
  display: block;
  color: #333;
  font-size: 28rpx;
  font-weight: 500;
  margin-bottom: 12rpx;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  padding: 0 90rpx 0 26rpx;
  border: 2rpx solid #e5e5e5;
  border-radius: 14rpx;
  font-size: 30rpx;
  background: #fafafa;
  color: #111;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #07c160;
  background: #fff;
  box-shadow: 0 0 0 8rpx rgba(7, 193, 96, 0.12);
}

.input-icon {
  position: absolute;
  right: 24rpx;
  top: 50%;
  transform: translateY(-50%);
  color: #b2b2b2;
  font-size: 34rpx;
}

.toggle-password {
  position: absolute;
  right: 24rpx;
  top: 50%;
  transform: translateY(-50%);
  color: #07c160;
  font-size: 34rpx;
  padding: 12rpx;
  z-index: 10;
}

.error-message {
  display: block;
  color: #fa5151;
  font-size: 24rpx;
  margin-top: 8rpx;
}

/* 记住密码和忘记密码 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 40rpx 0;
  font-size: 26rpx;
  color: #555;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.forgot-password {
  color: #07c160;
  font-weight: 500;
}

/* 登录按钮 */
.login-button {
  width: 100%;
  padding: 30rpx;
  background: #07c160;
  color: white;
  border: none;
  border-radius: 16rpx;
  font-size: 32rpx;
  font-weight: 600;
  box-shadow: 0 12rpx 30rpx rgba(7, 193, 96, 0.25);
  transition: opacity 0.2s ease;
}

.login-button:active {
  opacity: 0.86;
}

.login-button[disabled] {
  opacity: 0.6;
}

.button-loading {
  display: inline-block;
}

/* 成功提示 */
.success-message {
  background: #07c160;
  color: white;
  padding: 24rpx;
  border-radius: 14rpx;
  text-align: center;
  margin-bottom: 32rpx;
  width: 100%;
  max-width: 820rpx;
  box-shadow: 0 8rpx 24rpx rgba(7, 193, 96, 0.18);
}

/* 注册链接 */
.register-link {
  text-align: center;
  margin-top: 28rpx;
  color: #808080;
  font-size: 26rpx;
}

.register-link .link {
  color: #07c160;
  font-weight: 600;
  margin-left: 10rpx;
}
</style>
