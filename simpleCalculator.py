from tkinter import *
import math
import operator
import re

root = Tk()
root.title("Simple Calculator")
root.iconbitmap(r'C:\Users\casey\Documents\Python Scripts\calculator\calculator.ico')
root.geometry('500x440')

#Create entry boxes
e1 = Entry(root, width=20, bg='#000000', fg='#FFFFFF')
e2 = Entry(root, width=20, bg='#000000', fg='#FFFFFF')
e1.grid(row=0, column=1, columnspan=2, sticky='ew')
e2.grid(row=0, column=4, columnspan=2, sticky='ew')

#Create Labels
label1 = Label(root, text='Input:')
label2 = Label(root, text='Ans:')
label3 = Label(root, text='Created by: Casey Moore  \nCaseymoore19@gmail.com') 
label1.grid(row=0, column=0)
label2.grid(row=0, column=3, columnspan=1)
label3.grid(row=3, column=3, sticky="EWN", columnspan=2)

#Class for creating buttons, completely unneccesary but I wanted to practice with classes 
class Buttons():
    def __init__(self, root, text, func, padx, pady, args):
        self.root = root
        self.text = text
        self.padx = padx
        self.pady = pady 
        self.func = func
        self.args = args 
    
    
    
    def aButton(self, r=0, col=0, colspan = 1, sticky='ew'):
        self.r = r
        self.col = col
        self.colspan = colspan
        self.sticky = sticky
        self.button = Button(self.root, text=self.text, padx=self.padx, pady=self.pady, command=lambda: self.func(self.args))
        self.button.grid(row =self.r, column = self.col, columnspan= self.colspan, sticky=self.sticky)
        
#Everytime 0-9 button is clicked, store and update the string in the input box. 
def button_click(num):
    global button_number
    e1.insert('end', num)
    button_number += str(num)
    return button_number

#Input 'ANS' into box when ANS button is clicked
def button_ans(args):
    e1.insert(END, args)

