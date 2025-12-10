<template>
  <view class="register-container" :style="{ paddingTop: statusBarHeight + 'px' }">
    <!-- Logo区域 -->
    <view class="logo-section">
      <view class="logo-circle">
        <text class="logo-icon">✨</text>
      </view>
      <text class="title">创建账户</text>
      <text class="subtitle">填写信息完成注册</text>
    </view>

    <!-- 成功提示 -->
    <view class="success-message" v-if="showSuccess">注册成功！</view>

    <!-- 注册表单 -->
    <scroll-view class="form-scroll" scroll-y>
      <view class="form-container">
        <view class="form-group" :class="{ error: errors.nickname }">
          <text class="label">昵称</text>
          <view class="input-wrapper">
            <input 
              type="text" 
              v-model="formData.nickname"
              class="form-input" 
              placeholder="请输入昵称（2-20个字符）"
              @blur="validateNickname"
              @input="clearError('nickname')"
            />
            <text class="input-icon">✏️</text>
          </view>
          <text class="error-message" v-if="errors.nickname">{{ errors.nickname }}</text>
        </view>

        <view class="form-group" :class="{ error: errors.password }">
          <text class="label">密码</text>
          <view class="input-wrapper">
            <input 
              :type="showPassword ? 'text' : 'password'"
              v-model="formData.password"
              class="form-input" 
              placeholder="请输入密码（至少6位）"
              @blur="validatePassword"
              @input="onPasswordInput"
            />
            <text class="toggle-password" @click="togglePassword('password')">
              {{ showPassword ? '🙈' : '👁️' }}
            </text>
          </view>
          <view class="password-strength" v-if="formData.password.length > 0">
            <view class="strength-bar">
              <view class="strength-fill" :class="passwordStrengthClass"></view>
            </view>
            <text class="strength-text">密码强度：{{ passwordStrengthText }}</text>
          </view>
          <text class="error-message" v-if="errors.password">{{ errors.password }}</text>
        </view>

        <view class="form-group" :class="{ error: errors.confirmPassword }">
          <text class="label">确认密码</text>
          <view class="input-wrapper">
            <input 
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="formData.confirmPassword"
              class="form-input" 
              placeholder="请再次输入密码"
              @blur="validateConfirmPassword"
              @input="clearError('confirmPassword')"
            />
            <text class="toggle-password" @click="togglePassword('confirmPassword')">
              {{ showConfirmPassword ? '🙈' : '👁️' }}
            </text>
          </view>
          <text class="error-message" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</text>
        </view>

        <view class="form-group" :class="{ error: errors.gender }">
          <text class="label">性别</text>
          <view class="gender-group">
            <view 
              class="gender-option" 
              :class="{ active: formData.gender === 'male' }"
              @click="selectGender('male')"
            >
              <text class="gender-icon">{{ formData.gender === 'male' ? '🔘' : '⚪' }}</text>
              <text>男</text>
            </view>
            <view 
              class="gender-option" 
              :class="{ active: formData.gender === 'female' }"
              @click="selectGender('female')"
            >
              <text class="gender-icon">{{ formData.gender === 'female' ? '🔘' : '⚪' }}</text>
              <text>女</text>
            </view>
          </view>
          <text class="error-message" v-if="errors.gender">{{ errors.gender }}</text>
        </view>

        <view class="form-group" :class="{ error: errors.age }">
          <text class="label">年龄</text>
          <input 
            type="number" 
            v-model="formData.age"
            class="form-input age-input" 
            placeholder="请输入年龄（18-100岁）"
            @blur="validateAge"
            @input="clearError('age')"
          />
          <text class="error-message" v-if="errors.age">{{ errors.age }}</text>
        </view>

        <button 
          class="register-button" 
          :disabled="loading"
          @click="handleRegister"
        >
          <text v-if="loading" class="button-loading">注册中...</text>
          <text v-else>立即注册</text>
        </button>
      </view>
    </scroll-view>

    <!-- 跳转到登录页面 -->
    <view class="login-link">
      <text>已有账户？</text>
      <text class="link" @click="goToLogin">立即登录</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      statusBarHeight: 0, // 状态栏高度
      capsuleHeight: 0,   // 胶囊高度
      topPadding: 0,      // 页面顶部预留边距
      formData: {
        nickname: '',
        password: '',
        confirmPassword: '',
        gender: '',
        age: ''
      },
      showPassword: false,
      showConfirmPassword: false,
      loading: false,
      showSuccess: false,
      errors: {
        nickname: '',
        password: '',
        confirmPassword: '',
        gender: '',
        age: ''
      }
    };
  },
  // 合并重复的 onLoad 生命周期（原代码有两个 onLoad，导致冲突）
  onLoad() {
    this.calculateSafeArea();
    this.setStatusBar();
  },
  onShow() {
    this.setStatusBar();
  },
  computed: {
    passwordStrength() {
      const password = this.formData.password
      if (password.length === 0) return 0
      
      let strength = 0
      if (password.length >= 6) strength++
      if (password.length >= 10) strength++
      if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++
      if (/\d/.test(password)) strength++
      if (/[^a-zA-Z0-9]/.test(password)) strength++
      
      return strength
    },
    passwordStrengthClass() {
      const strength = this.passwordStrength
      if (strength <= 2) return 'weak'
      if (strength <= 3) return 'medium'
      return 'strong'
    },
    passwordStrengthText() {
      const strength = this.passwordStrength
      if (strength <= 2) return '弱'
      if (strength <= 3) return '中'
      return '强'
    }
  },
  methods: {
    // 新增：清除单个字段错误提示（原代码缺失，补充后表单输入时能正确清除错误）
    clearError(field) {
      this.errors[field] = '';
    },

    // 切换密码显示/隐藏
    togglePassword(type) {
      if (type === 'password') {
        this.showPassword = !this.showPassword
      } else {
        this.showConfirmPassword = !this.showConfirmPassword
      }
    },
    
    // 选择性别
    selectGender(gender) {
      this.formData.gender = gender
      this.clearError('gender')
    },
    
    // 密码输入
    onPasswordInput() {
      this.clearError('password')
      // 如果确认密码已输入，重新验证
      if (this.formData.confirmPassword) {
        this.validateConfirmPassword()
      }
    },
    
    // 验证昵称
    validateNickname() {
      const nickname = this.formData.nickname.trim()
      if (!nickname) {
        this.errors.nickname = '请输入昵称'
        return false
      }
      if (nickname.length < 2 || nickname.length > 20) {
        this.errors.nickname = '昵称长度应为2-20个字符'
        return false
      }
      this.errors.nickname = ''
      return true
    },
    
    // 验证密码
    validatePassword() {
      const password = this.formData.password
      if (!password) {
        this.errors.password = '请输入密码'
        return false
      }
      if (password.length < 6) {
        this.errors.password = '密码长度至少6位'
        return false
      }
      this.errors.password = ''
      return true
    },
    
    // 验证确认密码
    validateConfirmPassword() {
      const password = this.formData.password
      const confirmPassword = this.formData.confirmPassword
      if (!confirmPassword) {
        this.errors.confirmPassword = '请再次输入密码'
        return false
      }
      if (password !== confirmPassword) {
        this.errors.confirmPassword = '两次输入的密码不一致'
        return false
      }
      this.errors.confirmPassword = ''
      return true
    },
    
    // 验证年龄
    validateAge() {
      const age = parseInt(this.formData.age)
      if (!this.formData.age) {
        this.errors.age = '请输入年龄'
        return false
      }
      if (isNaN(age) || age < 18 || age > 100) {
        this.errors.age = '年龄应在18-100岁之间'
        return false
      }
      this.errors.age = ''
      return true
    },

    // 计算顶部安全区域（兼容多端）
    calculateSafeArea() {
      try {
        const systemInfo = uni.getSystemInfoSync();
        // 兼容 uni 多端，改用 uni 内置方法获取胶囊信息
        const menuButtonInfo = uni.getMenuButtonBoundingClientRect ? uni.getMenuButtonBoundingClientRect() : {};

        // 状态栏高度
        const statusBarHeight = systemInfo.statusBarHeight || 0;

        // 胶囊高度和顶部间距（异常时用默认值）
        const capsuleHeight = menuButtonInfo.height || 32;
        const capsuleTop = menuButtonInfo.top || statusBarHeight;

        // 计算顶部预留边距
        const topPadding = capsuleTop + capsuleHeight + 8; // 额外预留 8px 间距

        // 设置数据
        this.statusBarHeight = statusBarHeight;
        this.capsuleHeight = capsuleHeight;
        this.topPadding = topPadding;
      } catch (e) {
        console.error('获取胶囊信息失败', e);
        // 异常时设置默认值，避免页面错乱
        this.statusBarHeight = 20;
        this.topPadding = 60;
      }
    },

    // 修复：完整定义 setStatusBar 方法（原代码缺失方法包裹和 info 定义）
    setStatusBar() {
      try {
        const info = uni.getSystemInfoSync(); // 正确定义 info 变量
        this.statusBarHeight = info.statusBarHeight || 0;
      } catch (e) {
        console.error('获取状态栏高度失败', e);
        this.statusBarHeight = 20; // 异常时默认值
      }
    },
    
    // 表单验证
    validateForm() {
      const nicknameValid = this.validateNickname()
      const passwordValid = this.validatePassword()
      const confirmPasswordValid = this.validateConfirmPassword()
      const ageValid = this.validateAge()
      
      if (!this.formData.gender) {
        this.errors.gender = '请选择性别'
      } else {
        this.errors.gender = ''
      }
      
      return nicknameValid && passwordValid && 
             confirmPasswordValid && ageValid && 
             this.formData.gender
    },
    
    // 处理注册
    handleRegister() {
      if (!this.validateForm()) {
        return;
      }

      this.loading = true;

      // 模拟注册请求
      setTimeout(() => {
        this.loading = false;
        this.showSuccess = true;

        // 模拟跳转到 discover 页面（switchTab 用于 tabBar 页面）
        uni.switchTab({
          url: '/pages/discover/discover',
          fail: (err) => {
            // 若 discover 不是 tabBar 页面，改用 navigateTo
            uni.navigateTo({ url: '/pages/discover/discover' });
            console.warn('switchTab 失败，已改用 navigateTo', err);
          }
        });
      }, 1500);
    },
    
    // 跳转到登录页面
    goToLogin() {
      uni.navigateBack({
        delta: 1, // 返回上一页，若登录页是上级页面
        fail: () => {
          // 若返回失败，直接跳转登录页（避免页面栈异常）
          uni.navigateTo({ url: '/pages/login/login' });
        }
      });
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40rpx 30rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

/* Logo区域 */
.logo-section {
  text-align: center;
  margin-bottom: 50rpx;
}

.logo-circle {
  width: 160rpx;
  height: 160rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  margin: 0 auto 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 16rpx 40rpx rgba(102, 126, 234, 0.4);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.logo-icon {
  font-size: 80rpx;
}

.title {
  display: block;
  color: #333;
  font-size: 56rpx;
  font-weight: 600;
  margin-bottom: 16rpx;
}

.subtitle {
  display: block;
  color: #999;
  font-size: 28rpx;
}

/* 滚动容器 */
.form-scroll {
  width: 100%;
  max-width: 800rpx;
  max-height: calc(100vh - 400rpx);
  flex: 1;
}

/* 表单容器 */
.form-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 48rpx;
  padding: 60rpx 40rpx;
  box-shadow: 0 40rpx 120rpx rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(60rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 表单样式 */
.form-group {
  margin-bottom: 36rpx;
  position: relative;
}

.form-group.error .form-input,
.form-group.error .age-input {
  border-color: #ff4757;
}

.label {
  display: block;
  color: #555;
  font-size: 28rpx;
  font-weight: 500;
  margin-bottom: 16rpx;
}

.input-wrapper {
  position: relative;
}

.form-input,
.age-input {
  width: 100%;
  padding: 28rpx 90rpx 28rpx 30rpx;
  border: 4rpx solid #e0e0e0;
  border-radius: 24rpx;
  font-size: 32rpx;
  transition: all 0.3s ease;
  background: #f8f9fa;
  color: #333;
  box-sizing: border-box;
}

.form-input:focus,
.age-input:focus {
  border-color: #667eea;
  background: #fff;
  box-shadow: 0 0 0 8rpx rgba(102, 126, 234, 0.1);
}

.input-icon {
  position: absolute;
  right: 30rpx;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 36rpx;
}

.toggle-password {
  position: absolute;
  right: 30rpx;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 36rpx;
  padding: 10rpx;
  z-index: 10;
}

/* 密码强度 */
.password-strength {
  margin-top: 16rpx;
}

.strength-bar {
  height: 8rpx;
  background: #e0e0e0;
  border-radius: 4rpx;
  overflow: hidden;
  margin-bottom: 10rpx;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 4rpx;
}

.strength-fill.weak {
  width: 33%;
  background: #ff4757;
}

.strength-fill.medium {
  width: 66%;
  background: #ffa502;
}

.strength-fill.strong {
  width: 100%;
  background: #2ed573;
}

.strength-text {
  font-size: 24rpx;
  color: #999;
}

/* 性别选择 */
.gender-group {
  display: flex;
  gap: 24rpx;
  margin-top: 16rpx;
}

.gender-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28rpx 40rpx;
  border: 4rpx solid #e0e0e0;
  border-radius: 24rpx;
  background: #f8f9fa;
  font-size: 30rpx;
  color: #666;
  font-weight: 500;
  transition: all 0.3s ease;
}

.gender-option.active {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  color: #667eea;
  box-shadow: 0 0 0 8rpx rgba(102, 126, 234, 0.1);
}

.gender-icon {
  margin-right: 16rpx;
  font-size: 36rpx;
}

.link {
  color: #667eea;
  text-decoration: underline;
}

.error-message {
  display: block;
  color: #ff4757;
  font-size: 26rpx;
  margin-top: 10rpx;
  animation: shake 0.3s;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10rpx); }
  75% { transform: translateX(10rpx); }
}

/* 注册按钮 */
.register-button {
  width: 100%;
  padding: 32rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 24rpx;
  font-size: 32rpx;
  font-weight: 600;
  box-shadow: 0 8rpx 30rpx rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.register-button:active {
  transform: translateY(2rpx);
  box-shadow: 0 4rpx 15rpx rgba(102, 126, 234, 0.3);
}

.register-button[disabled] {
  opacity: 0.6;
}

.button-loading {
  display: inline-block;
}

/* 成功提示 */
.success-message {
  background: #2ed573;
  color: white;
  padding: 24rpx;
  border-radius: 16rpx;
  text-align: center;
  margin-bottom: 40rpx;
  animation: slideDown 0.3s;
  width: 100%;
  max-width: 800rpx;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 登录链接 */
.login-link {
  text-align: center;
  margin-top: 30rpx;
  color: rgba(255, 255, 255, 0.9);
  font-size: 28rpx;
}

.login-link .link {
  color: #fff;
  font-weight: 600;
  text-decoration: underline;
  margin-left: 10rpx;
}
</style>