import sys
import clr
import System
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

from System.Windows.Forms import Application, Form, ProgressBar
from System.Threading import ThreadStart, Thread
from System import Int32, Int64

__author__ = "Cyril POUPIN"
__copyright__ = "Copyright (c) 2022 Cyril.P"
__license__ = "MIT License"
__version__ = "2.0.3"

class ProgressBarUtils():

	def __init__(self):
		pass
		
	def __name__(self):
		return 'ProgressBarUtils'
		

	class ProgressBarDialog(Form):
		def __init__(self, theBroadcaster, numberLines, myTitle ):
			self._numberLines = numberLines
			self._theBroadcaster = theBroadcaster
			self._theBroadcaster.onChange += self.myFunction
			self._myTitle = myTitle
			self.InitializeComponent()
			Application.DoEvents()
			
		
		def InitializeComponent(self):
			self._buttonCancel = System.Windows.Forms.Button()
			self._progressBar1 = System.Windows.Forms.ProgressBar()
			self._label1 = System.Windows.Forms.Label()
			self._label_info = System.Windows.Forms.Label()
			self.SuspendLayout()
			# 
			# buttonCancel
			# 
			self._buttonCancel.Location = System.Drawing.Point(228, 96)
			self._buttonCancel.Name = "buttonCancel"
			self._buttonCancel.Size = System.Drawing.Size(116, 32)
			self._buttonCancel.TabIndex = 0
			self._buttonCancel.Text = "Quit"
			self._buttonCancel.UseVisualStyleBackColor = True
			self._buttonCancel.Click += self.ButtonCancelClick
			# 
			# progressBar1
			# 
			self._progressBar1.Location = System.Drawing.Point(12, 48)
			self._progressBar1.Name = "progressBar1"
			self._progressBar1.Size = System.Drawing.Size(535, 23)
			self._progressBar1.Minimum = 0
			self._progressBar1.Maximum = self._numberLines
			self._progressBar1.Step = 1
			self._progressBar1.Value = 0
			self._progressBar1.TabIndex = 1
			# 
			# label1
			# 
			self._label1.Location = System.Drawing.Point(12, 22)
			self._label1.Name = "label1"
			self._label1.Size = System.Drawing.Size(250, 23)
			self._label1.TabIndex = 2
			self._label1.Text = "Items Processing 0/" + str(self._numberLines)
			# 
			# label_info
			# 
			self._label_info.Location = System.Drawing.Point(12, 80)
			self._label_info.Name = "label_info"
			self._label_info.Size = System.Drawing.Size(400, 30)
			self._label_info.TabIndex = 3
			self._label_info.Text = ""
			# 
			# MainForm
			# 
			self.ClientSize = System.Drawing.Size(567, 140)
			self.MinimumSize = System.Drawing.Size.Add(self.ClientSize, System.Drawing.Size(20, 20))
			self.Controls.Add(self._label1)
			self.Controls.Add(self._label_info)
			self.Controls.Add(self._progressBar1)
			#self.Controls.Add(self._buttonCancel)
			self.Name = "MainForm"
			self.Text = self._myTitle
			self.ResumeLayout(False)
			
			
		def myFunction(self, txt_info = None):
			try:
				Application.DoEvents()
			except:pass	
			if self._progressBar1.Value < self._progressBar1.Maximum:
				self._progressBar1.PerformStep()
				self._label1.Text = "Items Processing {}/{}".format(str(self._progressBar1.Value), str(self._numberLines))
				if txt_info is not None:
					self._label_info.Text = txt_info
			else:
				self._progressBar1.Value = self._progressBar1.Maximum
				self._theBroadcaster.onChange -= self.myFunction	
				print("Close")
				self.Close()				
		
		def ButtonCancelClick(self, sender, e):
			self.Close()
			
	
			
	class EventHook():
		def __init__(self):
			self.__handlers = []
			
		def __iadd__(self, handler):
			self.__handlers.append(handler)
			return self
	
		def __isub__(self, handler):
			self.__handlers.remove(handler)
			return self
	
		def next_p(self, *args, **keywargs):
			for handler in self.__handlers:
				handler(*args, **keywargs)
	
		def clearObjectHandlers(self, inObject):
			for theHandler in self.__handlers:
				if theHandler.im_self == inObject:
					self -= theHandler
					
		def forceClearHandlers(self):
			for theHandler in self.__handlers:
				self -= theHandler
				
	
	class MyProgressBroadcaster():
		"""
		main Class to Start UI and build a custom Event with a  ContextManager
		"""
		def __init__(self, number_Iteration,  UI_Title = "Progress Bar"):
			self.f = None
			if isinstance(number_Iteration, (Int32, Int64, int)):
				self._number_Iteration = number_Iteration
			else:
				raise Exception("MyProgressBroadcaster : wrong 1st argument need an integer")
			if isinstance(UI_Title, str):    
				self._title = UI_Title
			else:
				raise Exception("MyProgressBroadcaster : wrong 2nd argument need an string")
			self.purg = False
			
		def __enter__(self):		
			self.onChange = ProgressBarUtils.EventHook()	
			Application.EnableVisualStyles()
			self.f = ProgressBarUtils.ProgressBarDialog(self, self._number_Iteration, self._title)
			self.f.Show()
			return 	self
			
		def __exit__(self, exc_type, exc_value, exc_tb):
			print("exit")
			if exc_type:
				error = "Error : {} at line {}\n".format( exc_value, exc_tb.tb_lineno)
				print("{}\n{}".format(exc_type.__name__, error))
			self.onChange.next_p()
			Thread.Sleep(500)
			self.onChange.forceClearHandlers()
			if self.f is not None:
				self.f.Dispose()
			
