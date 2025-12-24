<template>
  <view class="page" :style="{ paddingTop: topPadding + 'px' }">
    <scroll-view scroll-y class="scroll-area" :style="{ height: scrollHeight + 'px' }">
    <view class="search-row">
      <view class="search-box" @tap="goToSearch">
        <text class="search-icon">🔍</text>
        <text class="search-placeholder">搜索好友、话题或内容</text>
      </view>
      <view class="notify-btn" @tap="handleNotify">
        <text>🔔</text>
        <view class="badge" v-if="notifyCount > 0">{{ notifyCount }}</view>
      </view>
    </view>

    <view class="section-title">好友动态</view>
    <view class="post-card" v-for="item in posts" :key="item.id">
      <view class="post-header">
        <image class="avatar" :src="item.avatar" mode="aspectFill" />
        <view class="meta">
          <text class="name">{{ item.name }}</text>
          <text class="time">{{ item.time }}</text>
        </view>
        <text class="tag" v-if="item.tag">{{ item.tag }}</text>
      </view>

      <view class="text" v-if="item.text">{{ item.text }}</view>

      <view class="media-grid" v-if="item.type === 'image'">
        <image
          v-for="(img, idx) in item.media"
          :key="idx"
          class="media-img"
          :src="img"
          mode="aspectFill"
        />
      </view>

      <view class="media-video" v-if="item.type === 'video'">
        <video
          :src="item.media"
          :poster="item.poster"
          controls
          autoplay="false"
          show-center-play-btn
          object-fit="cover"
        />
      </view>

      <view class="actions-row">
        <view class="action" @tap="toggleLike(item)">
          <text>{{ item.liked ? '❤️' : '🤍' }}</text>
          <text class="action-text">{{ item.likes }}</text>
        </view>
        <view class="action" @tap="handleComment(item)">
          <text>💬</text>
          <text class="action-text">{{ item.comments }}</text>
        </view>
      </view>
    </view>
    
    <!-- 加载状态 -->
    <view class="loading-more" v-if="loadingPosts">
      <text>加载中...</text>
    </view>
    <view class="no-more" v-if="!hasMore && posts.length > 0">
      <text>没有更多动态了</text>
    </view>
    <view class="empty-posts" v-if="posts.length === 0 && !loadingPosts">
      <text>暂无动态</text>
    </view>
    
    <!-- 评论弹窗 -->
    <view class="comment-modal" v-if="showCommentModal" @tap="closeCommentModal">
      <view class="comment-content" @tap.stop>
        <view class="comment-header">
          <text class="comment-title">评论 ({{ currentPostComments.length }})</text>
          <text class="close-btn" @tap="closeCommentModal">✕</text>
        </view>
        
        <scroll-view class="comment-list" scroll-y>
          <view v-if="loadingComments" class="loading-comments">
            <text>加载评论中...</text>
          </view>
          <view v-else-if="currentPostComments.length === 0" class="empty-comments">
            <text>暂无评论，快来发表第一条评论吧～</text>
          </view>
          <view 
            class="comment-item" 
            v-for="comment in currentPostComments" 
            :key="comment.id"
          >
            <image class="comment-avatar" :src="comment.avatar" mode="aspectFill" />
            <view class="comment-body">
              <view class="comment-info">
                <text class="comment-name">{{ comment.name }}</text>
                <text class="comment-time">{{ comment.time }}</text>
              </view>
              <text class="comment-text">{{ comment.content }}</text>
            </view>
          </view>
        </scroll-view>

        <view class="comment-input-bar">
          <input
            class="comment-input"
            type="text"
            v-model="newCommentText"
            placeholder="说点什么..."
            confirm-type="send"
            @confirm="submitComment"
          />
          <button 
            class="send-btn" 
            :disabled="!newCommentText.trim() || submittingComment"
            @tap="submitComment"
          >
            {{ submittingComment ? '发送中...' : '发送' }}
          </button>
        </view>
      </view>
    </view>

    <!-- 消息通知弹窗 -->
    <view class="notify-modal" v-if="showNotifyModal" @tap="closeNotifyModal">
      <view class="notify-content" @tap.stop>
        <view class="notify-header">
          <text class="notify-title">消息通知</text>
          <view class="notify-actions">
            <text class="mark-read-btn" @tap="markAllAsRead" v-if="unreadCount > 0">
              全部已读
            </text>
            <text class="close-btn" @tap="closeNotifyModal">✕</text>
          </view>
        </view>
        
        <scroll-view class="notify-list" scroll-y>
          <view v-if="loadingNotifications" class="loading-notifications">
            <text>加载通知中...</text>
          </view>
          <view v-else-if="notifications.length === 0" class="empty-notify">
            <text>暂无消息</text>
          </view>
          <view 
            class="notify-item" 
            :class="{ unread: !notification.read }"
            v-for="notification in notifications" 
            :key="notification.id"
            @tap="handleNotifyClick(notification)"
          >
            <image class="notify-avatar" :src="notification.avatar" mode="aspectFill" />
            <view class="notify-body">
              <view class="notify-info">
                <text class="notify-name">{{ notification.name }}</text>
                <text class="notify-time">{{ notification.time }}</text>
              </view>
              <view class="notify-message">
                <text class="notify-icon">{{ getNotifyIcon(notification.type) }}</text>
                <text class="notify-text">{{ getNotifyText(notification) }}</text>
              </view>
              <view class="notify-post-preview" v-if="notification.postText">
                <text class="preview-text">{{ notification.postText }}</text>
              </view>
            </view>
            <view class="unread-dot" v-if="!notification.read"></view>
          </view>
        </scroll-view>
      </view>
    </view>
  </scroll-view>
  </view>
