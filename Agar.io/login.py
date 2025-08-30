import customtkinter
from PIL import Image

screen = customtkinter.CTk()

screen.geometry('700x500')
screen.resizable(False, False)

imgs = []
my_img_n = 2
for n in range(1, 6):
    imgs.append(f'awatars/{n}.png')


def l():
    global my_img_n
    my_img_n -= 1
    if my_img_n == -1: my_img_n = 4
    a = my_img_n+1
    if a == 5: a = 0
    img_l.configure(image=customtkinter.CTkImage(Image.open(imgs[my_img_n]), size=(300, 300)))
    bl.configure(image=customtkinter.CTkImage(Image.open(imgs[my_img_n-1]), size=(100, 100)))
    br.configure(image=customtkinter.CTkImage(Image.open(imgs[a]), size=(100, 100)))


def r():
    global my_img_n
    my_img_n += 1
    if my_img_n == 5: my_img_n = 0
    a = my_img_n+1
    if a == 5: a = 0
    img_l.configure(image=customtkinter.CTkImage(Image.open(imgs[my_img_n]), size=(300, 300)))
    bl.configure(image=customtkinter.CTkImage(Image.open(imgs[my_img_n-1]), size=(100, 100)))
    br.configure(image=customtkinter.CTkImage(Image.open(imgs[a]), size=(100, 100)))

def ywity():
    global username_end, my_img_n_end
    username_end = username.get()
    my_img_n_end = my_img_n+1
    screen.destroy()


title = customtkinter.CTkLabel(screen, text='Agar.io', font=('Comic Sans MS', 30, 'bold'))
title.pack()
bl = customtkinter.CTkButton(screen, text='', width=100, height=100, command=l, image=customtkinter.CTkImage(Image.open(imgs[my_img_n-1]), size=(100, 100)), fg_color='#EBEBEB', hover_color='#DDDDDD')
bl.pack(side='left', padx=(50, 0))
br = customtkinter.CTkButton(screen, text='', width=100, height=100, command=r, image=customtkinter.CTkImage(Image.open(imgs[my_img_n+1]), size=(100, 100)), fg_color='#EBEBEB', hover_color='#DDDDDD')
br.pack(side='right', padx=(0, 50))
img_l = customtkinter.CTkLabel(screen, image=customtkinter.CTkImage(Image.open(imgs[my_img_n]), size=(300, 300)), text='')
img_l.pack(pady=(30, 10))
username = customtkinter.CTkEntry(screen, placeholder_text='username', height=50, width=300, font=('Comic Sans MS', 30))
username.pack()
ywity_baton = customtkinter.CTkButton(screen, text='увійти', font=('Arial', 30, 'bold'), command=ywity)
ywity_baton.pack(pady=5)


screen.mainloop()

print(username_end)
print(my_img_n_end)
