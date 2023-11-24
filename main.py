from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageColor
from tkinter.filedialog import askopenfilename, asksaveasfilename
from dictionaries import fonts_dict

FONT = ("calibri", 13, "normal")
BLUE = "#053B50"
FILE_TYPES = (
    ("All Files", "*.*"),
    ("PNG", "*.png"),
    ("BMP", "*.bmp"),
    ("GIF", "*.gif"),
    ("JPEG", "*.jpg"))

opened_img = Image.open("start_img.png")
img_width, img_height = 800, 600
wm_x, wm_y = 400, 300
img_with_draw = None
img_to_label = None
watermark = ""
wm_text_font_symbol = "arial.ttf"
wm_text_size = "30"
wm_rgb_color = (0, 0, 0)
wm_opacity = 255

def open_file(event=None):  # filedialog
    global opened_img, img_width, img_height, wm_x, wm_y, img_to_label
    img_filename = askopenfilename(filetypes=FILE_TYPES)
    if img_filename:
        opened_img = Image.open(img_filename).convert(mode="RGBA")
        img_width, img_height = opened_img.size
        if img_width > 800 or img_height > 600:
            resize_factor = 800 / img_width
            img_width, img_height = int(img_width * resize_factor), int(img_height * resize_factor)
            opened_img = opened_img.resize((img_width, img_height), Image.LANCZOS)
        wm_x, wm_y = img_width // 2, img_height // 2
        img_to_label = ImageTk.PhotoImage(opened_img)
        img_label.config(image=img_to_label)
        add_text_button.config(state="normal")
        add_logo_button.config(state="normal")
        opacity_scale.config(state="normal")
        menu_file.entryconfig(1, state="normal")

def draw_wm():
    global img_with_draw, img_to_label
    base = opened_img.copy()
    if type(watermark) is str:
        txt = Image.new(mode="RGBA", size=base.size, color=(255, 255, 255, 0))
        wm_font = ImageFont.truetype(wm_text_font_symbol, int(wm_text_size))
        draw = ImageDraw.Draw(txt, mode="RGBA")
        draw.text(xy=(wm_x, wm_y), text=watermark, fill=wm_rgb_color + (wm_opacity,), font=wm_font, anchor="mm")
        img_with_draw = Image.alpha_composite(base, txt)
    elif type(watermark) is Image.Image:
        logo_txt = Image.new(mode="RGBA", size=watermark.size, color=(255, 255, 255, wm_opacity))
        fixed_x = (wm_x * 2 - watermark.width) // 2
        fixed_y = (wm_y * 2 - watermark.height) // 2
        base.paste(watermark, (fixed_x, fixed_y), logo_txt)
        img_with_draw = base
    img_to_label = ImageTk.PhotoImage(img_with_draw)
    img_label.config(image=img_to_label)

def add_text_watermark():  # Button
    global watermark
    watermark = wm_text_entry.get()
    wm_text_entry.delete(0, END)
    draw_wm()

def add_logo_watermark():  # Button
    global watermark
    logo_filename = askopenfilename(filetypes=FILE_TYPES)
    if logo_filename:
        watermark = Image.open(logo_filename).convert(mode="RGBA")
        draw_wm()

def change_text_color():  # Button
    global wm_rgb_color
    color = radio_color.get()
    wm_rgb_color = ImageColor.getrgb(color)
    color_display_label.config(bg=color)
    draw_wm()

def change_text_font(event=None):  # Combobox
    global wm_text_font_symbol
    font = text_fonts.get()
    wm_text_font_symbol = fonts_dict[font]
    draw_wm()

def change_text_size():  # Spinbox
    global wm_text_size
    wm_text_size = text_size_box.get()
    draw_wm()

def change_logo_size(arrow):  # Button
    global watermark
    if type(watermark) is Image.Image:
        n = 0
        if arrow == "up":
            if watermark.width < img_width / 2 and watermark.height < img_height / 2:
                n = 10
        elif arrow == "down":
            if watermark.width > 25 and watermark.height > 25:
                n = -10
        watermark = watermark.resize((watermark.width + n, watermark.height + n), Image.LANCZOS)
        draw_wm()

def change_position(arrow):  # Button
    global wm_x, wm_y
    if arrow == "up" and wm_y > 10:
        wm_y -= 10
    elif arrow == "down" and wm_y < img_height - 10:
        wm_y += 10
    elif arrow == "left" and wm_x > 10:
        wm_x -= 10
    elif arrow == "right" and wm_x < img_width - 10:
        wm_x += 10
    elif arrow == "center":
        wm_x, wm_y = img_width // 2, img_height // 2
    draw_wm()

def change_opacity(event=None):  # Scale
    global wm_opacity
    wm_opacity = opacity_scale.get()
    draw_wm()

def save_file(event=None):  # filedialog
    if img_with_draw:
        file_path = asksaveasfilename(initialfile="untitled", defaultextension=".png", filetypes=FILE_TYPES[1:])
        if file_path:
            if file_path[-4:] == ".jpg":
                img_jpeg = img_with_draw.convert("RGB")
                img_jpeg.save(file_path)
            else:
                img_with_draw.save(file_path)

def create_buttons(dictionary, frame, fun):  # Create Logo Size and Position Buttons
    for key, value in dictionary.items():
        b = Button(frame, text=value[0], bg="white", command=lambda direction=key: fun(direction))
        b.grid(column=value[1], row=value[2], pady=5)

