from .forms import SongForm,UserForm, LoginForm, PlaylistForm
from .models import Song, Playlist
from plist.feature.mp3_download import download_video_and_subtitle
from plist.feature.mp3_slice import song_slice
from plist.feature.get_artist_thumbnail import get_thumbnail
from plist.feature.youtube_recommend import recommend_song_list
from .documents import SongDocument

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


GENRE_CHOICES = (
    ('0', '가요'),  # First one is the value of select option and second is the displayed value in option
    ('1', 'R&B'),
    ('2', 'POP'),
    ('3', 'JAZZ'),
    ('4', '인디음악'),
    ('5', '댄스'),
    ('6', '랩/힙합'),
    ('7', '기타'),
)
TAG_CHOICES = (
    ('0', "우울할때"),
    ("1", "기분좋아지는"),
    ("2", "노동요"),
    ("3", "가사없는"),
    ("4", "산뜻,상큼한"),
    ("5", "신나는"),
    ("6", "2000년대"),
)


class UserCreateView(CreateView):
    form_class = UserForm
    template_name = 'registration/signup.html'
    success_url = "/"


# 메인 페이지
def main(request):
    my_song_list = Song.objects.all()

    # 전체 플레이 리스트 데이터를 가져옴
    play_all_list = Playlist.objects.all()
    playlist = []
    # 전체 플레이 리스트 데이터만큼 디테일을 만듬
    for detail_list in play_all_list:
        list_dict = {}
        song_list = []
        # 디테일 리스트에 노래가 비어있으면 무시
        if detail_list.play_list == 'empty':
            continue
        # 디테일 리스트에 노래들이 있으면 노래들을 리스트로 패킹(아직은 키값으로 유지)
        else:
            song_id_list = detail_list.play_list.split(',')
            # 리스트화된 노래들을 하나씩 뿌려줌(song에 있는 키값과 매칭)
            for song_id in song_id_list:
                song = get_object_or_404(Song, pk=song_id)
                # song에 있는 노래들을 하나씩 뿌려줘서 개별적으로 나타냄
                song_list.append(song)
            list_dict['my_playlist'] = detail_list
            list_dict['song_list'] = song_list
            playlist.append(list_dict)
            playlist = playlist[-3:]
    return render(request, 'plist/main.html', {'playlist': playlist, 'my_song_list':my_song_list})



 ############## 회원가입 / 로그인 ##############

# 회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            # login(request, new_user)
            return redirect('main')
    else:
        form = UserForm()
        return render(request, 'registration/signup.html', {'form': form})


# 로그인 페이지
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return HttpResponse('로그인 실패. 다시 시도해보세요')
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})



############## title / artist / genre / tag 검색 기능 ##############

# title 검색
@login_required
def search_title(request):
    q = request.GET.get('q')
    if q:
        songs = SongDocument.search().query('match',song_title=q)
    else:
        songs = ''

    # 플레이리스트 가져오기
    play_list = Playlist.objects.filter(author=request.user)

    return render(request, 'search/title.html', {'songs':songs, 'play_list':play_list})


# artist 검색
@login_required
def search_artist(request):
    a = request.GET.get('a')
    if a:
        singer = SongDocument.search().query('match',song_artist=a)
    else:
        singer = ''

    # 플레이리스트 가져오기
    play_list = Playlist.objects.filter(author=request.user)

    return render(request, 'search/artist.html', {'singer':singer, 'play_list':play_list})


# genre 검색
@login_required
def search_genre(request):
    # return render(request,'plist/genre.html')
    kpops = Song.objects.filter(song_genre='0')
    r_bs = Song.objects.filter(song_genre='1')
    pops = Song.objects.filter(song_genre='2')
    jazzs = Song.objects.filter(song_genre='3')
    indies = Song.objects.filter(song_genre='4')
    dances = Song.objects.filter(song_genre='5')
    hiphops = Song.objects.filter(song_genre='6')
    elses = Song.objects.filter(song_genre='7')
    # a = request.POST.get('pop')
    # if a:

    # 플레이리스트 가져오기
    play_list = Playlist.objects.filter(author=request.user)

    return render(request, 'search/genre.html',
                  {'kpops': kpops,
                   'pops': pops,
                   'r_bs': r_bs,
                   'jazzs': jazzs,
                   'indies':indies,
                   'dances': dances,
                   'hiphops':hiphops,
                   'elses': elses,
                   'play_list': play_list,
                   })


