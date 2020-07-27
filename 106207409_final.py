import wx
import sqlite3
import wx.lib.agw.hyperlink as hl
import requests
from ObjectListView import ObjectListView, ColumnDefn
import t2
import re
import datetime
from bs4 import BeautifulSoup
import os
import certifi
import urllib3

get = ''
cb = ' '
# clickboxchoice = {'爆':True,'99-80':True,'76-60'} 
APP_EXIT = 1
path2 = 'C:/Users/user/Desktop'

class Window1(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,parent=None,title = u"Ptt tool",size = (350,200))
		panel = wx.Panel(self)
		self.board='default'

###選擇看板
		self.choice = self.connect_with()
		wx.StaticText(parent=panel,label="選擇看板",pos=(15,20))
		self.choose_board = wx.ComboBox(panel,20,"",wx.Point(75,15),
			wx.Size(95,-1),self.choice,wx.CB_DROPDOWN)
		self.choose_board.Bind(wx.EVT_COMBOBOX,self.choose_board_exe)

##勾選要顯示的文章 用讚數搜索
		self.cb1 = wx.CheckBox(panel,label = u'爆',pos = (15,50))
		self.w1_text =wx.StaticText(parent=panel,label="",pos=(15,110))
		self.cb1.SetValue(wx.CHK_CHECKED)
		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 
		self.Centre() 
		self.Show(True) 


		self.main_btn1 = wx.Button(parent=panel,label=u"查詢",pos = (10,75))
		self.main_btn1.Bind(wx.EVT_BUTTON,self.main_btn1_exe)


		self.menuu()

	def menuu(self):
##建立上面menu
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		fileMenu2 = wx.Menu()

		menubar.Append(fileMenu,'&File')
		menubar.Append(fileMenu2,'&Setting')
		self.SetMenuBar(menubar)

		qmi = wx.MenuItem(fileMenu,APP_EXIT,'&Quit\tCtrl+Q')
		img = wx.Image('sign.bmp', wx.BITMAP_TYPE_ANY)
		img.Rescale(width=10,height=10)
		qmi.SetBitmap(wx.BitmapFromImage(img))
		
		fileMenu.Append(qmi)

		m_about = fileMenu.Append(wx.ID_ABOUT, "&My Favorite", "Information about this program")
		self.Bind(wx.EVT_MENU, self.ShowFrameFav, m_about)

		choose_download = fileMenu2.Append(wx.NewId(), "&Select Field", "Select download file")
		self.Bind(wx.EVT_MENU, self.Choose_download, choose_download)
		delete_fav_board = fileMenu2.Append(wx.NewId(), "&Delete board", "Select download file")
		self.Bind(wx.EVT_MENU, self.Delete_favboard, delete_fav_board)

		self.Bind(wx.EVT_MENU,self.OnQuit,id = APP_EXIT)

	def ShowFrameFav(sel,event):
		frame = MainFrame2()
		frame.Show()
	def Choose_download(self,event):
		frame0 =  Choose_field()
		frame0.Show()
	def Delete_favboard(self,event):
		self.Close()
		frame01 = Delete_fav_board()
		frame01.Show()


	def onChecked(self, e): 
		global cb
		cb = e.GetEventObject() 
		print (cb.GetLabel(),' is clicked',cb.GetValue())

	def OnQuit(self,e):
		self.Close()

	def connect_with(self):
		all_board = []
		self.conn = sqlite3.connect("final_data.db")
		self.c = self.conn.cursor()
		self.c.execute("SELECT DISTINCT NAME FROM OPTION")
		unit = self.c.fetchall()
		for i in unit :
			all_board.append(i[0])
		all_board.append(u'--自行新增--')
		return all_board
		self.conn.close()


	def choose_board_exe(self,event):
		global get
		get = self.choose_board.GetValue()
		if get =='--自行新增--':
			self.Close()
			frame2 = Addnewboard()
			frame2.Show()
		else:
			print("選擇"+get+"......")

	def main_btn1_exe(self,event):
		frame3 = MainFrame()
		print("看板查詢完畢")
		frame3.Show()

	def main_btn2_exe(self,event):
		pass

	def main_btn3_exe(self,event):
		pass


new_board = ''

class Addnewboard(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,parent=None,title= u"添加新看板",size=(280,150))
		panel = wx.Panel(self)

		wx.StaticText(parent=panel,label="輸入看板名稱看板",pos=(20,20))
		self.a = wx.StaticText(parent=panel,label=" ",pos=(20,85))
		self.input_new_board = wx.TextCtrl(panel, -1, size =(110, 25),pos=(125,15))
		self.addboard_btn1 = wx.Button(parent=panel,label=u"添加",pos=(35,50))
		self.addboard_btn1.Bind(wx.EVT_BUTTON,self.Addnewboard)
		self.addboard_btn2 = wx.Button(parent=panel,label=u"取消",pos=(135,50))
		self.addboard_btn2.Bind(wx.EVT_BUTTON,self.Cancel_Addnewboard)

