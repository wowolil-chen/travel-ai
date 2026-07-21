import requests

from langchain.tools import tool

from app.core.config import settings


@tool
def weather_tool(location: str) -> str:
    """
    查询未来三天天气。

    参数：
        location：地点名称。

    推荐传入：
        区县 > 城市 > 省份

    例如：
        祁连县
        广州市
        林芝市
        拉萨市
    """

    # =========================
    # 查询 LocationID
    # =========================

    geo_url = f"https://{settings.WEATHER_HOST}/geo/v2/city/lookup"

    geo_resp = requests.get(
        geo_url,
        params={
            "location": location,
            "key": settings.WEATHER_API_KEY,
        },
        timeout=10,
    )

    geo_data = geo_resp.json()

    print("Geo API：", geo_data)

    if geo_data.get("code") != "200":
        return "天气查询失败，无法解析地点。"

    locations = geo_data.get("location", [])

    if not locations:
        return "没有找到对应天气地点。"

    place = locations[0]

    location_id = place["id"]

    province = place["adm1"]

    city = place["name"]

    # =========================
    # 查询天气
    # =========================

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

    print("Weather API：", weather_data)

    if weather_data.get("code") != "200":
        return "天气查询失败。"

    daily = weather_data["daily"]

    result = []

    result.append(f"{province}{city}未来三天天气：")

    for day in daily:

        result.append(
            f"""
日期：{day['fxDate']}
白天：{day['textDay']}
夜晚：{day['textNight']}
温度：{day['tempMin']}～{day['tempMax']}℃
降水概率：{day['precip']}%
风向：{day['windDirDay']}
风力：{day['windScaleDay']}级
湿度：{day['humidity']}%
""".strip()
        )

    return "\n\n".join(result)