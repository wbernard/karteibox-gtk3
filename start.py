import sys
import gi
import sqlite3

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import os   # ermöglicht es herauszufinden ob ein file existiert
       
class StartSeite(Gtk.Window):

    def __init__(self):
    
        super().__init__(title="Karteikartenbox")
        
        self.set_default_size(400, 400)

        frame1 = Gtk.Frame(label="Kartei wählen") # in diesen Rahmen kommt alles hinein
        
        self.add(frame1)
        self.box1 = Gtk.Fixed()
        frame1.add(self.box1)

        bild = Gtk.Image.new_from_file("karteibox.png")
        bild.set_pixel_size(110)
        self.box1.put(bild, 150, 20)

        label1 = Gtk.Label()
        label1.set_use_markup(True)
        label1.set_label('<b><span foreground="blue" size="xx-large">Lernu!</span></b>')
        self.box1.put(label1, 160, 150)
        self.eing1 = Gtk.Entry()    # Eingabefenster
        self.eing1.set_width_chars(20)
        self.eing1.set_placeholder_text("Name der Kartei")
        self.box1.put(self.eing1, 50, 220)

        self.but = Gtk.Button(label="suchen")  # die Kartei suchen
        self.but.connect("clicked", self.db_erkunden)  # Funktion button_clicked wird ausgeführt bei klick
        self.box1.put(self.but, 270, 220)

    def db_erkunden(self, widget): # untersucht ob es eine Kartei mit dem Namen gibt
        
        self.name = self.eing1.get_text()
        db_name = self.name + '.db'
        os.getcwd() #return the current working directory
           
        for root, dirs, files in os.walk(os.getcwd()):
            if db_name in files:  # wenn es eine Datenbank für die Kartei gibt wird sie aufgerufen                         
                self.oeffne_kartei(self.name)
                break
            else:
                mtl = "Kartei "+self.name+" nicht gefunden!" \
                          " Neu erstellen?"
                self.mitteilung(mtl, self.name)
                break

        
    def mitteilung(self, mtl, name): # öffnet ein Fenster für die Mitteilung
        self.dialog = Gtk.MessageDialog(
                    transient_for=self,
                    buttons = Gtk.ButtonsType.YES_NO ,
                    message_type=Gtk.MessageType.QUESTION,
                    text = mtl)
        self.dialog.show()
        self.dialog.connect("response", self.ergebnis)
        return None
            
    def ergebnis(self, dialog, response):
        if response == Gtk.ResponseType.YES: # wenn ja, wird die Kartei erstellt
            self.erstel_kartei(self.name)
        elif response == Gtk.ResponseType.NO:
            print("WARN dialog closed by clicking NO button")

        self.dialog.destroy()

    def erstel_kartei(self, name):  # neue kartei wird erstellt
        db_name = self.name + '.db'
            #print(db_name)
        conn = sqlite3.connect(db_name)        
        c = conn.cursor() # eine cursor instanz erstellen
        #c.execute('DROP TABLE IF EXISTS karten')  # Tabelle wird gelöscht
            # Tabelle mit Karteikarten
        c.execute("""CREATE TABLE if not exists karten (
                                  vorne TEXT, hinten TEXT)""")
           
        conn.commit()    # Änderungen mitteilen   
        conn.close()   # Verbindung schließen

    def oeffne_kartei(self, *args):
        #print('kartei ' + self.name)
        win1.hide()   # schließt das Fenster der Karteikartenbox
        #name = self.name  # der eingegebene Namen wird übernommen
        
        win2 = KarteiSeite(self.name)
        win2.show_all()
        
