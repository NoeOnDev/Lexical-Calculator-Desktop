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
    messagebox.showerror("Error léxico", f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def analizar(operacion):
    lexer.input(operacion)
    resultado = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        resultado.append(f"{tok.type}('{tok.value}')")
    return ', '.join(resultado)

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



def calcular(operacion):
    try:
        operacion_preprocesada = preprocess_input(operacion)
        resultado = eval(operacion_preprocesada)
        resultado_operacion.set(resultado)
        resultado_lexico.set(analizar(operacion_preprocesada))
    except ZeroDivisionError:
        messagebox.showerror("Error", "División por cero no está permitida.")
    except Exception as e:
        messagebox.showerror("Error", str(e))



def eliminar():
    texto = resultado.get()
    if texto:
        resultado.set(texto[:-1])

def limpiar():
    resultado.set("")
    resultado_operacion.set('')
    resultado_lexico.set('')

def crear_boton(texto, comando):
    return tk.Button(frame_calculadora, text=texto, command=comando, width=5, height=2 , font=('arial', 10, 'bold'))

ventana = tk.Tk()
ventana.title("Calculadora Léxica")

ventana.geometry("800x600+100+100")
ventana.resizable(0, 0)

frame_calculadora = tk.Frame(ventana)
frame_calculadora.pack(expand=True)

resultado = tk.StringVar()
entrada = tk.Entry(frame_calculadora, textvariable=resultado, width=35, font=('arial', 18, 'bold'), state='normal', fg='black')
entrada.grid(row=0, column=0, columnspan=5)

resultado_operacion = tk.StringVar()
entrada_operacion = tk.Entry(frame_calculadora, textvariable=resultado_operacion, width=35, font=('arial', 18, 'bold'), state='readonly', fg='green')
entrada_operacion.grid(row=1, column=0, columnspan=5)

resultado_lexico = tk.StringVar()
entrada_lexico = tk.Entry(frame_calculadora, textvariable=resultado_lexico, width=35, font=('arial', 18, 'bold'), state='readonly', fg='blue')
entrada_lexico.grid(row=2, column=0, columnspan=5)

botones = [
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('+', 3, 3), ('C', 3, 4),
    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3), ('Eliminar', 4, 4),
    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('*', 5, 3),
    ('0', 6, 0), ('.', 6, 1), ('=', 6, 2), ('/', 6, 3), ('(', 5, 4), (')', 6, 4)
]

for (texto, fila, columna) in botones:
    comando = lambda x=texto: resultado.set(resultado.get() + x) if x != '=' else calcular(resultado.get())
    if texto == "Eliminar":
        crear_boton(texto, eliminar).grid(row=fila, column=columna)
    elif texto == "C":
        crear_boton(texto, limpiar).grid(row=fila, column=columna)
    else:
        crear_boton(texto, comando).grid(row=fila, column=columna)


ventana.mainloop()