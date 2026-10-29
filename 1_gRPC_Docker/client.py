import os
import socket
import time

import grpc

import saludo_pb2
import saludo_pb2_grpc


# Nombre del contenedor servidor dentro de la red de Docker
SERVIDOR = os.environ.get("SERVIDOR", "servidor:50051")
IDIOMAS = ["es", "en", "fr"]


def ciclo():
    canal = grpc.insecure_channel(SERVIDOR)
    stub = saludo_pb2_grpc.SaludoStub(canal)
    nombre = socket.gethostname()  # nombre del contenedor actual

    cnt = 0
    while True:
        # Cada petición usa un idioma distinto, rotando es, en, fr
        idioma = IDIOMAS[cnt % len(IDIOMAS)]

        # wait_for_ready espera a que el servidor esté disponible
        r = stub.Decir(saludo_pb2.Peticion(nombre=f"{nombre} #{cnt}", idioma=idioma), wait_for_ready=True)
        print(f"{cnt}: {r.mensaje}")

        # Cada 5 peticiones, también se despide
        if (cnt + 1) % 5 == 0:
            d = stub.Despedir(saludo_pb2.Peticion(nombre=nombre, idioma=idioma), wait_for_ready=True)
            print(f"   {d.mensaje}")

        cnt += 1
        time.sleep(1)


if __name__ == "__main__":
    ciclo()
