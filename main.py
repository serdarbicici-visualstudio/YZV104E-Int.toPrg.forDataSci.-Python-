# name-surname: Serdar Biçici
# student id: 150210331

from tkinter import *
from tkinter import ttk

import json

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import string
import random

import requests
from bs4 import BeautifulSoup

import time


root = Tk()
root.title("The Spelling Bee by Serdar")
root.geometry("700x775")
root.resizable(False, False)
root.config(background="#e3dac9")
root.iconbitmap("favicon.ico")
taskbar_icon = PhotoImage(file="taskbarlogo.png")
root.iconphoto(True, taskbar_icon)



##############################################################################

extra_l = ""

##############################################################################

def get_dictionary_meanings(word):
    
    url = f"https://www.merriam-webster.com/dictionary/{word}"

    response = requests.get(url)
   
    soup = BeautifulSoup(response.content, "html.parser")
    
    meaning_elements = soup.select(".dtText")
    
    meanings = [element.get_text() for element in meaning_elements]

    return meanings


##############################################################################
def random_letters():

    alphabet = list(string.ascii_uppercase)
    vowels = ["A", "E", "I", "O", "U"]
    letter_weights = [37207, 9341, 20394, 19865, 57894, 7102, 15750, 11196, 44308, 885, 4668, 26216, 13420, 34971, 30595, 14792, 954, 35739, 45715, 34457, 16564, 5123, 4540, 1419, 7902, 2012]
    global all_letters
    all_letters = list()

    middle_letter = random.choice(alphabet)
    letter_weights.pop(int(alphabet.index(middle_letter)))
    alphabet.remove(middle_letter)
    
    other_letters = list()
    for i in range(6):
        l = random.choices(population=alphabet, weights=letter_weights, k=1)
        letter_weights.pop(int(alphabet.index(l[0])))
        alphabet.remove(l[0])
        other_letters.append(l[0])

    all_letters = other_letters
    all_letters.append(middle_letter)
    vowel_count = 0
    for letter in all_letters:
        if letter in vowels:
            vowel_count += 1

    if vowel_count < 2 or vowel_count > 4:
        return random_letters()
       
    return  middle_letter, other_letters[0], other_letters[1], other_letters[2], other_letters[3], other_letters[4], other_letters[5]

def random_extra_letter():
    alphabet = list(string.ascii_uppercase)

    extra_letter = random.choice(alphabet)

    if extra_letter in all_letters:
        return random_extra_letter()
    
    return extra_letter


middle_letter, l1, l2, l3, l4, l5, l6 = random_letters()

##############################################################################

def word_list_check():
    
    correct_words_list = list()

    global letters
    letters = [l1, l2, l3, l4, l5 ,l6, middle_letter]

    with open("filtered_words1.txt", "r") as file:
        for word in file:
            if str(middle_letter) in word:
                correct_words_list.append(word.strip())
            
    correct_words_list = [word for word in correct_words_list if all(letter in letters for letter in word)]

    return correct_words_list

def letter_check():
    invalid_words = list()

    for i in letters:
        
        for word in valid_word_list:
            if i in word:
                pass
            else:
                invalid_words.append(word)

        if len(invalid_words) == len(valid_word_list):
            return False
        else:
            invalid_words.clear()

    return True
                
def pangram_check():
    for word in valid_word_list:
        if l1 in word and l2 in word and l3 in word and l4 in word and l5 in word and l6 in word:          
            return True, get_dictionary_meanings(word)
    
    return False, "This letters do not form any pangram"

l = 0
while l < 10 or l > 50:
    valid_word_list = word_list_check()

    if len(valid_word_list) < 10 or len(valid_word_list) > 50:
        middle_letter, l1, l2, l3, l4, l5, l6 = random_letters()
        l = len(valid_word_list)
        if letter_check() == False:
            pass
    else:    
        print(len(valid_word_list))#
        print(valid_word_list)#
        break


##############################################################################

def word_delete():
    global current_word
    current_word = ""
    word_label.config(text="Enter Word...")

##############################################################################
current_word = ""

def letter_button(word, letter):
   
    if len(word) > 20:
        
        word_label.config(text="Enter Word...")

        error_window = Toplevel(root)
        error_window.resizable(False, False)
        error_window.title("Error!")
        error_window.geometry("200x30")
        error_window_label = Label(error_window, text="You have exceeded character limit!", anchor="center")
        error_window_label.pack()
        
        return word_delete()
        
    global current_word
    
    word = word + letter
    current_word = word
    word_label.config(text=word)
    

word_label = Label(text="Enter Word...",
             font=60,
             anchor="center",
             background="#e3dac9"
             )


