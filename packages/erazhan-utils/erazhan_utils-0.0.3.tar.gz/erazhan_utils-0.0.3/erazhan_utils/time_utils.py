# -*- coding = utf-8 -*-
# @time: 2022/2/18 5:49 下午
# @Author: erazhan
# @File: time_utils.py

# ----------------------------------------------------------------------------------------------------------------------
import time

def backto_Ndays(N):
    cutoff_time=time.strftime('%Y-%m-%d', time.localtime(time.time()-86400*(N-1)))+" 00:00:00"
    return cutoff_time

def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def get_today():
    return time.strftime("%Y%m%d")

if __name__ == "__main__":
    pass