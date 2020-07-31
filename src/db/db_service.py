from .db_instance import UniqueObject


class MSSQL(object):
    conn, cur = UniqueObject.get_object()

    def __init__(self):
        pass

    def __del__(self):
        # print("\n  MSSQL object has been realsed!")
        pass

    def exec_query(self, sql, args=()):
        self.cur.execute(sql, args)
        res_list = self.cur.fetchall()
        # print(res_list)
        return res_list

    def exec_non_query(self, sql, args=()):
        try:
            self.cur.execute(sql, args)
            self.conn.commit()
        except:
            self.conn.rollback()
        # finally:
        #     self.cur.close()
        #     self.conn.close()
    # print("\nInserting exception!")
