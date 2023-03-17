import pandas as pd
from organizer import *
day = 3
hour = 17
minute = 0
step = 2
a, v, b, vw, time_limit = time_div_step(day, hour, minute, step)

start, end = give_default_dates(day_back=day, hour_back=hour, min_back=minute)
crap_bool = True
print("yeha")
print(time_limit)
hold1 = 0
hold2 = hour+day*24
hold3 = minute
# day w day-hold1

# 0,1,2,3...,divider-1, runs divider times
# oldu gibi
for count_time in range(time_limit):
    print(count_time, hold1,hold2,hold3)
    f, s, t, fo,ww = time_div_step(hold1, hold2, hold3, 2)
    print(f,s,t,fo)
    start, end = give_default_dates(day_back=hold1, hour_back=hold2, min_back=hold3, end_recent_day=hold1,
                                    end_recent_hour=hold2 - s, end_recent_min=hold3 - t)
    print(start,end)
    #temp_data3, temp_data2, save, devices, non_saved_log, titles_node = do_main(start, end, step)
    #temp_data2 = pd.DataFrame(temp_data2, columns=titles_node)
    print("here is : ")
    #if crap_bool:
    #    hold = temp_data2
    #    crap_bool = False

    #else:
    #    hold = pd.concat((hold, temp_data2), axis=0)

    hold1 = f
    hold2 = hold2 - s
    hold3 = hold3 - t
    hold4 = fo
