import sqlite3
import copy


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                MetaSingleton, cls).__call__(*args, **kwds)
        return cls._instances[cls]


# 커서 단일지점을 위한 싱글톤 패턴 적용
class DB(metaclass=MetaSingleton):
    def __init__(self, path):
        self.con = None
        self.cur = None
        self.path = path

    def getConnect(self):
        if self.con is None:
            self.con = sqlite3.connect(self.path, check_same_thread=False)
        return self.con

    def getCursor(self):
        if self.cur is None:
            self.cur = self.getConnect().cursor()
        return self.cur


# 테이블 복제를 위해 프로토타입 패턴 적용
class Table:
    def __init__(self, cols):
        self.con = None
        self.cur = None
        self.table = None
        self.cols = cols

    def clone(self):
        return copy.deepcopy(self)

    def setTable(self, con, cur, table):
        self.con = con
        self.cur = cur
        self.table = table

    def createTable(self):
        sql = 'CREATE TABLE IF NOT EXISTS %s (' % self.table
        for col, typ in self.cols.items():
            sql += '%s %s, ' % (col, ' '.join(typ))
        sql = sql[:-2] + ');'
        self.cur.execute(sql)
        self.con.commit()

    def insertData(self, column, value):
        sql = 'INSERT INTO %s (%s) VALUES("%s");' % (self.table, column, value)
        self.cur.execute(sql)
        self.con.commit()

    def updateData(self, col_val_dict, condition):
        sql = 'UPDATE %s SET %s WHERE %s;' % (self.table, ', '.join(
            ['"%s" = "%s"' % (col, val) for col, val in col_val_dict.items()]), condition)
        self.cur.execute(sql)
        self.con.commit()

    def deleteData(self, condition):
        sql = 'DELETE FROM %s WHERE %s' % (self.table, condition)
        self.cur.execute(sql)
        self.con.commit()

    def fetchAll(self):
        sql = 'SELECT * FROM %s;' % self.table
        return self.cur.execute(sql).fetchall()

    def fetchOne(self, condition):
        sql = 'SELECT * FROM %s WHERE %s' % (self.table, condition)
        return self.cur.execute(sql).fetchone()


# 테이블 초기화를 위한 파사드 패턴
def initTable(con, cur):
    do_table = Table({'id': ['INTEGER', 'PRIMARY', 'KEY',
                             'AUTOINCREMENT'], 'content': ['TEXT', 'NOT NULL']})
    schedule_table = do_table.clone()
    delegate_table = do_table.clone()
    dontdo_table = do_table.clone()

    do_table.setTable(con, cur, 'do')
    schedule_table.setTable(con, cur, 'schedule')
    delegate_table.setTable(con, cur, 'delegate')
    dontdo_table.setTable(con, cur, 'dontdo')

    do_table.createTable()
    schedule_table.createTable()
    delegate_table.createTable()
    dontdo_table.createTable()

    return do_table, schedule_table, delegate_table, dontdo_table
