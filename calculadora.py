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
    operacion_preprocesada = preprocess_input(operacion)
    lexer.input(operacion_preprocesada)
    resultado = []
    linea = 1
    while True:
        tok = lexer.token()
        if not tok:
            break
        tipo_dato = tok.type.lower()
        if tipo_dato == 'number':
            tipo_dato = 'integer'
        resultado.append(f"Linea {linea} - Data type: {tipo_dato}, Value: '{tok.value}', Position: {tok.lexpos}")
    return '\n'.join(resultado)

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


def mostrar_analisis_lexico(resultado_lexico):
    ventana_lexico = tk.Tk()
    ventana_lexico.geometry("500x500")
    ventana_lexico.title("Análisis Léxico")
    tk.Label(ventana_lexico, text=resultado_lexico, font=('Helvetica', 12, 'bold')).pack()
    ventana_lexico.mainloop()

def calcular(operacion):
    try:
        operacion = operacion.rstrip()
        operacion_preprocesada = preprocess_input(operacion)
        resultado = eval(operacion_preprocesada)
        resultado_operacion.set(resultado)
        entrada_operacion.config(state='normal')
        entrada_operacion.delete("1.0", tk.END)
        entrada_operacion.insert(tk.END, str(resultado))
        entrada_operacion.config(state='disabled')
        resultado_lexico = analizar(operacion_preprocesada)
        mostrar_analisis_lexico(resultado_lexico)
    except ZeroDivisionError:
        messagebox.showerror("Error", "División por cero no está permitida.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def eliminar():
    texto = entrada.get("1.0", 'end-2c')
    entrada.delete("1.0", tk.END)
    entrada.insert(tk.END, texto)

def limpiar():
    entrada.delete("1.0", tk.END)
    entrada_operacion.config(state='normal')
    entrada_operacion.delete("1.0", tk.END)
    entrada_operacion.config(state='disabled')

def crear_boton(texto, comando):
    return tk.Button(frame_calculadora, text=texto, command=comando, width=7, height=2 , font=('Helvetica', 10, 'bold'))

ventana = tk.Tk()
ventana.title("Calculadora Léxica")

ventana.geometry("400x500")
ventana.resizable(0, 0)

frame_calculadora = tk.Frame(ventana)
frame_calculadora.pack(expand=True)

resultado = tk.StringVar()
entrada = tk.Text(frame_calculadora, height=2, width=23, font=('Helvetica', 18, 'bold'), state='normal', fg='black')
entrada.grid(row=0, column=0, columnspan=7)

resultado_operacion = tk.StringVar()
entrada_operacion = tk.Text(frame_calculadora, height=2, width=23, font=('Helvetica', 18, 'bold'), state='disabled', fg='green')
entrada_operacion.grid(row=1, column=0, columnspan=7)

botones = [
    ('C', 2, 0), ('Del', 2, 1), ('(', 2, 2), (')', 2, 3),
    ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('+', 4, 3),
    ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('-', 5, 3),
    ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('*', 6, 3),
    ('0', 7, 0), ('.', 7, 1), ('=', 7, 2), ('/', 7, 3),
]

for (texto, fila, columna) in botones:
    comando = lambda x=texto: entrada.insert(tk.END, x) if x != '=' else calcular(entrada.get("1.0", tk.END).rstrip())
    if texto == "Del":
        crear_boton(texto, eliminar).grid(row=fila, column=columna)
    elif texto == "C":
        crear_boton(texto, limpiar).grid(row=fila, column=columna)
    else:
        crear_boton(texto, comando).grid(row=fila, column=columna)

ventana.mainloop()