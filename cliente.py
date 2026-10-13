# Sesion 13 - Cliente gRPC (unario)
# Corre primero el servidor en otra terminal: python servidor.py
import grpc

import saludo_pb2
import saludo_pb2_grpc

canal = grpc.insecure_channel("localhost:50051")
stub = saludo_pb2_grpc.SaludadorStub(canal)   # el "stub" de la sesion 11, ya real

peticion = saludo_pb2.SaludoRequest(nombre="Eduardo Lazo", matricula="20212702")
#respuesta = stub.SaludarUno(peticion)
for respuesta in stub.SaludarVarios(peticion):
    print("Llegio: ", respuesta.mensaje)

print("Fin del stream")
#print(f"Cliente recibio: {respuesta.mensaje}")