#與資料庫連結
	def connect_with(self):
		self.conn = sqlite3.connect("final_data.db")
		self.c = self.conn.cursor()

	def Addnewboard(self,event):
		self.connect_with()
		all_board = []
		self.c.execute("SELECT DISTINCT NAME FROM OPTION")
		unit = self.c.fetchall()
		for i in unit :
			all_board.append(i[0])

		new_board = self.input_new_board.GetValue()
		if new_board not in all_board :
			request = requests.get('https://www.ptt.cc/bbs/%s/index.html'%new_board)
			if request.status_code == 200:
				print('Web site exists')
				self.c.execute("INSERT INTO OPTION (NAME,SUM)VALUES(?,?)",(new_board,0))
				self.conn.commit()
				print('新增看板成功!')
				self.input_new_board.ChangeValue(' ')
				frame0 = Window1()
				frame0.Show()
				frame0.w1_text.SetLabel("新增看板%s成功!"%new_board)
				frame0.w1_text.SetForegroundColour((255,0,0))
				self.Close()
			else:
				print('Web site does not exist')
				self.a.SetLabel(u'PTT不存在此看板')
				self.a.SetForegroundColour((255,0,0))
		else:
			self.a.SetLabel(u'看板已存在清單中!')
			self.a.SetForegroundColour((255,0,0))
			self.input_new_board.ChangeValue(' ')
		self.conn.close()
	def Cancel_Addnewboard(self,event):
		frame = Window1()
		frame.Show()
		self.Destroy()

######ObjectListView開始###
import  wx.lib.newevent
from ObjectListView import ObjectListView, ColumnDefn,OLVEvent
OvlCheckEvent, EVT_OVL_CHECK_EVENT = wx.lib.newevent.NewEvent()

class MyOvl(ObjectListView):  
	def SetCheckState(self, modelObject, state):
		if self.checkStateColumn is None:
			return None
		else:
			r = self.checkStateColumn.SetCheckState(modelObject, state)
##事件
			e = OvlCheckEvent(object=modelObject, value=state)
			wx.PostEvent(self, e)

			return r

	def _HandleLeftDownOnImage(self, rowIndex, subItemIndex):
		column = self.columns[subItemIndex]
		if not column.HasCheckState():
			return

		self._PossibleFinishCellEdit()
		modelObject = self.GetObjectAt(rowIndex)
		if modelObject is not None:
			column.SetCheckState(modelObject, not column.GetCheckState(modelObject))
###事件
			e = OvlCheckEvent(object=modelObject, value=column.GetCheckState(modelObject))
			wx.PostEvent(self, e)

			self.RefreshIndex(rowIndex, modelObject)

class Post(object):
	def __init__(self,idd,push,title,author,date,URL):
		self.idd=idd
		self.push=push
		self.date = date
		self.author = author
		self.URL = URL
		self.title = title

