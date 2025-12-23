// API服务配置
const API_BASE_URL = '/api';

// 封装uni.request
const request = (url, method, data = {}) => {
  // 获取token
  const token = uni.getStorageSync('token');
  
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${API_BASE_URL}${url}`,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data);
        } else {
          reject(new Error(res.data.message || '请求失败'));
        }
      },
      fail: (err) => {
        reject(err);
      }
    });
  });
};

// 登录相关API
export const authApi = {
  // 用户登录
  login: (data) => request('/auth/login', 'POST', data),
  
  // 检查保存的登录信息
  checkCredentials: () => request('/auth/check-credentials', 'GET'),
  
  // 忘记密码
  forgotPassword: (data) => request('/auth/forgot-password', 'POST', data),
  
  // 保存用户登录信息
  saveCredentials: (data) => request('/auth/save-credentials', 'POST', data),
  
  // 加载用户登录信息
  loadCredentials: () => request('/auth/load-credentials', 'GET'),
  
  // 退出登录
  logout: () => request('/auth/logout', 'POST')
};

// 注册相关API
export const registerApi = {
  // 用户注册
  register: (data) => request('/auth/register', 'POST', data),
  
  // 检查昵称是否重复
  checkNickname: (nickname) => request(`/auth/check-nickname?nickname=${nickname}`, 'GET'),
  
  // 验证密码强度
  validatePasswordStrength: (data) => request('/auth/validate-password-strength', 'POST', data)
};

// 动态相关API
export const postsApi = {
  // 获取动态列表
  getPosts: (params) => request(`/posts?page=${params.page}&pageSize=${params.pageSize}`, 'GET'),
  
  // 点赞动态
  likePost: (id, data) => request(`/posts/${id}/like`, 'POST', data),
  
  // 获取动态评论
  getComments: (id, params) => request(`/posts/${id}/comments?page=${params.page}&pageSize=${params.pageSize}`, 'GET'),
  
  // 发布评论
  addComment: (id, data) => request(`/posts/${id}/comments`, 'POST', data),
  
  // 发布动态
  createPost: (data) => request('/posts', 'POST', data),
  
  // 删除我的动态
  deletePost: (id) => request(`/user/posts/${id}`, 'DELETE')
};

// 用户相关API
export const userApi = {
  // 获取用户个人信息
  getProfile: () => request('/user/profile', 'GET'),
  
  // 更新用户头像
  updateAvatar: (data) => request('/user/avatar', 'POST', data),
  
  // 更新用户昵称
  updateNickname: (data) => request('/user/nickname', 'POST', data),
  
  // 更新个性签名
  updateSignature: (data) => request('/user/signature', 'POST', data),
  
  // 修改密码
  updatePassword: (data) => request('/user/password', 'POST', data),
  
  // 获取我的动态列表
  getMyPosts: (params) => request(`/user/posts?page=${params.page}&pageSize=${params.pageSize}`, 'GET'),
  
  // 获取我的统计信息
  getStats: () => request('/user/stats', 'GET'),
  
  // 获取当前用户信息
  getCurrentUser: () => request('/user/current', 'GET')
};

// 搜索相关API
export const searchApi = {
  // 搜索
  search: (params) => request(`/search?query=${params.query}&type=${params.type}&page=${params.page}&pageSize=${params.pageSize}`, 'GET'),
  
  // 获取热门标签
  getHotTags: () => request('/tags/hot', 'GET'),
  
  // 获取搜索建议
  getSuggestions: (keyword) => request(`/search/suggestions?keyword=${keyword}`, 'GET'),
  
  // 保存搜索历史
  saveHistory: (data) => request('/search/history', 'POST', data),
  
  // 获取搜索历史
  getHistory: () => request('/search/history', 'GET'),
  
  // 清除搜索历史
  clearHistory: () => request('/search/history/clear', 'DELETE')
};

// 通知相关API
export const notificationApi = {
  // 获取消息通知
  getNotifications: (params) => request(`/notifications?page=${params.page}&pageSize=${params.pageSize}`, 'GET'),
  
  // 标记通知为已读
  markAsRead: (data) => request('/notifications/mark-as-read', 'POST', data)
};

// 上传相关API
export const uploadApi = {
  // 图片上传
  uploadImage: (filePath) => {
    return new Promise((resolve, reject) => {
      uni.uploadFile({
        url: `${API_BASE_URL}/upload/image`,
        filePath,
        name: 'file',
        header: {
          'Authorization': `Bearer ${uni.getStorageSync('token')}`
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(JSON.parse(res.data));
          } else {
            reject(new Error('上传失败'));
          }
        },
        fail: (err) => {
          reject(err);
        }
      });
    });
  },
  
  // 视频上传
  uploadVideo: (filePath) => {
    return new Promise((resolve, reject) => {
      uni.uploadFile({
        url: `${API_BASE_URL}/upload/video`,
        filePath,
        name: 'file',
        header: {
          'Authorization': `Bearer ${uni.getStorageSync('token')}`
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(JSON.parse(res.data));
          } else {
            reject(new Error('上传失败'));
          }
        },
        fail: (err) => {
          reject(err);
        }
      });
    });
  }
};

// 标签相关API
export const tagsApi = {
  // 获取常用标签
  getCommonTags: () => request('/tags/common', 'GET'),
  
  // 创建新标签
  createTag: (data) => request('/tags', 'POST', data)
};

// 系统相关API
export const systemApi = {
  // 获取安全区域信息
  getSafeArea: () => request('/system/safe-area', 'GET')
};

export default {
  auth: authApi,
  register: registerApi,
  posts: postsApi,
  user: userApi,
  search: searchApi,
  notification: notificationApi,
  upload: uploadApi,
  tags: tagsApi,
  system: systemApi
};
