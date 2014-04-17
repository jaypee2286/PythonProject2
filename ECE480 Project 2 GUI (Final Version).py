######################################################################
## Jorge Camacho                                                    ##
## John Paul Canlas                                                 ##
## Allen Khachikian                                                 ##
## Leonard Mendoza                                                  ##
## Justin Shen                                                      ##
##                                                                  ##
## ECE480 Spring 2013                                               ##
## Prof. Chandra                                                    ##
##                                                                  ##
## Project #2 - KMean Algorithm                                     ##
##                                                                  ##
## This program simulates the KMean Algorithm given a set           ##
##  of data points. It can run as many iterations as requested      ##
##  by the user.                                                    ##
######################################################################

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import math
import ntpath


### calculate() FUNCTION START
def calculate():
    
    print("Data points matrix again: " + str(data))
    
    ## clear CENTROIDS text box
    text_Box1.config(state=NORMAL)
    text_Box1.delete(1.0, END)
    text_Box1.config(state=DISABLED)
    
    try:
        iterations = int(entrybox.get())
        print("Iterations chosen: " + str(iterations))
    except:
        messagebox.showinfo("Error", "Invalid parameters. Please input a whole number for interations.")
    


    #initialize two centroids: c1 = (1,1) and c2 = (2,1)
    c1x = 1
    c1y = 1
    c2x = 2
    c2y = 1

    #initialize distance and group lists
    d = [[0,0,0,0],[0,0,0,0]]
    g = [[0,0,0,0],[0,0,0,0]]

    cnt = 0
    #start iteration loop
    while cnt < iterations:
        x = 0
        y = 0
        z = 0
        #calculate the distance list
        while x < (len(d[0])-1):
            firstTerm = math.pow((int(data[0][x])-c1x),2)
            secTerm = math.pow((int(data[1][x])-c1y),2)
            d[0][x] = math.sqrt(firstTerm + secTerm)
            x+=1

        while y < len(d[1]):
            firstTerm = math.pow((int(data[0][y])-c2x),2)
            secTerm = math.pow((int(data[1][y])-c2y),2)
            d[1][y] = math.sqrt(firstTerm + secTerm)
            y+=1
            
        #calculate group list
        while z < len(g[0]):
            if d[0][z] < d[1][z]:
                g[0][z] = 1
            elif d[0][z] > d[1][z]:
                g[1][z] = 1
            z+=1

        a = 0
        b = 0
        c = 0
        e = 0
        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        den1 = 0
        den2 = 0
        den3 = 0
        den4 = 0
        #recalculate centroids
        while a < len(g[0]):
            if g[0][a] == 1:
                num1+= int(data[0][a])
                den1+=1
            a+=1

        while b < len(g[0]):
            if g[0][b] == 1:
                num2+= int(data[1][b])
                den2+=1
            b+=1

        while c < len(g[1]):
            if g[1][c] == 1:
                num3+= int(data[0][c])
                den3+=1
            c+=1

        while e < len(g[1]):
            if g[1][e] == 1:
                num4+= int(data[1][e])
                den4+=1
            e+=1

        c1x = num1/den1
        c1y = num2/den2
        c2x = num3/den3
        c2y = num4/den4

        cnt+=1 #increment counter for entire loop

    #end iteration loop

    #print results
    print("Here is the distance matrix: " + str(d))
    print("Here is the group matrix: " + str(g))
    print("Here is the first centroid: (" + str(c1x) + "," + str(c1y) + ")")
    print("Here is the second centroid: (" + str(c2x) + "," + str(c2y) + ")")

    ## update CENTROIDS box with the results
    text_Box1.config(state=NORMAL)
    text_Box1.delete(1.0, END)
    text_Box1.insert(INSERT, "(" + str("%.2f" % c1x) + "," + str("%.2f" % c1y) + ")\n")
    text_Box1.insert(INSERT, "(" + str("%.2f" % c2x) + "," + str("%.2f" % c2y) + ")")
    text_Box1.config(state=DISABLED)


# END calculate()

