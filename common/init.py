import sys
### IMPOSTAZIONE PERCORSO LIBRERIE ESTERNE ###
sys.path.insert(0, '../modules')
import variables

import sqlite3 as sql


class Database(object):
    def __init__(self):
        sql.connect(variable.path + "")