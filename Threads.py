import subprocess
import threading
import queue

def ping_direccion_ip(direccion_ip, resultado_q):
    # Ejecutamos el comando ping para comprobar la conectividad de la dirección IP
    proceso = subprocess.Popen(['ping', '-n', '1', direccion_ip], stdout=subprocess.PIPE)
    salida = proceso.communicate()[0].decode('ISO-8859-1')

    # Mostramos un mensaje con la salida del ping para depuración
    print(f"Salida del ping para {direccion_ip}: {salida}")

    # Añadimos el resultado a la cola
    resultado_q.put((direccion_ip, salida))


def guardar_resultados(resultado_q):
    # Abrimos el archivo en modo de escritura y añadimos la salida del ping
    with open('resultados.txt', 'a') as archivo:
        while True:
            try:
                direccion_ip, salida = resultado_q.get(timeout=1)
                archivo.write(f"Salida del ping a {direccion_ip}:\n{salida}\n")
            except queue.Empty:
                # Salimos del bucle si la cola está vacía y no ha habido actividad durante 1 segundo
                break


if __name__ == '__main__':
    # Creamos la cola para almacenar los resultados de los pings
    resultado_q = queue.Queue()
    
    # Creamos tres hilos que ejecutan la función ping_direccion_ip
    hilo1 = threading.Thread(target=ping_direccion_ip, args=("www.google.com", resultado_q), name="Hilo 1")
    hilo2 = threading.Thread(target=ping_direccion_ip, args=("www.youtube.com", resultado_q), name="Hilo 2")
    hilo3 = threading.Thread(target=ping_direccion_ip, args=("www.facebook.com", resultado_q), name="Hilo 3")

    # Iniciamos los tres hilos
    hilo1.start()
    hilo2.start()
    hilo3.start()
        
    # Esperamos a que los hilos terminen
    hilo1.join()
    hilo2.join()
    hilo3.join()

    # Creamos el proceso para guardar los resultados en un archivo de texto
    proceso = threading.Thread(target=guardar_resultados, args=(resultado_q,))
    proceso.start()
    proceso.join()

