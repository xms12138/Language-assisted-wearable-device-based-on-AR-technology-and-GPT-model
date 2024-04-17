import pyaudio
import wave
import audioop
import cv2
import time
from http import HTTPStatus
from dashscope import Generation
import json
import dashscope
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import threading
import requests
inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    model_revision="v1.2.4")

# 设置API密钥的值
dashscope.api_key = 'sk-4c8f4e0c985d49d8b4bc327856790942'

dialogue = ""
global content
content = 'Hello, Sun Mingze'
new_audio_in = ""



def get_weather(location_code):
    url = f'https://devapi.qweather.com/v7/weather/now?location={location_code}&key=f23b6fe94e7b4dd88a595ec14e9a5e70'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'code' in data and data['code'] == '200':
            weather = data['now']
            weather_description = weather['text']
            temperature = weather['temp']
            wind_direction = weather.get('windDir', '无')  # 风向，如果不存在，默认为'无'
            wind_speed = weather.get('windScale', '无')  # 风力等级，如果不存在，默认为'无'
            humidity = weather.get('humidity', '无')  # 湿度，如果不存在，默认为'无'
            result = f"天气：{weather_description}\n温度：{temperature}°C\n风向：{wind_direction}\n风力等级：{wind_speed}\n湿度：{humidity}%"
            return result
        else:
            return "无法获取天气信息"
    else:
        return "无法获取天气信息"


def get_current_location_address():
    # 高德 API 密钥
    key = "2f66a8f74e7cd4eb4e67732c6fc446b1"
    # 获取当前位置的经纬度坐标
    url = f"http://restapi.amap.com/v3/ip?key={key}"
    response = requests.get(url)
    data = response.json()
    if data.get("status") == "1" and data.get("info") == "OK":
        address_parts = [data.get("province"), data.get("city"), data.get("district")]
        # 过滤掉空值
        address_parts = [part for part in address_parts if part is not None]
        # 使用join方法连接非空的地区信息
        address = "".join(address_parts)
        return address
    else:
        return "无法获取位置信息"


def get_location_code(city_name):
    # 使用城市搜索接口搜索城市名称
    url = f'https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key=f23b6fe94e7b4dd88a595ec14e9a5e70'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('code') == '200' and data.get('location'):
            location_info = data['location'][0]
            location_code = location_info['id']
            return location_code
    return None

def put_text_multiline(img, text, position, font, font_scale, font_color, thickness, max_line_width):
    lines = []
    font_height = cv2.getTextSize(text, font, font_scale, thickness)[0][1]
    line = ''
    for word in text.split():
        test_line = f'{line} {word}'.strip()
        width = cv2.getTextSize(test_line, font, font_scale, thickness)[0][0]
        if width <= max_line_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    y = position[1]
    for line in lines:
        cv2.putText(img, line, (position[0], y), font, font_scale, font_color, thickness)
        y += font_height


def run():
    #global text
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        exit()
    time_start = time.time()
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = 'Hello, Sun Mingze'
    text_position = (15, 30)
    font_scale = 0.7
    # font_color = (250, 206, 135)
    font_color = (0, 0, 0)
    thickness = 2
    max_line_width = 400  # 最大行宽
    copy = 'Hello, Sun Mingze'

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        put_text_multiline(frame, content, text_position, font, font_scale, font_color, thickness, max_line_width)

        cv2.imshow('VR VIVE', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



my_thread = threading.Thread(target=run)
my_thread.start()


def call_with_messages():
    global dialogue, content
    messages = [
        {'role': 'user', 'content': dialogue}]

    gen = Generation()
    response = gen.call(
        'qwen-max',
        messages=messages,
        result_format='message',  # set the result is message format.
    )
    if response.status_code == HTTPStatus.OK:
        # print(response)
        response_json = json.dumps(response)
        data_dict = json.loads(response_json)
        content = data_dict["output"]["choices"][0]["message"]["content"]
        print()
        # print(content)

        dialogue = dialogue + " " + content
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


while True:

    # 获取用户输入的新的audio_in的值
    new_audio_in = input("输入 'exit' 退出, 输入cont继续: ")

    if new_audio_in != 'cont':
        break  # 如果用户输入 'exit'，退出循环

    # 初始化PyAudio
    audio = pyaudio.PyAudio()

    # 音频参数
    sample_rate = 44100
    channels = 1
    format = pyaudio.paInt16
    frames_per_buffer = 1024
    # 打开音频输入流
    stream = audio.open(format=format, channels=channels, rate=sample_rate, input=True,
                        frames_per_buffer=frames_per_buffer)

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
            if rms > 4000:
                silence_start = None

            else:
                if silence_start is None:
                    silence_start = time.time()
                    # user_input = input("请输入内容（输入 'end' 结束）：")
                    # if user_input == 'end':
                    #     break

                # 如果静默超过3秒，停止录音
                if time.time() - silence_start >= 3:
                    break
        else:
            # 如果不在录音状态，检测rms是否大于200，然后开始录音
            if rms > 3000:
                recording = True
                silence_start = None
                print("有声音了")
        if silence_start != None:
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

    # 提问文本
    query_text = rec_result['text']

    if "天气" in query_text:
        current_address = get_current_location_address()
        location_code = get_location_code(current_address)
        weather_info = get_weather(location_code)
        content = "您的所在地是：" + current_address + weather_info
    else:
        dialogue = dialogue + " " + query_text + "(Answers should be limited to 20 words and answered in English)"

        call_with_messages()

        print(content)
my_thread.join()