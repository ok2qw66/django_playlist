from pydub import AudioSegment
import os

STATIC_SONG_PATH = '/home/django_playlist/plist/static/plist/audio/'


# 초 계산 함수
# 입력값 예시   9:10
def find_sec(input_time):
    input_time = str(input_time)
    print(input_time)
    min_sec = input_time.split(':')

    if len(min_sec) ==3 :
        return input_time
    else :
        return '00:'+input_time

    #return int(hour)*60*60*1000 + int(min) * 60 * 1000 + int(sec) * 1000

# print(find_sec('9:10'))


# mp3 slice 함수
def song_slice(song_name,start,end):

    # 시작/종료 초 가져오기
    # Time to miliseconds
    startTime = find_sec(start)
    endTime = find_sec(end)
    print(startTime, endTime)

    try:
        # Opening file and extracting segment
        audio_file = STATIC_SONG_PATH+song_name
        
        #song = AudioSegment.from_mp3(audio_file)
        #extract = song[startTime:endTime]
        ## Saving
        #extract.export(audio_file, format='mp3')
        
        os.system(f'ffmpeg -ss {startTime} -to {endTime} -i {audio_file}"_ori.mp3" -c copy {audio_file}".mp3"')  
        os.system(f'cd {STATIC_SONG_PATH}')
        os.system(f'rm {audio_file}_ori.mp3')
        print("finish mp3 slice!")
    except Exception as e:
        print('error:',e)


if __name__ == '__main__':
    print(find_sec('9:10'))
    song_slice('when','20:03','23:24')