### browse() FUNCTION START
def browse():
    ## open up an explorer window to browse for file
    filename = filedialog.askopenfilename()
    ## display filename (without full path)
    label_FileName.config(text=ntpath.basename(filename))
    global data
    del data[:]
    del px[:]
    del py[:]
    pdimension = 0
    
    ## try to read the file and check if the format is valid
    ## display error notification if it is invalid
    with open(filename,'r') as f:
        try:
            for line in f:
                pdimension = abs(line.index('(') - line.index(')'))//2
                newstr = line.replace('(','').replace(')','') #remove paranthese
                for element in newstr.split(','): #split on ','
                    x=-1
                    for subset in element.split(' '): #split on whitespace
                        x+=1
                        if(x%2==0): #even char, place in x-list
                            px.append(subset)
                        else: #odd char, place in y-list
                            py.append(subset)
            button_Calculate.config(state=NORMAL)
       
        except:
            messagebox.showinfo("Error", "Invalid file.")
            button_Calculate.config(state=DISABLED)            
    f.closed ## close file

    data = [[]]*pdimension              
    data[0]=list(px)
    data[1]=list(py)
    
    ## update POINTS (data) and CENTROIDS boxes
    ## first enable the box, then update, then disable the box
    ##   to prevent user modification
    text_Box0.config(state=NORMAL)
    text_Box0.delete(1.0, END)
    text_Box1.delete(1.0, END)
    print("Data points matrix: " + str(data))
    for i in range (len(data[0])):
        text_Box0.insert(INSERT, "(" + str(data[0][i]) + "," + str(data[1][i]) + ")\n")
    text_Box0.config(state=DISABLED)
    text_Box1.config(state=DISABLED)
    
# END browse()


### help_instructions() function start
### this function calls a pop up message box that gives a brief
###  explanation of how to use the program
def help_instructions():
    messagebox.showinfo("Instructions", "This program implements the KMean Algorithm "
                       "using four data points read from a file."
                        "The file must be formatted in the followign way:\n"
                        "(# #),(# #),(# #),(# #)\n"
                        "After selecting a file, input the number of iterations that the\n"
                        "algorithm will run. The data will display in the text boxes.")
# END help_instructions()


### help_about() function start
### this function calls a pop up message box that gives a brief
###  explanation about the program and it's creators
def help_about():
    messagebox.showinfo("About", "This program was created for Dr. Chandra in ECE480 at "
                        "Cal Poly Pomona Polytechnic University, Spring 2013 quarter.\n\n"
                        "Jorge Camacho\nJohn Paul Canlas\nAllen Khachikian\nLeonard Mendoza\nJustin Shen")
# END help_about



#########################################
#########################################
#### MAIN FUNCTION & GUI            #####
#########################################
#########################################

## create a GUI using Tk
root = Tk()

## add a frame to the GUI
## all widgets and objects will be put inside this frame
frame = ttk.Frame(root, height=400, width=400, padding="10 10 10 20")
frame.grid(row=0, column=0, sticky=(N, W, E, S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
root.title("ECE480 Project #2") # title of program

## NOTE: This GUI uses a grid formation to place all the widgets/objects.
         # The grid consists of rows and columns.
         # Each object is anchored to a spot or spots on the grid accordingly.

## define lists
px = []
py = []
data = []

## FILEMENU
## this is a basic filemenu
## users can open a file through this menu as well as
##  get instructions on how to use the program and also
##  a list of the creators
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open...", command=browse)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Instructions", command=help_instructions)
helpmenu.add_separator()
helpmenu.add_command(label="About", command=help_about)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

## algorithm iteration entry box
## this is a user-entry box used to obtain the number of iterations desired
entrybox = Entry(frame)
entrybox.grid(row=1, column=1, columnspan=2, sticky=W)
label_combobox = Label(frame, anchor=W, justify=LEFT, text="Iterations:")
label_combobox.grid(row=1, column=0, sticky=W)

## filename display box
## this displays a concatinated filename without the full path
label_FileName = Label(frame, width=20, anchor=W, bg="white", justify=LEFT, relief="ridge")
label_FileName.grid(row=0, column=1, columnspan=3, sticky=W)
label_Filename2 = Label(frame, anchor=W, justify=LEFT, text="Filename:")
label_Filename2.grid(row=0, column=0, sticky=W)

## BROWSE (for file) button
## call function browse() when clicked
button_Browse = Button(frame, text="BROWSE", command=browse) 
button_Browse.grid(row=0, column=4, sticky=W)

## CALCULATE button
## call function calculate() when clicked
button_Calculate = Button(frame, text="CALCULATE", command=calculate, state=DISABLED) 
button_Calculate.grid(row=1, column=4, sticky=W)

## POINTS (data) label & text display box
## this displays the data read from the file containing
##  the list of requests
label_Box0 = Label(frame, text="Points")
label_Box0.grid(row=2, column=0, sticky=N)
text_Box0 = Text(frame, height=4, width=7, state=DISABLED)
text_Box0.grid(row=3,column=0)

## CENTROIDS label & text display box
## this displays the order of requests/path taken of the head after calculation
label_Box1 = Label(frame, text="Centroids")
label_Box1.grid(row=2, column=1, sticky=N)
text_Box1 = Text(frame, height=4, width=12, state=DISABLED)
text_Box1.grid(row=3,column=1)


root.mainloop()
