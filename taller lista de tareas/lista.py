from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

#bd
class AlmacenTareas:
    def __init__(self, nombre_archivo='listaTareas.db'):
        self.conexion = sql.connect(nombre_archivo)
        self.gestor_db = self.conexion.cursor()
        self.gestor_db.execute('CREATE TABLE IF NOT EXISTS LISTA_DE_TAREAS (titulo VARCHAR(100))')

    def insertar_tarea(self, titulo_tarea):
        self.gestor_db.execute('INSERT INTO LISTA_DE_TAREAS (titulo) VALUES (?)', (titulo_tarea,))
        self.conexion.commit()

    def borrar_tarea(self, titulo_tarea):
        self.gestor_db.execute('DELETE FROM LISTA_DE_TAREAS WHERE titulo = ?', (titulo_tarea,))
        self.conexion.commit()

    def obtener_todas(self):
        self.gestor_db.execute('SELECT titulo FROM LISTA_DE_TAREAS')
        return self.gestor_db.fetchall()

    def cerrar(self):
        self.conexion.close()

#lo bonito
class GestorTareasApp:
    def __init__(self, ventana):
        self.basedatos = AlmacenTareas()
        self.lista_tareas = []

        ventana.title("lista de tareas")
        ventana.geometry("665x400+550+250")
        ventana.resizable(0, 0)

        self.panel_principal = Frame(ventana)
        self.panel_principal.pack(side="top", expand=True, fill="both")

        self.crear_componentes()
        self.cargar_tareas_guardadas()
        self.actualizar_listbox()

    def crear_componentes(self):
        Label(
            self.panel_principal,
            text="LISTA DE TAREAS\nescriba la tarea:",
            font=("arial", "14", "bold")
        ).place(x=20, y=30)

        self.entrada_tarea = Entry(
            self.panel_principal,
            font=("Arial", "14"),
            width=42
        )
        self.entrada_tarea.place(x=180, y=30)

        Button(
            self.panel_principal, text="agregar", width=15,
            font=("arial", "14", "bold"),
            command=self.agregar_tarea
        ).place(x=18, y=80)

        Button(
            self.panel_principal, text="eliminar", width=15,
            font=("arial", "14", "bold"),
            command=self.eliminar_tarea
        ).place(x=240, y=80)

        self.listbox_tareas = Listbox(
            self.panel_principal, width=70, height=9,
            font="bold", selectmode='SINGLE'
        )
        self.listbox_tareas.place(x=17, y=140)

        Button(
            self.panel_principal, text="modificar", width=15,
            font=("arial", "14", "bold"),
        ).place(x=460, y=80)

    def agregar_tarea(self):
        texto = self.entrada_tarea.get().strip()
        self.lista_tareas.append(texto)
        self.basedatos.insertar_tarea(texto)
        self.actualizar_listbox()
        self.entrada_tarea.delete(0, 'end')

    def eliminar_tarea(self):
        try:
            seleccionada = self.listbox_tareas.get(self.listbox_tareas.curselection())
            if seleccionada in self.lista_tareas:
                self.lista_tareas.remove(seleccionada)
                self.basedatos.borrar_tarea(seleccionada)
                self.actualizar_listbox()
        except:
            messagebox.showinfo('Error', 'No hay ninguna tarea seleccionada.')

    def actualizar_listbox(self):
        self.listbox_tareas.delete(0, 'end')
        for tarea in self.lista_tareas:
            self.listbox_tareas.insert('end', tarea)

    def cargar_tareas_guardadas(self):
        self.lista_tareas.clear()
        for (titulo,) in self.basedatos.obtener_todas():
            self.lista_tareas.append(titulo)
    
#el main
if __name__ == "__main__":
    ventana_principal = Tk()
    app = GestorTareasApp(ventana_principal)
    ventana_principal.mainloop()
    