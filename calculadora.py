import tkinter as tk
from tkinter import messagebox
import ply.lex as lex

tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    messagebox.showerror("Lexical Error", f"Illegal character: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def analyze(operation):
    preprocessed_operation = preprocess_input(operation)
    lexer.input(preprocessed_operation)
    result = []
    line = 1
    while True:
        tok = lexer.token()
        if not tok:
            break
        data_type = tok.type.lower()
        if data_type == 'number':
            data_type = 'integer'
        result.append(f"Line {line} - Data type: {data_type}, Value: '{tok.value}', Position: {tok.lexpos}")
    return '\n'.join(result)

def preprocess_input(input_str):
    processed_str = ""
    for i, char in enumerate(input_str):
        processed_str += char
        if char.isdigit() and i + 1 < len(input_str) and input_str[i + 1] == "(":
            processed_str += "*"
        elif char == ")" and i + 1 < len(input_str):
            if input_str[i + 1].isdigit() or input_str[i + 1] == "(":
                processed_str += "*"
    return processed_str


def show_lexical_analysis(lexical_result):
    lexical_window = tk.Tk()
    lexical_window.geometry("500x500")
    lexical_window.title("Lexical Analysis")
    tk.Label(lexical_window, text=lexical_result, font=('Helvetica', 12, 'bold')).pack()
    lexical_window.mainloop()

def calculate(operation):
    try:
        operation = operation.rstrip()
        preprocessed_operation = preprocess_input(operation)
        result = eval(preprocessed_operation)
        operation_result.set(result)
        operation_entry.config(state='normal')
        operation_entry.delete("1.0", tk.END)
        operation_entry.insert(tk.END, str(result))
        operation_entry.config(state='disabled')
        lexical_result = analyze(preprocessed_operation)
        show_lexical_analysis(lexical_result)
    except ZeroDivisionError:
        messagebox.showerror("Error", "Division by zero is not allowed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete():
    text = entry.get("1.0", 'end-2c')
    entry.delete("1.0", tk.END)
    entry.insert(tk.END, text)

def clear():
    entry.delete("1.0", tk.END)
    operation_entry.config(state='normal')
    operation_entry.delete("1.0", tk.END)
    operation_entry.config(state='disabled')

def create_button(text, command):
    return tk.Button(calculator_frame, text=text, command=command, width=10, height=2 , font=('Helvetica', 10, 'bold'), bg='#4CAF50', fg='white')

window = tk.Tk()
window.title("Lexical Calculator")

window.geometry("440x375")
window.resizable(0, 0)

calculator_frame = tk.Frame(window)
calculator_frame.pack(expand=True)

result = tk.StringVar()
entry = tk.Text(calculator_frame, height=2, width=30, font=('Helvetica', 18, 'bold'), state='normal', fg='black')
entry.grid(row=0, column=0, columnspan=7)

operation_result = tk.StringVar()
operation_entry = tk.Text(calculator_frame, height=2, width=30, font=('Helvetica', 18, 'bold'), state='disabled', fg='green')
operation_entry.grid(row=1, column=0, columnspan=7)

buttons = [
    ('C', 2, 0), ('Del', 2, 1), ('(', 2, 2), (')', 2, 3),
    ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('+', 4, 3),
    ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('-', 5, 3),
    ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('*', 6, 3),
    ('0', 7, 0), ('.', 7, 1), ('=', 7, 2), ('/', 7, 3),
]

for (text, row, column) in buttons:
    command = lambda x=text: entry.insert(tk.END, x) if x != '=' else calculate(entry.get("1.0", tk.END).rstrip())
    if text == "Del":
        create_button(text, delete).grid(row=row, column=column)
    elif text == "C":
        create_button(text, clear).grid(row=row, column=column)
    else:
        create_button(text, command).grid(row=row, column=column)

window.mainloop()