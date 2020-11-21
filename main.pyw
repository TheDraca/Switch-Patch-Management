from tkinter import *
from tkinter import ttk
from datetime import date
import platform
import os
import ReadSettings
import DatabaseControl
import DatabaseSetup


#Check for settings file
while os.path.exists(ReadSettings.File()) == False:
    ReadSettings.SetupSettings()


###SETUP Window Classes####
class window(Tk):
    WindowSize="{0}x{1}".format((ReadSettings.GetSetting("General","MainXWindowSize")),ReadSettings.GetSetting("General","MainYWindowSize"))
    def __init__(self,WindowSize=WindowSize):
        Tk.__init__(self)
        self.title(ReadSettings.GetSetting("General","Title"))
        #if "Windows" not in platform.platform():
            #self.attributes('-type', 'dialog') #Makes the windows free floating for certian unix window managers that like to force full screen
        #self.titlelabel()
        self.geometry(WindowSize)
    def titlelabel(self, text=ReadSettings.GetSetting("General","Title"), XPos=(int(WindowSize.split("x")[0])//2), YPos=10, Anchor="center" ):
        Label(self, text=text).place(anchor=Anchor, x=XPos, y=YPos) #Place the main label in the center by getting half the value of the X Window Size
        Label(self, text="").grid(row=0,column=0,sticky=N) #Enter a blank row to allow for other text using columns/rows to be positioned around title

    def label(self, text, row, column, sticky):
        Label(self, text=text).grid(row=row,column=column,sticky=sticky,)

    def button(self, text, command, row, column, sticky):
        Button(self, text=text, command=command).grid(row=row, column=column, sticky=sticky)

    #def listbox()

class dialogwindow(Tk):
    def __init__(self, WindowName=""):
        Tk.__init__(self)
        self.title("Alert")
        # if "Windows" not in platform.platform():
        #     self.attributes('-type', 'dialog') #Makes the windows free floating for certian unix window managers that like to force full screen
        self.titlelabel(WindowName)

    def titlelabel(self, text=ReadSettings.GetSetting("General","Title")):
        Label(self, text=text).grid(row=0,column=0,sticky=N) #Enter a blank row to allow for other text using columns/rows to be positioned around title

    def label(self, text, row, column, sticky):
        Label(self, text=text).grid(row=row,column=column,sticky=sticky)

    def button(self, text,  row, column, sticky, command):
        Button(self, text=text, command=command).grid(row=row, column=column, sticky=sticky)

    def CloseButton(self, text, row, column, sticky):
         Button(self, text=text, command=lambda : self.destroy()).grid(row=row, column=column, sticky=sticky)



def MakeLocationList():
    DatabaseLocations=DatabaseControl.GetLocations()
    LocationList = []

    for Location in DatabaseLocations:
        LocationList += Location

    return LocationList

def CreateNewTech(Name):
    if len(Name) == 0 or " " in Name or  "/n" in Name:
        BadTechName = dialogwindow("Error creating tech")
        BadTechName.label("Sorry but no spaces in tech names becuase SQL is hard \nAlso no empty names pls",1,0,N)
        BadTechName.CloseButton("Close",2,0,NE)

    elif Name in str(DatabaseControl.GetTechNames()):
        BadTechName = dialogwindow("Error creating tech")
        BadTechName.label("Sorry someone took that name",1,0,N)
        BadTechName.CloseButton("Close",2,0,NE)

    else:
        DatabaseControl.AddNewTech(Name)

def CreateNewSwitch(Name,Location,IPv4Address,IPv6Address,Notes=""):
    print(Name,Location,IPv4Address,IPv6Address,Notes)

    if len(Name) == 0 or " " in Name or  "/n" in Name:
        BadSwitchDetails = dialogwindow("Error creating switch")
        BadSwitchDetails.label("Sorry but no spaces in names becuase SQL is hard \nAlso no empty names pls",1,0,N)
        BadSwitchDetails.CloseButton("Close",2,0,NE)

    elif Name in str(DatabaseControl.GetSwitchNames()):
        BadSwitchDetails = dialogwindow("Error creating switch")
        BadSwitchDetails.label("Switch Name already exists!",1,0,N)
        BadSwitchDetails.CloseButton("Close",2,0,NE)

    elif len(IPv4Address) > 15:
        BadSwitchDetails = dialogwindow("Error creating switch")
        BadSwitchDetails.label("IPv4 address is longer than permitted",1,0,N)
        BadSwitchDetails.CloseButton("Close",2,0,NE)

    elif len(IPv6Address) > 39:
        BadSwitchDetails = dialogwindow("Error creating switch")
        BadSwitchDetails.label("IPv6 address is longer than permitted",1,0,N)
        BadSwitchDetails.CloseButton("Close",2,0,NE)

    else:
        DatabaseControl.AddNewSwitch(Name,Location,IPv4Address,IPv6Address,Notes)





def CreateNewTechWindow():
    CreateNewTechWindow = window()
    CreateNewTechWindow.label("Tech Name",1,0,W)
    
    NewTechName=ttk.Entry(CreateNewTechWindow)
    NewTechName.grid(row=1,column=1,sticky=W)

    CreateNewTechWindow.button("Create", lambda : CreateNewTech(NewTechName.get()), 1,2,NE)




def CreateNewSwitchWindow():
    CreateNewSwitchWindow = window()
    
    CreateNewSwitchWindow.label("Switch Name",1,0,W)
    NewSwitchName=ttk.Entry(CreateNewSwitchWindow)
    NewSwitchName.grid(row=1,column=1,sticky=W)


    CreateNewSwitchWindow.label("Switch Location",2,0,W)
    NewSwitchLocation = ttk.Combobox(CreateNewSwitchWindow,values=DatabaseControl.GetLocations())
    NewSwitchLocation.grid(row=2,column=1,sticky=E)


    CreateNewSwitchWindow.label("IPv4 Address",3,0,W)
    NewSwitchIPv4=ttk.Entry(CreateNewSwitchWindow)
    NewSwitchIPv4.grid(row=3,column=1,sticky=W)

    CreateNewSwitchWindow.label("IPv6 Address",4,0,W)
    NewSwitchIPv6=ttk.Entry(CreateNewSwitchWindow)
    NewSwitchIPv6.grid(row=4,column=1,sticky=W)

    #CreateNewSwitchWindow.label("Notes",4,0,W)
    
    





    CreateNewSwitchWindow.button("Create", lambda : CreateNewSwitch(NewSwitchName.get(),NewSwitchLocation.get(),NewSwitchIPv4.get(),NewSwitchIPv6.get()), 1,2,E)



#Window listing current switches
def ShowSwitches():
    SwtichList=[]
    row=2
    column=0
    ShowSwitchesWindow = window()
    ShowSwitchesWindow.titlelabel("Switches currentlly in the database:")
    ShowSwitchesWindow.geometry("400x400")

    ShowSwitchesWindow.label("ID",1,0,N)
    ShowSwitchesWindow.label("Name",1,1,N)
    ShowSwitchesWindow.label("Location",1,2,N)
    ShowSwitchesWindow.label("IPv4 address",1,3,N)
    ShowSwitchesWindow.label("IPv6 address",1,4,N)
    ShowSwitchesWindow.label("Notes",1,5,N)

    for SwitchRecord in DatabaseControl.GetSwitches():
        for Value in SwitchRecord:
            print(Value)
            ShowSwitchesWindow.label(Value,row,column,W)
            column+=1
        column=0
        row+=1

def CommitPatch(PatchType,Switch,Tech,PannelPort,SwitchUnit,SwitchPort,Notes="Null"):
    Date=date.today().strftime("%d/%m/%Y")
    if PatchType == "" or Switch  == "" or PannelPort  == "" or SwitchUnit  == "" or SwitchPort  == "":
        MissingDataWindow = dialogwindow("One or more fields are missing data")
        MissingDataWindow.CloseButton("Close",1,0,NE)

    else:
        Tech_ID = DatabaseControl.GetTechIDFromName(Tech)
        Switch_ID = DatabaseControl.GetSwitchIDFromName(Switch)
        DatabaseControl.AddPatch(Tech_ID,Switch_ID,PannelPort,SwitchUnit,SwitchPort,PatchType,Date=Date,Notes=Notes)


#Window to add patches to database
def AddPatch():
    AddPatchWindow = window()
    AddPatchWindow.geometry("{0}x{1}".format(ReadSettings.GetSetting("General","AddPatchXWindowSize"),ReadSettings.GetSetting("General","AddPatchYWindowSize")))
    AddPatchWindow.titlelabel("Enter patch details below",(int(ReadSettings.GetSetting("General","AddPatchXWindowSize"))//2))

    AddPatchWindow.label("What kind of patch?",1,0,W)
    SelectedPatchType = ttk.Combobox(AddPatchWindow,state="readonly",values="New Existing Removal")
    SelectedPatchType.grid(row=1,column=1,sticky=E)

    AddPatchWindow.label("Switch",2,0,W)
    SelectedSwitch = ttk.Combobox(AddPatchWindow,state="readonly",values=DatabaseControl.GetSwitchNames())
    SelectedSwitch.grid(row=2,column=1,sticky=E)

    AddPatchWindow.label("By Tech",3,0,W)
    SelectedTech = ttk.Combobox(AddPatchWindow,state="readonly",values=DatabaseControl.GetTechNames())
    SelectedTech.grid(row=3,column=1,sticky=E)

    AddPatchWindow.label("Pannel Port",4,0,W)
    SelectedPannelPort=ttk.Entry(AddPatchWindow)
    SelectedPannelPort.grid(row=4,column=1,sticky=E)

    AddPatchWindow.label("Switch Unit",5,0,W)
    SelectedSwitchUnit=ttk.Entry(AddPatchWindow)
    SelectedSwitchUnit.grid(row=5,column=1,sticky=E)  
    
    AddPatchWindow.label("Switch Port",6,0,W)
    SelectedSwitchPort=ttk.Entry(AddPatchWindow)
    SelectedSwitchPort.grid(row=6,column=1,sticky=E)  

    AddPatchWindow.label("Notes",7,0,W)
    NotesBox=ttk.Entry(AddPatchWindow)
    NotesBox.grid(row=7,column=1,sticky=E)  

    AddPatchWindow.button("Save&Commit",lambda: CommitPatch(SelectedPatchType.get(),SelectedSwitch.get(),SelectedTech.get(),SelectedPannelPort.get(),SelectedSwitchUnit.get(),SelectedSwitchPort.get(),NotesBox.get()),8,1,SW)


def SearchPatch(SearchTech,SearchLocation,SearchPannelPort,SearchUnit,SearchPort,SearchDate):
    SearchTerms="" #Setup SQL string to pass onto database cntrol


    #Add Tech to Search Terms
    if len(SearchTech.get()) != 0 and len(SearchTerms) != 0:
        SearchTerms += ' AND tech_id = "{0}"'.format(DatabaseControl.GetTechIDFromName(SearchTech.get()))
    elif len(SearchTech.get()) != 0:
        SearchTerms += ' tech_id = "{0}"'.format(DatabaseControl.GetTechIDFromName(SearchTech.get()))

    #Add location (using switch IDS) to search
    if len(SearchLocation.get()) != 0 and len(SearchTerms) != 0:
        SearchTerms += " AND (" #Switch searches need to be in a big bracket becuase they are ORs after ANDS
        for SwitchID in DatabaseControl.GetSwitchIDFromLocation(SearchLocation.get()):
            if "switch_id" in SearchTerms: #Handle multiple switches needing an OR
                SearchTerms += ' OR switch_id = "{0}"'.format(SwitchID[0])
            else:
                SearchTerms += ' switch_id = "{0}"'.format(SwitchID[0])
        SearchTerms += ")"
    elif len(SearchLocation.get()) != 0:
        SearchTerms += " (" #Switch searches need to be in a big bracket becuase other wise I have to position it at the end of the query 
        for SwitchID in DatabaseControl.GetSwitchIDFromLocation(SearchLocation.get()):
            if "switch_id" in SearchTerms: #Handle multiple switches needing an OR
                SearchTerms += ' OR switch_id = "{0}"'.format(SwitchID[0])
            else:
                SearchTerms += ' switch_id = "{0}"'.format(SwitchID[0])
        SearchTerms += ")"


    #Add PannelPort to Search Terms     
    if len(SearchPannelPort.get()) != 0 and len(SearchTerms) != 0:
        SearchTerms += ' AND PannelPort = "{0}"'.format(SearchPannelPort.get())
    elif len(SearchPannelPort.get()) != 0:
        SearchTerms += ' PannelPort = "{0}"'.format(SearchPannelPort.get())

    #Add Unit to Search Terms     
    if len(SearchUnit.get()) != 0 and len(SearchTerms) != 0:
        SearchTerms += ' AND Unit = "{0}"'.format(SearchUnit.get())
    elif len(SearchUnit.get()) != 0:
        SearchTerms += ' Unit = "{0}"'.format(SearchUnit.get())

    #Add Port to Search Terms     
    if len(SearchPort.get()) != 0 and len(SearchTerms) != 0:
        SearchTerms += ' AND Port = "{0}"'.format(SearchPort.get())
    elif len(SearchPort.get()) != 0:
        SearchTerms += ' Port = "{0}"'.format(SearchPort.get())

    #Add Date to Search Terms     
    if len(SearchDate.get()) != 0 and len(SearchTerms) != 0:
        SearchTerms += ' AND Date = "{0}"'.format(SearchDate.get())
    elif len(SearchDate.get()) != 0:
        SearchTerms += ' Date = "{0}"'.format(SearchDate.get())

    if SearchTerms == "":
        pass
    else:
        print ("SQL IS: SELECT * FROM PATCHES WHERE{0}".format(SearchTerms))
        
        #Create results window w/ headers
        SearchPatchResultsWindow=window()
        SearchPatchResultsWindow.titlelabel("Search Results for {0}".format(SearchTerms))
        SearchPatchResultsWindow.geometry("600x900")

        SearchPatchResultsWindow.label("Tech",2,0,N)
        SearchPatchResultsWindow.label("Switch",2,1,N)
        SearchPatchResultsWindow.label("Pannel Port",2,2,N)
        SearchPatchResultsWindow.label("Unit",2,3,N)
        SearchPatchResultsWindow.label("Port",2,4,N)
        SearchPatchResultsWindow.label("Date",2,5,N)
        SearchPatchResultsWindow.label("Type",2,6,N)


        #Loop though reults and add them into a row each
        row=3
        for PatchRecord in DatabaseControl.SearchPatch(SearchTerms):
            PatchID = PatchRecord[0]
            PatchTech = DatabaseControl.GetTechNameFromID(PatchRecord[1])
            PatchSwitch = DatabaseControl.GetSwitchNameFromID(PatchRecord[2])
            PatchPannel = PatchRecord[3]
            PatchUnit = PatchRecord[4]
            PatchPort = PatchRecord[5]
            PatchDate = PatchRecord[6]
            PatchNotes= PatchRecord[7]
            AlreadyPatched = PatchRecord[8]
            PatchRemoved = PatchRecord[9]

            if AlreadyPatched ==  0 and PatchRemoved == 0:
                PatchType="New"
            elif AlreadyPatched ==  1 and PatchRemoved == 0:
                PatchType="Existing"
            elif AlreadyPatched ==  1 and PatchRemoved == 1:
                PatchType="Removal"


            SearchPatchResultsWindow.label(PatchTech,row,0,W)
            SearchPatchResultsWindow.label(PatchSwitch,row,1,W)
            SearchPatchResultsWindow.label(PatchPannel,row,2,W)
            SearchPatchResultsWindow.label(PatchUnit,row,3,W)
            SearchPatchResultsWindow.label(PatchPort,row,4,W)
            SearchPatchResultsWindow.label(PatchDate,row,5,W)
            SearchPatchResultsWindow.label(PatchDate,row,5,W)
            SearchPatchResultsWindow.label(PatchType,row,6,W)

            row+=1


def SearchPatchesWindow():
    SearchPatchWindow=window()
    SearchPatchWindow.titlelabel("Set search terms")
    SearchPatchWindow.geometry("340x185")
    
    SearchPatchWindow.label("Tech",2,0,W)
    SearchTech=ttk.Combobox(SearchPatchWindow,state="readonly",values=DatabaseControl.GetTechNames())
    SearchTech.grid(row=2,column=1,sticky=W)
    SearchTechClearButton = ttk.Button(SearchPatchWindow, text="Clear", command=lambda : SearchTech.set(''))
    SearchTechClearButton.grid(row=2,column=2,sticky=E)

    SearchPatchWindow.label("Location",3,0,W)
    SearchLocation = ttk.Combobox(SearchPatchWindow,state="readonly",values=MakeLocationList())
    SearchLocation.grid(row=3,column=1,sticky=E)
    SearchLocationClearButton = ttk.Button(SearchPatchWindow, text="Clear", command=lambda : SearchLocation.set(''))
    SearchLocationClearButton.grid(row=3,column=2,sticky=E)
    
    SearchPatchWindow.label("Pannel Port",4,0,W)
    SearchPannelPort=ttk.Entry(SearchPatchWindow)
    SearchPannelPort.grid(row=4,column=1,sticky=W)

    SearchPatchWindow.label("Unit",5,0,W)
    SearchUnit=ttk.Entry(SearchPatchWindow)
    SearchUnit.grid(row=5,column=1,sticky=W)

    SearchPatchWindow.label("Port",6,0,W)
    SearchPort=ttk.Entry(SearchPatchWindow)
    SearchPort.grid(row=6,column=1,sticky=W)

    SearchPatchWindow.label("Date (DD/MM/YYYY)",7,0,W)
    SearchDate=ttk.Entry(SearchPatchWindow)
    SearchDate.grid(row=7,column=1,sticky=W)


    SearchPatchWindow.button("Search", lambda: SearchPatch(SearchTech,SearchLocation,SearchPannelPort, SearchUnit, SearchPort, SearchDate),10,2,E)



if DatabaseControl.CheckDatabaseExists() == False:
    NoDatabase = dialogwindow("No database")
    NoDatabase.label("{0} was not found".format(ReadSettings.GetSetting("Database","DatabaseLocation")),1,0,N)
    NoDatabase.button("Create now",2,0,NW, command=lambda : DatabaseSetup.SetupDatabase() and self.destroy())
    NoDatabase.CloseButton("Close",2,0,NE)

# if (DatabaseControl.CustomQuery("SELECT AlreadyPatched FROM PATCHES")[0])[0] == True:
#     print((DatabaseControl.CustomQuery("SELECT AlreadyPatched FROM PATCHES")[0])[0])
#     print("True")
# else:
#     print(DatabaseControl.CustomQuery("SELECT AlreadyPatched FROM PATCHES"))
#     print((DatabaseControl.CustomQuery("SELECT AlreadyPatched FROM PATCHES")[0])[0])

#Configure main window
MainWindow = window()
MainWindow.titlelabel()
#MainWindow.button("Setup Database",lambda : DatabaseSetup.SetupDatabase(),2,0,N)
MainWindow.button("Add patch(s)", lambda : AddPatch(),2,0,NE)
MainWindow.button("Search Patches", lambda : SearchPatchesWindow(),2,1,N)
MainWindow.button("Show Switches", lambda : ShowSwitches(),2,2,N)

MainWindow.button("Add New Tech", lambda : CreateNewTechWindow(),4,0,NE)
MainWindow.button("Add New Switch", lambda : CreateNewSwitchWindow(),4,1,NE)

#Spawn Main Window
MainWindow.mainloop()