#This function is called when any operator (except factorial) is clicked. It evaluates everything inside
#the input box and updates accordingly
def button_operator(args):
    global ans
    global expression
    global expression2
    global button_number
    global trigIdent

    try:
        #patterns that will be used to search for in input box
        matchObj = re.compile('[cst]..[(]')
        matchObj2 = re.compile('ANS')
        matchObj3 = re.compile('[-+//*^]ANS')
        matchObj4 = re.compile('[0-9]+[-+//*^][cst]..[(]')
        
        #first math operator has been clicked and no trig functions either
        if expression == '' and not re.match(matchObj, e1.get()):
            
            #If you click '=' after inputting numbers with no operator, just output that number
            if args[0] == operator.eq: 
                ans = float(button_number)
                e1.delete(0, END)
                e2.delete(0, END)
                button_number = ''
                e2.insert(0, ans)
                
            #ANS followed by some operator
            elif re.match(matchObj2, e1.get()):
                numList.append(ans)
                e1.insert(END, args[1])
                expression = args[0]
            else:
                numList.append(float(button_number))
                e1.insert(END, args[1])
                button_number = ''
                expression = args[0]

        else:
            #any operator other than '=' has been clicked. A Bunch of if statements to check various cases and update all
            #variables accordingly
            if args[0] != operator.eq:

                if re.search(matchObj, e1.get()):
                    if re.match(matchObj, e1.get()) and len(numList) < 1:
                        numList.append(float(button_number))
                        expression = args[0]
                        button_number = ''
                        e1.insert(END, args[1])
                    elif re.search(matchObj4, e1.get()) and len(numList) == 1:
                        numList.append(float(button_number))
                        expression2 = args[0]
                        button_number = ''
                        e1.insert(END, args[1])
                    elif re.search(matchObj4, e1.get()) and len(numList) > 1:
                        num[1] = expression2(num[1]+float(button_number))
                        expression2 = args[0]
                        button_number = ''
                        e1.insert(END, args[1])

                    else:
                        numList.append(float(button_number))
                        ans = expression(numList[0], numList[1])
                        numList.clear()
                        numList.append(ans)
                        expression = args[0]
                        button_number = ''
                        e1.insert(END, args[1])

            
                elif re.match(matchObj2,e1.get()):
                    numList.append(float(button_number))
                    ans = expression(numList[0], numList[1])
                    numList.clear()
                    numList.append(ans)
                    expression = args[0]
                    e1.insert(END, args[1])
                    button_number = ''

                else:
                    numList.append(float(button_number))
                    ans = expression(numList[0], numList[1])
                    numList.clear()
                    numList.append(ans)
                    expression = args[0]
                    e1.insert(END, args[1])
                    button_number = ''

            elif args[0] == operator.eq:
                if re.search(matchObj, e1.get()):
                    if re.match(matchObj, e1.get()) and len(numList) == 0:
                        if re.search(matchObj2, e1.get()):
                            e1.delete(0, END)
                            e2.delete(0, END)
                            ans = trigIdent(ans)
                            e2.insert(0, round(ans, 2))
                            button_number = ''
                            expression = ''
                            trigIdent = None
                        else:
                            e1.delete(0, END)
                            e2.delete(0, END)
                            ans = trigIdent(float(button_number))
                            e2.insert(0, round(ans,2))
                            button_number = ''
                            expression = ''
                            trigIdent = None
                    elif re.match(matchObj, e1.get()) and len(numList) >= 1:
                        e1.delete(0, END)
                        e2.delete(0, END)
                        numList.append(float(button_number))
                        ans = trigIdent(expression(numList[0], numList[1]))
                        e2.insert(0, round(ans, 3))
                        button_number = ''
                        expression = ''
                        trigIdent = None
                    
                    elif re.match(matchObj4, e1.get()):
                        if len(numList) == 1:
                            if re.search(matchObj2, e1.get()):
                                e1.delete(0, END)
                                e2.delete(0, END)
                                numList.append(trigIdent(ans))
                                ans = expression(numList[0], numList[1])
                                e2.insert(0, round(ans, 2))
                                button_number = ''
                                expression = ''
                                trigIdent = None
                            else:
                                e1.delete(0, END)
                                e2.delete(0, END)
                                numList.append(trigIdent(float(button_number)))
                                ans = expression(numList[0], numList[1])
                                e2.insert(0, round(ans,2))
                                button_number = ''
                                expression = ''
                                trigIdent = None
                        else:
                            e1.delete(0, END)
                            e2.delete(0, END)
                            ans = expression(numList[0], trigIdent(expression2(numList[1], float(button_number))))
                            e2.insert(0, round(ans,2))
                            button_number = ''
                            expression = ''
                            trigIdent = None


                    elif re.match(matchObj2, e1.get()):
                        e1.delete(0, END)
                        e2.delete(0, END)
                        numList.append(trigIdent(float(button_number)))
                        ans = expression(numList[0], numList[1])
                        e2.insert(0, round(ans,2))
                        numList.clear()
                        button_number = ''
                        expression = ''
                        trigIdent = None

                elif matchObj3.search(e1.get()):
                    e1.delete(0, END)
                    e2.delete(0, END)
                    numList.append(ans)
                    ans = expression(numList[0], numList[1])
                    numList.clear()
                    e2.insert(0, ans)
                    button_number = ''
                    expression = ''

                elif re.match(matchObj2, e1.get()):             
                    e1.delete(0, END)
                    e2.delete(0, END)
                    numList.append(float(button_number))
                    ans = expression(numList[0], numList[1])
                    numList.clear()
                    e2.insert(0, ans)
                    button_number = ''
                    expression = ''

                    
                else:
                    e1.delete(0, END)
                    e2.delete(0, END)
                    numList.append(float(button_number))
                    ans = expression(numList[0], numList[1])
                    numList.clear()
                    #e1.insert(0, 'ANS')
                    e2.insert(0, ans)
                    button_number = ''
                    expression = ''

    except ValueError:
        e1.delete(0, END)
        e1.insert(0, 'Error: Clear Screen')
    
    except ZeroDivisionError:
        e1.delete(0, END)
        e1.insert(0, 'Error: Division by zero')

