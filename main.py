import pandas as pd
import numpy as np
from datetime import date
from organizers import *


# read csv which contains queries
df = pd.read_csv('all_queries.csv')
recent_time = "10h"
step_func = "5s"

for name, col in df.iterrows():

    query_name = col["query_name"]
    query = col["query"]

    # booleans to execute a statement for each loop turn
    three_crap_boolean = True
    four_crap_boolean = True

    # get instance
    instance = organize_instance(query, recent_time)
    # get request
    request = curly_organizer(query, instance, step_func)
    # organize request
    organized_request = organize_url(request)

    print(organized_request)
