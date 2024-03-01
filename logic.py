import time
import random
import copy
from tkinter import *
from tkinter import ttk

start_time = None #Variable para el reloj
tiempo_transcurrido_proceso = 0 #Variable para el tiempo transcurrido
clock_running = True #Variable para validar si el reloj esta corriendo
lotes = [] #Array de lotes
lotes_terminados = [] #Array de lotes terminados
num_lote = 1 #Variable para el número de lote para los procesos terminados
end_lote = False
cont_procesos = 0 #Variable para contar los procesos terminados



#Función que actualiza el reloj
def update_clock(relojGlobal_label, root): 
    global start_time
    if start_time is None:
        start_time = time.time()
    if clock_running:
        elapsed_time = time.time() - start_time
        relojGlobal_label.config(text=f"Reloj: {int(elapsed_time)} segundos")
        root.after(1000, update_clock, relojGlobal_label, root)  # Actualiza el reloj cada 1000 milisegundos

#Funcion para detener el reloj
def stop_clock():
    global clock_running
    clock_running = False

#Funcion que retorna un numero aleatorio para el tiempo maximo estimado de un proceso
def getTiempoMaxEstimado():
    return random.randint(6, 12)

#Funcion para generar una operacion aleatoria
def getOperacion():
    operadores = ['+','-','*','/']
    operador = random.choice(operadores)
    datos = (random.randint(0,10), random.randint(0,10))
    while operador == '/' and datos[1] == 0:
        datos = (random.randint(0,10), random.randint(0,10))    
    operacion = f"{str(datos[0])} {operador} {str(datos[1])}"
    return operacion



#Funcion para generar lotes de procesos con datos aleatorios
def crear_lotes(n):
    nombre_programadores = ['Alan', 'Juan', 'Jenny', 'Luis', 'Maria', 'Pedro', 'Sofia', 'Tom', 'Valeria', 'Ximena']
    num_programa = 1
    global lotes
    lote = []
    
    for i in range(n):
        tiempo_maximo = getTiempoMaxEstimado()
        proceso = {
            'nombre': random.choice(nombre_programadores),
            'operacion': getOperacion(),
            'tiempo_maximo': tiempo_maximo,
            'tiempo_restante': tiempo_maximo,
            'numero_programa': num_programa,
            'interrumpido': False,
            'error': False
        }
        
        lote.append(proceso)
        num_programa += 1
        
        if len(lote) == 5:
            lotes.append(lote)
            
            lote = []
    if lote:
        lotes.append(lote)





#Funcion para escribir lotes a un archivo
def lotes_a_txt():
    global lotes
    if lotes != []:
        with open('datos.txt', 'w') as file:
            for i, lote in enumerate(lotes, start=1):
                file.write(f'Lote {i}:\n')
                file.write('\n')
                for proceso in lote:
                    file.write(f"{proceso['numero_programa']}. {proceso['nombre']}\n")
                    file.write(f"{proceso['operacion']}\n")
                    file.write(f"TME: {proceso['tiempo_maximo']}\n")
                    file.write('\n')
                    file.write('\n')
                file.write('\n')

