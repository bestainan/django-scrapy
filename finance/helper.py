# coding:utf-8
import datetime
import pytz
import requests
import tushare
from django.conf import settings

TZ = pytz.timezone('Asia/Shanghai')


class TushareStock(object):
    def __init__(self, code='600848', type='D'):
        self.code = code
        self.history_data = tushare.get_k_data(code=code,ktype=type)

    def yesterday_formart(self):
        # 要判断是否过了3点
        now_day = datetime.datetime.now(TZ)
        if now_day.hour > 15:
            # 大于15点就拿当日的记录
            return now_day.strftime('%Y-%m-%d')

        yesterday = now_day - datetime.timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')

    def day_formart(self, days):
        time = datetime.datetime.now(TZ) - datetime.timedelta(days=days)
        return time.strftime('%Y-%m-%d')

    def yesterday_open_price(self):
        # 昨日开盘价
        return self.history_data.tail(2).head(1).iloc[0]['open']

    def yesterday_high_price(self):
        # 昨日最高价
        return self.history_data.tail(2).head(1).iloc[0]['high']

    def yesterday_low_price(self):
        # 昨日最低价
        return self.history_data.tail(2).head(1).iloc[0]['low']

    def today_buy_point(self):
        # 今日买点 :昨日 ((开盘价 + 最高价 + 最低价) / 3 * 2 * (3 - 1)) / (3 + 1)
        open = self.yesterday_open_price()
        high = self.yesterday_high_price()
        low = self.yesterday_low_price()
        return (sum([open, high, low]) / 3 * 2 * (3 - 1)) / (3 + 1)

    def stop_loss(self):
        # 止损价 昨日开盘价*0.95
        open = self.yesterday_open_price()
        return open * 0.95

    def stop_make_money(self):
        # 止盈价：昨天的最高价*0.95
        return self.history_data.tail(2).head(1).high.values[0]

    def drag(self):
        # 阻力价：不包括当天 有开盘的 交易日的  19日内最高价的最高值
        return tushare.get_hist_data(code=self.code).head(19).high.max()

    def tomorrow_buy_point(self):
        # 明日买点：（昨日最低价 - 昨日开盘价 * 0.95） / 5 + 昨日最低价
        open = self.yesterday_open_price()
        low = self.yesterday_low_price()
        return (low - open * 0.95) / 5 + low

    def yesterday_prediction_point(self):
        # 昨测今日买点：1日前的((开盘价+最高价+最低价)/3*2*(4-1))/(4+1)+((最高价+最低价)/2-3日前的(开盘价+最高价+最低价)/3）/4
        return ''

    # def code_base_info(self):
    #     context = {}
    #     df = tushare.get_realtime_quotes(self.code)  # Single stock symbol
    #     context['name'] = df[['name']].iloc[0]['name']
    #     context['price'] = df[['price']].iloc[0]['price']
    #     context['open'] = df[['open']].iloc[0]['open']
    #     context['height'] = df[['high']].iloc[0]['high']
    #     context['low'] = df[['low']].iloc[0]['low']
    #     context['time'] = df[['date']].iloc[0]['date'] + '  ' + df[['time']].iloc[0]['time']
    #     return context


def stock_info(code):
    context = {}
    headers = {
        'Authorization': 'APPCODE ' + settings.ALIYUN_STOCK_APP_CODE
    }
    url = 'http://ali-stock.showapi.com/real-stockinfo?code={code}&needIndex=1&need_k_pic=1'.format(code=code)
    res = requests.get(url, headers=headers)
    res = res.json()['showapi_res_body']['stockMarket']
    context['name'] = res['name']
    context['price'] = res['nowPrice']
    context['open'] = res['openPrice']
    context['height_price'] = res['highLimit']
    context['low'] = res['downLimit']
    context['time'] = res['date'] + ' ' +res['time']
    return context