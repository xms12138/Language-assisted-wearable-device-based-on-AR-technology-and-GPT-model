from http import HTTPStatus
from dashscope import Generation
import dashscope

# 设置API密钥的值
dashscope.api_key = 'sk-4c8f4e0c985d49d8b4bc327856790942'



def call_with_messages():
    messages = [
{'role': 'user', 'content': '现在北京的天气'}]
     #    {'role': 'user', 'content': '我给你一篇文章，你帮我总结出摘要'}]
    gen = Generation()
    response = gen.call(
        'qwen-max',
        messages=messages,
        result_format='message',  # set the result is message format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    call_with_messages()