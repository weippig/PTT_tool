import wx
from ObjectListView import ObjectListView, ColumnDefn
 
########################################################################
class Book(object):
    def __init__(self, title, author, date, URL):
        self.date = date
        self.author = author
        self.URL = URL
        self.title = title
 
 
########################################################################
class MainPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.products = [Book("wxPython in Action", "Robin Dunn",
                              "1932394621", "Manning"),
                         Book("Hello World", "Warren and Carter Sande",
                              "1933988495", "Manning")
                         ]
 
        self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.setBooks()
 
        # Allow the cell values to be edited when double-clicked
        self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
 
        # create an update button
        updateBtn = wx.Button(self, wx.ID_ANY, "Update OLV")
        updateBtn.Bind(wx.EVT_BUTTON, self.updateControl)
 
        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)        
 
        mainSizer.Add(self.dataOlv, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(updateBtn, 0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(mainSizer)
 
    #----------------------------------------------------------------------
    def updateControl(self, event):
        """
 
        """
        print ("updating...")
        product_dict = [{"title":"Core Python Programming", "author":"Wesley Chun",
                         "date":"0132269937", "URL":"Prentice Hall"},
                        {"title":"Python Programming for the Absolute Beginner",
                         "author":"Michael Dawson", "date":"1598631128",
                         "URL":"Course Technology"},
                        {"title":"Learning Python", "author":"Mark Lutz",
                         "date":"0596513984", "URL":"O'Reilly"}
                        ]
        data = self.products + product_dict
        self.dataOlv.CreateCheckStateColumn()
        self.dataOlv.SetObjects(data)
        self.CheckBoxes = True

 
    #----------------------------------------------------------------------
    def setBooks(self, data=None):
        self.dataOlv.SetColumns([
            ColumnDefn("Title", "left", 220, "title"),
            ColumnDefn("Author", "left", 200, "author"),
            ColumnDefn("date", "right", 100, "date"),            
            ColumnDefn("URL", "left", 180, "URL")
        ])
 
        self.dataOlv.SetObjects(self.products)
 
########################################################################
class MainFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, 
                          title="ObjectListView Demo", size=(800,600))
        panel = MainPanel(self)
 
########################################################################
class GenApp(wx.App):
 
    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
 
    #----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = MainFrame()
        frame.Show()
        return True
 
#----------------------------------------------------------------------
def main():
    """
    Run the demo
    """
    app = GenApp()
    app.MainLoop()
 
def start():
    if __name__ == "__main__":
        main()