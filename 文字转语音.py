import json
import requests
import subprocess
API_URL = "https://api-inference.modelscope.cn/api-inference/v1/models/iic/speech_sambert-hifigan_tts_zh-cn_16k"
# 请用自己的SDK令牌替换{YOUR_MODELSCOPE_SDK_TOKEN}（包括大括号）
headers = {"Authorization": f"Bearer 8e6bacf5-2819-4ae2-b220-e09edd95d714"}
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    print(type(response))
    return json.loads(response.content.decode("utf-8"))
payload = {"input": "你在狗叫什么啊。你在狗叫什么！", "parameters": {"voice": "zhitian_emo"}}
output = query(payload)
audio_url = output['Data']['output_wav']
audio_data = requests.get(audio_url).content
with open('output.wav', 'wb') as f:
    f.write(audio_data)
subprocess.call(["start", "output.wav"], shell=True)

