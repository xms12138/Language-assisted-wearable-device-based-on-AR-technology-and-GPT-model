# import pyaudio
# import wave
# import time
# import audioop
# import numpy as np
#
# # 初始化PyAudio
# audio = pyaudio.PyAudio()
#
# # 音频参数
# sample_rate = 44100
# channels = 2
# format = pyaudio.paInt16
# frames_per_buffer = 1024
#
# # 打开音频输入流
# stream = audio.open(format=format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=frames_per_buffer)
#
# print("开始录音...")
#
# audio_data_list = []
# recording = False  # 是否正在录音
#
# silence_start = None
#
# while True:
#     audio_data = stream.read(frames_per_buffer)
#     audio_data_list.append(audio_data)
#
#     # 计算RMS值
#     rms = audioop.rms(audio_data, 2)
#     print(rms)
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


ans = pipeline(
    Tasks.acoustic_noise_suppression,
    model='damo/speech_frcrn_ans_cirm_16k')
result = ans(
    'C:/Users/HZH/Desktop/语音识别/recorded_audio.wav',
    output_path='output.wav')
