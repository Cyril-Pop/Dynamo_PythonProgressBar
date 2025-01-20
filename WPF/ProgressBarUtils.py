# Python Script | Module ProgressBarUtils
import sys
import clr
import System
from System import Array

clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("System.Xml")
clr.AddReference("PresentationCore")
clr.AddReference("System.Windows")
clr.AddReference("WindowsBase")
import System.Windows.Controls 
from System.Windows.Controls import *
from System.IO import StringReader
from System.Xml import XmlReader
from System.Windows import LogicalTreeHelper 
from System.Windows.Markup import XamlReader, XamlWriter
from System.Windows import Window, Application

import traceback

class ProgressBarUtils():
    def __init__(self):
        pass
        
    def __name__(self):
        return 'ProgressBarUtils'
        
        
    class ProgressBarDialog(Window):
        LAYOUT = '''
        <Window 
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        Title="Progression"
        Height="200" Width="400"
        MinHeight="200" MinWidth="400"
        ResizeMode="CanResizeWithGrip"
        x:Name="MainWindow">
        <Grid>
            <ProgressBar
                Name="pbar"
                Minimum="0" Maximum="100"
                Grid.Column="0" Grid.Row="0"
                HorizontalAlignment="Stretch" VerticalAlignment="Top"
                Margin="20,40,20,10"
                Height="30" />
            <TextBlock
                Name="progressText"
                TextAlignment="Center"
                Text="--"
                Height="20"
                VerticalAlignment="Top" HorizontalAlignment="Stretch"
                Grid.Row="0" Grid.Column="0"
                Margin="5,45,5,5" />
            <TextBlock
                Name="infotext"
                TextAlignment="Left"
                Text="--"
                Height="40"
                VerticalAlignment="Bottom" HorizontalAlignment="Stretch"
                Grid.Row="0" Grid.Column="0"
                Margin="20,20,20,25" />
        </Grid>
    </Window>'''
        
        def __init__(self, max, title = ""):
            super().__init__()
            xr = XmlReader.Create(StringReader(ProgressBarUtils.ProgressBarDialog.LAYOUT))
            self.winLoad = XamlReader.Load(xr) 
            self.progressText = LogicalTreeHelper.FindLogicalNode(self.winLoad, "progressText")
            self.pbar = LogicalTreeHelper.FindLogicalNode(self.winLoad, "pbar")
            self.infoText = LogicalTreeHelper.FindLogicalNode(self.winLoad, "infotext")
            self.new_value = 0
            self.new_textInfo = "--"
            self.infoText.Text = self.new_textInfo
            self.pbar.Maximum = max
            self.winLoad.Title = title
            self.method_info_dispatcher  = next(
                                                (m for m in self.winLoad.Dispatcher.GetType().GetMethods()\
                                                if "Void Invoke(System.Action, System.Windows.Threading.DispatcherPriority)" == m.ToString()),
                                                None)
            self._dispatch_updater()
            
    
        def _dispatch_updater(self):
            try:
                # ask WPF dispatcher for gui update
                if self.method_info_dispatcher is not None:
                    args = Array[System.Object]([System.Action(self._update_pbar), System.Windows.Threading.DispatcherPriority.Background])
                    self.method_info_dispatcher.Invoke(self.winLoad.Dispatcher, args)
            except Exception as ex:
                print(traceback.format_exc())
    
        def _update_pbar(self):
            try:
                self.pbar.Value = self.new_value
                self.progressText.Text = "Items Processing: {}/{}".format(int(self.pbar.Value), int(self.pbar.Maximum))
                self.infoText.Text = self.new_textInfo
                if self.pbar.Value == self.pbar.Maximum:
                    self.winLoad.Close()
            except Exception as ex:
                print(traceback.format_exc())
        
        def update_progress(self, value):
            try:
                self.new_value = value
                self._dispatch_updater()
                self.winLoad.Activate()
            except Exception as ex:
                print(traceback.format_exc())
            
    class MyProgressBroadcaster():
        """
        main Class to Start UI and build a custom Event with a  ContextManager
        """
        def __init__(self, numberLines, title = "My_progressBar"):
            self.numberLines = numberLines
            self.title = title
            self.ui = None
            
        def next(self, infoPgb="-"):
            if self.ui is not None:
                try:
                    self.ui.new_textInfo = infoPgb
                    self.ui.update_progress(self.ui.new_value + 1)
                except Exception as ex:
                    print(traceback.format_exc())
            
        def __enter__(self):        
            try:
                self.ui = ProgressBarUtils.ProgressBarDialog(self.numberLines, self.title)
                self.ui.winLoad.Show()
                return self
            except Exception as ex:
                print(traceback.format_exc())
                return None
            
        def __exit__(self, exc_type, exc_value, traceback):
            try:
                print(exc_type)
                print(exc_value)
                if traceback:
                    exc_tbnext = traceback
                    lst_lines_error = []
                    for i in range(2):
                        if exc_tbnext is not None:
                            lst_lines_error.append(str(exc_tbnext.tb_lineno))
                            exc_tbnext = exc_tbnext.tb_next
                        else:
                            break
                    #print(lst_lines_error)
                    error = "Error : {} at lines : line : {}".format( exc_value, " -> line : ".join(lst_lines_error))
                    print("{}\n{}".format(exc_type.__name__, error))
            except Exception as ex:
                print(traceback.format_exc())

OUT = ProgressBarUtils
