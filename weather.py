#!/usr/bin/env python
# -*- coding:utf-8 -*-
# API 说明
# https://dev.heweather.com/docs/api/weather

import sys
from datetime import date
from workflow import Workflow3, web

reload(sys)
sys.setdefaultencoding("utf8")

API_KEY = "405fb5e9d79a4215a4a32d61241a5849"
url = "https://free-api.heweather.net/s6/weather/now?"
kv = {"User-Agent": "Mozilla/5.0"}


def query_weather(query):
    """获取天气数据"""
    data = {"location": query, "key": API_KEY}
    r = web.get(url, params=data, headers=kv)
    r.raise_for_status()
    weather = r.json()
    return weather


def main(wf):
    query = wf.args[0]
    resoults = query_weather(query=query)
    d = resoults["HeWeather6"][0]
    city = d["basic"]["location"]

    day = d["now"]
    nowdate = date.today()  # 获取今天的日期
    title = "{}\t{}\t{}".format(city, nowdate, day["cond_txt"])
    subtitle = """温度:{0}℃|湿度:{1}%|风向:{2}|降水量:{3}""".format(
        day["tmp"], day["hum"], day["wind_dir"], day["pcpn"]
    )

    # 向alfred添加条目,传标题、副标题、
    # 图片路径(图片直接用的和风天气提供的天气图,每个图片的命名对应天气状态码)

    wf.add_item(
        title=title,
        subtitle=subtitle,
        valid=True,
        icon="images/{code}.png".format(code=day["cond_code"]),
    )
    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
