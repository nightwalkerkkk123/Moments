<template>
  <view class="page">
    <view class="loading">正在跳转...</view>
  </view>
</template>

<script>
export default {
  onLoad() {
    // 重定向到 discover 页面（tabBar 首页）
    uni.reLaunch({
      url: '/pages/discover/discover'
    })
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f7fb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading {
  color: #999;
  font-size: 28rpx;
}
</style>