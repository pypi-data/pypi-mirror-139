import time

# 别人的一处错误: 关于tm_wday
# -->这个里面就是错的:https://www.runoob.com/python/att-time-localtime.html
# int tm_wday; /* 星期 – 取值区间为[0,6]，其中0代表星期天，1代表星期一，以此类推 */

t = time.localtime()
print(t.tm_wday)  # 2 是星期三  5是星期六

# CTRL+B进入源码 朝上面翻了下:  weekday (0-6, Monday is 0)  星期一是0
