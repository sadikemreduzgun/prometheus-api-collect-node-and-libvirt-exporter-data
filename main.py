from organizer import *
import pandas as pd
import requests as rq
import numpy as np
from datetime import date
from reach_time import *
from check import check_installed


day = 0
hour = 12
minute = 0
# define default step and query function step
step = "2s"
# read csv which contains queries

# get default-recent time data

# start = "2023-02-21T10:59:25.479Z"
# end = "2023-02-21T19:59:25.479Z"
# start = "2023-02-27T06:22:25.479Z"
# end= "2023-02-28T07:39:25.479Z"
node_exist, libvirt_exist = check_installed()

if not node_exist:
    print("please install node exporter to monitored machine. ")
    exit()

if not libvirt_exist:
    print("please install libvirt exporter to monitored machine.")
    exit()


def do_main(start, end, step, step_func="5s"):

    queries = []
    df = pd.read_csv('all_queries.csv')
    df_nodes = pd.read_csv("node_queries.csv")
    df_libvs = pd.read_csv("libvirt_queries.csv")
    # define a boolean to be used to run a statement for once
    one_crap_boolean = True
    # get Virtual machine names
    devices = reach_device(start, end)
    # a weird boolean too, to execute a statement once
    two_crap_boolean = True
    # define a list to store query names which returns no data and save them in var/log.txt
    non_saved_log = []
    # define lists for to store column names
    titles = ["time_stamp"]
    titles_node = ["time_stamp"]
    titles_node_less = []
    title_count_lib = 0
    # read queries, organize them and gather their values
    # df.iloc[:, 2], df.iloc[:, 1]
    handling_bool = True
    # booleans to execute a statement for each loop turn
    three_crap_boolean = True
    four_crap_boolean = True

    for name, col in df_nodes.iterrows():

        query_name = col["query_name"]
        query = col["query"]

        # get instance to run curly organizer function
        instance = "{instance=" + f'{return_instance("node")}' + "}"
        # run curly organizer delete instance and replace it
        url = curly_organizer(query, instance, step_func)
        # get data after organizing the url
        url = organize_url(url, start, end, step)
        # hold URL to be used later
        hold = url
        # get data using requests modul
        metrics = rq.get(url)
        # load data into json
        print(url)
        data = metrics.json()

        try:
            if len(data['data']['result']) == 0:
                non_saved_log.append(str(datetime.now()) + "\tnode -> " + query_name)
                continue
        except:
            print("Potential time error. Please check if start and end times relevant.")
            non_saved_log.append("an error occured:\tERROR IN MAIN LOOP! ")
            continue
        # parse data
        # print("\n\n")
        # print(query_name)
        # print("number of data: ", len(data['data']['result'][0]['values']))

        all_data = np.array(data['data']['result'][0]['values'])
        # print("shape of numpy array: ", all_data.shape)
        # print("len([data][result]): ", len(data['data']['result']))
        # get metric data
        metric = all_data[:, 1][np.newaxis]
        # get time stamp data
        time_stamp = all_data[:, 0][np.newaxis]
        # titles_node.append(query_name)
        # metric = metric.apply(lambda x: GiB(float(x)), axis=1)
        # for executing just once

        if two_crap_boolean:
            temp_data2 = np.concatenate((time_stamp.T, metric.T), axis=1)
            two_crap_boolean = False
            titles_node.append(query_name)
        # merge data collectively
        else:
            # try to concate metrics because if length of metrics are different it returns error
            try:
                # connect metrics
                temp_data2 = np.concatenate((temp_data2, metric.T), axis=1)
                # add to columns list of df
                titles_node.append(query_name)
            # if metrics length is different, then this is executed to run it without interruption.
            # There is a problem like when the start and end time are close to the time now, we have a lenght which is 4 smaller than normal.
            except:
                # add query name to columns's list
                titles_node_less.append(query_name)
                # execute once to have something to concatenate
                if handling_bool:
                    temp_data3 = metric.T
                    handling_bool = False
                # conneect metrics
                else:
                    temp_data3 = np.concatenate((temp_data3, metric.T), axis=1)

    for name, col in df_libvs.iterrows():

        query_name = col["query_name"]
        query = col["query"]
        # a counter of device loop
        in_count = 1
        # processes of devices taken by a function
        for device in devices:
            # assign instance to run curly organizer function
            instance = "{instance=" + f'{return_instance("libvirt")}'+ ",domain=" + f'"{device}"'+"}"
            # run curly organizer delete instance and replace it
            url = curly_organizer(query, instance, step_func)
            # get data after organizing the url
            url = organize_url(url, start, end, step)
            # get data using requests modul
            metrics = rq.get(url)
            # turn data into dictionary
            metrics = metrics.json()
            # hold metrics data
            temp_metrics = metrics
            # move depending on if data is reached

            try:
                if len(temp_metrics['data']['result']) == 0:
                    now = str(datetime.now())
                    # save queries which returns no data
                    if query_name not in queries:
                        queries.append(query_name)
                        non_saved_log.append(str(datetime.now()) + "\tlibvirt -> " + query_name)
                        continue
                else:
                    # parse and dig into data
                    data = metrics['data']['result'][0]['values']
                    # load data into a numpy array
                    data = np.array(data)
                    # get metric values
                    metric = data[:, 1][np.newaxis]
                    # get time stamp values
                    time_stamp = data[:, 0][np.newaxis]
                    # for executing for 4 times
                    if one_crap_boolean:
                        # to create following structure:
                        """ time stamp: ts, metric = m
                        ts (connect) m = a                          a
                                                                (connect)                   
                        ts (connect) m = b                          b        =  PART
                                                                (connect)
                        ts (connect) m = c                          c
                        """
                        if in_count == len(devices):
                            one_crap_boolean = False
                            # 3 vertical, 4 horizontal connections done
                        # horizontally connect
                        temp_data = np.concatenate((time_stamp.T, metric.T), axis=1)

                        # execute for once for first element to connect second element
                        if three_crap_boolean:
                            save = temp_data
                            three_crap_boolean = False
                            titles.append(query)
                        # vertically connect horizontally connected elements
                        else:
                            save = np.concatenate((save, temp_data), axis=0)

                    # merge data collectively
                    else:
                        # to create following structure:
                        """ Connecting to PART above
                                           metric1
                                          (connect)
                            PART = PART +  metric2
                                          (connect)
                                           metric3
                        """
                        # run once and store first element
                        if four_crap_boolean:
                            saves = metric.T
                            four_crap_boolean = False
                        # perform operation mentioned above
                        else:
                            saves = np.concatenate((saves, metric.T), axis=0)
                        # if devices' loops' end is reached, add connected metrics
                        if in_count == len(devices):
                            save = np.concatenate((save, saves), axis=1)
                            # append queries into titles
                            titles.append(query_name)

            except:
                print("Potential time error. Please check if start and end time relevant. ")
                non_saved_log.append("an error occured: \t" + str(datetime.now()) + "\t ERROR IN MAIN LOOP!")
            # if there is data, go on

            # increment at the end of devices loop
            in_count += 1

    save = 123
    devices = 123

    temp_data3 = 123
    return temp_data3, temp_data2, save, devices, non_saved_log, titles_node
