import os
from PIL import Image, ImageOps, ImageFilter
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

workdir = ''
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadimage(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)

    def showImage(self,path):
        pixmapimage = QPixmap(path)
        label_width, label_height = lb_image.width(),lb_image.height()
        scaled_pixmap = pixmapimage.scaled(label_width,label_height,Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    
    def do_bw(self):
        self.image = ImageOps.grayscale(self.image)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.rotate(-90)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = ImageOps.mirror(self.image)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_blured(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)



    
    
    
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files,extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
                print(files)
    return result

def showFilenamesList():
    chooseWorkdir()
    files = filter(os.listdir(workdir), [".png", '.jpg', '.jpeg', 'gif','jfif'])
    for filename in files:
        image_list.addItem(filename)
    

def showChosenImage():
    if image_list.currentRow() >= 0:
        filename = image_list.currentItem().text()
        workimage.loadimage(workdir,filename)
        image_path = os.path.join(workimage.dir,workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()

app = QApplication([]) 
main_win = QWidget()
main_win.resize(700,500)
lb_image = QLabel('Картинка')
main_win.setWindowTitle('Easy Editor')
image_button = QPushButton('Папка')
left_button = QPushButton('Лево')
left_button.clicked.connect(workimage.do_left)
right_button = QPushButton('Право')
right_button.clicked.connect(workimage.do_right)
mirror_button = QPushButton('Зеркало')
mirror_button.clicked.connect(workimage.do_mirror)
sharpness_button = QPushButton('Резкость')
sharpness_button.clicked.connect(workimage.do_blured)
black_white_button = QPushButton('Ч/Б')
black_white_button.clicked.connect(workimage.do_bw)
image_list = QListWidget()
left_layout = QVBoxLayout()
right_layout1 = QVBoxLayout()
main_layout = QHBoxLayout()
buttons_layout = QHBoxLayout()
buttons_layout.addWidget(left_button)
buttons_layout.addWidget(right_button)
buttons_layout.addWidget(mirror_button)
buttons_layout.addWidget(sharpness_button)
buttons_layout.addWidget(black_white_button)
right_layout1.addWidget(lb_image)
right_layout1.addLayout(buttons_layout)

left_layout.addWidget(image_button)
left_layout.addWidget(image_list)

main_layout.addLayout(left_layout)
main_layout.addLayout(right_layout1)

def showChosenImage():
    if image_list.currentRow() >= 0:
        filename = image_list.currentItem().text()
        workimage.loadimage(workdir,filename)
        image_path = os.path.join(workimage.dir,workimage.filename)
        workimage.showImage(image_path)
    
image_button.clicked.connect(showFilenamesList)
image_list.currentRowChanged.connect(showChosenImage)
main_win.setLayout(main_layout)
main_win.show()
app.exec()