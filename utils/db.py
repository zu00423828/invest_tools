import sqlite3
import os
class DBtool:
    def __init__(self,db_path,db_init) -> None:
        # os.remove('virtualmemory.db')
        if db_init and os.path.exists(db_path):
            os.remove(db_path)
        self.db=sqlite3.connect(db_path)
        self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS TransactionHistory (
                symbol TEXT, 
                id INTEGER,
                orderId INTEGER,
                side INTEGER,
                price FLOAT,
                qty FLOAT,
                realizedPnl FLOAT,
                marginAsset TEXT,
                quoteQty FLOAT,
                commission FLOAT,
                commissionAsset TEXT,
                datetime DATETIME,
                positionSide TEXT,
                buyer BOOLEAN,
                maker BOOLEAN
            )
            '''
        )
        self.db.commit()
    def add_transactionhistory(self,data_list):
        for data in data_list:
            self.db.execute(
                '''INSERT INTO TransactionHistory VALUES(:symbol, :id, :orderId, :side, :price, :qty, :realizedPnl, :marginAsset, 
                :quoteQty, :commission, :commissionAsset, :time, :positionSide, :buyer, :maker)''',data)
            self.db.commit()
    def get_last_dat(self,):
        res=self.db.execute(
                '''
                    SELECT datetime FROM TransactionHistory ORDER BY datetime DESC LIMIT 1
                '''
                ).fetchall()
        self.db.commit()
        return res
    def get_data(self):
        res=self.db.execute(
            '''
                SELECT DATE(datetime),SUM(realizedPnl) FROM TransactionHistory GROUP BY  DATE(datetime)
            '''
            ).fetchall()
        self.db.commit()
        return res