# titles_node.append(query)



a,v,b,vw,time_limit = time_div_step(day, hour, minute, 2)

start, end = give_default_dates(day_back=day, hour_back=hour, min_back=minute)
crap_bool = True
print("yeha")
print(time_limit)
hold1 = 0
hold2 = hour+24*day
hold3 = minute
# day w day-hold1

# 0,1,2,3...,divider-1, runs divider times
# oldu gibi

for count_time in range(time_limit):

    f, s, t, fo, ww = time_div_step(hold1, hold2, hold3, 2)
    start, end = give_default_dates(day_back=hold1, hour_back=hold2, min_back=hold3, end_recent_day=hold1,
                                    end_recent_hour=hold2 - s, end_recent_min=hold3 - t)
    temp_data3, temp_data2, save, devices, non_saved_log, titles_node = do_main(start, end, step)
    temp_data2 = pd.DataFrame(temp_data2,columns=titles_node)
    print("here is : ", temp_data2)

    if crap_bool:
        hold = temp_data2
        crap_bool = False

    else:
        hold = pd.concat((hold, temp_data2), axis=0)

    hold1 = f
    hold2 = hold2 - s
    hold3 = hold3 - t
    hold4 = fo

# save node exporter data
try:

    print(hold.shape)
    print(len(titles_node))
    # print(temp_data3.shape)
    # load data into a dataframe
    try:
        # df_less = pd.DataFrame(temp_data3, columns=titles_node_less)
        df_less = pd.DataFrame(temp_data3)
    except:
        print("excepted")

    df = pd.DataFrame(hold)
    # df = pd.DataFrame(temp_data2,columns=titles_node)
    # save data in csv format
    try:
        df_all = pd.concat([df, df_less], axis=1)
    except:
        print("excepted2")

    # df.to_csv('../out/node_metrics.csv')
    print("Node data was successfully saved into the folder named out. ")
    print(df.shape)
    # df.to_csv('../out/less_node.csv')
    try:
        df_all.to_csv("out/node_data.csv")
    except:
        df.to_csv("out/node_data.csv")

    print("saved")

except:
    # print error in log.txt file
    with open('log.txt', 'w') as f:
        f.write("An error occured while loading node data into df or saving to file! " + str(date.today()))
        f.write('\n')
        f.close()

# get data into dataframe object
# dataframe = pd.DataFrame(save)

# save libvirt exporter data

try:
    # load save data into a dataframe
    df = pd.DataFrame(save)
    # df = pd.DataFrame(save, columns=titles)
    # turn df into a list to change order of columns
    my_list = df.columns.tolist()
    # load names of devices into a list
    names_devices = []
    for c in range(len(devices)):
        for i in range(int(len(df) / len(devices))):
            names_devices.append(devices[c])

    # print names of devices in the dataframe
    df["names"] = names_devices

    # change the order of colums of dataframe
    cols = df.columns.tolist()
    cols = cols[:1] + cols[-1:] + cols[1:-1]
    df = df[cols]

    # save data into a csv file
    df.to_csv('out/libvirt_data.csv')
    print("Libvirt exporter, VM data saved in out folder.")

    # save dataframe into new created cs
    # dataframe.to_csv('last_state.csv')

# print in log file if any problem occurs
except:
    with open('log.txt', 'a') as f:
        f.write("Error while loading the data into or saving the libvirt's csv file! " + str(date.today()))
        f.write('\n')
        f.close()

