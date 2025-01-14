# import time
# from datetime import datetime

# def difference_in_dates(todays_date(), date1):
#     def todays_date():
#         today = datetime.today()
#         formatted_today = today.strftime("%d/%m/%Y")
#         return formatted_today
#     date_format = "%d/%m/%Y"
#     a = time.mktime(time.strptime(date1, date_format))
#     delta = abs(formatted_today - a)
#     return int(delta / 86400)


# def todays_date():
#     today = datetime.today()
#     formatted_today = today.strftime("%d/%m/%Y")
#     return formatted_today

# print(difference_in_dates(todays_date(),"18/04/2005"))


# Function to read the DataFrame from a CSV file
import random
import pandas as pd
import geopandas as gpd
import streamlit as st
import matplotlib.pyplot as plt
import os
import numpy as np

