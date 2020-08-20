# import csv
# with open("./pest.csv") as file:
#     reader = csv.reader(file)
#     #print(list(reader))
#     for row in reader:
#         print(row)

import pandas as pd

weather_data = pd.read_csv('pest.csv')
print(weather_data)
