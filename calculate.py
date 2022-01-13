import tkinter as tk

window = tk.Tk()
window.title('window')
align_mode = 'nswe'
pad = 5


def define_layout(obj, cols=1, rows=1):
    def method(trg, col, row):
        for c in range(cols):
            trg.columnconfigure(c, weight=1)
        for r in range(rows):
            trg.rowconfigure(r, weight=1)
    if type(obj) == list:
        [method(trg, cols, rows) for trg in obj]
    else:
        trg = obj
        method(trg, cols, rows)


def calculate():
    b_p = float(buy_price.get())
    s_p = float(sell_price.get())
    q = float(quantity.get())
    cost = b_p*q*1.00075
    income = s_p*q*0.99925
    profilt = income-cost
    roi = profilt/cost*100
    cost_label['text'] = f'成本:{cost:0.6f}'
    income_label['text'] = f'收入:{income:0.6f}'
    profilt_label['text'] = f'利潤:{profilt:0.6f}'
    roi_label['text'] = f'報酬率:{roi:0.2f}%'


div_size = 150
img_size = div_size*2
div1 = tk.Frame(window, width=img_size, heigh=img_size, bg='pink')
div2 = tk.Frame(window, width=div_size+50, heigh=div_size+50, bg='orange')
div3 = tk.Frame(window, width=div_size+50, heigh=div_size+50, bg='green')
div1.grid(column=0, row=0, rowspan=2, padx=pad, pady=pad, sticky=align_mode)
div2.grid(column=1, row=0, padx=pad, pady=pad, sticky=align_mode)
div3.grid(column=1, row=1, padx=pad, pady=pad, sticky=align_mode)
define_layout(window, cols=2, rows=2)
define_layout([div1, div2, div3])
label = tk.Label(div1, bg="#ffffff", text="計算器", bd=8,
                 font=("Arial", 12), pady=5, width=25)
label.place(x=45, y=10)
label1 = tk.Label(div1, bg="#ffffff", text="買價:", bd=8,
                  font=("Arial", 12), pady=5)
label1.place(x=40, y=80)
buy_price = tk.Entry(div1, bd=8, width=10, font=("Arial", 12))
buy_price.place(x=150, y=80)
label1 = tk.Label(div1, bg="#ffffff", text="賣價:", bd=8,
                  font=("Arial", 12), pady=5)
label1.place(x=40, y=150)
sell_price = tk.Entry(div1, bd=8, width=10, font=("Arial", 12))
sell_price.place(x=150, y=150)
label1 = tk.Label(div1, bg="#ffffff", text="數量:", bd=8,
                  font=("Arial", 12), pady=5)
label1.place(x=40, y=220)
quantity = tk.Entry(div1, bd=8, width=10, font=("Arial", 12))
quantity.place(x=150, y=220)

summit = tk.Button(div1, bg='red', text='計算', font=(
    'Arial', 12), command=calculate, padx=10, pady=10)
summit.place(x=120, y=300)

label=tk.Label(div2,text='成本及收入', bd=10,
                      font=("Arial", 12), pady=5)
label.place(x=45,y=10)
cost_label = tk.Label(div2, text='成本:', bd=10,
                      font=("Arial", 12), pady=5)
income_label = tk.Label(div2, text='收入:', bd=10,
                        font=("Arial", 12), pady=5)
label=tk.Label(div3,text='利潤及報酬率', bd=10,
                      font=("Arial", 12), pady=5)
label.place(x=45,y=10)
profilt_label = tk.Label(div3, text='利潤:', bd=10,
                         font=("Arial", 12), pady=5)
roi_label = tk.Label(div3, text='報酬率:', bd=10,
                     font=("Arial", 12), pady=5)
cost_label.place(x=40, y=80)
income_label.place(x=40, y=140)
profilt_label.place(x=40, y=80)
roi_label.place(x=40, y=140)
window.mainloop()
