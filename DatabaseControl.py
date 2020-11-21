import ReadSettings
import sqlite3
import json
import os


#Check Database is there
def CheckDatabaseExists():
    if os.path.exists(ReadSettings.GetSetting("Database","DatabaseLocation")):
        return True
    else:
        return False

def AddNewSwitch(SwitchID, Location="", IPv4Address="", IPv6Address="", Notes=""):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""INSERT INTO SWITCHES (SwitchName, Location, IPv4Address, IPv6Address, Notes) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(SwitchID, Location, IPv4Address, IPv6Address, Notes))

    database.commit()
    database.close()

# def RemoveSwitch(SwitchID):
#     print("Do this maybe idk")

#Get List of columns FROM given TABLE for other functions
def GetTablesColumns(Table,cursor):
    cursor.execute("""PRAGMA table_info({0})""".format(Table))
    Result=cursor.fetchall()
    #Create an empty string to add all the table column names to
    TableColumns=""
    for Column in Result:
        #Ignore the auto increment id
        if Column[1]  != "{0}_id".format(Table):
            TableColumns +="{0}, ".format(Column[1])
    return TableColumns[:-2]



def GetSwitches():
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT * FROM SWITCHES""")
    Result = cursor.fetchall()

    database.commit()
    database.close()

    return(Result)

def GetSwitchNames():
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT SwitchName FROM SWITCHES""")
    Result = cursor.fetchall()
    database.close()

    return(Result)

def GetTechNames():
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT Tech FROM TECHS""")
    Result = cursor.fetchall()
    database.close()

    return(Result)

def GetLocations():
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT DISTINCT Location FROM SWITCHES""")
    Result = cursor.fetchall()
    database.close()
    return (Result)




def GetTechIDFromName(Name):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT TECHS_id FROM TECHS WHERE Tech = "{0}" """.format(Name))
    Result = cursor.fetchall()
    database.close()

    return str((Result[0])[0])



def GetTechNameFromID(ID):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT Tech FROM TECHS WHERE TECHS_id = "{0}" """.format(ID))
    Result = cursor.fetchall()
    database.close()

    return str((Result[0])[0])

def GetSwitchIDFromName(Name):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT SWITCHES_id FROM SWITCHES WHERE SwitchName = "{0}" """.format(Name))
    Result = cursor.fetchall()
    database.close()

    return str((Result[0])[0])

def GetSwitchNameFromID(ID):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT SwitchName FROM SWITCHES WHERE SWITCHES_id = "{0}" """.format(ID))
    Result = cursor.fetchall()
    database.close()

    return str((Result[0])[0])

def GetSwitchLocationFromID(ID):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT Location FROM SWITCHES WHERE SWITCHES_id = "{0}" """.format(ID))
    Result = cursor.fetchall()
    database.close()

    return str((Result[0])[0])

def GetSwitchIDFromLocation(Location):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""SELECT SWITCHES_id FROM SWITCHES WHERE Location = "{0}" """.format(Location))
    Result = cursor.fetchall()
    database.close()

    return (Result)


def AddPatch(Tech,Switch,PannelPort,SwitchUnit,SwitchPort,PatchType,Date,Notes):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    if PatchType == "New":
        AlreadyPatched=0
        PatchRemoved=0
    elif PatchType == "Existing":
        AlreadyPatched=1
        PatchRemoved=0
    elif PatchType == "Removal":
        AlreadyPatched=1
        PatchRemoved=1
    
    cursor.execute("""INSERT INTO PATCHES ({0}) VALUES ("{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}")""".format(GetTablesColumns("PATCHES",cursor),Tech,Switch,PannelPort,SwitchUnit,SwitchPort,Date,Notes,AlreadyPatched,PatchRemoved))
    database.commit()
    database.close()

def SearchPatch(SearchTerms):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()
    cursor.execute("""SELECT * FROM PATCHES WHERE{0}""".format(SearchTerms))
    Result = cursor.fetchall()
    database.close()
    print(Result)
    return Result


def CustomQuery(Query):
    database = sqlite3.connect(ReadSettings.GetSetting("Database","DatabaseLocation"))
    cursor = database.cursor()

    cursor.execute("""{0}""".format(Query))
    Result = cursor.fetchall()

    database.commit()
    database.close()

    return(Result)
