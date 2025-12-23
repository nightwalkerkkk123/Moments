from django.urls import path
###  搜索部分新增url（共6个）  ###
from .views import (
    SearchView, HotTagsView, SearchSuggestionsView,
    SearchHistoryView , SearchHistoryClearView
)
urlpatterns = [
    path('search', SearchView.as_view(), name='search'),
    path('tags/hot', HotTagsView.as_view(), name='hot-tags'),
    path('search/suggestions', SearchSuggestionsView.as_view(), name='suggestions'),
    path('search/history', SearchHistoryView.as_view(), name='history'),  # GET+POST
    path('search/history/clear', SearchHistoryClearView.as_view(), name='clear-history'),
]
####################