################################################

def on_item_selected(*args):
    selected_word = correct_words_listbox.get(correct_words_listbox.curselection())#####
    meaning = get_dictionary_meanings(selected_word)
    
    word_meaning_header_label.config(text=str(selected_word).title())
    word_meaning_label.config(text=str(meaning[0][1::]).capitalize(), wraplength=600, justify="left")


################################################

words_list = list()
correct_words_listbox = Listbox(root, 
                                background="#e3dac9", 
                                width=20, 
                                height=13,
                                justify=CENTER,
                                font=("Arial", 9, "bold"))


correct_words_listbox.bind("<<ListboxSelect>>", on_item_selected)

###############################################################

hint = ""

hint_header_label = Label(text="",
                            font=("Arial", 20, "bold"),
                            background="#e3dac9")

hint_label = Label(text=hint,
                     background="#e3dac9")

pangram_header_label = Label(text="",
                             font=("Arial", 20, "bold"),
                             background="#e3dac9")

pangram_label = Label(text="",
                      background="#e3dac9")

##############################################################

def random_hinted_word():
    hinted_word = random.choice(valid_word_list)

    if hinted_word not in words_list:
        return hinted_word
    else:
        return random_hinted_word()

score = 0
found_word_number = 0
extra_count = 3
extra_state = False
avg_time = list()


start_time = time.time()

def word_check(word):

    global extra_l
    global found_word_number
    global extra_count
    global extra_state
    global hint
    global score
    global start_time
    global end_time
    
    meaning = get_dictionary_meanings(word)

    if len(word) == 0:
        return

    if word in valid_word_list and word not in words_list:

        score = len(word) + score
        found_word_number += 1
        found_number_label.config(text=found_word_number)
        words_list.append(word)
        correct_words_listbox.insert(END, word)

        end_time = time.time()
        elapsed_time = end_time - start_time
        avg_time.append(elapsed_time)
        
        start_time = time.time()

        game_progress()

        if len(words_list) > len(valid_word_list)/2:
            pangram_state, pangram_string = pangram_check()
            if pangram_state == True:
                pangram_header_label.config(text="Hint for Pangram")
                pangram_label.config(text=pangram_string[0][1::].capitalize(), wraplength=600, justify="left")
            elif pangram_state == False:
                pangram_header_label.config(text="Hint for Pangram")
                pangram_label.config(text=pangram_string)
            
    elif len(meaning) != 0 and len(word) >= 3 and word not in words_list and middle_letter in word:
        score = len(word) + score
        found_word_number += 1
        found_number_label.config(text=found_word_number)
        words_list.append(word)
        correct_words_listbox.insert(END, word)

        end_time = time.time()
        elapsed_time = end_time - start_time
        avg_time.append(elapsed_time)
        
        start_time = time.time()

    
    if len(words_list) % 5 == 0 and len(words_list) != 0:
        hinted_word = random_hinted_word()
        
        hint = get_dictionary_meanings(hinted_word)[0]
        
        hint_header_label.config(text="Hint")

        hint_label.config(text=hint[1::].capitalize(), wraplength=600, justify="left")
    

    word_delete()


    if len(words_list) % 7 == 0 and extra_state != True and len(words_list) != 0:
        extra_state = True
        extra_l = random_extra_letter()
        button_extra.config(text=extra_l, activeforeground="#cb8e00",
                            activebackground="#FFFFFF",
                            foreground="#FFFFFF",
                            background="#cb8e00", 
                            borderwidth="0.1",
                            width=w1,
                            font=letter_font,
                            command=lambda: letter_button(current_word, extra_l))
    
    if extra_count == 0:
        extra_count = 3
        extra_state = False
        extra_l = ""
        button_extra.config(text=extra_l, 
                            background="#e3dac9", 
                            foreground="#e3dac9",
                            command=None)
        
    if extra_state:    
        extra_count -= 1
        extra_l = random_extra_letter()
        button_extra.config(text=extra_l, activeforeground="#cb8e00",
                            activebackground="#FFFFFF",
                            foreground="#FFFFFF",
                            background="#cb8e00", 
                            borderwidth="0.1",
                            width=w1,
                            font=letter_font,)


    found_valid_words = [x for x in words_list if x in valid_word_list]

    if len(found_valid_words) == len(valid_word_list):
        error_window = Toplevel(root)
        error_window.resizable(False, False)
        error_window.config(background="#e3dac9")
        error_window.title("Game Over!")
        error_window.geometry("350x150")
        error_window_label = Label(error_window, 
                                   text="\nYou have completed the game\nYou can click the SAVE button and choose another saved game", 
                                   anchor="center", 
                                   background="#e3dac9")
        error_window_label.pack()


