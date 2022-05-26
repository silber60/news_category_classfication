from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time

read_csv = []

for i in range(3):
     read_csv.append(pd.read_csv('./crawling_data{}.csv'.format(i), header=None))

final_concat = pd.concat(read_csv)
print(final_concat)

# final_concat.to_csv('./final_concat.csv', index=False)
final_concat.to_excel('./final_concat.xlsx', index=False)