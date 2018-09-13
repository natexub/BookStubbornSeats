#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import datetime
import json
import logging
import threading
import time

from __init__ import *
from libapi.login_exception import LoginException

units = Queue.Queue()


def json_file(filename='seat.json'):
    with open(filename, 'r') as f:
        seats_json = json.load(f)
    return seats_json


def login_one(ti, seat):
    try:
        p = ujnlib(ti['username'], ti['password'])
        units.put((p, (seat['room_id'], seat['seat_num']), (ti['begin'], ti['end'])))
    except LoginException as exception:
        logging.error(exception.err)


def reserve_one(p, seat, ti, is_tomorrow):
    if is_tomorrow != 1:
        try:
            p.setDateTomorrow()
        except IndexError as exception:
            p.quick(4)
        n_max_0 = 10
        while not logging.info("还未获取到日期,1s后开始重试...倒数%s次" % n_max_0) and n_max_0:
            time.sleep(1)
            n_max_0 -= 1

    n_max = 20
    while not p.book(ti[0], ti[1], seat[0], seat[1]) and n_max:
        logging.info("1s后开始重试...倒数%s次" % n_max)
        time.sleep(1)
        n_max -= 1



# 多线程登录
def login_all(lists):
    threads_login = []
    i = 0
    for per in lists:
        for ti in per['times']:
            t = threading.Thread(target=login_one, name='LoginThread-%s' % i, args=(ti, per))
            threads_login.append(t)
            i += 1
    n_threads = range(len(threads_login))
    for i in n_threads:
        threads_login[i].start()
    for i in n_threads:
        threads_login[i].join()


def wait_to(target_time):
    logging.info("等待到达指定时间...")
    str_target = str(datetime.datetime.now().date()) + " " + target_time
    struct_time_target = time.strptime(str_target, "%Y-%m-%d %H:%M:%S")
    stamp_target = time.mktime(struct_time_target)
    stamp_now = time.time()
    stamp_interval = stamp_target - stamp_now
    if stamp_interval > 0:
        time.sleep(stamp_interval)


def reserve_all(is_tomorrow):
    logging.info("开始运行")
    # obj,seat,time的数目一一对应,三个list一样长
    objs, seats, times = [], [], []

    lists = json_file()
    login_all(lists)

    # 将登录所得结果集分开
    while not units.empty():
        unit = units.get()
        objs.append(unit[0])
        seats.append(unit[1])
        times.append(unit[2])
    wait_to("05:00:03")

    # 多线程预约
    threads_reserve = []
    for i in range(len(objs)):
        t = threading.Thread(target=reserve_one, name='ReserveThread-%s' % i,
                             args=(objs[i], seats[i], times[i], is_tomorrow))
        threads_reserve.append(t)
    n_threads = range(len(threads_reserve))
    for i in n_threads:
        threads_reserve[i].start()
    for i in n_threads:
        threads_reserve[i].join()

    logging.info("结束")


def check_in():
    seats = json_file()
    hour = int(time.strftime("%H"))
    # date = time.strftime("%Y-%-m-%-d")
    accounts = []
    for seat in seats:
        for t in seat['times']:
            if t['begin'] == str(hour) or t['begin'] == str(hour + 1):
                p = ujnlib(t['username'], t['password'])
                p.checkIn()


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'c':
            check_in()
        elif sys.argv[1] == 'r':
            reserve_all(2)
    except IndexError as e:
        print("参数c:签到\n参数r:预约")