####################################################################

def adjust_label_placement(*args):
    label = word_label
    
    label.place(x=(root.winfo_width()- label.winfo_width()) // 2,
                y=(root.winfo_height() - label.winfo_height()) // 2)

###########################################################

style = ttk.Style()
style.theme_use("clam")
style.configure("colored.Horizontal.TProgressbar", 
                background="#cb8e00", 
                bordercolor="#e3dac9", 
                lightcolor="#e3dac9", 
                darkcolor="#e3dac9", 
                troughcolor="#e3dac9")

progress_bar = ttk.Progressbar(root, mode="determinate", length=700, maximum=len(valid_word_list), style="colored.Horizontal.TProgressbar")

def game_progress():
    
    progress_bar["value"] = len(words_list)
    root.update()
    
progress_bar.place(x=0,y=0)

################################################
w1 = 3 
#width of buttons


letter_font = ("Arial", 30, "bold")

button1 = Button(root, 
                 activebackground="#cb8e00",
                 activeforeground="#FFFFFF",
                 background="#FFFFFF",
                 foreground="#cb8e00", 
                 borderwidth="0.1",
                 width=w1,
                 font=letter_font,
                 command=lambda: letter_button(current_word, l1),
                 text=l1) 
button2 = Button(root, 
                 activebackground="#cb8e00",
                 activeforeground="#FFFFFF",
                 background="#FFFFFF",
                 foreground="#cb8e00", 
                 borderwidth="0.1",
                 width=w1,
                 font=letter_font,
                 command=lambda: letter_button(current_word, l2),
                 text=l2) 
button3 = Button(root, 
                 activebackground="#cb8e00",
                 activeforeground="#FFFFFF",
                 background="#FFFFFF",
                 foreground="#cb8e00", 
                 borderwidth="0.1",
                 width=w1,
                 font=letter_font,
                 command=lambda: letter_button(current_word, l3),
                 text=l3) 
button4 = Button(root, 
                 activebackground="#cb8e00",
                 activeforeground="#FFFFFF",
                 background="#FFFFFF",
                 foreground="#cb8e00", 
                 borderwidth="0.1",
                 width=w1,
                 font=letter_font,
                 command=lambda: letter_button(current_word, l4),
                 text=l4) 
button5 = Button(root, 
                 activebackground="#cb8e00",
                 activeforeground="#FFFFFF",
                 background="#FFFFFF",
                 foreground="#cb8e00", 
                 borderwidth="0.1",
                 width=w1,
                 font=letter_font,
                 command=lambda: letter_button(current_word, l5),
                 text=l5) 
button6 = Button(root, 
                 activebackground="#cb8e00",
                 activeforeground="#FFFFFF",
                 background="#FFFFFF",
                 foreground="#cb8e00", 
                 borderwidth="0.1",
                 width=w1,
                 font=letter_font,
                 command=lambda: letter_button(current_word, l6),
                 text=l6)
button7 = Button(root,#middle letter 
                 activeforeground="#cb8e00",
                 activebackground="#FFFFFF",
                 foreground="#FFFFFF",
                 background="#cb8e00", 
                 borderwidth="0.1",
                 width=w1,
                 font=letter_font,
                 command=lambda: letter_button(current_word, middle_letter),
                 text=middle_letter) 

button_extra = Button(root,
                 activeforeground="#cb8e00",
                 activebackground="#FFFFFF",
                 foreground="#cb8e00",
                 background="#e3dac9",
                 borderwidth="0.1",
                 width=w1,
                 font=letter_font,
                 command=None,
                 text=extra_l) 

del_button = Button(root,
                 activeforeground="#cb8e00",
                 activebackground="#FFFFFF",
                 foreground="#FFFFFF",
                 background="#cb8e00",
                 borderwidth="0.1",
                 text="Delete",
                 width=6,
                 font=("Arial", 14, "bold"),
                 command=word_delete)

enter_button = Button(root,
                 activeforeground="#cb8e00",
                 activebackground="#FFFFFF",
                 foreground="#FFFFFF",
                 background="#cb8e00", 
                 borderwidth="0.1",
                 width=6,
                 font=("Arial", 14, "bold"),
                 command=lambda: word_check(current_word),
                 text="Enter") 

#################################################


def plot_graph():
    
    if len(words_list) <= 1:
        return

    global stats

    values = avg_time  

    fig = Figure(figsize=(max(avg_time), len(valid_word_list)), dpi=100)#y, x
    ax = fig.add_subplot(111)

    x_labels = words_list  
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels)
    ax.tick_params(axis='x', rotation=270)
    ax.plot(values)

    stats = Toplevel(root)
    stats.title("The Spelling Bee by Serdar")
    stats.geometry("700x775")
    stats.resizable(False, False)
    stats.config(background="#e3dac9")
    stats.iconbitmap("favicon.ico")
    taskbar_icon = PhotoImage(file="taskbarlogo.png")
    stats.iconphoto(True, taskbar_icon)

    header = Label(stats, text="Statistics\n", font=("Arial", 16, "underline"), background="#e3dac9", justify="center")
    header.pack()

    score_header = Label(stats, text="Score:\n", font=("Arial", 12, "italic"), background="#e3dac9", justify="center")
    score_header.pack()
    score_label = Label(stats, text=score, font=("Arial", 12, "bold"), background="#e3dac9", justify="center")
    score_label.pack()

    avg_word_length_header = Label(stats, text="\nAvg. word length is:\n", font=("Arial", 12, "italic"), background="#e3dac9", justify="center")
    avg_word_length_header.pack()

    avg_word_length = [len(x) for x in words_list]
    avg_word_length = sum(avg_word_length) / len(words_list)
    avg_word_length = str(avg_word_length)[0:3]
    avg_word_length_label = Label(stats, text=avg_word_length, font=("Arial", 12, "bold"), background="#e3dac9", justify="center")
    avg_word_length_label.pack()

    canvas_header = Label(stats, text="\nWord Finding Time Graph in Seconds", font=("Arial", 12, "italic"), background="#e3dac9", justify="center")
    canvas_header.pack()

    canvas = FigureCanvasTkAgg(fig, master=stats)
    canvas.draw()
    canvas.get_tk_widget().pack()


