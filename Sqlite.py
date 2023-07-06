import sqlite3
import pandas as np
import pandas as pd
import time


class Database():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)  # 允许sqlite被多个线程同时访问
        self.cur = self.conn.cursor()

    def insert_findjob_user(self, table_name, email, gender, age, city, area, professional, job_type, phone, valkey,
                            create_time, recent_login_time):
        self.cur.execute("INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?)".format(table_name),
                         (email, gender, age, city, area, professional, job_type, phone, valkey,
                          create_time, recent_login_time,))
        self.conn.commit()

    def insert_changejob_user(self, table_name, email, gender, age, city, area, job_year, present_job, phone, valkey,
                              create_time, recent_login_time):
        self.cur.execute("INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?)".format(table_name),
                         (email, gender, age, city, area, job_year, present_job, phone, valkey,
                          create_time, recent_login_time,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def sql_search(self, table_name, e_mail):
        self.cur.execute("select email from {} where email =?;".format(table_name), (e_mail,))  # 執行
        self.conn.commit()
        ret = self.cur.fetchone()
        return ret

    def sql_search_secretkey(self, table_name, e_mail):
        self.cur.execute("select valkey from {} where email =?;".format(table_name), (e_mail,))  # 執行
        self.conn.commit()
        ret = self.cur.fetchone()
        return ret

    def get_val(self, table_name, e_mail):
        self.cur.execute("select valkey from {} where email =?;".format(table_name), (e_mail,))  # 執行
        self.conn.commit()
        ret = self.cur.fetchone()
        return ret

    def get_time(self, table_name, e_mail):
        self.cur.execute("select recent_login_time from {} where email =?;".format(table_name), (e_mail,))  # 執行
        self.conn.commit()
        ret = self.cur.fetchone()
        return ret

    def update_findjob_user(self, table_name, email, gender, age, city, area, professional, job_type, phone,
                            recent_login_time):
        self.cur.execute(
            "UPDATE {} SET gender=?,age=?,city=?,area=?,professional=?,job_type=?,phone=?,recent_login_time=? WHERE email=?"
            .format(table_name), (gender, age, city, area, professional, job_type, phone, recent_login_time, email,))
        self.conn.commit()

    def update_changejob_user(self, table_name, email, gender, age, city, area, job_year, present_job, phone,
                              recent_login_time):
        self.cur.execute(
            "UPDATE {} SET gender=?,age=?,city=?,area=?,job_year=?,present_job=?,phone=?,recent_login_time=? WHERE email=?"
            .format(table_name), (gender, age, city, area, job_year, present_job, phone, recent_login_time, email,))
        self.conn.commit()

    def get_findjob_lastinfo(self, table_name, e_mail):
        self.cur.execute(
            "select gender, age, city, area, professional, job_type, email,phone from {} where email =?;".format(
                table_name), (e_mail,))  # 執行
        self.conn.commit()
        ret = self.cur.fetchone()
        return ret

    def get_changejob_lastinfo(self, table_name, e_mail):
        self.cur.execute(
            "select gender, age, city, area, job_year, present_job, email,phone from {} where email =?;".format(
                table_name), (e_mail,))  # 執行
        self.conn.commit()
        ret = self.cur.fetchone()
        return ret

    def read_jobtype_convert(self):
        ret=pd.read_sql("select * from jobtype_convert;", self.conn)
        return ret


if __name__ == '__main__':
    db = Database('DataBase.db')  # 獲取資料庫
    db._cur.execute("SELECT * FROM Q_staff where 市縣='彰化縣' ")  # 執行
    db._conn.commit()
    data = db._cur.fetchall()
    db._cur.execute("PRAGMA table_info(Q_staff)")  # 執行
    db._conn.commit()
    columns = db._cur.fetchall()
    columns_name = [name[1] for name in columns]
    df = pd.DataFrame(data, columns=columns_name)
    print(df)
