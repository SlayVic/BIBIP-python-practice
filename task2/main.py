import tkinter as tk
from calculator import calculate


class Application(tk.Frame):
    height = 23  # * height of textbox in characters
    width = 42  # * width of textbox in characters

    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        # * event on changing size to chage output box size
        self.master.bind('<Configure>', self.set_sizes)
        self.input = tk.Text(self.master)  # * create textBox
        # * create output box on right side
        self.output = tk.Message(self.master)
        self.configure_widgets()  # * configure widgets

    def configure_widgets(self):
        self.input.pack(side=tk.LEFT)  # * pack on the left side
        self.input['height'] = self.height  # * set sizes
        self.input['width'] = self.width    # * set sizes
        self.master.update()  # * update window
        self.input['font'] = ("Arial", 14)  # * set font
        self.input.bind('<Key>', self.calculate)  # * make event on key press

        # * pack output widget next to input textbox
        self.output.pack(side=tk.LEFT)
        self.output['font'] = ("Arial", 14)  # * set font
        self.set_sizes()  # * set output sizes

    def set_sizes(self, *tmp):
        self.master.update()
        # * output box fill extra space next to text box
        self.output['width'] = self.master.winfo_width()-10 - \
            self.input.winfo_width()

    # * get answers
    def calculate(self, *tmp):
        text = self.input.get("1.0", tk.END)[:-1]  # * get text without \n
        # * add pressed key character 'couse tkinter suck.
        if tmp[0].char:
            text += tmp[0].char

        height = self.height-1  # * counter of how much lines need
        lines = text.split('\n')
        end_text = ''

        # * calculate each line
        for line in lines:
            if not line.startswith('bin'):  # * for binary conversion
                # * if not bin
                end_text += str(calculate(line))+'\n'
            else:  # * bin
                try:
                    # * send line without bin and remove 0b from bin() return
                    end_text += bin(calculate(line[3:]))[2:]+'\n'
                except:  # * if cant get bin, like in float numbers
                    end_text += "Cant\n"
            height -= 1  # * -1 void line
        end_text += '\n'*height  # * add void lines to align widget right
        self.output['text'] = end_text  # * change output widget text


# * make window
root = tk.Tk()
root.geometry('597x507')  # * size
root.minsize(597, 507)  # * min size
root.resizable(True, False)  # * resize lock
root.title('Shashkov inline calculator')  # * title
app = Application(master=root)  # * start class
app.mainloop()  # * start program work
