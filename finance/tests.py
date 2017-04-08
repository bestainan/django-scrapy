# #!/usr/bin/env python
# # -*- coding: gb2312 -*-
# from mongoengine import *
# import time
# import datetime
# # import TradeX
#
# MARKETS = [
#     {13: '111081'},
#     {13: '111082'},
# ]
# TIME_FORMAT = {
#     0: '%Y-%m-%d %H:%M',
#     1: '%Y-%m-%d %H:%M',
#     2: '%Y-%m-%d %H:%M',
#     3: '%Y-%m-%d %H:%M',
#     4: '%Y%m%d',
#     5: '%Y%m%d',
#     6: '%Y%m%d',
#     7: '%Y-%m-%d %H:%M',
#     8: '%Y-%m-%d %H:%M',
#     9: '%Y%m%d',
#     10: '%Y%m%d',
#     11: '%Y%m%d',
# }
#
# MONGO_HOST = 'dds-m5ea0fc94e106de42.mongodb.rds.aliyuncs.com'
# MONGO_PORT = 3717
# MONGO_DATABASE = 'finance'
# MONGO_USERNAME = 'root'
# MONGO_PASSWORD = '1234qwer'
#
# connect(MONGO_DATABASE, host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME,
#         password=MONGO_PASSWORD)
#
#
# class FuturesTimeSharing(Document):
#     market = IntField()
#     code = StringField(max_length=32)
#     update_time = DateTimeField()
#     list_data = ListField()
#
#
# class FuturesK(Document):
#     market = IntField()
#     type = IntField()
#     code = StringField(max_length=32)
#     update_time = DateTimeField()
#     list_data = ListField()
#
#
# class Finance(object):
#     def __init__(self, host="59.175.238.38", port=7727):
#         self.host = host
#         self.port = port
#         self.content_server()
#
#     def item_infomation(self, market_num, item_name):
#         res = self.conn.GetInstrumentQuote(market_num, item_name)
#
#         return self.__format_data(res)
#
#     def content_server(self):
#         while 1:
#             try:
#                 self.conn = TradeX.TdxExHq_Connect(self.host, self.port)
#                 break
#             except:
#                 pass
#
#     def reload_server(self):
#         del self.conn
#         self.content_server()
#         print u'�������ӳɹ�'
#
#     def item_K(self, market, item_name, start=1, count=200, d_type=9):
#         """
#         type:K������
#                 0 = 5����K��
#                 1 = 15����K��
#                 2 = 30����K��
#                 3 = 1СʱK��
#                 4 = ��K��
#                 5 = ��K��
#                 6 = ��K��
#                 7 = 1����
#                 8 = 1����K��
#                 9 = ��K��
#                 10 = ��K��
#                 11 = ��K��
#         """
#         while 1:
#             res = self.conn.GetInstrumentBars(d_type, market, item_name, start, count)
#             if '10038' in res[0]:
#                 self.reload_server()
#             else:
#                 break
#         return self.__format_data(res, time_format=TIME_FORMAT[d_type])
#
#     def time_sharing(self, market, item_name, start=0, count=200):
#         # ��ʱͼ
#         res = self.conn.GetTransactionData(market, item_name, start, count)  # count Ϊ����
#         return self.__format_data(res)
#
#     def __format_data(self, res, time_format='%Y-%m-%d %H:%M'):
#         context = {
#             "t": [],
#             "c": [],
#             "o": [],
#             "h": [],
#             "l": [],
#             'v': [],
#             'b': [],
#             'g': [],
#             "s": "ok"
#         }
#         u"tʱ��0	o���̼�1	h��߼�2	l��ͼ�3	c���̼�4	�ֲ�5	�ɽ�6	����7"
#         values = res[1].split('\n')[1:]
#
#         for _line_value in values:
#             _line_data = _line_value.split('\t')
#             _timestamp = int(time.mktime(time.strptime(_line_data[0], time_format)))
#             context['t'].append(_timestamp)
#             context['c'].append(float(_line_data[4]))
#             context['o'].append(float(_line_data[1]))
#             context['h'].append(float(_line_data[2]))
#             context['l'].append(float(_line_data[3]))
#             context['v'].append(int(_line_data[6]))
#             context['b'].append(float(_line_data[7]))
#             context['g'].append(int(_line_data[5]))
#         return context
#
#
# if __name__ == '__main__':
#     f = Finance()
#
#     res = f.item_K(13, '111081', d_type=9)
#     for i in xrange(20):
#         _datetime = datetime.datetime.now()
#         print _datetime.strftime('%Y-%m-%d %H:%M:%S')
#         try:
#             for market in MARKETS:
#                 for _market, name in market.iteritems():
#                     # res = f.time_sharing(_market, name)
#                     # FuturesTimeSharing.objects(market=_market, code=name).update_one(
#                     #     list_data=res,
#                     #     update_time=_datetime,
#                     #     upsert=True
#                     # )
#                     for _index in xrange(12):
#                         res = f.item_K(_market, name, d_type=_index)
#                         if res['t']:
#                             FuturesK.objects(market=_market, code=name, type=_index).update_one(
#                                 list_data=res,
#                                 update_time=_datetime,
#                                 upsert=True
#                             )
#         except:
#             pass
