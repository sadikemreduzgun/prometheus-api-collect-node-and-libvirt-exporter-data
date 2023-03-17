import pandas as pd
import requests as rq


# can be used to reload back when wanted to turn back to old state
def split_csv():
    # load the dataframe  into "df"
    df = pd.read_csv("all_queries.csv")
    # define empty directories and lists to create a dataframe
    nodes = {}
    libvirts = {}
    node_data =[]
    node_name = []
    libv_data = []
    libv_name=[]
    
    # get names and colummn names of queries of main query csv
    for name, col in df.iterrows():
        # assign values
        query_name = col["query_name"]
        query = col["query"]

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
                # store desired data
                node_data.append(query)
                node_name.append(query_name)

            # if "libvirt" is found, return instance as stated
            if check_word == "libvirt":
                # store desired data
                libv_data.append(query)
                libv_name.append(query_name)
            # if can't be found return error

    # load into node dictionary    
    nodes["query_name"] = node_name
    nodes["query"] = node_data
    # load into libvirt dictionary
    libvirts["query_name"] = libv_name
    libvirts["query"] = libv_data
    
    # load dictionaries into dataframes and save them in the same directory.
    pd.DataFrame(nodes).to_csv("node_queries.csv",index=False)
    pd.DataFrame(libvirts).to_csv("libvirt_queries.csv",index=False)
#df_node = pd.DataFrame(nodes)
#df_libv = pd.DataFrame(libvirts)

#print(df_node, df_libv)
# a function to return interfaces and jobs, gets functionally-updatet start time


def delete_row(df, num):
    # remove the entered number of element of the given dataframe
    df = pd.concat((df.iloc[0:num,:],df.iloc[num+1:len(df),:]),axis=0, ignore_index=True)
    return df


# df = delete_row(df)


def add_row(df):
    # get query and query name
    query_name = input("Query name: ")
    query = input("Query: ")
    # add those in the df
    df = df.append({"query_name":query_name, "query":query}, ignore_index=True)
    
    return df

# usage : df = add_row(df)
