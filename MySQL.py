from __future__ import print_function
from __future__ import unicode_literals
import pymysql.cursors
import json
import os
import sqlite3
from os.path import expanduser

isDevelopment = False
file_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.realpath(os.path.join(file_path,os.pardir))
DatabaseClass = None

class SQLiteDB:
    connection = None

    @staticmethod
    def init_connection():
        folder_path = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(folder_path,"esl.db")
        user_db_path = expanduser("~/esl.db")
        print("esl.db file location=",folder_path)
        if(os.path.exists(user_db_path)):
            SQLiteDB.connection = sqlite3.connect(user_db_path)
        else:
            SQLiteDB.connection = sqlite3.connect(db_path)


    @staticmethod
    def __formatSingleResult(names,record):
        if not names:
            return None
        if not record:
            return None
        print('single',names,record)
        output = {}
        name_length = len(names)
        record_length = len(record)
        if name_length != record_length:
            return "ERROR!"
        for i in range(name_length):
            output[names[i]] = record[i]
        return output

    @staticmethod
    def __formatManyResult(names,records):
        if not names:
            return None
        if records is None:
            return None
        print('many',names,records)
        output_list = []
        name_length = len(names)
        
        if(len(records) == 0):
            return []
        record_length = len(records[0])
        record_number = len(records)
        if name_length != record_length:
            return "ERROR!"
        
        for i in range(record_number):
            output = SQLiteDB.__formatSingleResult(names,records[i])
            output_list.append(output)
        return output_list

    @staticmethod
    def execute(sql,onObtainedData=None,onFailure=None,fetchone=False):
        if not SQLiteDB.connection:
            SQLiteDB.init_connection()
        try:
            cursor = SQLiteDB.connection.cursor()
            SQLiteDB.connection.row_factory = sqlite3.Row
            cursor.execute(sql)
            SQLiteDB.connection.commit()
            names = None
            if cursor.description:
                names = list(map(lambda x: x[0], cursor.description))
            if fetchone:
                results = cursor.fetchone()
                formated_result = SQLiteDB.__formatSingleResult(names,results)
            else:
                results = cursor.fetchall()
                formated_result = SQLiteDB.__formatManyResult(names,results)
            
            # print(names)
            # print(results)
            
            if onObtainedData:
                return onObtainedData(formated_result)
            else:
                return formated_result
        except Exception as e:
            print("Error occured:",e)
            if onFailure:
                return onFailure(str(e))
        finally:
            SQLiteDB.connection.close()
            SQLiteDB.connection = None


class MySQLDB_thread:
    def __init__(self,configuration_json_path):
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.realpath(os.path.join(file_path,os.pardir))
        with open(os.path.join(file_path,configuration_json_path)) as f:
            credentials = json.load(f)
        self.conn = pymysql.connect(host=credentials['host'],
                             user=credentials['user'],
                             password=credentials['password'],
                             db=credentials['database'],
                             charset=credentials['charset'],
                             port=credentials['port'],
                             cursorclass=pymysql.cursors.DictCursor)

    def execute(self,sql,onObtainedData=None,onFailure=None,fetchone=False,return_affected_rows=False):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                self.conn.commit()
                if fetchone:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
                if onObtainedData:
                    return onObtainedData(result)
                else:
                    if not return_affected_rows:
                        return result
                    return result,cursor.rowcount
        except Exception as e:
            print("Error occured",e)
            if onFailure:
                return onFailure(str(e))
        finally:
            self.conn.close()
            


DatabaseClass = MySQLDB_thread

class Database:
    @staticmethod
    def execute(sql,onObtainedData=None,onFailure=None,fetchone=False,return_affected_rows=False):
        db = DatabaseClass()
        if return_affected_rows and onObtainedData is None:
            result,row_numbers = db.execute(sql,onObtainedData,onFailure,fetchone,return_affected_rows)
            return result,row_numbers
        else:
            result = db.execute(sql,onObtainedData,onFailure,fetchone,return_affected_rows)
            return result

            
if __name__ == '__main__':
    print("mysql example")
    def onResultObtained(result):
        print("result=",result)
    sql = "select * from Account"

    Database.execute(sql,onResultObtained)
