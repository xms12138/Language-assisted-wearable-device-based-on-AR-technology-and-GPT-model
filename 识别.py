from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    model_revision="v1.2.4")

rec_result = inference_pipeline(audio_in='recorded_audio.wav')


while True:
    # 获取用户输入的新的audio_in的值
    new_audio_in = input("请输入新的audio_in的值（或输入 'exit' 退出）: ")

    if new_audio_in == 'exit':
        break  # 如果用户输入 'exit'，退出循环

    # 使用新的audio_in值运行inference_pipeline
    rec_result = inference_pipeline(audio_in=new_audio_in)

    # 打印结果
    print(rec_result)
