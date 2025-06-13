import tkinter as tk
from tkinter import *
from tkinter import PhotoImage, filedialog, messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import os
import json 
class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MIND DETECTIVE")
        menu_bar = Menu(root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_to_file)  
        file_menu.add_command(label="Load", command=self.load_from_file)  
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu_bar)
        #scrollbar = tk.Scrollbar(self.canvas, orient="vertical")
        #scrollbar.pack(side="right", fill="y")

    
        self.canvas = tk.Canvas(root,width=1250, height=900, bg="black")
        self.canvas.pack()

        self.points = []
        self.kal = "white"
        self.point_counter = 1
        self.image = PhotoImage(file="kke.png")
        self.imga = "kke.png"
        self.pointsx = []
        self.images = []
        self.lines = []
        self.li = []
        self.line_id = None


        self.delete_button = tk.Button(root, text="Delete Line", command=self.delete_line)
        self.delete_button.pack(pady=10)
        self.change = tk.Button(root, text="Transpernt", command=self.colour)
        self.change.pack(side="left", pady=10)
        self.chae = tk.Button(root, text="Disconnect", command=self.dis)
        self.chae.pack(side="left", pady=10)
        self.chae1 = tk.Button(root, text="yellow", command=lambda: self.set_kal("yellow"))
        self.chae1.pack(side="left", pady=10)
        self.chae2 = tk.Button(root, text="black", command=lambda: self.set_kal("Black"))
        self.chae2.pack(side="left", pady=10)
        self.chae3 = tk.Button(root, text="blue", command=lambda: self.set_kal("Blue"))
        self.chae3.pack(side="left", pady=10)
        self.chae3 = tk.Button(root, text="white", command=lambda: self.set_kal("White"))
        self.chae3.pack(side="left", pady=10)


        self.canvas.bind("<Button-1>", self.on_click)

        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Change Photo", command=self.change_photo)
        self.context_menu.add_command(label="Add text", command=self.add_text)
        self.context_menu.add_command(label="SHOW", command=self.show_img)

        #self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-3>", self.on_right_click)

    def set_kal(self, value):
        self.kal = value

    def on_click(self, event):
        k = 0

        point_name = f"Point {self.point_counter}"
        for img in self.images:
   
            distance = ((event.x - img['x']) ** 2 + (event.y - img['y']) ** 2) ** 0.5
 
            if distance <= 50:
                self.points.append((img['x'], img['y']))
                k = 1
                break
        if k == 0:
            self.points.append((event.x, event.y))
            self.pointsx.append((event.x, event.y))

            image_id = self.canvas.create_image(event.x - 10, event.y - 10, image=self.image)
            self.images.append({'id': image_id, 'x': event.x, 'y': event.y, 'image': self.image, 'text': None, 'loc': self.imga})
            k = f"{event.x},{event.y}"


        if len(self.points) == 2:
            self.line_id = self.canvas.create_line(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1], fill=self.kal, width=5)
            self.lines.append({'lin':self.line_id,'col':self.kal,'x1':self.points[0][0],'y1':self.points[0][1],'x2':self.points[1][0],'y2':self.points[1][1]})
            img=self.images[-1]
            if img['line']==None:
             img['line']=self.line_id 
            a, b = self.points[1][0], self.points[1][1]
            self.points.clear() 
            self.points.append((a, b))

    def on_right_click(self, event):
        """Detect right-click on canvas and show context menu."""
        for img in self.images:
            distance = ((event.x - img['x']) ** 2 + (event.y - img['y']) ** 2) ** 0.5
            if distance <= 50:
                self.selected_image_id = img['id']  
                self.context_menu.post(event.x_root, event.y_root)
                break

    def delete_line(self):
        if self.lines or self.images:
            if self.lines:
                line_id = self.lines.pop()
                self.canvas.delete(line_id['lin'])
             image_id=self.images[-1]
            if image_id['line']==None or line_id['lin']==image_id['line']  :
             image_id = self.images.pop()
             self.canvas.delete(image_id['id'])
            self.pointsx.pop()
            self.points.clear()
            if self.pointsx:
                self.points.append((self.pointsx[-1][0], self.pointsx[-1][1]))
            self.line_id = None  

    def colour(self):
        abg = self.canvas.cget("background")
        if abg == "black":
            self.canvas.config(bg="white")
        if abg == "white":
            self.canvas.config(bg="black")

    def dis(self):
        self.points.clear()

    def show_img(self):
        for img in self.images:
            if img['id'] == self.selected_image_id:
                if img['loc']==None:
                       messagebox.showwarning("Trynaa finda a BUG Bitch","https://t.me/XCZGITHUB")
                else:
                       os.system(f'start "" "{img["loc"]}"')
                break

    def change_photo(self):
        """Open file dialog to change the selected image."""
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
        if file_path and self.selected_image_id:
            new_width, new_height = 110, 110
            img = Image.open(file_path)
            img = img.resize((new_width, new_height))
            new_image = ImageTk.PhotoImage(img)
            for img in self.images:
                if img['id'] == self.selected_image_id:
                    img['image'] = new_image
                    img['loc'] = file_path
                    self.canvas.itemconfig(self.selected_image_id, image=new_image)  
                    break

    def add_text(self):
        """Prompt user for text input and add it to the canvas."""
        text = simpledialog.askstring("Input", "Enter text to add:")
        if text:
            for img in self.images:
                if img['id'] == self.selected_image_id:
                    img['image'] = None
                    img['loc'] = None
                    img['text'] = text
                    self.canvas.delete(img['id'])
                    text_id = self.canvas.create_text(img['x'], img['y'], text=text, fill="white", font=("Helvetica", 25, "bold"))
                    img['id'] = text_id  
    def zoom(self,event):
     x = event.x
     y = event.y
     if event.delta > 0:
        factor = 1.1
     elif event.delta < 0:
        factor = 0.9
     self.canvas.scale("all", x, y, factor, factor)

    def save_to_file(self):
        """Save the current state to a .mind file."""
        data = {
        'points': self.pointsx,
        'lines': [{'lin': line['lin'], 'col': line['col'], 'x1': line['x1'], 'y1': line['y1'], 'x2': line['x2'], 'y2': line['y2']} for line in self.lines],
        'images': [{'id': img['id'], 'x': img['x'], 'y': img['y'], 'text': img['text'], 'loc': img['loc']} for img in self.images],
        'background_color': self.canvas.cget("background"),
        'line_color': self.kal
    }
        file_path = filedialog.asksaveasfilename(defaultextension=".mind", filetypes=[("Mind Files", "*.mind"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(data, f)
     
    def load_from_file(self):
     """Load the state from a .mind file."""
     file_path = filedialog.askopenfilename(filetypes=[("Mind Files", "*.mind"), ("All Files", "*.*")])
     if file_path:
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.canvas.config(bg=data['background_color'])  
            self.kal = data['line_color'] 
            self.pointsx = data['points']  
            self.lines = data['lines']  
            self.images = data['images']  
            self.canvas.delete("all")  
          
            for img in self.images:
              
                print(img)
                image_path = img['loc']
                print(image_path)
                if image_path==None:
                   text_id = self.canvas.create_text(img['x'], img['y'], text=img['text'], fill="white", font=("Helvetica", 25, "bold"))
                   img['id'] = text_id
                else:         
                 new_image = Image.open(image_path)
                 new_image = new_image.resize((110, 110)) 
                 img['image'] = ImageTk.PhotoImage(new_image) 
                 image_id = self.canvas.create_image(img['x'] - 10, img['y'] - 10, image=img['image'])
                 img['id'] = image_id 
            # Redraw all lines
            for line in self.lines:
                self.canvas.create_line(line['x1'], line['y1'], line['x2'], line['y2'], fill=line['col'], width=5)

            #for point in self.pointsx:
                #self.canvas.create_image(point[0] - 10, point[1] - 10, image=self.image)    


root = tk.Tk()
app = GraphApp(root)
root.mainloop()