class KarteiSeite(Gtk.Window):

    def __init__(self, name):
    
        super().__init__(title="Kartei")

        self.name = name

        self.set_default_size(400, 400)

        frame1 = Gtk.Frame(label="Karteikarte wählen") # in diesen Rahmen kommt alles hinein
        
        self.add(frame1)
        self.box1 = Gtk.Fixed()
        frame1.add(self.box1)

        bild = Gtk.Image.new_from_file("kartei.png")
        bild.set_pixel_size(110)
        self.box1.put(bild, 150, 20)
        
        label1 = Gtk.Label()
        label1.set_use_markup(True)
        label1.set_label(name)
        self.box1.put(label1, 160, 150)
        self.eing1 = Gtk.Entry()
        self.eing1.set_width_chars(20)
        self.eing1.set_placeholder_text("Name der Karteikarte")
        self.box1.put(self.eing1, 50, 220)

        self.but = Gtk.Button(label="suchen")  # die Kartei suchen
        self.but.connect("clicked", self.db_erkunden)  # Funktion button_clicked wird ausgeführt bei klick
        self.box1.put(self.but, 270, 220)

    def db_erkunden(self, *args): # untersucht ob es eine Karteikarte mit dem Namen gibt
        self.kart_name = self.eing1.get_text()
        self.db_name = self.name + '.db'
        print (self.db_name)

        conn = sqlite3.connect(self.db_name)  #Verbindung mit Kartei wird hergestellt
        c = conn.cursor()

        c.execute('SELECT rowid, * FROM karten') # rowid heißt, dass eine eigene originale ID erstellt wird * bedeutet alles  
        records = c.fetchall() # alles aus karten wird in records eingelesen, die ID ist dann in record[0]
        print('Daten der Kartei')
        print(records)
        karte_da = 'N'   # Karte gibt es nicht
        for record in records: # alle Zeilen werden durchsucht
            if self.kart_name in record: # sucht nach der Karteikarte in records
                self.zeige_karte(self.name, self.kart_name)
                print(self.kart_name)
                karte_da = 'J'  # Karte gibt es
                break
            else:
                pass
            
        conn.commit()    # Änderungen mitteilen   
        conn.close()   # Verbindung schließen

        if not karte_da =='J':
            mtl = "Karte "+self.kart_name+" nicht gefunden!" \
                      " Neu erstellen?"
            self.mitteilung(mtl)

 
    def mitteilung(self, mtl): # öffnet ein Fenster für die Mitteilung
        self.dialog = Gtk.MessageDialog(                    
                    buttons = Gtk.ButtonsType.YES_NO ,
                    message_type=Gtk.MessageType.QUESTION,
                    text = mtl)
        self.dialog.show()
        self.dialog.connect("response", self.ergebnis)
        return None

    def ergebnis(self, dialog, response):
        if response == Gtk.ResponseType.YES:
            print (self.kart_name)
            kart_name = self.kart_name
            self.leere_karte(kart_name)
        elif response == Gtk.ResponseType.NO:
            print("WARN dialog closed by clicking NO button")

        self.dialog.destroy()

    def zeige_karte(self, name, kart_name):
        #print ('karte', kart_name,' ist da')        
        #win2 = KarteiSeite(self.name)
        win2.hide()   # schließt das Fenster der Kartei
        win3 = KartenSeite(self.name, self.kart_name)  # Eingabeseite der Karte
        win3.hide()
        
        win4 = KarteVorn(name, kart_name) 
        win4.show_all()
            
    def leere_karte(self, *args):
        #print ('ich schreibe '+ self.kart_name)
        #win2 = KarteiSeite(self.name)
        win2.hide()   # schließt das Fenster der Kartei
        kart_name = self.kart_name  # Namen der Karte
        
        win3 = KartenSeite(self.name, self.kart_name)  # Eingabeseite der Karte
        win3.show_all()


class KartenSeite(Gtk.Window):

    def __init__(self, name, kart_name):
    
        super().__init__(title="Karteikarte")

        self.name = name
        self.kart_name = kart_name
        
        self.set_default_size(400, 400)

        frame1 = Gtk.Frame() # in diesen Rahmen kommt alles hinein
        
        self.add(frame1)
        self.box1 = Gtk.Fixed()
        frame1.add(self.box1)

        bild = Gtk.Image.new_from_file("karte.png")
        bild.set_pixel_size(110)
        self.box1.put(bild, 150, 20)

        label1 = Gtk.Label()
        label1.set_use_markup(True)
        label1.set_label(kart_name)
        self.box1.put(label1, 160, 150)
        self.eing1 = Gtk.Entry()
        self.eing1.set_width_chars(20)
        self.eing1.set_placeholder_text("Text der Karteikarte")
        self.box1.put(self.eing1, 50, 220)

        self.but = Gtk.Button(label="speichern")  # die Kartei suchen
        self.but.connect("clicked", self.txt_speichern)  # Funktion button_clicked wird ausgeführt bei klick
        self.box1.put(self.but, 270, 220)
    
    def txt_speichern(self, *args):
        #print ('speichern der Karte ',self.kart_name)
        db_name = self.name + '.db'
        kart_text = self.eing1.get_text()
        
        conn = sqlite3.connect(db_name)        
        c = conn.cursor() # eine cursor instanz erstellen
        c.execute("""INSERT INTO karten VALUES (
                    :vorne, :hinten)""",              
                    {'vorne': self.kart_name,
                    'hinten': kart_text})
        
        conn.commit()    # Änderungen mitteilen   
        conn.close()   # Verbindung schließen

        #win3 = KartenSeite(name, self.kart_name)
        win3.hide() # schließt Eingabeseite der Karte
        KarteiSeite.zeige_karte(self, self.name, self.kart_name)


