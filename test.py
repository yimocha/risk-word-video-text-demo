from moviepy.editor import VideoFileClip

# 替换为你的视频文件路径
video_path = 'E:/视频/111.mp4'
# 替换为你希望保存的音频文件路径
audio_path = 'E:/视频/audio.mp3'

# 加载视频文件
video_clip = VideoFileClip(video_path)

# 提取音频
audio_clip = video_clip.audio

# 保存音频文件
audio_clip.write_audiofile(audio_path)

# 释放资源
audio_clip.close()
video_clip.close()
