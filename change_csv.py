import pandas as pd
import requests as rq

df = pd.read_csv("all_query.csv")


def org_ins(query):

    # a boolean for searching the word
    found = False
    # define an empty string to be used
    check_word = ""
    # if searched word is at the start immediately decide and finish
    # if first 4 letters form node, return instance which is created
    if query[0:4] == "node":
        # return instance created by return_instance function
        return "node", "{instance=" + f'{return_instance("node")}' + "}"

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
            return "node", "{instance=" + f'{return_instance("node")}' + "}"

    # if can't be found return error
    return -1, -1


# a function to return interfaces and jobs, gets functionally-updatet start time
def return_instance(which=""):

    if which == "node":
        # assign query
        query = "node_load1"
        # load dates and query into URL
        url = f"http://localhost:9090/api/v1/query?query={query}"

        # get data using requests
        data = rq.get(url)
        # turn data into dictionary
        data = data.json()

        # parse data to get instance
        result = data['data']['result'][0]['metric']['instance']
        # return reached instance
        return f'"{result}"'

    elif which == "libvirt":
        # assign query
        query = "libvirt_domain_block_stats_allocation"
        # load query and time data into URL
        url = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=30s"

        # get data using requests library
        data = rq.get(url)
        # turn data into dictionary to be able to pars
        data = data.json()

        # parse data to get instance
        result = data['data']['result'][0]['metric']['instance']

        # return data
        return f'"{result}"'

    # if something goes wrong return error
    else:
        return -1


for name, col in df.iterrows():

    query_name = col["query_name"]
    query = col["query"]
