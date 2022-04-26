from select import select
import numpy
import tkinter as tk
from tkinter import ttk
from unidecode import unidecode
import unicodedata

result = False
first = True

known = {}

with open('liste pokemon.txt', 'r', encoding='utf-8') as fd:
    pokemon_list = fd.read().split(' ')
    pokemon_list.insert(0,"default")

for i in range(1,899):
    known[i] = 0

known[0] = 6

def generate_pkm():
    nbr = 0
    while known[nbr]>2:
        nbr = numpy.random.randint(1,899)
    return nbr, pokemon_list[nbr]

def generate_shiny():
    shiny_num = numpy.random.randint(0,6)
    return 'S' if shiny_num <2 else ''

def get_image(select_poke, shiny):
    img_string = 'img/'+str(select_poke).zfill(3)
    img_string = img_string+shiny+'.png'
    return tk.PhotoImage(file=img_string)

select_poke, name_poke = generate_pkm()
shiny = generate_shiny()

def enter_pressed(image_label, prompt):
    global select_poke
    global name_poke
    global result
    if first:
        return
    if not result:
        print(unidecode(entry.get()).lower())
        print(unidecode(name_poke).lower())

        if unidecode(entry.get()).lower() != unidecode(name_poke).lower() and entry.get() != 's':
            prompt.config(text = name_poke)
            result = True
            return
    if entry.get() == 's':
        known[select_poke] = 3
    known[select_poke] = known[select_poke]+1
    entry.delete(0, 'end')
    select_poke, name_poke = generate_pkm()
    shiny = generate_shiny()
    new_pkm_image = get_image(select_poke, shiny)
    image_label.config(image = new_pkm_image)
    image_label.image = new_pkm_image
    prompt.config(text = "Quel est ce pokémon ?")
    result = False
    return


root = tk.Tk()
root.title('Pokemon Guesser')
root.geometry('640x720')




pkm_image = get_image(select_poke, shiny)

image_label = tk.Label(root, image = pkm_image)

prompt = tk.Label(root, text="Quel est ce pokémon ?", font = "Arial 24 bold")

entry = tk.Entry(font = "Arial 24", width = 10, justify='center')


root.bind('<Return>', lambda event: enter_pressed(image_label, prompt))
first = False

image_label.pack()

prompt.pack()

entry.pack()
entry.focus()

root.mainloop()