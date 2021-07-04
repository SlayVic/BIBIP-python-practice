import tkinter as tk
from calculator import calculate

class Application(tk.Frame):
    height=23
    width=42
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.master.bind('<Configure>',self.set_sizes)
        self.input = tk.Text(self.master)
        self.output = tk.Message(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.input.pack(side=tk.LEFT)
        self.input['height'] = self.height
        self.input['width'] = self.width
        self.master.update()
        self.input['font']=("Arial", 14)
        self.input.bind('<Key>', self.calculate)
        
        self.output.pack(side=tk.LEFT, pady=(0,0))
        self.output['font']=("Arial", 14)
        self.set_sizes()
        
    def set_sizes(self, *tmp):
        self.master.update()
        self.output['width'] = self.master.winfo_width()-10-self.input.winfo_width()
    
    def calculate(self, *tmp):
        self.input.update()
        text=self.input.get("1.0",tk.END)[:-1]
        if tmp[0].char:
            text+=tmp[0].char
        height = self.height
        lines = text.split('\n')
        end_text=''
        for line in lines:
            if line.startswith('bin'):
                try:
                    end_text+=bin(calculate(line[3:]))[2:]+'\n'
                except:
                    end_text+="Cant\n"
            else:
                end_text+=str(calculate(line))+'\n'
            height -= 1
        end_text+='\n'*(height-1)
        self.output['text']=end_text

root = tk.Tk()
root.geometry('597x507')
root.minsize(597, 507)
root.resizable(True, False)
root.title('Shashkov inline calculator')
app = Application(master=root)
app.mainloop()