</template>

<script>
import { postsApi, notificationApi } from '../../services/api';
export default {
  data() {
    return {
      statusBarHeight: 0, // 状态栏高度
      capsuleHeight: 0,   // 胶囊高度
      topPadding: 0,       // 页面顶部预留边距
      posts: [],
      currentPage: 1,
      pageSize: 10,
      hasMore: true,
      loadingPosts: false,
      notifyCount: 0,
      showCommentModal: false,
      currentPostId: null,
      currentPostComments: [],
      newCommentText: '',
      submittingComment: false,
      showNotifyModal: false,
      notifications: [],
      loadingNotifications: false,
      commentsData: {},
      loadingComments: false,
    }
  },
  computed: {
    unreadCount() {
      return this.notifications.filter(n => !n.read).length
    }
  },
  onLoad() {
    this.updateUnreadCount()
    this.calculateScrollHeight()
    this.setStatusBar()
    this.calculateSafeArea()
    this.loadPosts()
  },
  onReady() {
    this.calculateScrollHeight()
    this.setStatusBar()
  },
  onShow() {
    this.calculateScrollHeight()
    this.setStatusBar()
  },
  methods: {
    // 加载动态列表
    async loadPosts() {
      if (this.loadingPosts || !this.hasMore) return;
      
      this.loadingPosts = true;
      try {
        const response = await postsApi.getPosts({
          page: this.currentPage,
          pageSize: this.pageSize
        });
        
        if (response.success && response.data && response.data.posts) {
          const newPosts = response.data.posts;
          this.posts = this.currentPage === 1 ? newPosts : [...this.posts, ...newPosts];
          this.currentPage++;
          this.hasMore = newPosts.length === this.pageSize;
        } else {
          this.hasMore = false;
        }
      } catch (error) {
        console.error('加载动态失败', error);
        uni.showToast({ title: '加载动态失败', icon: 'none' });
      } finally {
        this.loadingPosts = false;
      }
    },
    
    goToSearch() {
      uni.navigateTo({
        url: '/pages/search/search'
      })
    },
    async toggleLike(item) {
      try {
        const newLikedState = !item.liked;
        await postsApi.likePost(item.id, { liked: newLikedState });
        
        // 更新本地状态
        item.liked = newLikedState;
        item.likes += newLikedState ? 1 : -1;
        this.$forceUpdate();
      } catch (error) {
        console.error('点赞操作失败', error);
        uni.showToast({ title: '操作失败', icon: 'none' });
      }
    },
    async handleComment(item) {
      this.currentPostId = item.id
      this.showCommentModal = true
      this.newCommentText = ''
      
      try {
        this.loadingComments = true
        const response = await postsApi.getComments(item.id, { page: 1, pageSize: 20 })
        this.currentPostComments = response.success && response.data && response.data.comments ? response.data.comments : []
        this.commentsData[item.id] = this.currentPostComments
      } catch (error) {
        console.error('加载评论失败', error)
        uni.showToast({ title: '加载评论失败', icon: 'none' })
      } finally {
        this.loadingComments = false
      }
    },
    closeCommentModal() {
      this.showCommentModal = false
      this.currentPostId = null
      this.currentPostComments = []
      this.newCommentText = ''
    },
    async submitComment() {
      const content = this.newCommentText.trim()
      if (!content) {
        uni.showToast({ title: '请输入评论内容', icon: 'none' })
        return
      }

      this.submittingComment = true

      try {
        const response = await postsApi.addComment(this.currentPostId, { content })
        
        if (response.success && response.data) {
          // 更新本地评论列表
          if (!this.commentsData[this.currentPostId]) {
            this.commentsData[this.currentPostId] = []
          }
          this.commentsData[this.currentPostId].unshift(response.data)
          this.currentPostComments = this.commentsData[this.currentPostId]

          // 更新动态的评论数
          const post = this.posts.find(p => p.id === this.currentPostId)
          if (post) {
            post.comments++
          }

          this.newCommentText = ''
          uni.showToast({ title: '评论成功', icon: 'success' })
        } else {
          uni.showToast({ title: '评论失败', icon: 'none' })
        }
      } catch (error) {
        console.error('发布评论失败', error)
        uni.showToast({ title: '评论失败', icon: 'none' })
      } finally {
        this.submittingComment = false
      }
    },
    async handleNotify() {
      this.showNotifyModal = true
      
      try {
        this.loadingNotifications = true
        const response = await notificationApi.getNotifications({ page: 1, pageSize: 20 })
        if (response.success && response.data && response.data.notifications) {
          this.notifications = response.data.notifications
        } else {
          this.notifications = []
        }
        this.updateUnreadCount()
      } catch (error) {
        console.error('加载通知失败', error)
        uni.showToast({ title: '加载通知失败', icon: 'none' })
        this.notifications = []
      } finally {
        this.loadingNotifications = false
      }
    },
    closeNotifyModal() {
      this.showNotifyModal = false
    },
    getNotifyIcon(type) {
      const icons = {
        like: '❤️',
        comment: '💬',
        follow: '➕',
        system: '🔔'
      }
      return icons[type] || '🔔'
    },
    getNotifyText(notification) {
      const texts = {
        like: '赞了你的动态',
        comment: '评论了你的动态',
        follow: '关注了你',
        system: '系统通知'
      }
      let text = texts[notification.type] || '通知'
      if (notification.type === 'comment' && notification.commentContent) {
        text += `：${notification.commentContent}`
      }
      return text
    },
    handleNotifyClick(notification) {
      if (!notification.read) {
        notification.read = true
        this.updateUnreadCount()
      }
      
      this.closeNotifyModal()
      
      if (notification.postId) {
        setTimeout(() => {
          if (notification.type === 'comment') {
            const post = this.posts.find(p => p.id === notification.postId)
            if (post) {
              this.handleComment(post)
            }
          } else {
            uni.showToast({ 
              title: `查看动态 #${notification.postId}`, 
              icon: 'none',
              duration: 1500
            })
          }
        }, 300)
      }
    },
    async markAllAsRead() {
      const unreadNotifications = this.notifications.filter(n => !n.read)
      if (unreadNotifications.length === 0) {
        uni.showToast({ title: '没有未读通知', icon: 'none' })
        return
      }
      
      const notificationIds = unreadNotifications.map(n => n.id)
      
      try {
        await notificationApi.markAsRead({ notificationIds })
        
        // 更新本地状态
        this.notifications.forEach(notify => {
          notify.read = true
        })
        this.updateUnreadCount()
        uni.showToast({ title: '已全部标记为已读', icon: 'success' })
      } catch (error) {
        console.error('标记通知已读失败', error)
        uni.showToast({ title: '操作失败', icon: 'none' })
      }
    },
    updateUnreadCount() {
      this.notifyCount = this.notifications.filter(n => !n.read).length
    },
    // 修复：补全 try-catch 闭合，修正逻辑
    setStatusBar() {
      try {
        const info = uni.getSystemInfoSync()
        this.statusBarHeight = info.statusBarHeight || 0
      } catch (e) {
        console.error('获取系统信息失败', e)
      }
    },
    calculateSafeArea() {
      try {
        const systemInfo = uni.getSystemInfoSync();
        // 兼容微信小程序和 App 端获取胶囊信息
        const menuButtonInfo = uni.getMenuButtonBoundingClientRect ? uni.getMenuButtonBoundingClientRect() : {};

        // 状态栏高度
        const statusBarHeight = systemInfo.statusBarHeight || 0;

        // 胶囊高度和顶部间距（默认值兼容）
        const capsuleHeight = menuButtonInfo.height || 32;
        const capsuleTop = menuButtonInfo.top || statusBarHeight;

        // 计算顶部预留边距（胶囊底部到顶部的距离 + 额外 8px 间距）
        const topPadding = capsuleTop + capsuleHeight + 8;

        // 设置数据
        this.statusBarHeight = statusBarHeight;
        this.capsuleHeight = capsuleHeight;
        this.topPadding = topPadding;
      } catch (e) {
        console.error('获取胶囊信息失败', e);
        // 异常时设置默认值
        this.topPadding = 44;
      }
    },
    // 修复：合并重复的 calculateScrollHeight 方法
    calculateScrollHeight() {
      try {
        const systemInfo = uni.getSystemInfoSync()
        // 计算可用高度：屏幕高度 - 顶部预留边距 - 底部预留间距（40rpx = 20px）
        this.scrollHeight = systemInfo.windowHeight - this.topPadding - 20;
        
        this.$nextTick(() => {
          // 确保高度计算正确（避免初始值为 0）
          if (this.scrollHeight <= 0) {
            this.scrollHeight = systemInfo.windowHeight - 44 - 20; // 默认顶部边距 44px
          }
        })
      } catch (e) {
        console.error('计算滚动高度失败', e);
        this.scrollHeight = 600; // 异常时设置默认高度
      }
    }
  }
}
</script>

