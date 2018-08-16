# *- coding:utf8 *-
import datetime
import re
"""
统一日期交互格式 
存进数据是 20180414182524
传给前端是 2017-08-06 12:35:26
"""
format_for_db = '%Y%m%d%H%M%S'
format_for_web_second = '%Y-%m-%d %H:%M:%S'
re_format_for_web = r"^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$"
format_forweb_no_second = '%Y-%m-%d %H:%M'
format_forweb_no_HMS = "%Y-%m-%d"


def get_db_time_str(time_info=None):
    if time_info:
        if re.match(re_format_for_web, time_info):
            return datetime.datetime.strptime(time_info, format_for_web_second).strftime(format_for_db)
        else:
            return datetime.datetime.strptime(time_info, format_forweb_no_second).strftime(format_for_db)
    return datetime.datetime.now().strftime(format_for_db)


def get_web_time_str(time_str, formattype=format_for_web_second):
    return datetime.datetime.strptime(time_str, format_for_db).strftime(formattype)
