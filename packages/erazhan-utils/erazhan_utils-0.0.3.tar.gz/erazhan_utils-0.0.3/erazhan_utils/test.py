# -*- coding = utf-8 -*-
# @time: 2022/2/21 1:21 下午
# @Author: erazhan
# @File: test.py

# ----------------------------------------------------------------------------------------------------------------------

import os
import time
from logging_utils import create_log_file, FileLogger, update_logger, write_logger
from erazhan_utils import get_time

def test_logging_utils():

    app_version = "v122"
    logger_name = "v122"
    app_log_dir = "./"
    project_name = "emr"
    app_log_file = create_log_file(project_name, app_log_dir, app_version)

    the_FH = FileLogger(app_log_dir)
    the_FH.create_logger(app_log_file, logger_name = logger_name) # logger_name = "v5_online"
    the_FH.logger.info("创建初始日志,进程pid:%d"%os.getpid())

    app_log_file = create_log_file(app_log_dir, app_version)
    the_FH.create_logger(app_log_file, logger_name = logger_name)
    text = "测试写入信息"
    write_logger(text,the_FH,info_type= 'info')
    for _ in range(61):
        print(_,get_time())
        time.sleep(1)
    update_logger(the_FH,project_name,app_log_dir,app_version,logger_name)
    text = "重新写入信息"
    write_logger(text, the_FH, info_type='info')

if __name__ == "__main__":
    test_logging_utils()
    pass