<style scoped>
.page {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: #f5f7fb;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

/* 加载状态样式 */
.loading-more, .no-more, .empty-posts {
  text-align: center;
  padding: 20rpx;
  color: #999;
  font-size: 26rpx;
}

.loading-comments, .loading-notifications {
  text-align: center;
  padding: 40rpx;
  color: #999;
  font-size: 28rpx;
}

.scroll-area {
  width: 100%;
  padding: 20rpx 24rpx;
  padding-bottom: 40rpx;
  box-sizing: border-box;
}

.search-row {
  display: flex;
  align-items: center;
  gap: 16rpx;
  width: 100%;
  box-sizing: border-box;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 999rpx;
  padding: 12rpx 18rpx;
  box-shadow: 0 10rpx 20rpx rgba(0, 0, 0, 0.04);
  border: 1rpx solid #eef0f5;
  min-width: 0;
  box-sizing: border-box;
}

.search-icon {
  margin-right: 10rpx;
  font-size: 28rpx;
}

.search-placeholder {
  flex: 1;
  font-size: 28rpx;
  color: #999;
}

.notify-btn {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 10rpx 20rpx rgba(102, 126, 234, 0.3);
}

.badge {
  position: absolute;
  top: -6rpx;
  right: -6rpx;
  min-width: 26rpx;
  height: 26rpx;
  border-radius: 999rpx;
  background: #ff5f5f;
  color: #fff;
  font-size: 20rpx;
  padding: 0 8rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.section-title {
  margin: 20rpx 0;
  color: #666;
  font-size: 28rpx;
}

.post-card {
  width: 100%;
  background: #fff;
  border-radius: 24rpx;
  padding: 24rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
  margin-bottom: 24rpx;
  box-sizing: border-box;
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  margin-right: 16rpx;
  background: #f2f2f2;
}

.meta {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.name {
  font-size: 30rpx;
  color: #333;
  font-weight: 600;
}

.time {
  font-size: 24rpx;
  color: #999;
}

.tag {
  padding: 8rpx 16rpx;
  border-radius: 999rpx;
  background: rgba(102, 126, 234, 0.12);
  color: #667eea;
  font-size: 22rpx;
}

.text {
  color: #444;
  font-size: 30rpx;
  line-height: 1.6;
  margin-bottom: 16rpx;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10rpx;
  margin-top: 10rpx;
  margin-bottom: 12rpx;
  width: 100%;
  box-sizing: border-box;
}

.media-img {
  width: 100%;
  height: 220rpx;
  border-radius: 16rpx;
  background: #f2f2f2;
  object-fit: cover;
  box-sizing: border-box;
}

.media-video {
  width: 100%;
  box-sizing: border-box;
}

.media-video video {
  width: 100%;
  height: 360rpx;
  border-radius: 16rpx;
  overflow: hidden;
  background: #000;
  box-sizing: border-box;
}

.actions-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10rpx;
}

.action {
  display: flex;
  align-items: center;
  gap: 8rpx;
  color: #666;
  font-size: 26rpx;
}

.action-text {
  color: #666;
}

/* 评论弹窗 */
.comment-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: flex-end;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.comment-content {
  width: 100%;
  max-height: 80vh;
  background: #fff;
  border-radius: 32rpx 32rpx 0 0;
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

.comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx 32rpx;
  border-bottom: 1rpx solid #eee;
}

.comment-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
}

.close-btn {
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  color: #999;
  border-radius: 50%;
  background: #f5f5f5;
}

.comment-list {
  flex: 1;
  padding: 20rpx 32rpx;
  min-height: 200rpx;
  max-height: 50vh;
}

.empty-comments {
  text-align: center;
  padding: 100rpx 0;
  color: #999;
  font-size: 28rpx;
}

.comment-item {
  display: flex;
  margin-bottom: 32rpx;
}

.comment-avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  margin-right: 20rpx;
  background: #f2f2f2;
  flex-shrink: 0;
}

