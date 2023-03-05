from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk

import PIL
from PIL import Image, ImageTk

Image.MAGICK_PATH = r"C:\Program Files\gs\gs10.00.0\bin"

NUMBER_OF_WORDS = 0


def open_image():
    global image
    try:
        filetypes = {
            ("All Files", "*.*"),
        }
        file = fd.askopenfile(filetypes=filetypes)
        img = Image.open(file.name)
        if img.size[0] > 690 or img.size[1] > 490:
            resized_img = img.resize(size=(img.size[0]//2, img.size[1]//2))
            img = resized_img
        image = ImageTk.PhotoImage(image=img)
        canvas.itemconfig(image_container, image=image)
    except PIL.UnidentifiedImageError:
        msg = "cannot identify image file %r" % file.name
        raise PIL.UnidentifiedImageError(msg)
    else:
        add_text.configure(state="active")
        save_button.configure(state="active")
        h['command'] = canvas.xview
        v['command'] = canvas.yview
        h.grid(column=1, row=2, sticky="W E")
        v.grid(column=2, row=1, sticky="N S")
        text.destroy()


def font_changed(font):
    canvas.itemconfig(tagOrId=f"text_container{NUMBER_OF_WORDS}", font=font)


def move_text(event):
    canvas.moveto(tagOrId=f"text_container{NUMBER_OF_WORDS}", x=event.x, y=event.y)


def save_as_png():
    dirname = fd.askdirectory(
        title='Choose Directory')

    filetypes = {
        ("png file", "*.png"),
    }
    file_name = fd.asksaveasfilename(filetypes=filetypes,
                                     title='Save File As...',
                                     defaultextension='.png',
                                     initialdir=dirname)
    canvas.postscript(file=f"{file_name}.eps", colormode='color')
    img = Image.open(f"{file_name}.eps")
    img.save(f'{file_name}', 'png')
    img.show()


def close_dialogue_box(popup, canvas_text):
    global NUMBER_OF_WORDS, canvas
    NUMBER_OF_WORDS += 1
    canvas.create_text(350, 250, text=canvas_text.get(), tags=f"text_container{NUMBER_OF_WORDS}")
    canvas.tag_bind(f"text_container{NUMBER_OF_WORDS}", "<B1-Motion>", move_text)
    root.tk.call('tk', 'fontchooser', 'configure', '-font', 'helvetica 24', '-command', root.register(font_changed))
    root.tk.call('tk', 'fontchooser', 'show')
    popup.destroy()


def add_text_func():
    popup = Tk()
    text = StringVar()
    add_text = ttk.Entry(popup, textvariable=text)
    add_text.focus_set()
    add_text.pack()
    button = ttk.Button(popup, text="Submit", command=lambda: close_dialogue_box(popup, add_text))
    button.pack()


root = Tk(className="Watermarkly")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_height = 620
window_width = 900
root.geometry(
    f"{window_width}x{window_height}-{int((screen_width - window_width) / 2)}-"
    f"{int((screen_height - window_height) / 2)}")
# root.resizable(False, False)

# Frame
frame = ttk.Frame(root, borderwidth=2, relief="sunken", height=500, width=700)
frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky="nwes")

# Logo
image = ImageTk.PhotoImage(image=Image.open("PngItem_48012.png"))
h = ttk.Scrollbar(frame, orient=HORIZONTAL)
v = ttk.Scrollbar(frame, orient=VERTICAL)
canvas = Canvas(frame, width=700, height=500, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set,
                xscrollcommand=h.set)
image_container = canvas.create_image(350, 250, image=image, anchor="center")
canvas.grid(column=1, row=1)


# Add Watermark Text
text = ttk.Label(frame, text="Add Watermark", font=("Segoe UI", 14, "normal"))
text.grid(row=2, column=1)

# Select Button
select_button = ttk.Button(frame, text="Select", command=lambda: open_image())
select_button.grid(column=0, row=3)

# Add Text Button
add_text = ttk.Button(frame, text="Add Text", command=lambda: add_text_func(), state="disabled")
add_text.grid(column=1, row=0)

# Save Image Button
save_button = ttk.Button(frame, text="Save Image", command=lambda: save_as_png(), state="disabled")
save_button.grid(column=2, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
