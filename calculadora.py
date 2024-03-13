import tkinter as tk
from tkinter import messagebox

def calcular(operacion):
    try:
        resultado_operacion.set(eval(operacion))
    except ZeroDivisionError:
        messagebox.showerror("Error", "División por cero no está permitida.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def eliminar():
    texto = resultado.get()
    if len(texto)>0:
        resultado.set(texto[:-1])

def limpiar():
    resultado.set("")
    resultado_operacion.set('')

def crear_boton(texto, comando):
    return tk.Button(frame_calculadora, text=texto, command=comando, width=5, height=2)

ventana = tk.Tk()
ventana.title("Calculadora")

ventana.geometry("800x600")
ventana.resizable(0, 0)

frame_calculadora = tk.Frame(ventana)
frame_calculadora.place(relx=0.5, rely=0.5, anchor='center')

resultado = tk.StringVar()
entrada = tk.Entry(frame_calculadora, textvariable=resultado, width=20, font=('arial', 20, 'bold'), state='readonly', fg='black')
entrada.grid(row=0, column=0, columnspan=5)

resultado_operacion = tk.StringVar()
entrada_operacion = tk.Entry(frame_calculadora, textvariable=resultado_operacion, width=20, font=('arial', 20, 'bold'), state='readonly', fg='green')
entrada_operacion.grid(row=1, column=0, columnspan=5)

crear_boton("1", lambda: resultado.set(resultado.get() + '1')).grid(row=2, column=0)
crear_boton("2", lambda: resultado.set(resultado.get() + '2')).grid(row=2, column=1)
crear_boton("3", lambda: resultado.set(resultado.get() + '3')).grid(row=2, column=2)
crear_boton("+", lambda: resultado.set(resultado.get() + '+')).grid(row=2, column=3)
crear_boton("Eliminar", eliminar).grid(row=2, column=4)

crear_boton("4", lambda: resultado.set(resultado.get() + '4')).grid(row=3, column=0)
crear_boton("5", lambda: resultado.set(resultado.get() + '5')).grid(row=3, column=1)
crear_boton("6", lambda: resultado.set(resultado.get() + '6')).grid(row=3, column=2)
crear_boton("-", lambda: resultado.set(resultado.get() + '-')).grid(row=3, column=3)
crear_boton("Limpiar", limpiar).grid(row=3, column=4)

crear_boton("7", lambda: resultado.set(resultado.get() + '7')).grid(row=4, column=0)
crear_boton("8", lambda: resultado.set(resultado.get() + '8')).grid(row=4, column=1)
crear_boton("9", lambda: resultado.set(resultado.get() + '9')).grid(row=4, column=2)
crear_boton("*", lambda: resultado.set(resultado.get() + '*')).grid(row=4, column=3)

crear_boton("0", lambda: resultado.set(resultado.get() + '0')).grid(row=5, column=0)
crear_boton(".", lambda: resultado.set(resultado.get() + '.')).grid(row=5, column=1)
crear_boton("=", lambda: calcular(resultado.get())).grid(row=5, column=2)
crear_boton("/", lambda: resultado.set(resultado.get() + '/')).grid(row=5, column=3)

ventana.mainloop()