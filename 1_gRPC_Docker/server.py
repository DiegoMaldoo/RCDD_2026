import socket
from concurrent import futures

import grpc

import saludo_pb2
import saludo_pb2_grpc

PUERTO = 50051

SALUDOS = {"es": "Hola", "en": "Hello", "fr": "Bonjour"}
DESPEDIDAS = {"es": "Adiós", "en": "Goodbye", "fr": "Au revoir"}


class Saludo(saludo_pb2_grpc.SaludoServicer):
    def Decir(self, request, context):
        print(f"Petición recibida de: {request.nombre}")
        # Si el idioma es desconocido (o viene vacío), se responde en español
        saludo = SALUDOS.get(request.idioma, SALUDOS["es"])
        return saludo_pb2.Respuesta(mensaje=f"{saludo} {request.nombre}, soy {socket.gethostname()}")

    def Despedir(self, request, context):
        print(f"Despedida de: {request.nombre}")
        despedida = DESPEDIDAS.get(request.idioma, DESPEDIDAS["es"])
        return saludo_pb2.Respuesta(mensaje=f"{despedida} {request.nombre}")


def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    saludo_pb2_grpc.add_SaludoServicer_to_server(Saludo(), server)
    # 0.0.0.0 para aceptar conexiones de otros contenedores (localhost no sirve)
    server.add_insecure_port(f"0.0.0.0:{PUERTO}")
    server.start()
    print(f"Servidor gRPC escuchando en el puerto {PUERTO}")
    server.wait_for_termination()


if __name__ == "__main__":
    servir()
