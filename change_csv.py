import pandas as pd
import requests as rq

df = pd.read_csv("all_queries.csv")
nodes = {}
libvirts = {}
node_data =[]
node_name = []
libv_data = []
libv_name=[]
for name, col in df.iterrows():

    query_name = col["query_name"]
    query = col["query"]

    print(query)
    # a boolean for searching the word
    found = False
    # define an empty string to be used
    check_word = ""

    # if searched word is at the start immediately decide and finish
    # if first 4 letters form node, return instance which is created
    if query[0:4] == "node":

        node_data.append(query)
        node_name.append(query_name)
    # if first 7 letters form libvirt, return instance which is created
    if query[0:7] == "libvirt":

        libv_data.append(query)
        libv_name.append(query_name)
    # if not continue searching
    for char in query:
        # as we know if word is not at the start, it is after a "(" because it must be a query function
        if char == "(":
            # search for "(" if found, step on this execution of for loop
            found = True
            continue
        # search letters after "(" character
        if found:
            check_word += char

        # if "node" is found, return instance as stated
        if check_word == "node":

            node_data.append(query)
            node_name.append(query_name)

        # if "libvirt" is found, return instance as stated
        if check_word == "libvirt":

            libv_data.append(query)
            libv_name.append(query_name)
        # if can't be found return error


nodes["query name"] = node_name
nodes["query"] = node_data

libvirts["query name"] = libv_name
libvirts["query"] = libv_data

pd.DataFrame(nodes).to_csv("node_queries.csv")
pd.DataFrame(libvirts).to_csv("libvirt_queries.csv")
#df_node = pd.DataFrame(nodes)
#df_libv = pd.DataFrame(libvirts)

#print(df_node, df_libv)
# a function to return interfaces and jobs, gets functionally-updatet start time

