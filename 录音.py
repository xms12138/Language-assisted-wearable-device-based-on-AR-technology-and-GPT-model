import pyaudio
import wave
import time


audio = pyaudio.PyAudio()


sample_rate = 44100  # 采样率
channels = 1         # 声道数（1表示单声道，2表示立体声）
format = pyaudio.paInt16  # 位深度


stream = audio.open(format=format, channels=channels, rate=sample_rate, input=True,
                    frames_per_buffer=1024)  # 设置frames_per_buffer适当的大小

print("开始录音...")

audio_data_list = []
recording_time = 10  # 录音时长（秒）
start_time = time.time()

while time.time() - start_time < recording_time:
    audio_data = stream.read(1024)  # 捕获1024个样本
    audio_data_list.append(audio_data)


stream.stop_stream()
stream.close()
audio.terminate()


output_file = "recorded_audio.wav"
with wave.open(output_file, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(audio_data_list))

print("录音已保存为 WAV 文件:", output_file)


