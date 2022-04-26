from select import select
import numpy
import json
import tkinter as tk
from tkinter import ttk
from unidecode import unidecode
import unicodedata

result = False
first = True

known = {}
gen = {1:1, 2:152, 3:252, 4:387, 5:495, 6:650, 7:722, 8:810, 9:899}
current_gen = 1
number_known = 0

with open('liste pokemon.txt', 'r', encoding='utf-8') as fd:
    pokemon_list = fd.read().split(' ')
    pokemon_list.insert(0,"default")

for i in range(1,899):
    known[str(i)] = 0

known[str(0)] = 3

def save():
    global known
    global current_gen
    with open('save.txt', 'w') as save_file:
        save_file.write(json.dumps(known))

def load():   
    global known
    global number_known
    global current_gen
    with open('save.txt', 'r') as save_file:
        known = json.load(save_file)
    
    number_known = 0
    for i in range(1,899):
        if known[str(i)]>2:
            number_known = number_known + 1

    if number_known >= 898:
        return

    while sum(known[str(i)] for i in range(gen[current_gen],gen[current_gen+1])) >= (gen[current_gen+1]-gen[current_gen])*3:
        current_gen = current_gen + 1
        if current_gen == 9:
            current_gen = 1  
    


def generate_pkm():
    global number_known
    nbr = 0
    if number_known >= 898:
        return 1, pokemon_list[1]
    while known[str(nbr)]>2 or nbr > 898:
         nbr = numpy.random.randint(gen[current_gen],gen[current_gen+1])
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
    global current_gen
    global number_known
    if number_known >= 898:
        prompt.config(text = "Tu les connais tous !")
    if first:
        return
    if entry.get().isnumeric():
        generation = int(entry.get(), base=10)
        if generation > 0 and generation < 9:
            current_gen = generation
            result = True
            known[str(select_poke)] = known[str(select_poke)] - 1
        
    if not result:
        print(unidecode(entry.get()).lower())
        print(unidecode(name_poke).lower())

        if unidecode(entry.get()).lower() != unidecode(name_poke).lower() and entry.get() != 's':
            prompt.config(text = name_poke)
            result = True
            return

    if entry.get() == 's':
        known[str(select_poke)] = 2
    known[str(select_poke)] = known[str(select_poke)]+1
    if known[str(select_poke)]>2:
        number_known = number_known+1

    while sum(known[str(i)] for i in range(gen[current_gen],gen[current_gen+1])) >= (gen[current_gen+1]-gen[current_gen])*3:
        current_gen = current_gen + 1
        if current_gen == 9:
            current_gen = 1  
    
    entry.delete(0, 'end')
    select_poke, name_poke = generate_pkm()
    shiny = generate_shiny()
    new_pkm_image = get_image(select_poke, shiny)
    image_label.config(image = new_pkm_image)
    image_label.image = new_pkm_image
    prompt.config(text = "Quel est ce pokémon ? Nombre appris : "+str(number_known).zfill(3))
    result = False
    return


root = tk.Tk()
root.title('Pokemon Guesser')
root.geometry('1000x720')




pkm_image = get_image(select_poke, shiny)

image_label = tk.Label(root, image = pkm_image)

prompt = tk.Label(root, text="Quel est ce pokémon ? Nombre appris : "+str(number_known).zfill(3), font = "Arial 24 bold")

entry = tk.Entry(font = "Arial 24", width = 10, justify='center')


root.bind('<Return>', lambda event: enter_pressed(image_label, prompt))
first = False

savebtn = tk.Button(root, text='Save', command=save)
loadbtn = tk.Button(root, text='Load', command=load)

image_label.pack()

prompt.pack()

entry.pack()

savebtn.pack()
loadbtn.pack()

entry.focus()



root.mainloop()