.comment-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.comment-info {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 8rpx;
}

.comment-name {
  font-size: 28rpx;
  color: #333;
  font-weight: 600;
}

.comment-time {
  font-size: 24rpx;
  color: #999;
}

.comment-text {
  font-size: 28rpx;
  color: #444;
  line-height: 1.6;
  word-break: break-all;
}

.comment-input-bar {
  display: flex;
  align-items: center;
  padding: 20rpx 32rpx;
  border-top: 1rpx solid #eee;
  background: #fff;
  gap: 16rpx;
}

.comment-input {
  flex: 1;
  padding: 16rpx 24rpx;
  background: #f5f5f5;
  border-radius: 999rpx;
  font-size: 28rpx;
  color: #333;
}

.send-btn {
  padding: 16rpx 32rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 999rpx;
  font-size: 28rpx;
  font-weight: 500;
}

.send-btn[disabled] {
  opacity: 0.5;
  background: #ccc;
}

/* 消息通知弹窗 */
.notify-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: flex-end;
  animation: fadeIn 0.3s ease;
}

.notify-content {
  width: 100%;
  max-height: 85vh;
  background: #fff;
  border-radius: 32rpx 32rpx 0 0;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease;
}

.notify-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx 32rpx;
  border-bottom: 1rpx solid #eee;
}

