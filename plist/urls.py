from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # 메인페이지
    path('', views.main, name='main'),
    ############## 회원가입 / 로그인 / 로그아웃 ##############
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    ############## title / artist / genre / tag 검색 ##############
    path('search/title/', views.search_title, name='title'),
    path('search/artist/', views.search_artist, name='artist'),
    path('search/genre/', views.search_genre, name='genre'),
    path('search/tag/', views.search_tag, name='tag'),
    ############## 노래 추가  / 노래 상세정보 / playlist에 노래추가 / playlist에 노래삭제 ##############
    path('song/new/', views.song_new, name='song_new'),
    path('song/<int:pk>/', views.song_detail, name='song_detail'),
    path('song/add/<int:play_pk>/<int:song_pk>/<int:path_pk>/', views.song_add_playlist, name='song_add_playlist'),
    path('song/delete/<int:play_pk>/<int:song_pk>/', views.song_delete, name='song_delete'),
    ############## playlist 추가 / playlist 상세정보 / 모든사용자 playlist ##############
    path('playlist/new/', views.play_new, name='play_new'),
    path('playlist/<int:pk>/', views.play_detail, name='play_detail'),
    path('playlist/all/', views.play_all, name='play_all'),
    ############## 내 playlist / playlist copy / playlist delete /playlist rename /  ##############
    path('mypage/playlist/', views.my_play, name='my_play'),
    path('playlist/copy/<int:pk>/', views.play_copy, name='play_copy'),
    path('playlist/delete/<int:pk>', views.play_delete, name='play_delete'),
    path('playlist/rename/<int:pk>/',views.play_rename,name='play_rename'),
    ############## My detail에서 확인 가능한 playlist 상세정보 / song 상세정보 ##############
    path('myPage/myDetail/playlists/',views.my_detail_play, name='my_detail_play'),
    path('myPage/myDetail/songs/', views.my_detail_song, name='my_detail_song'),
    ############## 관리자권한 가진 사용자만 노래제거 가능 ##############
    path('admin/song/remove/<int:pk>/',views.admin_song_remove,name='admin_song_remove'),
]
