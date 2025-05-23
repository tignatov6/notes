#начни тут создавать приложение с умными заметками
# Imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import  multiprocessing as mp
import random
import time
#import psutil
import json
print('Libriries imported')

#defs

def showNote():
    key = NotesList.selectedItems()[0].text()
    NoteTextEdit.setText(notes[key]['text'])
    TagsList.clear()
    TagsList.addItems(notes[key]['tags'])

def addNote():
    noteName, ok = QInputDialog.getText(
        WinMain, 'Добавить заметку', 'Введите название заметки...'
    )
    if ok:
        notes[noteName] = {
            'text': "",
            'tags': []
        }
    NotesList.clear()
    NotesList.addItems(notes)

    with open('notes_data.json', 'w') as file:
        json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    
def delNote():
    try:
        key = NotesList.selectedItems()[0].text()
        print(key)
        ok = QInputDialog.getText(
            WinMain, 'Удаление заметки', 'Нажмите ОК для удаления заметки'
        )
        if ok:
            del notes[key]
            with open('notes_data.json', 'w') as file:
                json.dump(notes,file,sort_keys=True,ensure_ascii=False)
            NoteTextEdit.setText('')
            TagsList.clear()
            NotesList.clear()
            NotesList.addItems(notes)
    except:
        print('No notes selected!')

def saveNote():
    if NotesList.selectedItems() and NoteTextEdit.toPlainText() != '' and NotesList.selectedItems()[0].text() != '':
        key = NotesList.selectedItems()[0].text()
        notes[key]['text'] = NoteTextEdit.toPlainText()
        with open('notes_data.json', 'w') as file:
                json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    
def addTag():
    key = NotesList.selectedItems()[0].text()
    tag = EnterTagLineEdit.text()
    if tag and not tag in notes[key]['tags'] and NotesList.selectedItems():
        notes[key]['tags'].append(tag)
        TagsList.addItem(tag)
        EnterTagLineEdit.clear()
        with open('notes_data.json', 'w') as file:
                json.dump(notes,file,sort_keys=True,ensure_ascii=False)

def delTag():
    if TagsList.selectedItems():
        key = NotesList.selectedItems()[0].text()
        tag = TagsList.selectedItems()[0].text()
        notes[key]['tags'].remove(tag)
        TagsList.clear()
        TagsList.addItems(notes[key]['tags'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)


def SearchTag():
    tag = EnterTagLineEdit.text()
    if tag != '' and SearchByTagButton.text() == 'Искать заметки по тегу':
        notes_filtred = dict()
        for key in notes:
            if tag in notes[key]['tags']:
                notes_filtred[key] = notes[key]
        SearchByTagButton.setText('Отменить поиск')
        NotesList.clear()
        TagsList.clear()
        NoteTextEdit.clear()
        NotesList.addItems(notes_filtred)
    else:
        NotesList.clear()
        NotesList.addItems(notes)
        EnterTagLineEdit.clear()
        SearchByTagButton.setText('Искать заметки по тегу')

def Move():
    if(NoteTextEdit.toPlainText().upper() == 'W'):
        WinMain.move(WinMain.x(),WinMain.y()-10)
    if(NoteTextEdit.toPlainText().upper() == 'S'):
        WinMain.move(WinMain.x(),WinMain.y()+10)
    if(NoteTextEdit.toPlainText().upper() == 'A'):
        WinMain.move(WinMain.x()-10,WinMain.y())
    if(NoteTextEdit.toPlainText().upper() == 'D'):
        WinMain.move(WinMain.x()+10,WinMain.y())
    if(NoteTextEdit.toPlainText()):
        NoteTextEdit.setText('')


# Init App
App = QApplication([])
WinMain = QWidget()
WinMain.resize(900,600)
oImage = QImage("background.png")
sImage = oImage.scaled(QSize(900,600))
palette = QPalette()
palette.setBrush(QPalette.Window, QBrush(sImage))
# WinMain.setPalette(palette)
WinMain.show()



# App items

# Lines
HLine0 = QHBoxLayout() # Main Line
VLine1 = QVBoxLayout() # Level 1
VLine2 = QVBoxLayout() # Level 1
HLine1 = QHBoxLayout() # Level 2
HLine2 = QHBoxLayout() # Level 2


# Lables
NotesListLable = QLabel('Список заметок')
TagsListLable = QLabel('Список тегов')


# Buttons
CreateNoteButton = QPushButton('Создать заметку')
CreateNoteButton.setIcon(QIcon('CreateNoteButton.png'))
DeleteNoteButton = QPushButton('Удалить заметку')
DeleteNoteButton.setIcon(QIcon('DeleteNoteButton.png'))
SaveNoteButton = QPushButton('Сохранить заметку')
SaveNoteButton.setIcon(QIcon('SaveNoteButton.png'))
AddTagButton = QPushButton('Добавить к заметке')
AddTagButton.setIcon(QIcon('AddTagButton.png'))
UnpinTagButton = QPushButton('Открепить от заметки')
UnpinTagButton.setIcon(QIcon('UnpinTagButton.png'))
SearchByTagButton = QPushButton('Искать заметки по тегу')
SearchByTagButton.setIcon(QIcon('SearchByTagButton.png'))

#CreateNoteButton.setStyleSheet("QPushButton {border: 0px;}") 
#CreateNoteButton.setStyleSheet("background-image : url(background_lighter.png);") 


# Lists
NotesList = QListWidget()
TagsList = QListWidget()


# TextEdit
NoteTextEdit = QTextEdit()
NoteTextEdit.setPlaceholderText('Введите заметку:')


# LineEdit
EnterTagLineEdit = QLineEdit()
EnterTagLineEdit.setPlaceholderText('Введите тег:')


# CreateLayouts
WinMain.setLayout(HLine0)
HLine0.addLayout(VLine1)
HLine0.addLayout(VLine2)
VLine2.addWidget(NotesListLable)
VLine2.addWidget(NotesList)
VLine2.addLayout(HLine1)
HLine1.addWidget(CreateNoteButton)
HLine1.addWidget(DeleteNoteButton)
VLine2.addWidget(SaveNoteButton)
VLine2.addWidget(TagsListLable)
VLine2.addWidget(TagsList)
VLine2.addWidget(EnterTagLineEdit)
VLine2.addLayout(HLine2)
HLine2.addWidget(AddTagButton)
HLine2.addWidget(UnpinTagButton)
VLine2.addWidget(SearchByTagButton)
VLine1.addWidget(NoteTextEdit)

# App Logic



with open('notes_data.json', 'r') as file:
    notes = json.load(file)
    #print(notes)

NotesList.addItems(notes)
NotesList.itemClicked.connect(showNote)
CreateNoteButton.clicked.connect(addNote)
DeleteNoteButton.clicked.connect(delNote)
SaveNoteButton.clicked.connect(saveNote)
#NoteTextEdit.textChanged.connect(Move)
NoteTextEdit.textChanged.connect(saveNote)
AddTagButton.clicked.connect(addTag)
AddTagButton.clicked.connect(addTag)
UnpinTagButton.clicked.connect(delTag)
SearchByTagButton.clicked.connect(SearchTag)

# start the app
App.exec()