# tag 검색
@login_required
def search_tag(request):
    # return render(request,'plist/genre.html')
    tag_0 = Song.objects.filter(song_tag='0')
    tag_1 = Song.objects.filter(song_tag='1')
    tag_2 = Song.objects.filter(song_tag='2')
    tag_3 = Song.objects.filter(song_tag='3')
    tag_4 = Song.objects.filter(song_tag='4')
    tag_5 = Song.objects.filter(song_tag='5')
    tag_6 = Song.objects.filter(song_tag='6')

    # 플레이리스트 가져오기
    play_list = Playlist.objects.filter(author=request.user)

    return render(request, 'search/tag.html',
                  {'tag_0': tag_0,
                   'tag_1': tag_1,
                   'tag_2': tag_2,
                   'tag_3': tag_3,
                   'tag_4': tag_4,
                   'tag_5': tag_5,
                   'tag_6': tag_6,
                   'play_list':play_list,
                   })



############## 노래 추가  / 노래 상세정보 / playlist에 노래추가 / playlist에 노래삭제 ##############

# 새로운 노래 추가
@login_required
def song_new(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            # mp3 파일 뽑아내는 작업
            download_video_and_subtitle(form.cleaned_data['song_url'], form.cleaned_data['song_title'])

            # mp3 파일 자르는 작업
            song_slice(form.cleaned_data['song_title'],form.cleaned_data['song_start'],form.cleaned_data['song_end'])

            # 가수 이미지 썸네일 만드는 작업
            verify = get_thumbnail(form.cleaned_data['song_artist'])
            if verify:
                thumbnail = form.cleaned_data['song_artist']
            else:
                thumbnail = 'default'

            # db에 넣기
            song = Song.objects.create(song_title=form.cleaned_data['song_title'],\
                                       song_artist=form.cleaned_data['song_artist'], \
                                       song_url=form.cleaned_data['song_url'],
                                       song_genre=form.cleaned_data['song_genre'], \
                                       song_start=form.cleaned_data['song_start'], \
                                       song_end=form.cleaned_data['song_end'], \
                                       song_tag=form.cleaned_data['song_tag'], \
                                       song_thumbnail=thumbnail,\
                                       song_detail=form.cleaned_data['song_detail'],\
                                       author=request.user,
                                       )

            return redirect('index')
        else:
            return HttpResponse('문제가 발생했습니다. 다시 시도해 주세요.')
    else:
        form = SongForm()
        return render(request, 'plist/myPage/song_new.html', {'form': form})


# 특정 song detail 정보 가져오기
def song_detail(request,pk):
    song = get_object_or_404(Song, pk=pk)
    song_tag = TAG_CHOICES[int(song.song_tag)]
    song_genre = GENRE_CHOICES[int(song.song_genre)]
    # 추천 노래 리스트 받아오기
    recommend_list = recommend_song_list(song.song_url)
    return render(request, 'plist/song_detail.html', \
                  {'song': song,'genre':song_genre[1], 'tag':song_tag[1],\
                   'recommend_list':recommend_list})


# playlist에 노래 추가
@login_required
def song_add_playlist(request, play_pk, song_pk, path_pk):
    # 노래 추가할 playlist 객체 가져오기
    new_playlist = get_object_or_404(Playlist, pk=play_pk)
    
    # 만약 기존에 노래목록이 있었다면 str => list 형태변환
    if new_playlist.play_list != 'empty':
        song_list = new_playlist.play_list.split(',')
    # 기존에 노래가 없는 empty 상태였다면    
    else:
        song_list = []

    # 새로 추가하려는 노래가 기존목록에 없을때만 추가
    if str(song_pk) not in song_list:
        song_list.append(str(song_pk))
        new_list = ",".join(song_list)
        new_playlist.play_list = new_list
        new_playlist.save()

    # 처음에 노래추가했던 페이지로 리다이렉트
    # 1: title 로 보내기
    if path_pk == 1:
        return redirect('title')
    # 2: artist 로 보내기
    elif path_pk == 2:
        return redirect('artist')
    # 3: genre 로 보내기
    elif path_pk == 3:
        return redirect('genre')
    # 4: tag 로 보내기
    elif path_pk == 4:
        return redirect('tag')


# playlist에서 노래 제거
@login_required
def song_delete(request, play_pk, song_pk):
    # 노래 제거할 playlist 객체 가져오기
    select_playlist = get_object_or_404(Playlist, pk=play_pk)
    # 제거할 song_pk
    del_pk = song_pk
    song_list = select_playlist.play_list.split(',')
    # song_pk 제거
    for i in song_list:
        if str(del_pk) == i:
            song_list.remove(str(del_pk))
    
    # 제거한 노래 뺴고 다시 string으로 만들기
    new_list = ",".join(song_list)

    # 노래 제거 후 빈 리스트라면 empty값 넣어주기
    if not new_list :
        select_playlist.play_list = 'empty'
    # 노래가 있다면 수정하기    
    else:
        select_playlist.play_list = new_list
        
    select_playlist.save()
    return redirect('my_detail_play')



############## playlist 추가 / playlist 상세정보 / 모든사용자 playlist ##############

# 새로운 playlist 추가
@login_required
def play_new(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            
            # db에 넣기
            playlist = Playlist.objects.create(play_title=form.cleaned_data['play_title'],
                                                author=request.user,
                                               # 노래 목록 없으므로 empty 값 지정
                                                play_list='empty',
                                                play_detail='',
                                        )
            return redirect('my_play')
        else:
            return HttpResponse('문제가 발생했습니다. 다시 시도해주세요.')
    
    else:
        form = PlaylistForm()
        return render(request, 'plist/myPage/playlist_new.html', {'form':form})


# 특정 playlist 들어있는 노래목록 가져오기
def play_detail(request, pk):
    play_detail_list = get_object_or_404(Playlist, pk=pk)

    song_list = []
    # 노래 목록 리스트에 노래 추가되어 있을 경우에만 song 객체 가져오기
    if play_detail_list.play_list != 'empty':
        song_id_list = play_detail_list.play_list.split(',')
        # song_id_list에서 song_id 하나씩 꺼내 해당 song 객체 찾기
        for song_id in song_id_list:
            song = get_object_or_404(Song,pk=song_id)
            song_list.append(song)
        verify = True
    # 노래 목록 리스트가 빈 값이면 false 처리
    else:
        verify = False

    return render(request, 'plist/play_detail.html', {'play_detail_list': play_detail_list, 'song_list':song_list, 'verify':verify})


# 모든 사용자의 playlist 불러오기
def play_all(request):
    # 전체 플레이 리스트 데이터를 가져옴
    play_all_list = Playlist.objects.all()
    playlist = []
    # 전체 플레이 리스트 데이터만큼 디테일을 만듬
    for detail_list in play_all_list:
        list_dict = {}
        song_list = []
        # 디테일 리스트에 노래가 비어있으면 무시
        if detail_list.play_list == 'empty':
            continue
        # 디테일 리스트에 노래들이 있으면 노래들을 리스트로 패킹(아직은 키값으로 유지)
        else:
            song_id_list = detail_list.play_list.split(',')
            # 리스트화된 노래들을 하나씩 뿌려줌(song에 있는 키값과 매칭)
            for song_id in song_id_list:
                song = get_object_or_404(Song, pk=song_id)
                # song에 있는 노래들을 하나씪 뿌려줘서 개별적으로 나타냄
                song_list.append(song)
            list_dict['my_playlist'] = detail_list
            list_dict['song_list'] = song_list
            playlist.append(list_dict)

    return render(request, 'plist/playlist_all.html', {'playlist': playlist})



############## 내 playlist / playlist copy / playlist delete /playlist rename /  ##############

# 내 playlist 목록 가져오기
@login_required
def my_play(request):
    # 전체 플레이 리스트 데이터를 가져옴
    play_all_list = Playlist.objects.filter(author=request.user)
    play_list = []

    for detail_list in play_all_list:
        list_dict = {}
        song_list = []
        # 노래 목록이 비어있으면 false 처리
        if detail_list.play_list == 'empty':
            list_dict['verify'] = False
            list_dict['song_list'] = song_list
        # 노래 목록이 있다면 노래 객체 song_list에 담기
        else:
            list_dict['verify'] = True
            song_id_list = detail_list.play_list.split(',')
            # song_id_list에 담긴 song_id별로 song 객체 찾기
            for song_id in song_id_list:
                song = get_object_or_404(Song, pk=song_id)
                song_list.append(song)
            list_dict['song_list'] = song_list

        list_dict['my_playlist'] = detail_list
        play_list.append(list_dict)

    return render(request, 'plist/myPage/my_playlist.html', {'play_list': play_list})


# 다른 사람 플레이 리스트 -> 내 플레이리스트에 추가
@login_required
def play_copy(request,pk):
    # 다른 사람 플레이리스트 가져오기
    playlist = get_object_or_404(Playlist,pk=pk)
    # 로그인 사용자 계정으로 플레이리스트 db에 추가
    playlist = Playlist.objects.create(play_title=str(playlist.author)+'의 플레이리스트\n'+playlist.play_title+'copy',
                            author=request.user,
                            play_list=playlist.play_list,
                            play_detail='',
                            )

    return redirect('my_play')


# playlist 삭제
@login_required
def play_delete(request,pk):
    del_playlist = get_object_or_404(Playlist, pk=pk)
    del_playlist.delete()
    return redirect('my_detail_play')


# playlist 이름 변경하기
@login_required
def play_rename(request,pk):
    # 이름변경할 플레이리스트 찾기
    re_playlist = get_object_or_404(Playlist, pk=pk)
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            re_playlist.play_title = form.cleaned_data['play_title']
            re_playlist.save()
            return redirect('my_detail_play')
        else:
            return HttpResponse('문제가 발생했습니다. 다시 시도해주세요.')

    else:
        # 해당 playlist 담긴 Form 전달
        form = PlaylistForm(instance=re_playlist)
        return render(request, 'plist/myPage/playlist_rename.html', {'form': form})



############## My detail에서 확인 가능한 playlist 상세정보 / song 상세정보 ##############

# 내 playlist 상세정보
@login_required
def my_detail_play(request):
    # 내가 추가한 플레이리스트 모두 불러오기
    my_playlists = Playlist.objects.filter(author=request.user)
    info_list = []

    for detail_list in my_playlists:
        list_dict = {}
        song_list = []
        # 해당 플레이리스트에 노래가 없다면 false 처리
        if detail_list.play_list == 'empty':
            verify = False
        # 노래가 있다면 노래 객체불러와서 song_list에 담기    
        else:
            verify = True
            song_id_list = detail_list.play_list.split(',')
            for song_id in song_id_list:
                song = get_object_or_404(Song, pk=song_id)
                song_list.append(song)

        list_dict['my_playlist'] = detail_list
        list_dict['song_list'] = song_list
        list_dict['verify'] = verify
        info_list.append(list_dict)

    return render(request, 'plist/myPage/my_detail_playlist.html', {'info_list': info_list})


# 내가 추가한 song 상세정보
def my_detail_song(request):
    # 관리자계정이면 모든 노래리스트 보여주고
    if request.user.id == 1:
        song_list = Song.objects.all()
    # 일반 사용자면 사용자가 등록한 노래만 보여준다    
    else:
        song_list = Song.objects.filter(author=request.user)
    return render(request, 'plist/myPage/my_detail_song.html', {'song_list':song_list})



############## 관리자권한 가진 사용자만 노래제거 가능 ##############

# 노래 제거(관리자만 가능)
def admin_song_remove(request, pk):
    songs_list = Song.objects.filter(author=request.user)
    # 관리자 계정인지 확인 => 노래제거
    if request.user.id == 1:
        for song in songs_list:
            if song.id == pk:
                songs_list.remove(song)
                song.delete()

    return redirect('my_detail_song')


