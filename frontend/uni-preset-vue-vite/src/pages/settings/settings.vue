<template>
  <view class="settings-container">
    <!-- 自定义导航栏 -->
    <view class="custom-navbar">
      <view class="navbar-content">
        <text class="navbar-back" @tap="handleBack">返回</text>
        <text class="navbar-title">设置</text>
        <text class="navbar-placeholder"></text>
      </view>
    </view>

    <!-- 加载状态 -->
    <view class="loading-mask" v-if="loading">
      <view class="loading-content">
        <text class="loading-icon">⏳</text>
        <text class="loading-text">加载中...</text>
      </view>
    </view>

    <scroll-view scroll-y class="settings-scroll">
      <view class="settings-section">
        <view class="settings-item" @tap="handleAccountSettings">
          <text class="settings-icon">👤</text>
          <text class="settings-label">账号设置</text>
          <text class="settings-arrow">›</text>
        </view>
      </view>

      <view class="settings-section">
        <view class="settings-item logout" @tap="handleLogout">
          <text class="settings-icon">🚪</text>
          <text class="settings-label">退出登录</text>
        </view>
      </view>
    </scroll-view>

    <!-- 账号设置弹窗 -->
    <view class="account-modal" v-if="showAccountModal" @tap="closeAccountSettings">
      <view class="account-modal-content" @tap.stop>
        <view class="account-modal-header">
          <text class="account-modal-title">账号设置</text>
          <text class="account-modal-close" @tap="closeAccountSettings">×</text>
        </view>

        <view class="account-modal-body">
          <!-- 头像 -->
          <view class="account-section">
            <view class="section-title">头像</view>
            <view class="avatar-row">
              <image class="avatar-preview" :src="accountForm.avatar" mode="aspectFill" />
              <button class="btn-outline" size="mini" @tap="chooseAvatar">更换头像</button>
            </view>
          </view>

          <!-- 昵称 -->
          <view class="account-section">
            <view class="section-title">昵称</view>
            <view class="input-wrapper">
              <input
                class="text-input"
                type="text"
                v-model="accountForm.nickname"
                placeholder="请输入昵称（2-20个字符）"
                maxlength="20"
              />
            </view>
            <button class="btn-primary block" size="default" @tap="saveNickname">保存昵称</button>
          </view>

          <!-- 个性签名 -->
          <view class="account-section">
            <view class="section-title">个性签名</view>
            <view class="input-wrapper">
              <textarea
                class="text-area"
                v-model="accountForm.signature"
                placeholder="写点什么吧（最多60字）"
                maxlength="60"
                :auto-height="true"
                :show-confirm-bar="false"
              />
              <text class="text-counter">{{ accountForm.signature.length }}/60</text>
            </view>
            <button class="btn-primary block" size="default" @tap="saveSignature">保存签名</button>
          </view>

          <!-- 密码 -->
          <view class="account-section">
            <view class="section-title">修改密码</view>
            <view class="input-wrapper">
              <input
                class="text-input"
                type="password"
                v-model="accountForm.oldPassword"
                placeholder="请输入旧密码"
              />
            </view>
            <view class="input-wrapper">
              <input
                class="text-input"
                type="password"
                v-model="accountForm.newPassword"
                placeholder="请输入新密码（至少6位）"
              />
            </view>
            <view class="input-wrapper">
              <input
                class="text-input"
                type="password"
                v-model="accountForm.confirmPassword"
                placeholder="请再次输入新密码"
              />
            </view>
            <button class="btn-primary block" size="default" @tap="savePassword">保存密码</button>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      showAccountModal: false,
      accountForm: {
        avatar: 'https://picsum.photos/200',
        nickname: '小程序用户',
        signature: '记录生活 · 分享精彩',
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      loading: false
    }
  },
  onLoad() {
    this.getUserProfile()
  },
  methods: {
    handleBack() {
      uni.navigateBack()
    },
    async getUserProfile() {
      try {
        this.loading = true
        const response = await uni.request({
          url: '/api/user/profile',
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`
          }
        })
        
        if (response[1].statusCode === 200 && response[1].data.success) {
          const userData = response[1].data.data
          this.accountForm.avatar = userData.avatar
          this.accountForm.nickname = userData.nickname
          this.accountForm.signature = userData.signature
        } else {
          uni.showToast({ title: response[1].data.message || '获取用户信息失败', icon: 'none' })
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        uni.showToast({ title: '获取用户信息失败', icon: 'none' })
      } finally {
        this.loading = false
      }
    },
    handleAccountSettings() {
      this.showAccountModal = true
    },
    closeAccountSettings() {
      this.showAccountModal = false
    },
    chooseAvatar() {
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          const filePath = res.tempFilePaths[0]
          // 将图片转换为base64编码
          uni.getFileSystemManager().readFile({
            filePath: filePath,
            encoding: 'base64',
            success: async (fileData) => {
              try {
                this.loading = true
                const base64Image = `data:image/jpeg;base64,${fileData.data}`
                const response = await uni.request({
                  url: '/api/user/avatar',
                  method: 'POST',
                  data: {
                    avatar: base64Image
                  },
                  header: {
                    'Authorization': `Bearer ${uni.getStorageSync('token')}`,
                    'Content-Type': 'application/json'
                  }
                })
                
                if (response[1].statusCode === 200 && response[1].data.success) {
                  this.accountForm.avatar = response[1].data.data.avatar
                  uni.showToast({ title: '头像已更新', icon: 'success' })
                  this.emitProfileUpdate()
                } else {
                  uni.showToast({ title: response[1].data.message || '头像更新失败', icon: 'none' })
                }
              } catch (error) {
                console.error('头像更新失败:', error)
                uni.showToast({ title: '头像更新失败', icon: 'none' })
              } finally {
                this.loading = false
              }
            },
            fail: () => {
              uni.showToast({ title: '图片处理失败', icon: 'none' })
            }
          })
        },
        fail: () => {
          uni.showToast({ title: '选择失败', icon: 'none' })
        }
      })
    },
    async saveNickname() {
      const name = this.accountForm.nickname.trim()
      if (name.length < 2 || name.length > 20) {
        uni.showToast({ title: '昵称需2-20个字符', icon: 'none' })
        return
      }
      
      try {
        this.loading = true
        const response = await uni.request({
          url: '/api/user/nickname',
          method: 'POST',
          data: {
            nickname: name
          },
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (response[1].statusCode === 200 && response[1].data.success) {
          uni.showToast({ title: '昵称已保存', icon: 'success' })
          this.emitProfileUpdate()
        } else {
          uni.showToast({ title: response[1].data.message || '昵称保存失败', icon: 'none' })
        }
      } catch (error) {
        console.error('昵称保存失败:', error)
        uni.showToast({ title: '昵称保存失败', icon: 'none' })
      } finally {
        this.loading = false
      }
    },
    async saveSignature() {
      const sig = this.accountForm.signature.trim()
      if (sig.length > 60) {
        uni.showToast({ title: '签名不能超过60个字符', icon: 'none' })
        return
      }
      
      try {
        this.loading = true
        const response = await uni.request({
          url: '/api/user/signature',
          method: 'POST',
          data: {
            signature: sig
          },
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (response[1].statusCode === 200 && response[1].data.success) {
          uni.showToast({ title: '签名已保存', icon: 'success' })
          this.emitProfileUpdate()
        } else {
          uni.showToast({ title: response[1].data.message || '签名保存失败', icon: 'none' })
        }
      } catch (error) {
        console.error('签名保存失败:', error)
        uni.showToast({ title: '签名保存失败', icon: 'none' })
      } finally {
        this.loading = false
      }
    },
    async savePassword() {
      const { oldPassword, newPassword, confirmPassword } = this.accountForm
      if (!oldPassword || !newPassword || !confirmPassword) {
        uni.showToast({ title: '请填写完整信息', icon: 'none' })
        return
      }
      if (newPassword.length < 6) {
        uni.showToast({ title: '新密码至少6位', icon: 'none' })
        return
      }
      if (newPassword !== confirmPassword) {
        uni.showToast({ title: '两次输入不一致', icon: 'none' })
        return
      }
      
      try {
        this.loading = true
        const response = await uni.request({
          url: '/api/user/password',
          method: 'POST',
          data: {
            oldPassword,
            newPassword,
            confirmPassword
          },
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (response[1].statusCode === 200 && response[1].data.success) {
          uni.showToast({ title: '密码已更新', icon: 'success' })
          this.accountForm.oldPassword = ''
          this.accountForm.newPassword = ''
          this.accountForm.confirmPassword = ''
        } else {
          uni.showToast({ title: response[1].data.message || '密码修改失败', icon: 'none' })
        }
      } catch (error) {
        console.error('密码修改失败:', error)
        uni.showToast({ title: '密码修改失败', icon: 'none' })
      } finally {
        this.loading = false
      }
    },
    emitProfileUpdate() {
      uni.$emit('profileUpdated', {
        avatar: this.accountForm.avatar,
        nickname: this.accountForm.nickname.trim() || '小程序用户',
        signature: this.accountForm.signature.trim() || '记录生活 · 分享精彩'
      })
    },
    async handleLogout() {
      uni.showModal({
        title: '提示',
        content: '确定要退出登录吗？',
        success: async (res) => {
          if (res.confirm) {
            try {
              this.loading = true
              const response = await uni.request({
                url: '/api/auth/logout',
                method: 'POST',
                header: {
                  'Authorization': `Bearer ${uni.getStorageSync('token')}`
                }
              })
              
              if (response[1].statusCode === 200 && response[1].data.success) {
                // 清除本地存储的token
                uni.removeStorageSync('token')
                uni.showToast({ title: '已退出登录', icon: 'success' })
                // 延迟返回，让用户看到成功提示
                setTimeout(() => {
                  uni.navigateBack()
                }, 1500)
              } else {
                uni.showToast({ title: response[1].data.message || '退出登录失败', icon: 'none' })
              }
            } catch (error) {
              console.error('退出登录失败:', error)
              uni.showToast({ title: '退出登录失败', icon: 'none' })
            } finally {
              this.loading = false
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  background: #f5f7fb;
  display: flex;
  flex-direction: column;
}

/* 自定义导航栏 */
.custom-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: #fff;
  border-bottom: 1rpx solid #eee;
}

.navbar-content {
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30rpx;
  padding-top: var(--status-bar-height, 44rpx);
}

.navbar-back {
  font-size: 30rpx;
  color: #333;
  padding: 10rpx 0;
}

.navbar-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #333;
}

.navbar-placeholder {
  width: 60rpx;
}

.settings-scroll {
  flex: 1;
  margin-top: calc(var(--status-bar-height, 44rpx) + 88rpx);
  padding: 30rpx;
}

.settings-section {
  background: #fff;
  border-radius: 24rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.settings-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f5f5f5;
  transition: background 0.2s;
}

.settings-item:last-child {
  border-bottom: none;
}

.settings-item:active {
  background: #f8f8f8;
}

.settings-item.logout {
  color: #ff5f5f;
  justify-content: center;
}

.settings-icon {
  font-size: 36rpx;
  margin-right: 24rpx;
  width: 50rpx;
  text-align: center;
}

.settings-label {
  flex: 1;
  font-size: 30rpx;
  color: #333;
}

.settings-item.logout .settings-label {
  color: #ff5f5f;
}

.settings-arrow {
  font-size: 36rpx;
  color: #ccc;
}

/* 账号设置弹窗 */
.account-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 200;
  display: flex;
  align-items: flex-end;
}

.account-modal-content {
  width: 100%;
  max-height: 90vh;
  background: #fff;
  border-radius: 40rpx 40rpx 0 0;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.account-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx;
  border-bottom: 1rpx solid #eee;
}

.account-modal-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #333;
}

.account-modal-close {
  font-size: 48rpx;
  color: #999;
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #f5f5f5;
  line-height: 1;
}

.account-modal-body {
  flex: 1;
  padding: 30rpx;
  overflow-y: auto;
}

.account-section {
  margin-bottom: 40rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 16rpx;
}

.avatar-row {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.avatar-preview {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background: #f2f2f2;
}

.btn-outline {
  border: 1rpx solid #667eea;
  color: #667eea;
  background: #fff;
  border-radius: 999rpx;
  padding: 0 20rpx;
  font-size: 28rpx;
}

.input-wrapper {
  margin-bottom: 20rpx;
}

.text-input {
  width: 100%;
  height: 80rpx;
  padding: 0 24rpx;
  background: #f5f7fb;
  border-radius: 16rpx;
  font-size: 28rpx;
  color: #333;
}

.text-area {
  width: 100%;
  min-height: 140rpx;
  padding: 20rpx 24rpx;
  background: #f5f7fb;
  border-radius: 16rpx;
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
}

.text-counter {
  display: block;
  text-align: right;
  margin-top: 8rpx;
  color: #999;
  font-size: 24rpx;
}

.btn-primary {
  height: 88rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 30rpx;
  font-weight: 600;
  border-radius: 999rpx;
  border: none;
}

.btn-primary.block {
  width: 100%;
  margin-top: 10rpx;
}

/* 加载状态样式 */
.loading-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
}

.loading-icon {
  font-size: 64rpx;
  animation: spin 1.5s linear infinite;
}

.loading-text {
  font-size: 30rpx;
  color: #666;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

