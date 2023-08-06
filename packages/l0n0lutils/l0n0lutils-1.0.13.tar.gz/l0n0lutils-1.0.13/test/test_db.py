import sys
import logging
sys.path.insert(0, ".")


from l0n0lutils.dbmysql import DbMysqlHelper

helper = DbMysqlHelper('127.0.0.1', 3306, 'root', '', 'test')
helper.db.update("ttt", {"b":5, "c":4}, {"a":1})
# helper.add_table("t1", """
# `id` int not null auto_increment,
# `data` varchar(123),
# primary key (`id`)
# """)
# helper.create_tables()
# helper.db.insert("t1", ['data'], ['aaab'])
# ret = helper.db.select("t1", ['id', 'data'])
# print(ret)
