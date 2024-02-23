from tkinter import *
from tkinter import ttk
from logic import update_clock, generar_procesos, resultados_a_txt

root = Tk()

#----- Frames -----
content = ttk.Frame(root, borderwidth=10, relief='ridge' ,width=200, height=200)
enEsperaFrame = ttk.Frame(content,  width=100, height=100)
ejecucionFrame = ttk.Frame(content,  width=100, height=100)
terminadosFrame = ttk.Frame(content,  width=100, height=100)

#----- Campos y etiquetas -----

#contenido del frame "en espera"
noProcesos_label = ttk.Label(enEsperaFrame, text="# Procesos") #Ingrese el número de procesos
noProcesos_entry = ttk.Entry(enEsperaFrame, width=8)

enEspera_label = ttk.Label(enEsperaFrame, text="EN ESPERA") #Procesos en espera
procesosEnEspera_text = Text(enEsperaFrame, width=20, height=20)

noLotesPendientes_label = ttk.Label(enEsperaFrame, text="# De lotes pendientes") #Número de lotes pendientes
#----------------------------------

#contenido del frame "en ejecución"
ejecucion_label = ttk.Label(ejecucionFrame, text="EN EJECUCIÓN") #Proceso en ejecución
ejecucion_text = Text(ejecucionFrame, width=20, height=10)
#----------------------------------

#contenido del frame "terminados"
relojGlobal_label = ttk.Label(terminadosFrame, text="Reloj Global") #Reloj global

terminados_label = ttk.Label(terminadosFrame, text="TERMINADOS") #Procesos terminados
terminados_text = Text(terminadosFrame, width=20, height=20)
#----------------------------------

#----- Botones ----- 
#Generar procesos y obtener resultados
generarBtn = ttk.Button(enEsperaFrame, command=lambda: generar_procesos(noProcesos_entry, ejecucion_text, noLotesPendientes_label, root, procesosEnEspera_text, terminados_text, obtenerResultadosBtn, relojGlobal_label), text="Generar")
obtenerResultadosBtn = ttk.Button(terminadosFrame, state='disabled', command=resultados_a_txt, text="OBTENER RESULTADOS")

#--- Grid Layout ---
content.grid(column=0, row=0)
enEsperaFrame.grid(column=0, row=0, columnspan=2)
ejecucionFrame.grid(column=2, row=0, columnspan=2, padx=15)
terminadosFrame.grid(column=4, row=0, columnspan=2, padx=10)

#en espera
noProcesos_label.grid(column=0, row=0)
noProcesos_entry.grid(column=1, row=0)
generarBtn.grid(column=2, row=0, padx=10)

enEspera_label.grid(column=0, row=1, columnspan=3, pady=10)
procesosEnEspera_text.grid(column=0, row=2, columnspan=3)

noLotesPendientes_label.grid(column=0, row=3, columnspan=2, pady=10)
#------------------

#en ejecución
ejecucion_label.grid(column=0, row=0, columnspan=2, pady=10)
ejecucion_text.grid(column=0, row=1, columnspan=2)
#------------------

#terminados
relojGlobal_label.grid(column=0, row=0)
terminados_label.grid(column=0, row=1, columnspan=2, pady=10)
terminados_text.grid(column=0, row=2, columnspan=2)
obtenerResultadosBtn.grid(column=0, row=3, columnspan=2, pady=10)

#------------------

#Llama a la función mainloop
root.mainloop()