def saved_game_analysis():
    game_info = saved_games.get()

    try:
        with open('usernames.json', 'r') as file:
            previous_games = json.load(file)
    except json.decoder.JSONDecodeError:
        previous_games = list()


    for data in previous_games:
        
        if data["username"] == game_info:

            if len(data["found_words"]) <= 1:
                return

            global stats
            
            values = data["word_time_list"]  

            fig = Figure(figsize=(max(values), len(data["all_words"])), dpi=100)#y, x
            ax = fig.add_subplot(111)

            x_labels = data["found_words"]  
            ax.set_xticks(range(len(x_labels)))
            ax.set_xticklabels(x_labels)
            ax.tick_params(axis='x', rotation=270)

            ax.plot(values)

            stats = Toplevel(root)
            stats.title("The Spelling Bee by Serdar")
            stats.geometry("700x775")
            stats.resizable(False, False)
            stats.config(background="#e3dac9")
            stats.iconbitmap("favicon.ico")
            taskbar_icon = PhotoImage(file="taskbarlogo.png")
            stats.iconphoto(True, taskbar_icon)

            letters = ",".join(data["letters"])
            stats_header = "Statistics of " + data["username"] + " with letters " + letters.lower() + "," + str(data["middle_letter"]).upper() 

            header = Label(stats, 
                           text=stats_header, 
                           font=("Arial", 16, "underline"), 
                           background="#e3dac9", 
                           justify="center")
            header.pack()

            score_header = Label(stats, 
                                 text="\nScore:\n", 
                                 font=("Arial", 12, "italic"), 
                                 background="#e3dac9", 
                                 justify="center")
            score_header.pack()
            score_label = Label(stats, 
                                text=data["score"], 
                                font=("Arial", 12, "bold"), 
                                background="#e3dac9", 
                                justify="center")
            score_label.pack()

            avg_word_length_header = Label(stats, 
                                           text="\nAvg. word length is:\n", 
                                           font=("Arial", 12, "italic"), 
                                           background="#e3dac9", 
                                           justify="center")
            avg_word_length_header.pack()

            avg_word_length = [len(x) for x in data["found_words"]]
            avg_word_length = sum(avg_word_length) / len(data["found_words"])
            avg_word_length = str(avg_word_length)[0:3]
            avg_word_length_label = Label(stats, text=avg_word_length, 
                                          font=("Arial", 12, "bold"), 
                                          background="#e3dac9", 
                                          justify="center")
            avg_word_length_label.pack()

            canvas_header = Label(stats, 
                                  text="\nWord Finding Time Graph in Seconds", 
                                  font=("Arial", 12, "italic"), 
                                  background="#e3dac9", 
                                  justify="center")
            canvas_header.pack()

            canvas = FigureCanvasTkAgg(fig, master=stats)
            canvas.draw()
            canvas.get_tk_widget().pack()