def button_trig(args):
    global trigIdent
    e1.insert(END, args[1])
    trigIdent = args[0]

def button_pi(pi):
    global button_number
    e1.delete(0, END)
    e1.insert(0, pi)
    button_number = pi

def button_clear(args):
    global ans
    global expression
    global numList
    global trigIdent
    global button_number
    e1.delete(0,END)
    e2.delete(0, END)
    numList.clear()
    expression = ''
    button_number = ''
    ans = 0
    trigIdent = None

#evaluate the factorial of a number clicked
def button_fact(operator):
    global button_number
    global ans
    try:
        if re.match('ANS', e1.get()):
            e1.delete(0, END)
            e2.delete(0, END)
            ans = math.factorial(ans)
            e2.insert(0, ans)
            button_number = ''
        else:
            e1.delete(0, END)
            e2.delete(0, END)
            ans = math.factorial(float(button_number))
            e2.insert(0, ans)
            button_number = ''
    except ValueError:
        e1.delete(0, END)
        e1.insert(0, "ValueError: Clear Screen")
        
#turn a number into a negative, works with long expressions
def button_neg(operator):
    global button_number
    numLen = len(button_number)
    button_number = operator(float(button_number))
    count = len(e1.get())
    e1.delete(count-numLen,count)
    e1.insert(count-numLen, button_number)
    
#My global variables to keep track of everything 
ans = 0
numList = []
expression = ''
expression2 = ''
button_number = ''
trigIdent = None



#define buttons 0 - 9 with a for loop 
count=0
buttons = {}
for i in range(0,10):
    buttons['button_{}'.format(i)] = Button(root, text='{}'.format(i), padx=30, pady=30, command=lambda i=i: button_click(i))
for k, v in buttons.items():
    if count < 3:
        v.grid(row=3, column=count, sticky='ew')
    elif 2 < count < 6:
        v.grid(row=4, column = count-3, sticky='ew') 
    elif 5 < count < 9:
        v.grid(row=5, column= count-6, sticky='ew')
    count +=1

#Define and draw all other buttons

button_equal = Buttons(root, '=', button_operator, 155, 30, (operator.eq, '='))
button_equal.aButton(7,1,4)
button_add = Buttons(root, '+', button_operator, 30, 30, (operator.add, '+'))
button_add.aButton(6,0,1)
button_minus = Buttons(root, '-', button_operator, 30, 30, (operator.sub, '-'))
button_minus.aButton(6,1,1)
button_divide = Buttons(root, '/', button_operator, 30, 30, (operator.truediv, '/'))
button_divide.aButton(6,2,1)
button_mult = Buttons(root, '*', button_operator, 30, 30, (operator.mul, '*'))
button_mult.aButton(5,3,1)
button_pow = Buttons(root, '^', button_operator, 30, 30, (operator.pow, '^'))
button_pow.aButton(5,4,1)
button_ANS = Buttons(root, 'ANS', button_ans, 30, 30, 'ANS')
button_ANS.aButton(5,5,1)
button_factorial = Buttons(root, '!', button_fact, 30, 30, math.factorial)
button_factorial.aButton(4,3,1)
button_negative = Buttons(root, 'NEG', button_neg, 30, 30, operator.neg)
button_negative.aButton(4,4,1)
button_pi = Buttons(root, '\u03C0', button_click, 30, 30, math.pi)
button_pi.aButton(6,3,1)
button_cos= Buttons(root, 'cos', button_trig, 30, 30, (math.cos, 'cos('))
button_cos.aButton(6,4,1)
button_sin = Buttons(root, 'sin', button_trig, 30, 30, (math.sin, 'sin('))
button_sin.aButton(6,5,1)
button_tan = Buttons(root, 'tan', button_trig, 30, 30, (math.tan, 'tan('))
button_tan.aButton(7,5,1)
button_clear =Buttons(root, 'C', button_clear, 30, 30, None)
button_clear.aButton(7,0,1)

#Draw to screen
root.mainloop()
