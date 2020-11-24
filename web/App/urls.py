from django.urls import path, re_path

from App import views

app_name = 'App'
urlpatterns = [
    path('', views.index, name='index1'),
    path('index/', views.index, name='index'),
    path("list/", views.list, name='list'),
    path("add/<int:num>/", views.add, name='add'),
    path("del/<int:num>/", views.del_focus, name='del'),
    path("search/",views.search,name='search'),
    path("findauthor/<path:author>/",views.findauthor,name='finda'),
    path("findpublisher/<publisher>/",views.findpublisher,name='findp'),
]
