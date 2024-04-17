import pyaudio
import numpy as np
import time

# 参数设置
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 单声道
RATE = 44100  # 采样率
CHUNK = int(0.5 * RATE)  # 窗口大小为0.5秒，根据采样率计算
RECORD_SECONDS = 5  # 录制总时长5秒

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording...")

try:
    rms_values = []  # 用于存储RMS值
    start_time = time.time()

    while time.time() - start_time < RECORD_SECONDS:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(audio_data ** 2))
        rms_values.append(rms)

except KeyboardInterrupt:
    print("Recording stopped.")

stream.stop_stream()
stream.close()
p.terminate()

print(rms_values)
# 计算总录制时间内的平均RMS
average_rms = np.mean(rms_values)
print("Average RMS over {} seconds: {:.2f}".format(RECORD_SECONDS, average_rms))
