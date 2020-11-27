"""
大公司市值排名脚本
"""
import asyncio
import http.client
import json
import urllib.parse
from typing import Dict

CODE_MAP = {
    "NASDAQ:AAPL": "苹果",
    "NASDAQ:AMZN": "亚马逊",
    "NASDAQ:MSFT": "微软",
    "NASDAQ:GOOGL": "谷歌",
    "NASDAQ:FB": "FB",
    "NASDAQ:NVDA": "英伟达",
    "NASDAQ:ADBE": "Adobe",
    "NASDAQ:NFLX": "网飞",
    "NASDAQ:INTC": "英特尔",
    "NASDAQ:DIS": "迪士尼",
    "NASDAQ:TSLA": "特斯拉",
    # 中国公司
    "NASDAQ:BABA": "阿里",
    "HK:00700": "腾讯",
    "NASDAQ:TSM": "台积电",
    "HK:03690": "美团",
    "NASDAQ:PDD": "拼多多",
    "NASDAQ:JD": "京东",
    "HK:01810": "小米",
    "NASDAQ:BIDU": "百度",
    "NASDAQ:IQ": "爱奇艺",
    "NASDAQ:TCOM": "携程",
    "NASDAQ:BILI": "B站",
    "NASDAQ:MOMO": "陌陌",
    "NASDAQ:DADA": "达达",
    "NASDAQ:NIO": "蔚来",
    "NASDAQ:XPEV": "小鹏",
    "NASDAQ:LI": "理想",
}

CONN = http.client.HTTPSConnection("api.readhub.cn", timeout=3)


def _market_cap(stock_code: str) -> float:
    """
    获取市值数据
    """
    params = urllib.parse.urlencode({"code": stock_code})
    CONN.request(
        "GET",
        f"/finance/companyStock?{params}",
        headers={
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
            )
        },
    )
    res = CONN.getresponse()
    if res.status == 200:
        result = json.loads(res.read().decode("utf-8"))
        cap = result.get("data", {}).get("marketCapital", "")
        if "亿美元" in cap:
            mkt_value = float(cap.rstrip(" 亿美元"))
            return mkt_value

    return 0


def _output(result: Dict[str, float]) -> None:
    """
    输出内容
    """
    items = sorted(result.items(), key=lambda x: x[1], reverse=True)
    for rank, (name, value) in enumerate(items, start=1):
        print(f"{rank:02}. {name:8}\t{value:15.2f} 亿美元")


async def main() -> None:
    """
    主函数
    """
    loop = asyncio.get_event_loop()
    ret: Dict[str, float] = {}
    for code, name in CODE_MAP.items():
        result = loop.run_in_executor(None, _market_cap, code)
        ret[str(name)] = await result

    _output(ret)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