class Select_post(wx.Panel):
	def __init__(self,parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		self.dataOlv = MyOvl(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
		self.dataOlv.SetColumns([
			ColumnDefn("Push", "left", 80, "push"),
			ColumnDefn("Title", "left", 220, "title"),
			ColumnDefn("Author", "left", 200, "author"),
			ColumnDefn("date", "left", 100, "date"),			
			ColumnDefn("URL", "left", 180, "URL")])

		self.dataOlv.Bind(EVT_OVL_CHECK_EVENT, self.HandleCheckbox)
		self.dataOlv.CreateCheckStateColumn()
		# self.into()
		self.hey()
		self.scrab()

		self.post_btn1 = wx.Button(self,wx.ID_ANY,u"下載圖片")
		self.post_btn2 = wx.Button(self,wx.ID_ANY,u"加入我的最愛")
		self.post_btn1.Bind(wx.EVT_BUTTON,self.open_download)
		self.post_btn2.Bind(wx.EVT_BUTTON,self.Add_to_my_fav)

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		smallSizer = wx.BoxSizer(wx.HORIZONTAL)
		mainSizer.Add(self.dataOlv, 1, wx.ALL|wx.EXPAND, 5)
		smallSizer.Add(self.post_btn1, 0, wx.ALL|wx.CENTER, 5)
		smallSizer.Add(self.post_btn2, 0, wx.ALL|wx.CENTER, 5)
		mainSizer.Add(smallSizer, 0, wx.ALL|wx.CENTER, 5)
		self.SetSizer(mainSizer)

		self.select_true=[]
		self.select_false=[]
	def hey(self):
		self.ur = ''
		self.next_page = ''

	##得到打勾的狀態
	def HandleCheckbox(self, e):
		# print(e.object.title, e.value)
		self.get_idd = e.object.idd
		self.get_value = e.value
		if e.value is True:
			self.select_true.append(self.get_idd)
		else:
			self.select_false.append(self.get_idd)

	def rr(self,event):
		for i in self.select_true:
			if i in self.select_false:
				self.select_true.remove(i)
				self.select_false.remove(i)
		print('打勾勾是')
		print(self.select_true) ##click
		print(get)

	def fetch(self,url):
		soup=BeautifulSoup(requests.get(url,cookies={'over18':'1'}).text,'lxml') #18歲的確認
		return soup
	def get_anything(self,url): #印出爆的檔案
		from time import sleep
		soup = self.fetch(url)
		for i in soup.find_all('div','r-ent'):
			nrec = i.find('div','nrec').text.strip() ##爆
			title = i.find('div','title').text.strip()
			author = i.find('div','author').text.strip()
			date = i.find('div','date').text.strip()
			if self.aa <=9:
				try:
					if  '爆' in nrec:
						print("已搜索到")
						idd = 0
						self.ur = 'https://www.ptt.cc'+ i.find('div','title').find('a').get("href")
						all_ = self.aa,str(nrec),str(title),str(author),str(date),str(self.ur)
						self.all_post.append(all_)
						print(all_)
						self.aa+=1
				except AttributeError:
					print('there has nothing')
			else:
				self.flag=False

		for i in soup.find_all('a','btn wide'): #找出下一頁
			if '上頁' in i.text:
				self.next_page = 'https://www.ptt.cc'+i.attrs['href']
			
		sleep(0.5)#暫停十秒，一直向伺服器請求會被暫停，顯示錯
		if self.flag is 	True:
			self.get_anything(self.next_page)

	def scrab(self):
		make_up = self.fetch('https://www.ptt.cc/bbs/%s/index3181.html'%get)
		self.aa = 0
		self.flag = True
		self.all_post = []
		self.get_anything('https://www.ptt.cc/bbs/%s/index.html'%get)

		self.posts = []
		for i in self.all_post:
			self.posts.append(Post(i[0],i[1],i[2],i[3],i[4],i[5]))
		self.dataOlv.SetObjects(self.posts)


	def Add_to_my_fav(self,event):
		conn = sqlite3.connect("final_data.db")
		c = conn.cursor()
		fav = []
		for i in self.select_true:
			print(self.all_post[int(i)][2]+"   已加入我的最愛")
			c.execute("INSERT INTO MYFAV(TITLE,AUTHOR,DATEE,URL)VALUES(?,?,?,?)"\
				,(self.all_post[int(i)][2],self.all_post[int(i)][3],self.all_post[int(i)][4],self.all_post[int(i)][5]))
		conn.commit()
		conn.close()
		self.Show_message_fav()
	def open_download(self,event):
		global path2
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		for i in self.select_true:
			if i in self.select_false:
				self.select_true.remove(i)
				self.select_false.remove(i)
		global path2
		print('進入'+path2)
		for i in self.select_true:
			aa = self.all_post[i][5] #網址
			try:
				if ':'not in self.all_post[i][2]:
					os.mkdir(path2+"/{0}".format(self.all_post[i][2]))
					hey = path2+"/{0}".format(self.all_post[i][2])
					print('建立資料夾 '+self.all_post[i][2])
				else:
					folder_name = 'Re'+self.all_post[i][2].split(':')[1]
					print(print('建立資料夾 '+folder_name))
					hey = path2+"/{0}".format(folder_name)
					os.mkdir(path2+"/{0}".format(folder_name))
			except FileExistsError :
				print("資料夾已存在，進入資料夾......")
			search_url = soup=BeautifulSoup(requests.get(aa,cookies={'over18':'1'}).text,'lxml')
			for i in search_url.find_all('a',href=re.compile((".*?\.jpg"))):
				Download(hey,i.get("href"))
		print('下載完畢!')
		self.Show_message()
	def Show_message(self):
		wx.MessageBox('下載成功', 'Info', 
			wx.OK | wx.ICON_INFORMATION)
	def Show_message_fav(self):
		wx.MessageBox('成功加入我的最愛', 'Info', 
			wx.OK | wx.ICON_INFORMATION)



class MainFrame(wx.Frame):
	#----------------------------------------------------------------------
	def __init__(self):
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, 
			title="Search Result", size=(800,600))
		panel = Select_post(self)


class MainFrame2(wx.Frame):##我的最愛
	#----------------------------------------------------------------------
	def __init__(self):
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, 
			title="My favorite", size=(800,600))
		panel = ShowFav(self)


