#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi, urllib, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio, Gdk
from gi.repository import GdkPixbuf, GLib

class Gdeb(Gtk.FileChooserDialog):
    SelectDebFiles = []
    ProjeName = ''
    ProjePath = ''
    DesktopIconDict = {}
    PyDict = {}
    DesktopFile = ''
    DesktopFilePath = ''
    #PythonMainFile = ''
    #AppIconFile = ''
    def make(self, DesktopCheckButton):
        #print (self.DesktopIconDict)
        #print (self.PyDict)
        #print self.DesktopFile
        DebMakeString, DesktopMakeString = "", ""
        DebMakeFolder = self.ProjePath+'/'+self.ProjeName+'/'+'DEBIAN'
        if os.path.isdir(DebMakeFolder) is False:
            os.makedirs(DebMakeFolder)
        os.system('touch '+DebMakeFolder+'/control')
        for makefile in zip([self.PackageEntry.get_text(), self.VersionEntry.get_text(), self.SectionEntry.get_text(), 
                self.PriorityEntry.get_text(), self.ContactEntry.get_text(), self.CpuEntry.get_active_text(),
                    self.DescriptionEntry.get_text()], 
                        ['Package:', 'Version:', 'Section:', 'Priority:', 
                            'Maintainer:', 'Architecture:', 'Description:']):
            DebMakeString = DebMakeString + makefile[1]+chr(32)+makefile[0] +'\n'
        with open(DebMakeFolder+'/control', 'w') as control:
            control.write(DebMakeString)
        for makefile in zip(['Version', 'Name', 'Encoding', 'Comment', 
                'Path', 'Exec', 'Icon', 'Terminal', 'Type', 'Categories'],
                    [self.VersionEntry.get_text(), self.PackageEntry.get_text(), 'UTF-8', self.DescriptionEntry.get_text(), 
                        '/usr/local/bin/'+self.ProjeName, 
                            self.ExceComboBoxText.get_active_text().lower()+' '+self.PyDict[self.MainComboBoxText.get_text()]['py'], 
                            self.DesktopIconDict[self.DesktopIconComboBoxText.get_text()]['png'],
                            'false', 'Application', 
                            self.CategoriesComboBoxText.get_active_text()[0:self.CategoriesComboBoxText.get_active_text().find(' ')]+';']):
            DesktopMakeString = DesktopMakeString + str(makefile[0]+'='+makefile[1]) + '\n'
        with open(self.DesktopFilePath+'/'+self.PackageEntry.get_text()+'.desktop', 'w') as control:
            control.write('[Desktop Entry]\n'+DesktopMakeString)
        os.system('dpkg-deb --build '+ self.ProjePath+'/'+self.ProjeName)
        os.system('rm -R '+self.DesktopFile)
        exit()
    def __init__(self, BetaApp):
        self.DebMakeWindow = Gtk.Window()
        self.DebMakeWindow.set_default_size(300, 300)
        self.DebMakeWindow.set_border_width(11)
        self.DebMakeWindow.set_position(Gtk.WindowPosition.CENTER)
        self.DebMakeWindow.set_resizable(False)
        self.Headerbar = Gtk.HeaderBar()
        self.Headerbar.set_show_close_button(True)
        self.Headerbar.props.title = 'Meerkat'
        self.DebMakeWindow.set_titlebar(self.Headerbar)
        self.BlueToothButton = Gtk.ToggleButton('M')
        self.BlueToothButton.set_active(1)
        self.BlueToothButton.connect('clicked', self.yardim)
        self.Headerbar.pack_start(self.BlueToothButton)
        self.Box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.DebMakeWindow.add(self.Box)
        self.ListBox = Gtk.ListBox()
        self.ListBox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.Box.pack_start(self.ListBox, True, True, 0)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.BoxRow.add(self.Hbox)
        self.DesktopProjeLabel = Gtk.Label("Proje", xalign=0)
        self.DesktopProjeButton = Gtk.Button('Aç')
        self.DesktopProjeButton.connect('clicked', self.on_folder_clicked)
        self.Hbox.pack_start(self.DesktopProjeLabel, True, True, 0)
        self.Hbox.pack_start(self.DesktopProjeButton, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.PackageLabel = Gtk.Label("Proje", xalign=0)
        self.PackageEntry = Gtk.Entry()
        self.PackageEntry.set_width_chars(24)
        self.PackageEntry.set_sensitive(False)
        self.PackageEntry.set_text('') 
        self.Hbox.pack_start(self.PackageLabel, True, True, 0)
        self.Hbox.pack_start(self.PackageEntry, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.ExceLabel = Gtk.Label("Exce", xalign=0)
        self.ExceComboBoxText = Gtk.ComboBoxText()
        self.ExceComboBoxText.insert(0, "0", "Python"+' '*35)
        self.ExceComboBoxText.insert(1, "1", "Python3") 
        self.ExceComboBoxText.set_active(0)    
        self.ExceComboBoxText.set_sensitive(True)
        self.Hbox.pack_start(self.ExceLabel, True, True, 0)
        self.Hbox.pack_start(self.ExceComboBoxText, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        self.BoxRow.add(self.Hbox)
        self.MainLabel = Gtk.Label("Ana Dosya", xalign=0)
        self.MainComboBoxText = Gtk.Entry()
        self.MainButton = Gtk.Button()
        self.MainButton.connect("clicked", self.SelectAppFileFileChooser, self.MainComboBoxText)
        #self.MainComboBoxText.set_wrap_width(25)
        #self.MainComboBoxText.insert(0, "0", "Python")  
        self.MainComboBoxText.set_sensitive(True)
        self.Hbox.pack_start(self.MainLabel, True, True, 0)
        self.Hbox.pack_start(self.MainComboBoxText, False, True, 0)
        self.Hbox.pack_start(self.MainButton, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        self.BoxRow.add(self.Hbox)
        self.DesktopIconLabel = Gtk.Label("Simge", xalign=0)
        self.DesktopIconComboBoxText = Gtk.Entry()
        self.DesktopIconButton = Gtk.Button()
        self.DesktopIconButton.connect("clicked", self.SelectAppFileFileChooser, self.DesktopIconComboBoxText)
        #self.DesktopIconComboBoxText.insert(0, "0", "Python")
        #self.DesktopIconComboBoxText.insert(1, "1", "Python3"+' '*26) 
        self.DesktopIconComboBoxText.set_sensitive(True)
        self.Hbox.pack_start(self.DesktopIconLabel, True, True, 0)
        self.Hbox.pack_start(self.DesktopIconComboBoxText, False, True, 0)
        self.Hbox.pack_start(self.DesktopIconButton, False, True, 0)
        self.ListBox.add(self.BoxRow)

        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.VersionLabel = Gtk.Label("Versiyon", xalign=0)
        self.VersionEntry = Gtk.Entry()
        self.VersionEntry.set_width_chars(24)
        self.VersionEntry.set_text('0.1')
        self.Hbox.pack_start(self.VersionLabel, True, True, 0)
        self.Hbox.pack_start(self.VersionEntry, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.CategoriesLabel = Gtk.Label("Kategori", xalign=0)
        self.CategoriesComboBoxText = Gtk.ComboBoxText()
        self.CategoriesComboBoxText.insert(0, "0", "GNOME")
        self.CategoriesComboBoxText.insert(1, "1", "GTK ")
        self.CategoriesComboBoxText.insert(2, "2", "Graphics ")
        self.CategoriesComboBoxText.insert(3, "3", "Office ")
        self.CategoriesComboBoxText.insert(4, "4", "Settings ")
        self.CategoriesComboBoxText.insert(5, "5", "System ")
        self.CategoriesComboBoxText.insert(6, "6", "Utility ")
        self.CategoriesComboBoxText.insert(7, "7", "Development"+' '*23)
        self.CategoriesComboBoxText.insert(8, "8", "Education ")
        self.CategoriesComboBoxText.insert(9, "9", "Game ")
        self.CategoriesComboBoxText.insert(10, "10", "Science ")
        self.CategoriesComboBoxText.set_active(7)    
        self.CategoriesComboBoxText.set_sensitive(True)
        self.Hbox.pack_start(self.CategoriesLabel, True, True, 0)
        self.Hbox.pack_start(self.CategoriesComboBoxText, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.SectionLabel = Gtk.Label("Section", xalign=0)
        self.SectionEntry = Gtk.Entry()
        self.SectionEntry.set_width_chars(24)
        self.SectionEntry.set_text('base')
        self.Hbox.pack_start(self.SectionLabel, True, True, 0)
        self.Hbox.pack_start(self.SectionEntry, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.PriorityLabel = Gtk.Label("Priority", xalign=0)
        self.PriorityEntry = Gtk.Entry()
        self.PriorityEntry.set_width_chars(24)
        self.PriorityEntry.set_text('optional')
        self.Hbox.pack_start(self.PriorityLabel, True, True, 0)
        self.Hbox.pack_start(self.PriorityEntry, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.ContactLabel = Gtk.Label("İletişim", xalign=0)
        self.ContactEntry = Gtk.Entry()
        self.ContactEntry.set_width_chars(24)
        self.ContactEntry.set_text('@glabald')
        self.Hbox.pack_start(self.ContactLabel, True, True, 0)
        self.Hbox.pack_start(self.ContactEntry, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.DescriptionLabel = Gtk.Label("Açıklama", xalign=0)
        self.DescriptionEntry = Gtk.Entry()
        self.DescriptionEntry.set_width_chars(24)
        self.DescriptionEntry.set_text('Masaüstü Uygulaması')
        self.Hbox.pack_start(self.DescriptionLabel, True, True, 0)
        self.Hbox.pack_start(self.DescriptionEntry, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.CpuLabel = Gtk.Label("İslemci Mimarisi", xalign=0)
        self.CpuEntry = Gtk.ComboBoxText()
        self.CpuEntry.insert(0, "0", "i386")
        self.CpuEntry.insert(1, "1", "i684")
        self.CpuEntry.set_sensitive(True)
        self.CpuEntry.set_active(0)   
        #self.CpuEntry.set_text('i386') #'platform.machine()' 'amd64'
        self.Hbox.pack_start(self.CpuLabel, True, True, 0)
        self.Hbox.pack_start(self.CpuEntry, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.StartUpLabel = Gtk.Label("Başlangıçta Çalıştır", xalign=0)
        self.StartUpCheckButton = Gtk.CheckButton()
        #self.Hbox.pack_start(self.StartUpLabel, True, True, 0)
        #self.Hbox.pack_start(self.StartUpCheckButton, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.OpenSourceLabel = Gtk.Label("Açık Kaynak", xalign=0)
        self.OpenSourceButton = Gtk.CheckButton()
        self.OpenSourceButton.set_active(True)
        self.OpenSourceButton.set_sensitive(False)
        #self.Hbox.pack_start(self.OpenSourceLabel, True, True, 0)
        #self.Hbox.pack_start(self.OpenSourceButton, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.BoxRow.add(self.Hbox)
        self.DesktopLabel = Gtk.Label("Desktop Kısayol", xalign=0)
        self.DesktopCheckButton = Gtk.CheckButton()
        self.DesktopCheckButton.set_active(True)
        self.DesktopCheckButton.set_sensitive(False)
        self.Hbox.pack_start(self.DesktopLabel, True, True, 0)
        self.Hbox.pack_start(self.DesktopCheckButton, False, True, 0)
        self.ListBox.add(self.BoxRow)
        self.ListBox2 = Gtk.ListBox()
        self.ListBox2.set_selection_mode(Gtk.SelectionMode.NONE)
        self.Box.pack_start(self.ListBox2, True, True, 0)
        self.BoxRow = Gtk.ListBoxRow()
        self.Hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.BoxRow.add(self.Hbox)
        self.DesktopLabel = Gtk.Label("Deb Paket Dosyası", xalign=0)
        self.DesktopMakeButton = Gtk.Button('Oluştur')
        self.DesktopMakeButton.set_sensitive(False)
        self.DesktopMakeButton.connect('clicked', self.make)
        self.Hbox.pack_start(self.DesktopLabel, True, True, 0)
        self.Hbox.pack_start(self.DesktopMakeButton, False, True, 0)
        self.ListBox2.add(self.BoxRow)
        self.DebMakeWindow.show_all()
    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Buraya Kaydet", None,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        dialog.set_current_folder('/home')
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.ProjePath = dialog.get_filename()
            self.ProjeName = os.path.split(dialog.get_filename())[1]
            self.DesktopFile = self.ProjePath+'/'+self.ProjeName+'.desktop'
            os.system('touch '+self.DesktopFile)
            os.system('chmod +x '+self.DesktopFile)
            self.DesktopProjeButton.set_label('OK')
            self.DesktopProjeButton.set_sensitive(False)
            self.Run(self.ProjePath)
        elif response == Gtk.ResponseType.CANCEL:
            #print("")
            pass
        dialog.destroy()
    def SelectAppFileFileChooser(self, widget, data):
        if data is self.MainComboBoxText:
            title = 'Ana Python Dosyasını Seç'
        elif data is self.DesktopIconComboBoxText:
            title = 'Kısayol Simgesini Seç'
        dialog = Gtk.FileChooserDialog(title, None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_current_folder(self.ProjePath)
        if (title == 'Ana Python Dosyasını Seç'):
            self.SadecePy(dialog)
        if (title == 'Kısayol Simgesini Seç'):
            self.SadecePng(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            #print("File selected: " + dialog.get_filename(), data)
            SelectFile = os.path.split(dialog.get_filename())[1]
            data.set_text(SelectFile)
            if (len(self.MainComboBoxText.get_text()) > 0 and len(self.DesktopIconComboBoxText.get_text()) > 0):
                self.DesktopMakeButton.set_sensitive(True)
        elif response == Gtk.ResponseType.CANCEL:
            #print("")
            pass
        dialog.destroy()
    def SadecePng(self, dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*.png")
        filter_any.add_pattern("*.ico")
        dialog.add_filter(filter_any)
    def SadecePy(self, dialog):
        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        filter_py.add_pattern("*.pyc")
        dialog.add_filter(filter_py)     
    def Run(self, path):
        self.SelectDebFiles = []
        self.ProjeName = os.path.split(path)[1]
        self.ProjePath = path
        self.PackageEntry.set_text(self.ProjeName)
        if os.path.exists(self.ProjePath+'/'+self.ProjeName) is True:
            os.system('rm -R ' + self.ProjePath+'/'+self.ProjeName)
        for j in os.walk(path):
            if len(j[2]) is not 0:
                for sub in j[2]:
                    self.SelectDebFiles.append(j[0]+'/'+sub)
        for source in self.SelectDebFiles:
            if (source[-4:] == '.deb'): continue
            if (source[-4:] == '.png' or source[-4:] == '.ico'): 
                #self.DesktopIconComboBoxText.append_text(os.path.split(source)[1])
                PngFile = os.path.split(source)[1]
                PngPath = '/usr/local/bin/'+os.path.split(source)[0][os.path.split(source)[0].find(self.ProjeName):]+'/'+PngFile
                #self.DesktopIconComboBoxText.set_active(0) 
                self.DesktopIconDict[PngFile] = {'png':PngPath}
            if (source[-3:] == '.py' or source[-4:] == '.pyc'): 
                #self.MainComboBoxText.append_text(os.path.split(source)[1])
                PyFile = os.path.split(source)[1]
                PyPath = '/usr/local/bin/'+os.path.split(source)[0][os.path.split(source)[0].find(self.ProjeName):]+'/'+PyFile
                self.PyDict[PyFile] = {'py':PyPath}
            if (os.path.split(source)[1].find('.desktop') is -1):
                target = self.ProjePath+'/'+self.ProjeName+'/usr/local/bin/'+os.path.split(source)[0][os.path.split(source)[0].find(self.ProjeName):]
            if (os.path.split(source)[1].find('.desktop') > -1):
                target = self.ProjePath+'/'+self.ProjeName+'/usr/share/applications/'
                self.DesktopFilePath = target
            if os.path.exists(target) is False:
                os.makedirs(target)
            os.system('cp -avr ' + source + ' ' + target)
    def tamamla(self, string):
        return string + ' '*(44-len(string)+len(string))
    def yardim(self, widget):
        #self.BlueToothButton.set_active(1)
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "")
        dialog.format_secondary_text(
            "<Contact>\nemail: globalapplication@yandex.com\nforum.pardus.org.tr user(globald) \n")
        dialog.run()
        dialog.destroy()
    def Cikis(self, widget):
        #self.BlueToothButton.set_active(1)
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "")
        dialog.format_secondary_text(
            "Deb Paket Dosyası Oluşturuldu.")
        dialog.run()
        dialog.destroy()
def main(BetaApp=None):
    Gdeb(BetaApp)
    Gtk.main()
if __name__ == '__main__':
    main()
