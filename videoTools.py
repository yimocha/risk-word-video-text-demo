import os

import moviepy.editor as mp
import speech_recognition as sr


def video_to_text(video_path):
    # 从视频中提取音频
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    temp_audio_file = "temp_audio.wav"
    audio.write_audiofile(temp_audio_file)

    # 识别音频中的文字
    r = sr.Recognizer()
    with sr.AudioFile(temp_audio_file) as source:
        audio_data = r.record(source)
    try:
        text = r.recognize_google(audio_data, language='zh-CN')  # 设置为中文，如果需要其他语言，请修改此参数
        return text
    except sr.UnknownValueError:
        print("无法识别音频内容")
    except sr.RequestError as e:
        print(f"请求错误：{e}")
    finally:
        # 删除音频
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)

# video_path = "E:/视频/111.mp4"
# print(video_to_text(video_path))
