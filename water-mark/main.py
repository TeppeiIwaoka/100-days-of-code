import PIL
from PIL import ImageTk, ImageDraw, ImageFont
from tkinter import filedialog
from tkinter import *


def add_water_mark_to_img():
    text = water_mark_text.get()
    with PIL.Image.open(file) as image:
        image_size = image.size
        image_width = image_size[0]
        image_height = image_size[1]
        editable_picture = ImageDraw.Draw(image)
        font = ImageFont.truetype("System/Library/Fonts/Supplemental/Arial Unicode.ttf", 100)
        text = f"©{text}"
        text_size = editable_picture.textsize(text, font)
        text_width = text_size[0]
        text_height = text_size[1]
        position = (image_width - text_width, image_height - text_height)
        copyright_text = PIL.Image.new("RGB", (text_width, (text_height)), color="#CCCCCC")
        editable_picture = ImageDraw.Draw(copyright_text)
        editable_picture.text((0,0), text, fill="#ffffff", font=font)
        copyright_text.putalpha(100)
        image.paste(copyright_text, position, copyright_text)
        save_dir = "/Users/iwaokateppei/Desktop"
        filename = filedialog.asksaveasfilename(initialdir=save_dir, filetypes=[('image files', '.png')])
        image.save(filename)




window = Tk()
window.title("Water Mark Maker")
window.config(padx=50, pady=50)
label = Label(text="Please select image you want to Add water mark.", width=40, bg="yellow",
              font=("Arial", 18, "normal"))
label.grid(column=0, row=0, columnspan=3)

canvas = Canvas(width=500, height=500, highlightthickness=0)
file = filedialog.askopenfilename(title="Please select a photo you want to add water mark")

original = PIL.Image.open(file)
original = original.resize((500, 500))
photo = ImageTk.PhotoImage(original)
canvas.create_image(0, 0, image=photo, anchor="nw")
canvas.grid(column=0, row=1, columnspan=3)

water_mark_label = Label(text="Input your water mark text:")
water_mark_label.grid(column=0, row=2)
water_mark_text = Entry(width=20)
water_mark_text.grid(column=1, row=2)
water_mark_text.focus()
water_mark_button = Button(text="Add to Photo", width=14, command=add_water_mark_to_img)
water_mark_button.grid(column=2, row=2)

quit_button = Button(text='Quit', command=window.quit, width=20)
quit_button.grid(column=0, row=3, columnspan=3)
window.mainloop()