.notify-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
}

.notify-actions {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.mark-read-btn {
  font-size: 26rpx;
  color: #667eea;
  padding: 8rpx 16rpx;
}

.notify-list {
  flex: 1;
  padding: 20rpx 0;
  min-height: 200rpx;
  max-height: 65vh;
}

.empty-notify {
  text-align: center;
  padding: 100rpx 0;
  color: #999;
  font-size: 28rpx;
}

.notify-item {
  display: flex;
  align-items: flex-start;
  padding: 24rpx 32rpx;
  position: relative;
  background: #fff;
  transition: background 0.2s;
}

.notify-item.unread {
  background: #f8f9ff;
}

.notify-item:active {
  background: #f0f0f0;
}

.notify-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin-right: 20rpx;
  background: #f2f2f2;
  flex-shrink: 0;
}

.notify-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.notify-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8rpx;
}

.notify-name {
  font-size: 30rpx;
  color: #333;
  font-weight: 600;
}

.notify-time {
  font-size: 24rpx;
  color: #999;
}

.notify-message {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-bottom: 8rpx;
}

.notify-icon {
  font-size: 28rpx;
}

.notify-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.5;
  flex: 1;
}

.notify-post-preview {
  margin-top: 8rpx;
  padding: 12rpx 16rpx;
  background: #f5f5f5;
  border-radius: 12rpx;
  border-left: 4rpx solid #667eea;
}

.preview-text {
  font-size: 26rpx;
  color: #888;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  overflow: hidden;
}

.unread-dot {
  position: absolute;
  top: 30rpx;
  right: 32rpx;
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: #ff5f5f;
}
</style>