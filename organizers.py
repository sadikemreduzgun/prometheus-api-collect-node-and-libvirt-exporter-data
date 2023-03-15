import requests as rq


# organizes the query, selects and returns query
def curly_organizer(query, selection="{job=node-exporter}", step_function="5s"):

    # create a string to return
    hold_str = ""
    # booleans for operations
    # run once and if searched item is found, delete it.
    boole1 = False
    boole2 = False

    # look at letters one by one and organize
    for letter in query:
        # when "{" is encountered, delete until "}"
        # then place in "selection"
        if letter == "{":
            boole1 = True
            pass
        elif letter=="[":
            boole2 = True
            pass
        # place chosen step time into
        if boole1 or boole2:

            if letter == "}":
                hold_str += str(selection)
                boole1 = False
            elif letter == "]":
                # after deleting [some time]
                # place in desired time
                hold_str += f"[{step_function}]"
                boole2 = False
            else:
                pass

        # adds letters that are not in curly branches
        else:

            hold_str += letter

    # return the hold_str string after performing step choice of some query functions
    return hold_str


def organize_url(query):
    # define a string to order and return
    url_str = ""
    # get some chars which create problems,
    # change them to URL utf-8 characters
    for letter in query:
        # if there is (") character, change it to "%22"
        if letter == "\"":
            url_str += "%22"
        # if there is "+" character, change it to "%2B"
        elif letter == "+":
            url_str += "%2B"
        # if there is "*" character, change it to %2A
        elif letter == "*":
            url_str += "%2A"

        #        elif letter=="-":
        #            url_str+="%2D"
        # if there is no character which we search, don't change and add
        else:
            url_str += letter

    # return ordered string-url
    url_str = f"http://localhost:9090/api/v1/query?query={url_str}"

    return url_str


# a function to return interfaces and jobs, gets functionally-updatet start time
def return_instance():

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


def organize_instance(query, time):

    return "{instance=" + f'{return_instance()}' + "}" + f"{time}"
