import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from PIL import Image, ImageDraw

import matplotlib.pyplot as plt
from keras.models import load_model, Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten


width, height = 200, 200 #Initilize width anf height of canvas

mnist_width, mnist_height = 28, 28 

#load pre-trained model
model = load_model('cnn.h5')

#Define new image
#This will be the backend canvas not shown to the user
#Used for prediction of the user digit
im = Image.new(mode='L', size=(width,height), color=0)

#Funtion intilizing draw object for backend
draw = ImageDraw.Draw(im)

#PIL library image
#Front end image shown to the user

#Set up canvas to draw on
root = Tk()
drawing_area = Canvas(root, width=width, height=height, bg='black')

#set up variables to track state of mouse
#https://svn.python.org/projects/python/trunk/Demo/tkinter/guido/paint.py #Base code for frontend canvas

b1 = 'up' #state of mouse left button
xold, yold = None, None #Coordinates of mouse when left button down

def main():

	'''
	main function initilizing program
	'''
	
	drawing_area.pack() #Creates visual of canvas
	
	#Calling motion function when mouse moves
	drawing_area.bind('<Motion>', motion)
	#Calls b1down function when mouse left button is down
	drawing_area.bind('<ButtonPress-1>', b1down)
	#Calls b1up function when left button is released
	drawing_area.bind('<ButtonRelease-1>', b1up)
	
	#creating button to clear screen and backend image
	clear_b = Button(root, text='clear', command = clear_im)
	clear_b.pack()
	#creating button to prediction
	predict_b = Button(root, text='predit', command= predict)
	predict_b.pack()
	root.mainloop()
	


def b1down(event):
	#Function makes sure that you draw only when mouse left click
	#occurs; defined in main()
	
	global b1
	
	b1 = 'down'
	

def b1up(event):
	#resets line when mouse is released
	global b1, xold, yold
	
	b1 = 'up'
	xold = None
	yold = None

	
	
def clear_im():

	global im, draw
	
	im = Image.new(mode='L', size=(width,height), color=0)
	draw = ImageDraw.Draw(im)
	
	drawing_area.delete('all')
	
	

	
def predict():
	

	im2 = im.resize((mnist_width, mnist_height), resample=Image.LANCZOS)
	#im2.save('mnist_conv.jpg', 'JPEG')
	im2 = np.asarray(im2).reshape(-1,28,28,1)
	
	#im2 = im2/255
	
	print(np.argmax(model.predict(im2)))

	
def motion(event):

	if b1 == 'down':
		global xold, yold
		if (xold and yold) is not None:
			#Call to draw line between current point and old point
			event.widget.create_line(xold,yold, event.x, event.y, smooth=True, fill='white', width = 5)
			draw.line([(xold, yold), (event.x, event.y)], fill=255, width=15)
			
		
		xold = event.x
		yold = event.y
		
		
		
if __name__ == '__main__':

	main()

