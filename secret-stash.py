from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np

def numtbin(data):
    return bin(data)[2:].zfill(8)

def texttbin(data):
    bindat = ''.join(format(ord(i), '08b') for i in data)
    return bindat

def encode():
    try:
        sec_text = entry0.get(1.0, 'end-1c')

        bintext = ''.join(bin(ord(i))[2:].zfill(8) for i in sec_text)
        bintext += '0101111001011110010111100101111001011110'
        imgpath = path.get()
        if len(sec_text) == 0 and imgpath == '':
            messagebox.showerror('Error!!', "Select an Image and Enter some Text!!!")
        elif len(sec_text) == 0:
            messagebox.showerror('Error!!', "Enter some Text!!!")
        elif path.get() == '':
            messagebox.showerror('Error!!', "Select an Image !!!")
        else:
            pix = cv2.imread(path.get())
            dat_place = 0
            bin_dat_length = len(bintext)

            for i in pix:
                for j in i:
                    r, g, b = map(numtbin, j)

                    if dat_place < bin_dat_length:
                        j[0] = np.array(int(r[:-1] + bintext[dat_place])).astype(np.uint8)
                        dat_place += 1
                    if dat_place < bin_dat_length:
                        j[1] = np.array(int(g[:-1] + bintext[dat_place])).astype(np.uint8)
                        dat_place += 1
                    if dat_place < bin_dat_length:
                        j[2] = np.array(int(b[:-1] + bintext[dat_place])).astype(np.uint8)
                        dat_place += 1
                    if dat_place >= bin_dat_length:
                        break
        return pix
    except:
        y = messagebox.showwarning('Try Again !!!', 'Invalid Operation')
        return y

def btn_encodedta():
    x = encode()
    print(x.any())
    # if x != 'ok':
    if x.any():
        filename = filedialog.asksaveasfilename()
        if filename:
            cv2.imwrite(filename, x)

def decode():
    m = []
    l = ''
    entry0.delete('1.0', 'end')
    if path.get() == '':
        messagebox.showerror('Error!!!', "Please Select an image file to decode!!!")
    else:
        text = ''

        pix = cv2.imread(path.get())
        for i in pix:
            for j in i:
                r, g, b = map(numtbin, j)
                text += r[-1]
                text += g[-1]
                text += b[-1]
                if text[-40:len(text)] == '0101111001011110010111100101111001011110':
                    break
                else:
                    continue
            break

        for i in text:
            l += i
            if len(l) == 8:
                m.append(l)
                l = ''
        l = ''
        for i in m:
            l += chr(int(i, 2))
            if l[-5:len(l)] == '^^^^^':
                l = l.replace('^^^^^', '')
                break
        entry0.insert(END, l)

def askdir():
    file = filedialog.askopenfile(filetypes=[('PNG', "*.png"), ('JPG', "*.jpg")])
    try:
        path.set(file.name)
    except:
        messagebox.showerror("Error", "Select an image file")

tk = Tk()
tk.title("Secret Stash")
path = StringVar()
tk.geometry("613x532")
tk.configure(bg="#ffffff")
canvas = Canvas(
    tk,
    bg="#ffffff",
    height=532,
    width=613,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file="assets/background.png")
background = canvas.create_image(
    570.5, 266.0,
    image=background_img)

encodebutton = PhotoImage(file="assets/encodebutton.png")
b0 = Button(
    image=encodebutton,
    borderwidth=0,
    highlightthickness=0,
    command=btn_encodedta,
    relief="flat")
b0.place(
    x=61, y=450,
    width=152,
    height=52)

decodebutton = PhotoImage(file="assets/decodebutton.png")
b1 = Button(
    image=decodebutton,
    borderwidth=0,
    highlightthickness=0,
    command=decode,
    relief="flat")
b1.place(
    x=392, y=450,
    width=151,
    height=52)

selectimage = PhotoImage(file="assets/selectimage.png")
b2 = Button(
    image=selectimage,
    borderwidth=0,
    highlightthickness=0,
    command=askdir,
    relief="flat")
b2.place(
    x=506, y=24,
    width=59,
    height=60)

entry0_img = PhotoImage(file="assets/bigentrybox.png")
entry0_bg = canvas.create_image(
    296.0, 262.0,
    image=entry0_img)
entry0 = Text(
    bd=0,
    bg="#a2b5f7",
    highlightthickness=0)
entry0.place(
    x=76.0, y=138,
    width=440.0,
    height=246)
canvas.create_text(
    116.5, 34.5,
    text="TARGET IMAGE",
    fill="#3446a5",
    font=("None", int(10.0)))
entry1_img = PhotoImage(file="assets/smallentrybox.png")
entry1_bg = canvas.create_image(
    276.0, 59.5,
    image=entry1_img)
entry1 = Entry(
    fg='#3446A5',
    textvariable=path,
    bd=0,
    bg="#bcccf8",
    highlightthickness=0)
entry1.place(
    x=68, y=46,
    width=416,
    height=25)

tk.resizable(0, 0)
tk.mainloop()
