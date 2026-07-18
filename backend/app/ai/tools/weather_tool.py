import requests

from langchain.tools import tool

from app.core.config import settings


@tool
def weather_tool(city: str) -> str:
    """
    查询未来三天天气。

    参数：
        city：城市名称，例如广州、北京、上海。

    返回：
        天气描述。
    """

    # 城市查询
    city_url = (
        f"https://{settings.WEATHER_HOST}/geo/v2/city/lookup"
    )

    city_resp = requests.get(
        city_url,
        params={
            "location": city,
            "key": settings.WEATHER_API_KEY,
        },
        timeout=10,
    )

    city_data = city_resp.json()

    print("Geo API 返回：", city_data)

    if city_data.get("code") != "200":
        return f"城市查询失败：{city_data}"

    locations = city_data.get("location")

    if not locations:
        return f"没有找到城市：{city}"

    location = locations[0]

    location_id = location["id"]
    city_name = location["name"]
    province = location["adm1"]

    # 查询天气
    weather_url = (
        f"https://{settings.WEATHER_HOST}/v7/weather/3d"
    )

    weather_resp = requests.get(
        weather_url,
        params={
            "location": location_id,
            "key": settings.WEATHER_API_KEY,
        },
        timeout=10,
    )

    weather_data = weather_resp.json()

    print("Weather API 返回：", weather_data)

    if weather_data.get("code") != "200":
        return f"天气查询失败：{weather_data}"

    today = weather_data["daily"][0]

    return (
        f"{province}{city_name}今日天气："
        f"{today['textDay']}，"
        f"温度 {today['tempMin']}～{today['tempMax']}℃，"
        f"白天风向 {today['windDirDay']}，"
        f"风力 {today['windScaleDay']}级，"
        f"湿度 {today['humidity']}%。"
    )