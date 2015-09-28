import Tkinter as tk
import astroph as aph

class astroph_app(tk.Frame):

    def __init__(self,parent):
        tk.Frame.__init__(self, parent, background = "white")
        self.parent = parent
        self.astroph = aph.get_artlist()

        self.initialize()

    def initialize(self):
        self.parent.title("Today's Astro-Ph")

        self.grid()
        
        for k in range(len(self.astroph)):
            self.create_article(k,k*2)


    def create_article(self, i, j):
        title = tk.Label(self, text = self.astroph[i].title)
        title.grid(row = j, columnspan = 2,sticky=tk.W)
        abstract = tk.Label(self, text = self.astroph[i].abstract)
        abstract.grid(row = j + 1, columnspan = 4,sticky=tk.W)
        self.rowconfigure(j+1, pad = 8)

if __name__=='__main__':
    root = tk.Tk()
    root.geometry("400x400+300+300")
    app = astroph_app(root)
    app.mainloop()
