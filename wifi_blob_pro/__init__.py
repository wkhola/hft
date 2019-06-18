#!/usr/bin/python
# encoding:utf-8

# import time
#
# L1 = "2649821731631836529481632803462831616487712734074314936141303241873417434716340124362304724324324324324323412121323164329751831"
# L2 = "1045091731748365195814509145981509438583247509149821493213241431431319999999999999999999999999999999999999999999999999341344779"
#
# startTime = time.time()
# # 长度强行扭转到一致 不够前面补0
# max_len = len(L1) if len(L1) > len(L2) else len(L2)
# l1 = L1.zfill(max_len)
# l2 = L2.zfill(max_len)
#
# a1 = list(l1)
# a2 = list(l2)
# # 长度一致 每个对应的位置的相加的和 %10 前一位补1 如果>10 否则0  99+99最大3位所以多一位
# a3 = [0] * (max_len + 1)
#
# for index in range(max_len - 1, -1, -1):
#     index_sum = a3[index + 1] + int(a1[index]) + int(a2[index])
#     less = index_sum - 10
#     a3[index + 1] = index_sum % 10
#     a3[index] = 1 if less >= 0 else 0
# if a3[0] == 0:
#     a3.pop(0)
# a33 = [str(i) for i in a3]
# print(''.join(a33))
# print('耗时{0}ms'.format(time.time() - startTime))

event = dict({
    "actors": {
        "L": [{
            "S": "Fay Wray"
        }, {
            "S": "Robert Armstrong"
        }, {
            "S": "Bruce Cabot"
        }]
    },
    "directors": {
        "L": [{
            "S": "Merian C. Cooper"
        }, {
            "S": "Ernest B. Schoedsack"
        }]
    },
    "genres": {
        "L": [{
            "S": "Adventure"
        }, {
            "S": "Fantasy"
        }, {
            "S": "Horror"
        }]
    },
    "image_url": {
        "S": "http://ia.media-imdb.com/images/M/MV5BMTkxOTIxMDU2OV5BMl5BanBnXkFtZTcwNjM5NjQyMg@@._V1_SX400_.jpg"
    },
    "plot": {
        "S": "A film crew goes to a tropical island for an exotic location shoot and discovers a colossal giant gorilla who takes a shine to their female blonde star."
    },
    "rank": {
        "N": "3551"
    },
    "rating": {
        "N": "8"
    },
    "release_date": {
        "S": "1933-03-07T00:00:00Z"
    },
    "running_time_secs": {
        "N": "6000"
    }
})
from pyecharts import Bar
bar = Bar("我的第一个图表", "这里是副标题")
bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
# bar.print_echarts_options()
bar.render(path='snapshot.gif')
bar.render(path='snapshot.png')
bar.render(path='snapshot.pdf')

