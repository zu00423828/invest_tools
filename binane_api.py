from datetime import  datetime, timedelta
from datetime import datetime
from typing import List, Tuple
from binance.futures import Futures
import pandas as pd
from utils.db import DBtool
import os
import yaml
class MyFutures(Futures):
    def get_account_trades(self,**kwargs):
        """Account Trade List (USER_DATA)
        Get trades for a specific account and symbol.

        GET /fapi/v1/userTrades

        https://binance-docs.github.io/apidocs/futures/en/#account-trade-list-user_data

        Args:
            symbol (str)
        Keyword Args:
            startTime (int, optional)
            endTime (int, optional)
            fromId (int, optional): Trade id to fetch from. Default gets most recent trades.
            limit (int, optional): Default 500; max 1000.
            recvWindow (int, optional)

        If startTime and endTime are both not sent, then the last 7 days' data will be returned.
        The time between startTime and endTime cannot be longer than 7 days.
        The parameter fromId cannot be sent with startTime or endTime.
        """
        url_path = "/fapi/v1/userTrades"
        params = { **kwargs}
        return self.sign_request("GET", url_path, params)


def insert_data_to_db(df:pd.DataFrame):
    df.rename(columns={'time':'datetime'},inplace=True)
    df['datetime']=df['datetime'].apply(timestamp2datetime)
    # origin_data.to_csv('out.csv',index=None)
    df.to_sql(name='TransactionHistory',con=dbtool.db,if_exists='append',index=False)

def process_anyday_data(data:List[Tuple]):
    data=[{"date":date,"benefit":benefit} for date,benefit in data] 
    any=pd.DataFrame(data)
    print(any)
    print(any['benefit'].sum())


def datetime2timestamp(dt:datetime):
    ''' Converts a datetime object to UNIX timestamp in milliseconds. '''
    ts=int(dt.timestamp())*1000
    return ts

def timestamp2datetime(ts:datetime.timestamp):
    ts/=1000
    dt=datetime.fromtimestamp(int(ts))
    return dt

def get_binane_data():
    client = MyFutures(key=config['binance_api_key'], secret=config['binance_api_secret'],base_url="https://fapi.binance.com")
    yesterday=datetime.now()-timedelta(days=1)
    db_last_recode_datetime=dbtool.get_last_dat()[0][0]
    db_last_recode_datetime=datetime.strptime(db_last_recode_datetime,'%Y-%m-%d %H:%M:%S')
    print(type(db_last_recode_datetime),db_last_recode_datetime)
    start_time=datetime(yesterday.year,yesterday.month,yesterday.day,0,0,0)
    ts_s=datetime2timestamp(start_time)
    # ts_e=datetime2timestamp(end_time)
    result = client.get_account_trades( startTime=ts_s,recvWindow=6000)
    new_data=pd.DataFrame(result)
    insert_data_to_db(new_data)

if __name__=="__main__":
    with open('config.yaml') as f:
        config=yaml.load(f,yaml.FullLoader)
    db_init=True
    dbtool=DBtool(config['db_path'],db_init)
    if db_init : 
        df=pd.read_csv(config['old_data_path'])
        insert_data_to_db(df)
    get_binane_data()
    
    process_anyday_data(dbtool.get_data())
    