import pyaudio
import wave
import time
import audioop
import numpy as np
import pyttsx3
import json
import requests
import subprocess


from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    model_revision="v1.2.4")
API_URL = "https://api-inference.modelscope.cn/api-inference/v1/models/iic/speech_sambert-hifigan_tts_zh-cn_16k"
# 请用自己的SDK令牌替换{YOUR_MODELSCOPE_SDK_TOKEN}（包括大括号）
headers = {"Authorization": f"Bearer 8e6bacf5-2819-4ae2-b220-e09edd95d714"}
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    print(type(response))
    return json.loads(response.content.decode("utf-8"))

from http import HTTPStatus
from dashscope import Generation
import json
import dashscope

# 设置API密钥的值
dashscope.api_key = 'sk-1824b1eb9cab4ce2b6a448e6c176053e'

dialogue = ""

def call_with_messages():
    global dialogue
    messages = [
        {'role': 'user', 'content': dialogue}]


    gen = Generation()
    response = gen.call(
        'qwen-max',
        messages=messages,
        result_format='message',  # set the result is message format.
    )
    if response.status_code == HTTPStatus.OK:
        #print(response)
        response_json = json.dumps(response)
        data_dict = json.loads(response_json)
        content = data_dict["output"]["choices"][0]["message"]["content"]
        print()
        print(content)
        payload = {"input": content, "parameters": {"voice": "zhitian_emo"}}
        output = query(payload)
        audio_url = output['Data']['output_wav']
        audio_data = requests.get(audio_url).content
        with open('output.wav', 'wb') as f:
            f.write(audio_data)
        subprocess.call(["start", "output.wav"], shell=True)
        dialogue = dialogue + " " + content

    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))







while True:
    # 获取用户输入的新的audio_in的值
    new_audio_in = input("输入 'exit' 退出, 输入cont继续: ")

    if new_audio_in == 'exit':
        break  # 如果用户输入 'exit'，退出循环

    # 初始化PyAudio
    audio = pyaudio.PyAudio()

    # 音频参数
    sample_rate = 44100
    channels = 2
    format = pyaudio.paInt16
    frames_per_buffer = 1024
    # 打开音频输入流
    stream = audio.open(format=format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=frames_per_buffer)

    print("开始录音...")

    audio_data_list = []
    recording = False  # 是否正在录音

    silence_start = time.time()

    while True:
        audio_data = stream.read(frames_per_buffer)
        audio_data_list.append(audio_data)

        # 计算RMS值
        rms = audioop.rms(audio_data, 2)

        if recording:
            # 如果正在录音，检测rms是否大于300
            if rms>300:
                silence_start = None
            else:
                if silence_start is None:
                    silence_start = time.time()


                # 如果静默超过3秒，停止录音
                if time.time() - silence_start >= 2:
                    break
        else:
            # 如果不在录音状态，检测rms是否大于200，然后开始录音
            if rms>200:
                recording = True
                silence_start = None
                print("有声音了")
        if silence_start !=None:
            if time.time() - silence_start >= 3:
                break

    # 停止音频流和关闭设备
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 保存录制的音频数据为WAV文件
    output_file = "recorded_audio.wav"
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(audio_data_list))

    print("录音已保存为 WAV 文件:", output_file)


    rec_result = inference_pipeline(audio_in='recorded_audio.wav')


    # 打印结果
    print(rec_result)

    text = rec_result['text']

    dialogue = dialogue + " " + text



    if __name__ == '__main__':
        call_with_messages()
        #print(dialogue)
