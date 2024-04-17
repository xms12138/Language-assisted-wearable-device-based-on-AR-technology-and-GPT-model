import requests


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


# if __name__ == "__main__":
#     current_address = get_current_location_address()
#     location_code = get_location_code(current_address)
#     weather_info = get_weather(location_code)
#     print("您的所在地是："+current_address)
#     print(weather_info)

def weather_runs():
    current_address = get_current_location_address()
    location_code = get_location_code(current_address)
    weather_info = get_weather(location_code)
    print("您的所在地是：" + current_address)
    print(weather_info)
