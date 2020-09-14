from django.db import models

GENRE_CHOICES = (
            ('', 'Select Genre'),
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
            ("", "Select Tag"),
            ('0', "우울할때"),
            ("1", "기분좋아지는"),
            ("2", "노동요"),
            ("3", "가사없는"),
            ("4", "산뜻,상큼한"),
            ("5", "신나는"),
            ("6", "2000년대"),
        )


# 노래 모델
class Song(models.Model):
    # song 제목
    song_title = models.CharField(max_length=100)
    # 아티스트
    song_artist = models.CharField(max_length=30)
    # youtube 링크
    song_url = models.CharField(max_length=400)
    # 장르 (목록에서 선택)
    song_genre = models.CharField(choices=GENRE_CHOICES, max_length=128)
    # 태그 (목록에서 선택)
    song_tag = models.CharField(choices=TAG_CHOICES, max_length=128)
    # 시작 시간
    song_start = models.CharField(max_length=100, null=True)
    # 끝 시간
    song_end = models.CharField(max_length=100, null=True)
    # 이미지 필드
    song_thumbnail = models.ImageField(blank=True, null=True)
    # 노래 상세정보
    song_detail = models.TextField(blank=True, null=True)
    # 노래 추가한 사용자
    author = models.ForeignKey('auth.User', on_delete=models.SET_DEFAULT,default=1)  # ForeignKey 는 class

    def __str__(self):
        return self.song_title + '('+self.song_artist+')'


# playlist 모델
class Playlist(models.Model):
    # playlist 작성자
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # ForeignKey 는 class
    # playlist 제목
    play_title = models.CharField(max_length=200)
    # playlist에 들어가는 노래리스트
    play_list = models.CharField(max_length=200)
    # playlist 상세정보
    play_detail = models.TextField(null=True)

    def __str__(self):
        return self.play_title
