####################  搜索部分开始  ######################
# 顶部统一改成相对引用（方便移动）
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import Post, SearchHistory
from .serializers import PostSerializer, SearchHistorySerializer
from datetime import datetime
# 需要用到 User
from django.contrib.auth import get_user_model
User = get_user_model()

# --------------- 1.搜索接口  ---------------
class SearchView(generics.GenericAPIView):
    """
    GET /api/search ?keyword=&tag=&date=&page=&pageSize=
    支持关键词、标签和日期的组合筛选
    """
    serializer_class = PostSerializer

    def get(self, request):
        kw   = request.GET.get('keyword','').strip()
        tag  = request.GET.get('tag','').strip()
        date = request.GET.get('date','')          # YYYY-MM-DD
        page = int(request.GET.get('page',1))
        pz   = int(request.GET.get('pageSize',10))

        qs = Post.objects.all()
        if kw:
            qs = qs.filter(Q(text__icontains=kw)|Q(author__username__icontains=kw))
        if tag:
            qs = qs.filter(tag=tag)
        if date:
            try:
                d = datetime.strptime(date,'%Y-%m-%d').date()
                qs = qs.filter(created_at__date=d)
            except ValueError:
                pass

        total = qs.count()
        start = (page-1)*pz
        posts = qs[start:start+pz]

        ser = PostSerializer(posts, many=True, context={'request':request})
        return Response({'success':True,
                         'data':{'results':ser.data,'total':total}})

# --------------- 2.热门标签接口  ---------------
class HotTagsView(generics.GenericAPIView):
    """
    GET /api/tags/hot
    """
    def get(self, request):
        # 按 tag 出现次数倒序
        tags = (Post.objects.values('tag')
                            .annotate(c=Count('id'))
                            .order_by('-c')[:20])
        data = [t['tag'] for t in tags if t['tag']]
        return Response({'success':True,'data':{'tags':data}})

# --------------- 3.搜索建议接口  ---------------
class SearchSuggestionsView(generics.GenericAPIView):
    """
    GET /api/search/suggestions ?keyword=
    """
    def get(self, request):
        kw = request.GET.get('keyword','').strip()
        if not kw:
            return Response({'success':True,'data':{'suggestions':[]}})
        # 简单示范：从用户名、tag、历史关键词中模糊匹配
        user_qs = User.objects.filter(username__icontains=kw)[:5]
        tag_qs  = (Post.objects.filter(tag__icontains=kw)
                               .values_list('tag',flat=True).distinct()[:5])
        hist_qs = (SearchHistory.objects.filter(keyword__icontains=kw)
                                        .values_list('keyword',flat=True)
                                        .distinct()[:5])
        sugs = list({u.username for u in user_qs}) + list(tag_qs) + list(hist_qs)
        sugs = list(dict.fromkeys(sugs))[:10]   # 去重
        return Response({'success':True,'data':{'suggestions':sugs}})


# --------------- 4+5.保存/获取搜索历史  ---------------
# 根据接口文档，最好合并这两个接口，使得该url同时支持 GET 和 POST 方法
class SearchHistoryView(generics.GenericAPIView):
    """
    GET  /api/search/history   -> 获取历史（带分页）
    POST /api/search/history   -> 保存历史
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SearchHistorySerializer

    # ---------- GET ----------
    def get(self, request):
        qs = SearchHistory.objects.filter(user=request.user)[:10]  # 采用固定大小的分页
        ser = self.get_serializer(qs, many=True)
        return Response({'success': True, 'data': {'history': ser.data}})

    # ---------- POST ----------
    def post(self, request):
        keyword = request.data.get('keyword', '').strip()
        tag = request.data.get('tag', '').strip()
        date = request.data.get('date', '')
        if not keyword:
            return Response({'success': False, 'message': '关键词不能为空'}, status=400)
        SearchHistory.objects.update_or_create(
            user=request.user,
            keyword=keyword,
            tag=tag,
            date=date or datetime.today().date(),
            defaults={'created_at': datetime.now()}
        )
        return Response({'success': True, 'message': '搜索历史已保存'})

# --------------- 6.清除搜索历史  ---------------
class SearchHistoryClearView(generics.GenericAPIView):
    """
    DELETE /api/search/history/clear
    """
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        SearchHistory.objects.filter(user=request.user).delete()
        return Response({'success':True,'message':'搜索历史已清除'})


####################  搜索部分结束  ######################