class KarteVorn(Gtk.Window):

    def __init__(self, name, kart_name):
    
        super().__init__(title="Karte vorn")

        self.name = name
        self.kart_name = kart_name
        
        self.set_default_size(400, 400)

        frame1 = Gtk.Frame() # in diesen Rahmen kommt alles hinein
        
        self.add(frame1)
        self.box1 = Gtk.Fixed()
        frame1.add(self.box1)

        bild = Gtk.Image.new_from_file("karte.png")
        bild.set_pixel_size(110)
        self.box1.put(bild, 150, 20)

        label1 = Gtk.Label()
        label1.set_use_markup(True)
        label1.set_label(kart_name)
        self.box1.put(label1, 150, 150)

        self.but = Gtk.Button(label="zeige Rückseite")  # die Kartei suchen
        self.but.connect("clicked", self.zeige_hinten)  # Funktion button_clicked wird ausgeführt bei klick
        self.box1.put(self.but, 150, 220)

    def zeige_hinten(self, widget):
        #win4 = KarteVorn(self.name, self.kart_name)
        win4.hide()   # schließt das Fenster der Kartei vorne
         
        win5 = KarteHinten(self.name, self.kart_name)
        win5.show_all()

class KarteHinten(Gtk.Window):

    def __init__(self, name, kart_name):
    
        super().__init__(title="Karte hinten")

        self.name = name
        self.kart_name = kart_name
        
        self.set_default_size(400, 400)

        frame1 = Gtk.Frame() # in diesen Rahmen kommt alles hinein
        
        self.add(frame1)
        self.box1 = Gtk.Fixed()
        frame1.add(self.box1)
        label1 = Gtk.Label()
        label1.set_use_markup(True)
        label1.set_label(self.kart_name)
        self.box1.put(label1, 150, 150)

        self.db_name = self.name + '.db'
        #print (self.db_name + ' in win5')
        
        conn = sqlite3.connect(self.db_name)  #Verbindung mit Kartei wird hergestellt
        c = conn.cursor()
        
        c.execute('SELECT rowid, * FROM karten') # rowid heißt, dass eine eigene originale ID erstellt wird * bedeutet alles  
        records = c.fetchall() # alles aus karten wird in records eingelesen, die ID ist dann in record[0]
        for record in records: # alle Zeilen werden durchsucht
            if self.kart_name in record: # sucht nach der Karteikarte in records
                self.text_hinten = record[2]
                print(self.text_hinten)
                break
            else:
                pass            
        
        conn.commit()    # Änderungen mitteilen   
        conn.close()   # Verbindung schließen
        
        label2 = Gtk.Label()
        label2.set_use_markup(True)
        label2.set_label(self.text_hinten)
        self.box1.put(label2, 150, 180)

        self.but = Gtk.Button(label="zur Kartei")  # die Kartei suchen
        self.but.connect("clicked", self.zu_kartei)  # Funktion button_clicked wird ausgeführt bei klick
        self.box1.put(self.but, 150, 220)

    def zu_kartei(self, widget):
        #win4 = KarteVorn(self.name, self.kart_name)
        win5 = KarteHinten(self.name, self.kart_name)
        
        #win4.connect("destroy", Gtk.main_quit)
        #win5.connect("destroy", Gtk.main_quit)
        #win4.hide()        
        #win5.hide()
        win2 = KarteiSeite(self.name)
        win2.show_all()


        
        
win1 = StartSeite()
name = 'Karteiname'
win2 = KarteiSeite(name)
kart_name = 'Kartenname'
win3 = KartenSeite(name, kart_name)
win4 = KarteVorn(name, kart_name)
#win5 = KarteHinten(name, kart_name)

win1.connect("destroy", Gtk.main_quit)
win2.connect("destroy", Gtk.main_quit)
win3.connect("destroy", Gtk.main_quit)
win4.connect("destroy", Gtk.main_quit)
#win5.connect("destroy", Gtk.main_quit)

win1.show_all()
Gtk.main()