class FavPost(object):
	def __init__(self,idd,title,author,date,URL):
		self.idd=idd
		self.date = date
		self.author = author
		self.URL = URL
		self.title = title
class ShowFav(wx.Panel):
	def __init__(self,parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		self.Fav_dataOlv = MyOvl(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
		self.Fav_dataOlv.SetColumns([
			ColumnDefn("Title", "left", 220, "title"),
			ColumnDefn("Author", "left", 200, "author"),
			ColumnDefn("date", "left", 100, "date"),			
			ColumnDefn("URL", "left", 180, "URL")])

		self.Fav_dataOlv.Bind(EVT_OVL_CHECK_EVENT, self.HandleCheckbox)
		self.Fav_dataOlv.CreateCheckStateColumn()
		# self.into()
		# self.hey()
		# self.scrab()

		self.post_btn1 = wx.Button(self,wx.ID_ANY,u"下載圖片")
		self.post_btn2 = wx.Button(self,wx.ID_ANY,u"刪除")
		# self.post_btn3 = wx.Button(self,wx.ID_ANY,u"回到初始頁")
		self.post_btn1.Bind(wx.EVT_BUTTON,self.Fav_Download)
		self.post_btn2.Bind(wx.EVT_BUTTON,self.Fav_Delete)
		# self.post_btn3.Bind(wx.EVT_BUTTON,self.Fav_Back)

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		smallSizer = wx.BoxSizer(wx.HORIZONTAL)
		mainSizer.Add(self.Fav_dataOlv, 1, wx.ALL|wx.EXPAND, 5)
		smallSizer.Add(self.post_btn1, 0, wx.ALL|wx.CENTER, 5)
		smallSizer.Add(self.post_btn2, 0, wx.ALL|wx.CENTER, 5)
		# smallSizer.Add(self.post_btn3, 0, wx.ALL|wx.CENTER, 5)
		mainSizer.Add(smallSizer, 0, wx.ALL|wx.CENTER, 5)
		self.SetSizer(mainSizer)
		self.select_true = []
		self.select_false=[]

		self.SearchMyFav()
	def HandleCheckbox(self, e):
		# print(e.object.title, e.value)
		self.get_idd = e.object.idd
		self.get_value = e.value
		if e.value is True:
			self.select_true.append(self.get_idd)
		else:
			self.select_false.append(self.get_idd)
	def SearchMyFav(self):
		conn = sqlite3.connect("final_data.db")
		c = conn.cursor()
		c.execute("SELECT * FROM MYFAV")
		unit = c.fetchall()
		self.allfav = []
		idd = 0
		for i in unit:
			# print(i)
			self.allfav.append(i)
		fav = []
		for i  in  self.allfav:
			fav.append(FavPost(idd,i[0],i[1],i[2],i[3]))
			idd+=1
		self.Fav_dataOlv.SetObjects(fav)
		conn.close()
	def Fav_Download(self,event):
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		for i in self.select_true:
			if i in self.select_false:
				self.select_true.remove(i)
				self.select_false.remove(i)
		# print(self.select_true)##取消的消失了
		global path2
		print('進入'+path2)
		for i in self.select_true:
			aa = self.allfav[i][3] #網址
			try:
				if ':'not in self.allfav[i][0]:
					os.mkdir(path2+"/{0}".format(self.allfav[i][0]))
					hey = path2+"/{0}".format(self.allfav[i][0])
					print('建立資料夾 '+self.allfav[i][0])
				else:
					folder_name = 'Re'+self.allfav[i][0].split(':')[1]
					print(print('建立資料夾 '+folder_name))
					hey = path2+"/{0}".format(folder_name)
					os.mkdir(path2+"/{0}".format(folder_name))
			except FileExistsError :
				print("資料夾已存在，進入資料夾......")
			# localpath =  path2+"/%s"%allfav[i][]
			make_up = soup=BeautifulSoup(requests.get(aa,cookies={'over18':'1'}).text,'lxml')
			self.amount = len(make_up.find_all('a',href=re.compile((".*?\.jpg"))))
			# self.Loading()
			for i in make_up.find_all('a',href=re.compile((".*?\.jpg"))):
				# print(i.get("href"))
				self.amount -=1
				Download(hey,i.get("href"))
		print('下載完畢!')
		self.Show_message()

	def Fav_Delete(self,event):
		conn = sqlite3.connect("final_data.db")
		c = conn.cursor()
		for i in self.select_true:
			if i in self.select_false:
				self.select_true.remove(i)
				self.select_false.remove(i)
		for i in  self.select_true:
			print(self.allfav[i][0]+' 已刪除')##要被刪掉的文章名稱
			c.execute("DELETE FROM MYFAV WHERE TITLE=?", (self.allfav[i][0],))##記得加上逗號!
		conn.commit()
		conn.close()
		self.Show_message_delete()
		self.SearchMyFav()
	def Show_message(self):
		wx.MessageBox('下載成功', 'Info', 
			wx.OK | wx.ICON_INFORMATION)
	def Show_message_delete(self):
		wx.MessageBox('刪除成功', 'Delete successfully', 
			wx.OK | wx.ICON_INFORMATION)


class Download:
	def __init__(self,path,url):
		self.path = path
		self.url = url
		print('download image.....', url)
		rs = requests.session()
		res_img = rs.get(url, stream=True, verify=False)
		file_name = url.split('/')[-1]
		file = os.path.join(path, file_name)
		try:
			with open(file, 'wb') as out_file:
				out_file.write(res_img.content)
		except Exception as e:
			print(e)

class Choose_field(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,parent=None,title=u"選擇資料夾",size=(500,150))
		panel = wx.Panel(self)
		wx.StaticText(parent=panel,label=u"選擇資料夾",pos=(10,10))
		self.textbox2 = wx.TextCtrl(panel, -1, size =(250, 25),pos=(110,10))
		self.btn = wx.Button(parent=panel,label=u"瀏覽",pos=(370,10))
		self.btn3 = wx.Button(parent=panel,label=u"確定",pos=(370,50))
		# self.Bind(wx.EVT_BUTTON,self.OnButton1,self.btn)
		self.Bind(wx.EVT_BUTTON,self.OnButton1,self.btn)
		self.Bind(wx.EVT_BUTTON,self.Ok,self.btn3)
		# self.Show()

	def OnButton1(self, event):
		global path2
		print(path2)
		file_wildcard = "All files(*.*)|*.*"
		dlg = wx.DirDialog(self,u"選擇文件夾",style=wx.DD_DEFAULT_STYLE)
		if dlg.ShowModal() == wx.ID_OK:

			path2 = dlg.GetPath().replace('\\','/')
			self.textbox2.SetLabel(path2)
		print(path2)
		dlg.Destroy()

	def Ok(self,event):
		self.Destroy()

class Yes(wx.Frame):
	def ShowFrameFav(sel,event):
		frame = 	MainFrame2()
		frame.Show()

class Delete_fav_board(wx.Frame):
	"""docstring for Delete_fav_board"""
	def __init__(self):
		wx.Frame.__init__(self,parent=None,title=u"刪除我的常用看板",size=(300,150))
		panel = wx.Panel(self)
		wx.StaticText(parent=panel,label=u"選擇要刪除的看板",pos=(10,20))
		self.choice = self.connect()
		self.select_delete = wx.ComboBox(panel,20,"",wx.Point(120,15),
			wx.Size(95,-1),self.choice,wx.CB_DROPDOWN)
		# self.select_delete.Bind(wx.EVT_COMBOBOX,self.select_delete_exe)
		self.sure_delete = wx.Button(parent=panel,label=u"刪除",pos = (10,50))
		self.sure_delete.Bind(wx.EVT_BUTTON,self.delete_exe)
	def delete_exe(self,event):
		select_d = self.select_delete.GetValue()
		conn = sqlite3.connect("final_data.db")
		c = conn.cursor()
		c.execute("DELETE FROM OPTION WHERE NAME=?", (select_d,))
		conn.commit()
		conn.close()
		print(select_d+"已刪除")
		frame0 = Window1()
		frame0.Show()
		self.Close()
		self.Show_message_delete()
	def connect(self):
		all_board = []
		conn = sqlite3.connect("final_data.db")
		c = conn.cursor()
		c.execute("SELECT NAME FROM OPTION")
		unit = c.fetchall()
		for i in unit :
			all_board.append(i[0]) ##i是tuple
		conn.close()
		return all_board
	def Show_message_delete(self):
		wx.MessageBox('刪除成功', 'Delete successfully', 
		wx.OK | wx.ICON_INFORMATION)




if __name__ =="__main__":
	app = wx.App(False)
	frame = Window1()
	frame.Show()
	app.MainLoop()