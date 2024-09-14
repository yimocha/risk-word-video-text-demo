from pydub import AudioSegment
import speech_recognition as sr

# 音频文件路径
mp3_path = 'E:/视频/audio.mp3'
wav_path = 'E:/视频/audio.wav'

# 将 MP3 转换为 WAV
audio = AudioSegment.from_mp3(mp3_path)
audio.export(wav_path, format='wav')

# 初始化识别器
recognizer = sr.Recognizer()

# 加载音频文件
with sr.AudioFile(wav_path) as source:
    # 录音
    audio_data = recognizer.record(source)

    # 识别音频
    try:
        text = recognizer.recognize_google(audio_data, language='zh-CN')  # 设置为中文，如果需要其他语言，请修改此参数
        print("识别结果：")
        print(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition 无法理解音频")
    except sr.RequestError as e:
        print(f"请求错误; {e}")

# 删除临时的 WAV 文件（可选）
import os

os.remove(wav_path)
