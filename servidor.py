# Sesion 13 - Servidor gRPC (unario)
# Antes de correrlo: bash compilar.sh
import time
import grpc
from concurrent import futures

import saludo_pb2        # generado por protoc: los mensajes
import saludo_pb2_grpc   # generado por protoc: la clase base del servicio




class SaludadorServicio(saludo_pb2_grpc.SaludadorServicer):
   def SaludarUno(self, request, context):
         if not request.matricula.isdigit():
             context.abort(grpc.StatusCode.INVALID_ARGUMENT,f"Matricula invalida: {request.matricula}")
         suma = sum(int(d) for d in request.matricula if d.isdigit())
         mensaje = f"Hola, {request.nombre}! Los digitos de tu matricula {request.matricula} suman {suma}."
         return saludo_pb2.SaludoResponse(mensaje=mensaje)
   
   
   def SaludarVarios(self, request, context):
    suma = 0
    digitos = [d for d in request.matricula if d.isdigit()]

    for i, digito in enumerate(digitos, start=1):
        time.sleep(1)
        suma += int(digito)

        yield saludo_pb2.SaludoResponse(
            mensaje=f"Digito {i} de {len(digitos)}: {digito}"
        )

    yield saludo_pb2.SaludoResponse(
        mensaje=f"Listo, {request.nombre}: tus digitos suman {suma}"
    )  
    


servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
saludo_pb2_grpc.add_SaludadorServicer_to_server(SaludadorServicio(), servidor)
servidor.add_insecure_port("[::]:50051")
servidor.start()
print("Servidor gRPC escuchando en el puerto 50051...")
servidor.wait_for_termination()
