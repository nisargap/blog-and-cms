import sqlite3
class Database:

    def __init__(self, name):

        self.__inst = sqlite3.connect(name + ".db", check_same_thread = False)

    def getInstance(self):

        return self.__inst

    def query(self, stmt, args = (), one = False):

        cur = self.__inst.execute(stmt, args)
        rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
        
        return (rv[0] if rv else None) if one else rv

    def getWhere(self, where):

        # building where clause
        whereClause = ""

        if len(where) == 2:
            whereClause = where[0] + " = ?"
        elif len(where) > 2:
            for i in range(len(where)):

                if i % 2 == 0 and i != len(where) - 2:
                    whereClause += where[i] + " = ? and "
                elif i == len(where) - 2:
                    whereClause += where[i] + " = ?"

        return whereClause

    def getArgs(self, where):

        args = list()

        for i in range(len(where)):
            if i % 2 != 0:
                args.append(where[i])

        return args

    def select(self, table, item, where):    

        stmt = "select "+ item +" from " + table + " where " + self.getWhere(where)

        return self.query(stmt, self.getArgs(where))

    def delete(self, table, where):

        stmt = "delete from " + table + " where " + self.getWhere(where)

        return self.query(stmt, self.getArgs(where))

    def updateParse(self, fields):

        parsedStr = ""
        for i in range(len(fields)):

            if i % 2 == 0:

                parsedStr += fields[i] + " =  \"" + fields[i + 1] + "\","

        return parsedStr[:-1]

    def update(self, table, fields, where):

        stmt = "update " + table + " set " + self.updateParse(fields) + " where " + self.getWhere(where)

        print(stmt)

        return self.query(stmt, self.getArgs(where))


    def getAll(self, table, item):

        stmt = "select " + item + " from " + table

        return self.query(stmt)

    def getBinds(self, fields):

        # qStr will have ?,?,?,? so if i != len(fields) - 1 then += ?, else += ?
        qStr = ""

        for i in range(len(fields)):

            if i != len(fields) - 1:
                qStr += "?,"
            else:
                qStr += "?"

        return qStr

    def getDict(self, fields, identifier):

        if identifier != "keys" and identifier != "values":

            return False

        returnStr = ""
        returnList = []
        for key in fields:

            #returnStr += key + "," if identifier == "keys" else returnList.append(fields[key])
            if identifier == "keys":

                returnStr += key + ","
            else:
                returnList.append(fields[key])

        if identifier == "keys":

            return returnStr[:-1]

        else:
            return returnList


    def insert(self, table, fields):

        stmt = "insert into " + table + " (" + self.getDict(fields, "keys") + ") values " + " (" + self.getBinds(fields) + ") "

        return self.query(stmt, self.getDict(fields, "values"))

    def count(self, table, where):
        query = "select count(*) from " + table + " where " + self.getWhere(where)

        cur = self.__inst.execute(query, self.getArgs(where))
        return cur.fetchone()[0]

    def closeInstance(self):
        self.__inst.close()