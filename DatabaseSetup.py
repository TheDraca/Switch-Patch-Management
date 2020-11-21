import ReadSettings
import sqlite3


def CreateTable(TableName, Content, cursor):
    AutoID = "{0}_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE".format(TableName)
    cursor.execute("""CREATE TABLE IF NOT EXISTS {0} ({1}, {2})""".format(TableName, AutoID, Content))

def SetupDatabase():
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    CreateTable("TECHS", "Tech varchar(255)", cursor)
    CreateTable("ENDUSERS", "EndUser varchar(255)", cursor)
    CreateTable("SWITCHES", "SwitchName varchar(255), Location varchar(255), IPv4Address varchar(15), IPv6Address varchar(39), Notes varchar(255)", cursor)
    CreateTable("PATCHES", "tech_id INTEGER, switch_id INTEGER, PannelPort varchar(255), Unit INTEGER, Port INTEGER, Date varchar(10), Notes varchar(255), AlreadyPatched BOOLEAN, PatchRemoved BOOLEAN", cursor)


    database.commit()
    database.close()
