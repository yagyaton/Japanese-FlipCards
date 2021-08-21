from tkinter import *
import pandas
import random
import os
#Using OS so check if the file Learnt Words is empty, so I can add header to it, otherwise not.



#----------------------------------------Setting up the window------------------------------------------------#
window=Tk()
window.title(string="Nihongo no Flashcards")
window.config(bg="dark turquoise", padx=130, pady=70 )
window.minsize(1100,720)
#---------------------------------------------------------------------------------------------------------------#




#--------------------------------------------READING FROM CSV FILE---------------------------------------------#
#Reading from the csv file and making a data frame
jv=pandas.read_csv("./Japanese Vocab/Japanesevocab.csv")
# print(jv)
#Setting up the database list for the words
jwords=list(jv.Furigana)
#---------------------------------------------------------------------------------------------------------------#




# -----------------------------JUST TRYING SHIT OUT FOR READING FROM DATAFRAMES---------------------------------#
# currentword=random.choice(jwords)
# x=int(str(jv[jv.Furigana==currentword].Kanji)[:3])
# x=jv[jv.Furigana==currentword].to_dict(orient="split")
# # print(jv.iloc[[2],[0,1,2,3]])
# print(x)
# x=jv[jv.Furigana==currentword][1:]
# print(jv.loc[x])
# print(jv.index[x])
# print(jv.loc[x].at["Furigana"])
# print(type(jv[jv.Furigana==currentword].Furigana))
# print(len(jwords))
# ---------------------------------------------------------------------------------------------------------------#




#--------------------------------------------------FLASHCARD INITIALIZATION--------------------------------------#
# Setting up the flashcard canvas, I am setting up these globally so I can use them in both the fuctions, otherwise they'b only be limited to nextcard function
flashcard=Canvas(width=816, height=480, bg="snow", highlightthickness=5, highlightbackground="white")
flashcard.grid(row=0, column=0, columnspan=2)
language=flashcard.create_text(425,150,text="", font=("Roboto", 35, "italic"))
mainword=flashcard.create_text(425,270,text="", font=("Roboto", 40, "bold italic"))
support=flashcard.create_text(425,350,text="", font=("Roboto", 40))
#----------------------------------------------------------------------------------------------------------------#




#-------------------------------------------------FLIPCARD FUNCTIONS---------------------------------------------#
#Next word on flashcard appear function
x=0
currentword=""
def flipcard():
    flashcard.config(bg="lemon chiffon")
    flashcard.itemconfig(language, text="English")
    flashcard.itemconfig(mainword,text=jv.loc[x].at["Meaning"])
    flashcard.itemconfig(support,text=jv.loc[x].at["Romaji"])

def nextcard():
    flashcard.config(bg="snow")
    global x, fliptimer, currentword
    currentword=random.choice(jwords)
    window.after_cancel(fliptimer)
    x=int(str(jv[jv.Furigana==currentword].Kanji)[:3])
    #string dtype is sliced and first 3 characters hold index number, which is converted to integer and assigned to x
    flashcard.itemconfig(language, text="Japanese")
    flashcard.itemconfig(mainword,text=jv.loc[x].at["Kanji"])
    flashcard.itemconfig(support,text=jv.loc[x].at["Furigana"]) 
    #Calling the flipcard function after 3 seconds
    fliptimer=window.after(5000, flipcard)      

fliptimer=window.after(5000, flipcard) 
nextcard()
#----------------------------------------------------------------------------------------------------------------#
    



#--------------------------------------Right, Wrong button functions----------------------------------------------#
def rightnext():
    global jv
    #---------------------------------Copying learnt Word to a different CSV File--------------------#
    writehead=False
    try:
        if os.stat("./Learnt Words/Learnt Japanese Words.csv").st_size == 0:
            writehead=True
        else:
            writehead=False
    except FileNotFoundError:
        writehead=True
        with open("./Learnt Words/Learnt Japanese Words.csv", "w") as fh:
            pass
    finally: 
        jv[jv.Furigana==currentword].to_csv("./Learnt Words/Learnt Japanese Words.csv", mode='a', header=writehead, index=False)
    #---------------------------------------------------------------------------------------------------#
    
    jwords.remove(jv.loc[x].at["Furigana"])
    #----------------------------Rewriting csv file with deleted row in data frame----------------------#
    jv = jv.drop(jv.index[x-1]) #Index (x-1) because earlier it was counting header as a row and deleting wrong element
    jv.to_csv("./Japanese Vocab/Japanesevocab.csv", index=False)
    #---------------------------------------------------------------------------------------------------#
    print(len(jwords))
    nextcard()

def wrongnext():
    nextcard()
#-----------------------------------------------------------------------------------------------------------------#




#------------------------------------------Setting up the buttons-------------------------------------------------#
rightimage=PhotoImage(file="./images/right.png")
wrongimage=PhotoImage(file="./images/wrong.png")

dontknow=Button(image=wrongimage,bg="dark turquoise", padx=50, pady=50, highlightthickness=0, command=wrongnext)
dontknow.grid(row=1, column=0, sticky="w")
know=Button(image=rightimage, bg="dark turquoise", padx=50, pady=50, highlightthickness=0, command=rightnext)
know.grid(row=1, column=1, sticky="e")
#------------------------------------------------------------------------------------------------------------------#


window.mainloop()


#Trying shit out about a 2nd window popping up.
# window2=Tk()
# window2.title(string="2nd")
# window2.mainloop()
