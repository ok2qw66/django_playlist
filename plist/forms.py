from django import forms
from .models import Song, Playlist
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


# 플레이리스트 추가 폼
class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('play_title',)
        widgets = {
            'play_title': forms.TextInput(attrs={'class': 'form-control','placeholder':'플레이리스트 제목을 입력하세요'}),
        }
        labels = {
            'play_title': '',
        }


# 노래 추가 폼
class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('song_title','song_artist','song_url','song_genre'\
                  ,'song_tag','song_start','song_end','song_detail',)
        GENRE_CHOICES = (
            ('0', '가요'),
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
        widgets = {
            'song_genre': forms.Select(choices=GENRE_CHOICES, attrs={'class': 'form-control'}),
            'song_title': forms.TextInput(attrs={'class': 'form-control'}),
            'song_artist': forms.TextInput(attrs={'class': 'form-control'}),
            'song_url': forms.TextInput(attrs={'class': 'form-control'}),
            'song_tag': forms.Select(choices=TAG_CHOICES, attrs={'class': 'form-control'}),
            'song_start': forms.TextInput(attrs={'class': 'form-control','placeholder':'시:분:초 형태로 입력\t\tex) 0분 0초   0:0'}),
            'song_end': forms.TextInput(attrs={'class': 'form-control','placeholder':'시:분:초 형태로 입력\t\tex) 1시간 5초   1:0:5'}),
            'song_detail': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'song_title': '노래 제목',
            'song_artist': '가수',
            'song_url': 'Youtube URL',
            'song_genre': '장르',
            'song_tag': '노래 태그',
            'song_start': '시작시간',
            'song_end': '종료시간',
            'song_detail': '노래 상세 정보'
        }