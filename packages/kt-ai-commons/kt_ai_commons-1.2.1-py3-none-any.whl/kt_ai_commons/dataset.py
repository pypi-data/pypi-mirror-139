import pandas as pd

def query_onenavi_train():
    
    return pd.read_csv("https://gitlab.dspace.kt.co.kr/AISP2022/AISP2022/-/raw/master/onenavi_train.csv", sep = "|")