def save_game():

    global username_entry
    global saved_games

    save = Toplevel(root)
    save.title("The Spelling Bee by Serdar")
    save.geometry("350x375")
    save.resizable(False, False)
    save.config(background="#e3dac9")
    save.iconbitmap("favicon.ico")
    taskbar_icon = PhotoImage(file="taskbarlogo.png")
    save.iconphoto(True, taskbar_icon)


    thanks_message = Label(save, text="\n\nThank you for playing\n\n", font=("Arial", 12, "italic"), background="#e3dac9")
    thanks_message.pack()

    username_entry = Entry(save, width=24)
    username_entry.pack()

    save_button = Button(save, 
                         text='Save',
                         background="#cb8e00",
                         width="20",
                         borderwidth="0.1",
                         command=save_username)
    save_button.pack()

    empty_label = Label(save, text="\n\n", background="#e3dac9")
    empty_label.pack()

    saved_games = ttk.Combobox(save, 
                        background="#e3dac9",
                        width=18, 
                        height=13,
                        justify=CENTER,      
                        font=("Arial", 9, "bold"))
    try:
        with open('usernames.json', 'r') as file:
            previous_games = json.load(file)
    except json.decoder.JSONDecodeError:
        previous_games = list()

    usernames_list = list()
    for data in previous_games:
        usernames_list.append(data["username"])
    saved_games["values"] = usernames_list
    saved_games.pack()
    
    enter_game = Button(save, text="Enter Game", background="#cb8e00", width="20", command=saved_game_analysis)#command ekle
    enter_game.pack()


def save_username():

    try:
        with open('usernames.json', 'r') as file:
            existing_data = json.load(file)
    except json.decoder.JSONDecodeError:
        existing_data = list()

    user_data = dict()
    username = username_entry.get()

    user_data["username"] = username
    user_data["letters"] = [l1, l2, l3, l4, l5, l6]
    user_data["middle_letter"] = middle_letter
    user_data["word_time_list"] = avg_time
    user_data["found_words"] = words_list
    user_data["all_words"] = valid_word_list
    user_data["score"] = score

    existing_data.append(user_data)

    with open('usernames.json', 'w') as file:
        json.dump(existing_data, file)


button_save = Button(root,
                 activeforeground="#cb8e00",
                 activebackground="#FFFFFF",
                 foreground="#FFFFFF",
                 background="#cb8e00",
                 borderwidth="0.1",
                 text=" Save ",
                 width=6,
                 font=("Arial", 14, "bold"),
                 command=save_game)

button_save.place(x=230, y=733)

button_analysis = Button(root,
                 activeforeground="#cb8e00",
                 activebackground="#FFFFFF",
                 foreground="#FFFFFF",
                 background="#cb8e00",
                 borderwidth="0.1",
                 text="Analysis",
                 width=6,
                 font=("Arial", 14, "bold"),
                 command=plot_graph)

button_analysis.place(x=400, y=733)

#################################################

found_number_header_label = Label(text="You have found...",
                                 font=("Arial", 18, "bold"),
                                 background="#e3dac9")

found_number_label = Label(text=found_word_number,
                           font=("Arial", 80, "bold"),
                           background="#e3dac9")

found_number_header_end_label = Label(text="words",
                                 font=("Arial", 18, "bold"),
                                 background="#e3dac9")

#################################################

word_meaning_header_label = Label(text="",
                                   background="#e3dac9",
                                   font=("Arial", 20, "bold"))

word_meaning_label = Label(text="",
                           background="#e3dac9")

#################################################

#middle column
button1.place(x=310, y=105)#80 uzunluk#85
button7.place(x=310, y=190)
button2.place(x=310, y=275)

#left column
button3.place(x=225, y=147)
button4.place(x=225, y=232)

#right column
button5.place(x=395, y=147)
button6.place(x=395, y=232)

#current word
root.bind("<Configure>", adjust_label_placement)

#extra letter button
button_extra.place(x=310, y=25)

#delete button
del_button.place(x=230, y=440)

#enter button
enter_button.place(x=400, y=440)

#found words counter
found_number_header_label.place(x=490, y=120)
found_number_label.place(x=540, y=165)
found_number_header_end_label.place(x=550, y=290)

#correct words display
correct_words_listbox.place(x=45, y=120)

#word meaning
word_meaning_header_label.place(x=50, y=500)
word_meaning_label.place(x=50, y=540)

#hints
hint_header_label.place(x=50, y=580)
hint_label.place(x=50, y=620)

#pangrams

pangram_header_label.place(x=50, y=660)
pangram_label.place(x=50, y=700)


root.mainloop()