#Funcion para escribir resultados a un archivo
def resultados_a_txt():
    global lotes_terminados 
    with open('Resultados.txt', 'w') as file:            
        for proceso in lotes_terminados: #Muestra los procesos terminados
            if type(proceso) == str:
                file.write(f"{proceso}\n\n")
            else:
                if proceso['error']:
                    file.write(f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\n\n")
                else:
                    resultado = round(eval(proceso['operacion']), 4)
                    file.write(f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']} = {resultado}\n\n")


def en_espera(lotes, procesosEnEspera_text):
    global end_lote
    lote_actual = lotes[0]
    if len(lote_actual) == 1:  # Si solo queda un proceso en el lote actual
        end_lote = True
        if lotes[1:]:
            lote_siguiente = lotes.pop(1)  # Toma el siguiente lote
            lote_actual.extend(lote_siguiente)
            
    procesosEnEspera_text.delete('1.0', END)  
    for proceso in lote_actual[1:]:
        if proceso['interrumpido']:  #Si el proceso fue interrumpido
            procesosEnEspera_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\nTME: {proceso['tiempo_maximo']}\nTiempo restante: {round(proceso['tiempo_restante'])}\n\n")
        else:
            procesosEnEspera_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\nTME: {proceso['tiempo_maximo']}\n\n")

def en_ejecucion(lotes, ejecucion_text, tiempo_inicio_proceso):
    global tiempo_transcurrido_proceso
    
    lote_actual = lotes[0]  # Toma el primer lote
    procesoEnEjecucion = lote_actual[0]  # Toma el primer proceso en espera
    
    if tiempo_inicio_proceso is None:  # Si es la primera vez que se llama a la función para este proceso
        tiempo_inicio_proceso = time.time() - start_time
        tiempo_transcurrido_proceso = 0
        
    tiempo_transcurrido_proceso += 1
    tiempo_transcurrido = tiempo_transcurrido_proceso
    
    if procesoEnEjecucion['error']:  # If the process has an error
        tiempo_restante = 0
    elif procesoEnEjecucion['interrumpido']:  # If the process was interrupted
        tiempo_restante = procesoEnEjecucion['tiempo_restante'] - tiempo_transcurrido
    else:
        tiempo_restante = procesoEnEjecucion['tiempo_maximo'] - tiempo_transcurrido
    
    ejecucion_text.delete('1.0', END) 
    
    if lote_actual: #Muestra el proceso en ejecución
        if procesoEnEjecucion['interrumpido']:
            ejecucion_text.insert(END, f"{procesoEnEjecucion['numero_programa']}. {procesoEnEjecucion['nombre']}\n{procesoEnEjecucion['operacion']}\nTiempo ejecutado:{procesoEnEjecucion['tiempo_maximo'] - procesoEnEjecucion['tiempo_restante']}\nTME: {round(tiempo_restante) if tiempo_restante > 0 else 0}")
        else:
            ejecucion_text.insert(END, f"{procesoEnEjecucion['numero_programa']}. {procesoEnEjecucion['nombre']}\n{procesoEnEjecucion['operacion']}\nTME: {round(tiempo_restante) if tiempo_restante > 0 else 0}")
    return tiempo_restante, tiempo_inicio_proceso


def terminados(lotes, terminados_text, procesos_terminados, tiempo_restante, tiempo_inicio_proceso, ejecucion_text, obtenerResultadosBtn):
    lote_actual = lotes[0]
    global num_lote, cont_procesos, lotes_terminados, end_lote
    
    if tiempo_restante <= 0:  #? cambiar el tiempo a 0
        if len(procesos_terminados) == 0 or cont_procesos % 5 == 0:  # Si hemos terminado 5 procesos
            procesos_terminados.append(f"Lote {num_lote}:")  # Añadimos el número de lote
            num_lote += 1
        procesos_terminados.append(lote_actual.pop(0))  # Elimina el proceso de la lista de procesos en espera y lo añade a la lista de procesos terminados
        end_lote = False
        cont_procesos += 1
        tiempo_inicio_proceso = None  # Resetea el tiempo de inicio para el próximo proceso
        if not lote_actual:  # Si el lote actual está vacío
            lotes.pop(0)  # Elimina el lote de la lista de lotes
            ejecucion_text.delete('1.0', END)
            
    terminados_text.delete('1.0', END)
    
    for proceso in procesos_terminados: #Muestra los procesos terminados
        if type(proceso) == str:
            terminados_text.insert(END, f"{proceso}\n\n")
        else:
            if proceso['error']:
                terminados_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\n\n")
            else:
                resultado = round(eval(proceso['operacion']), 4)
                terminados_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']} = {resultado}\n\n")
    
    # Si todos los lotes están vacíos, habilita el botón obtenerResultadosBtn
    if not lotes:
        lotes_terminados = copy.deepcopy(procesos_terminados)
        obtenerResultadosBtn.config(state='normal')
        stop_clock() #Detiene el reloj si no hay más procesos
    
    return tiempo_inicio_proceso


def ejecutar_proceso(lotes, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text, terminados_text, obtenerResultadosBtn, procesos_terminados=[], tiempo_inicio_proceso=None):
    if lotes:  
        #Funcion para mostrar el proceso en ejecución
        tiempo_restante, tiempo_inicio_proceso = en_ejecucion(lotes, ejecucion_text, tiempo_inicio_proceso)
        en_espera(lotes, procesosEnEspera_text) #Funcion para mostrar los procesos en espera
        #Funcion para mostrar los procesos terminados
        tiempo_inicio_proceso = terminados(lotes, terminados_text, procesos_terminados, tiempo_restante, tiempo_inicio_proceso, ejecucion_text, obtenerResultadosBtn)
        cantidad_lotes = max(0, len(lotes) - 1) #Si no hay lotes, se muestra 0
        # Actualiza el número de lotes pendientes
        noLotesPendientes_label.config(text=f"# De lotes pendientes: {cantidad_lotes}")
        # Llama a la función de nuevo después de 1 segundo
        root.after(1000, ejecutar_proceso, lotes, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text, terminados_text, obtenerResultadosBtn, procesos_terminados, tiempo_inicio_proceso)


#Funcion para generar procesos y ejecutarlos
def generar_procesos(noProcesos_entry, ejecucion_text, noLotesPendientes_label, root, procesosEnEspera_text, terminados_text, obtenerResultadosBtn, relojGlobal_label):
    global lotes
    n = int(noProcesos_entry.get())
    crear_lotes(n)
    lotes_a_txt()
    update_clock(relojGlobal_label, root)  # Inicia el reloj 
    ejecutar_proceso(lotes, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text, terminados_text, obtenerResultadosBtn)  # Inicia el "bucle"

# Función para interrumpir el proceso actual
def interrumpir_proceso():
    global tiempo_transcurrido_proceso, end_lote
    if lotes:  # Si hay lotes
        lote_actual = lotes[0]  # Toma el primer lote
        if lote_actual and end_lote == False:  # Si hay procesos en el lote
            proceso = lote_actual.pop(0)  # Toma y elimina el primer proceso
            proceso['tiempo_restante'] -= tiempo_transcurrido_proceso  # Actualiza el tiempo restante
            proceso['interrumpido'] = True  # Marca el proceso como interrumpido
            lote_actual.append(proceso)  # Mueve el proceso al final de la cola de espera
            tiempo_transcurrido_proceso = 0  # Resetea el tiempo transcurrido

# Función para terminar el proceso actual
def terminar_proceso():
    global tiempo_transcurrido_proceso
    if lotes:  # Si hay lotes
        lote_actual = lotes[0]  # Toma el primer lote
        if lote_actual:  # Si hay procesos en el lote
            proceso = lote_actual[0]  # Toma el primer proceso
            proceso['error'] = True  # Marca el proceso como interrumpido
            proceso['operacion'] += ' = ERROR'  # Asigna ERROR a la operación
            tiempo_transcurrido_proceso = 0  # Resetea el tiempo transcurrido