# Window + Menubar Widget
window = Tk()
window.title("Image Watermarking App")
menubar = Menu(window)
menu_file = Menu(menubar, tearoff=False)
menubar.add_cascade(menu=menu_file, label="File")
menu_file.add_command(label="📂 Open", accelerator="Ctrl+N", activebackground="#6499E9", command=open_file)
menu_file.add_command(label="💾 Save As", accelerator="Ctrl+S", activebackground="#6499E9", state="disabled", command=save_file)
window.bind("<Control-n>", open_file)  # ADD "event=None" to func
window.bind("<Control-s>", save_file)  # ADD "event=None" to func
menu_file.add_separator()
menu_file.add_command(label="Exit", activebackground="gray", command=window.quit)
window.config(menu=menubar, bg=BLUE, padx=20, pady=20)

# Frame Widget
wm_input_frame = Frame(bg=BLUE)
wm_input_frame.grid(column=0, row=6, pady=20, sticky="w")
text_color_frame = Frame(bg=BLUE)
text_color_frame.grid(column=3, row=0, padx=10)
text_font_frame = Frame(bg=BLUE)
text_font_frame.grid(column=3, row=1)
text_size_frame = Frame(bg=BLUE)
text_size_frame.grid(column=3, row=2)
logo_size_frame = Frame(bg=BLUE)
logo_size_frame.grid(column=3, row=3)
position_frame = Frame(bg=BLUE)
position_frame.grid(column=3, row=4)
opacity_frame = Frame(bg=BLUE)
opacity_frame.grid(column=3, row=5)

# Image Label Widget
start_img = ImageTk.PhotoImage(opened_img)
img_label = Label(width=800, height=600, image=start_img, bg="lightgrey", highlightthickness=0)
img_label.grid(column=0, row=0, rowspan=6)

# WM Text Input Widgets
wm_text_label = Label(wm_input_frame, text="Watermark Text:", font=FONT, fg="white", bg=BLUE)
wm_text_label.grid(column=0, row=0)
wm_text_entry = Entry(wm_input_frame, width=50, font=FONT)
wm_text_entry.focus()
wm_text_entry.grid(column=1, row=0, padx=5)
add_text_button = Button(wm_input_frame, text="Add Text", font=("calibri", 10, "normal"), width=8, bg="white", command=add_text_watermark, state="disabled")
add_text_button.grid(column=2, row=0, padx=10)
or_label = Label(wm_input_frame, text="Or", font=("calibri", 12, "normal"), fg="white", bg=BLUE)
or_label.grid(column=3, row=0)
add_logo_button = Button(wm_input_frame, text="Add Logo", font=("calibri", 10, "normal"), width=8, bg="white", command=add_logo_watermark, state="disabled")
add_logo_button.grid(column=4, row=0, padx=10, sticky="w")

# WM Color Buttons Widget
text_color_label = Label(text_color_frame, text="Watermark Text Color:", font=FONT, fg="white", bg=BLUE)
text_color_label.grid(column=0, row=0, columnspan=3, padx=10)
wm_text_colors = ["red", "blue", "yellow", "purple", "green", "orange", "grey", "white", "black"]
radio_color = StringVar()
for i in range(len(wm_text_colors)):
    wm_color = wm_text_colors[i]
    radio_color_button = Radiobutton(text_color_frame, text=wm_color.title(), value=wm_color, variable=radio_color, fg="white", bg=BLUE, command=change_text_color)
    radio_color_button.grid(column=i % 3, row=i // 3 + 1, sticky="w")
color_display_label = Label(text_color_frame, width=2, bg="white")
color_display_label.grid(column=1, row=4)

# WM Text Font Combobox Widget
text_font_label = Label(text_font_frame, text="Watermark Text Font:", font=FONT, fg="white", bg=BLUE)
text_font_label.grid(column=0, row=0)
wm_text_fonts_name = [key for (key, value) in fonts_dict.items()]
text_fonts = StringVar()
text_fonts.set("Arial")
font_combobox = ttk.Combobox(text_font_frame, values=wm_text_fonts_name, textvariable=text_fonts, width=22, state="readonly")
font_combobox.bind("<<ComboboxSelected>>", change_text_font)
font_combobox.grid(column=0, row=1)

# WM Text Size Spinbox Widget
text_size_label = Label(text_size_frame, text="Watermark Text Size:", font=FONT, fg="white", bg=BLUE)
text_size_label.grid(column=0, row=0)
t_var = StringVar()
t_var.set("30")
text_size_box = Spinbox(text_size_frame, from_=12, to=90, width=3, bd=3, textvariable=t_var, command=change_text_size)
text_size_box.grid(column=0, row=1)

# WM Logo Size Buttons Widget
logo_size_label = Label(logo_size_frame, text="Watermark Logo Size:", font=FONT, fg="white", bg=BLUE)
logo_size_label.grid(column=0, row=0, columnspan=4)
wm_logo_size_dict = {"up": ["➕", 2, 1], "down": ["➖", 1, 1]}
create_buttons(wm_logo_size_dict, logo_size_frame, change_logo_size)

# WM Position Buttons Widget
position_label = Label(position_frame, text="Watermark Position:", font=FONT, fg="white", bg=BLUE)
position_label.grid(column=0, row=0, columnspan=5)
wm_positions_dict = {"up": ["⏫", 2, 1], "down": ["⏬", 2, 3], "left": ["⏪", 1, 2], "right": ["⏩", 3, 2], "center": ["⏹", 2, 2]}
create_buttons(wm_positions_dict, position_frame, change_position)

# WM Opacity Scale Widget
opacity_label = Label(opacity_frame, text="Watermark Opacity:", font=FONT, fg="white", bg=BLUE)
opacity_label.grid(column=0, row=0)
o_var = IntVar()
o_var.set(255)
opacity_scale = Scale(opacity_frame, from_=0, to=255, orient="horizontal", fg="white", bg=BLUE,
                      highlightthickness=0, variable=o_var, state="disabled", command=change_opacity)
opacity_scale.grid(column=0, row=1)

window.mainloop()
