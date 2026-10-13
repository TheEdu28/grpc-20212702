import grpc

import saludo_pb2
import saludo_pb2_grpc

canal = grpc.insecure_channel("localhost:50051")
stub = saludo_pb2_grpc.SaludadorStub(canal)

# 1) Tu matricula valida
r = stub.SaludarUno(saludo_pb2.SaludoRequest(nombre="Eduardo Lazo", matricula="20212702"))
print("1)", r.mensaje)

# 2) Tu matricula con una X al final: el servidor debe rechazarla
try:
    stub.SaludarUno(saludo_pb2.SaludoRequest(nombre="Eduardo Lazo", matricula="20212702X"))
except grpc.RpcError as e:
    print("2) Error:", e.code().name, "-", e.details())

# 3) Streaming con tiempo limite de 2 segundos
try:
    for r in stub.SaludarVarios(saludo_pb2.SaludoRequest(nombre="Eduardo Lazo", matricula="20212702"), timeout=2):
        print("3) Llego:", r.mensaje)
except grpc.RpcError as e:
    print("3) Error:", e.code().name, "-", e.details())