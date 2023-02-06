from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Courier"

word_nr = 0
lang = ["French", "English"]
side = 0

# load csv
data = pd.read_csv("data/french_words.csv")

french = data["French"].tolist()
english = data["English"].tolist()


# check
def change():
    global side
    if len(english) > 0:
        side -= 1
        side = abs(side)

        canvas.itemconfig(bg_img, image=img[side])
        canvas.itemconfig(language, text=lang[side])
        canvas.itemconfig(word, text=english[word_nr])


def new(result):
    global word_nr
    global side

    if len(english) > 0:
        if result:
            print(word_nr, len(english))
            french.pop(word_nr)  # INDEX OUT OF RANGE
            english.pop(word_nr)
            df = pd.DataFrame({'French': french,
                               'English': english})
            df.to_csv('data/french_words.csv', index=False)

    side -= 1
    side = abs(side)

    if len(english) > 0:
        word_nr = random.randint(0, len(english) - 1)
        canvas.itemconfig(word, text=french[word_nr])
        canvas.itemconfig(bg_img, image=img[side])
        canvas.itemconfig(language, text=lang[side])
        window.after(3000, change)
    else:
        canvas.itemconfig(word, text="won")
        canvas.itemconfig(language, text="You")


def good():
    new(1)


def bad():
    new(0)


# UI
window = Tk()
img = [PhotoImage(file="images/card_front.png"), PhotoImage(file="images/card_back.png")]
window.title("Flashcards")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

bg_img = canvas.create_image(400, 263, image=img[0])
canvas.grid(column=0, row=0, columnspan=2)
language = canvas.create_text(400, 100, text=lang[0], font=(FONT_NAME, 35))
word = canvas.create_text(400, 250, text=french[word_nr], font=(FONT_NAME, 40, "bold"))

wrong = PhotoImage(file="images/wrong.png")
cross_button = Button(image=wrong, bg=BACKGROUND_COLOR, borderwidth=0, command=bad)
cross_button.grid(column=0, row=1)

right = PhotoImage(file="images/right.png")
tick_button = Button(image=right, bg=BACKGROUND_COLOR, borderwidth=0, command=good)
tick_button.grid(column=1, row=1)

window.after(3000, change)

window.mainloop()
