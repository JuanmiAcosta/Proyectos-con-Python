import glob
import sys

from calculadora import Calculadora

import math

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    # ACTÚA EN CIERTOS CASOS COMO CLIENTE TB
    transport2 = TSocket.TSocket("localhost", 9091)
    transport2 = TTransport.TBufferedTransport(transport2)
    protocol2 = TBinaryProtocol.TBinaryProtocol(transport2)

    client = Calculadora.Client(protocol2)

    # ACTUACIÓN COMO SERVIDOR
    handler = CalculadoraHandler(client)
    processor = Calculadora.Processor(handler)
    transport = TSocket.TServerSocket(host="127.0.0.1", port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    transport.open()
    transport2.open()

    print("iniciando servidor...")
    server.serve()
    print("fin")

def noError(result):
    result.errnum=0
    result.msg=""
    result.data=0

def noErrorVector(result):
    result.errnum=0
    result.msg=""
    result.data=[]

class CalculadoraHandler:
    def __init__(self,client):
        self.log = {}
        self.client=client

    def ping(self):
        print("me han hecho ping()")

    def pingAlgebraica(self):
        print("A mi me quedó Álgebra, estate atento...")
        self.client.ping()

    def suma(self, num1, num2):
        print("sumando " + str(num1) + " con " + str(num2))

        result = Calculadora.result()
        noError(result)
        result.data = num1+num2
        result.msg="La suma " + str(num1) + " + " + str(num2) + " es: " + str(result.data)

        return result

    def resta(self, num1, num2):
        print("restando " + str(num1) + " con " + str(num2))

        result = Calculadora.result()
        noError(result)
        result.data = num1 - num2
        result.msg="La resta " + str(num1) + " - " + str(num2) + " es: " + str(result.data)

        return result
    
    def multiplicacion(self, num1, num2):
        print("multiplicando " + str(num1) + " con " + str(num2))

        result = Calculadora.result()
        noError(result)
        result.data = num1 * num2
        result.msg="La multiplicación " + str(num1) + " * " + str(num2) + " es: " + str(result.data)

        return result
    
    def division(self, num1, num2):
        print("dividiendo " + str(num1) + " con " + str(num2))

        result = Calculadora.result()
        noError(result)

        if (num2 == 0):
            result.errnum=1
            result.msg="División entre 0"
        else:
            result.data = num1 / num2
            result.msg="La división " + str(num1) + " / " + str(num2) + " es: " + str(result.data)

        return result
    
    def seno(self, num1):
        print("sacando seno de " + str(num1))

        result = Calculadora.result()
        noError(result)
        result.data = math.sin(math.radians(num1))
        result.msg="El seno de " + str(num1) + " es: " + str(result.data)

        return result

    def coseno(self, num1):
        print("sacando coseno de " + str(num1))

        result = Calculadora.result()
        noError(result)
        result.data = math.cos(math.radians(num1))
        result.msg="El coseno de " + str(num1) + " es: " + str(result.data)

        return result

    def tangente(self, num1):
        print("sacando tangente de " + str(num1))

        result = Calculadora.result()
        noError(result)
        result.data = math.tan(math.radians(num1))
        result.msg="La tangente de " + str(num1) + " es: " + str(result.data)

        return result
    
    def convGradosRadianes(self, num1):
        print("convirtiendo grados a radianes de " + str(num1))

        result = Calculadora.result()
        noError(result)
        result.data = math.radians(num1)
        result.msg="La conversión de " + str(num1) + " grados a radianes es: " + str(result.data)

        return result

    def convRadianesGrados(self, num1):
        print("convirtiendo radianes a grados de " + str(num1))

        result = Calculadora.result()
        noError(result)
        result.data = math.degrees(num1)
        result.msg="La conversión de " + str(num1) + " radianes a grados es: " + str(result.data)

        return result

    def algEuclides(self, num1, num2):
        print("mandando a calcular el algoritmo de euclides de " + str(num1) + " y " +str(num2))

        result = self.client.algEuclides(num1,num2)
        return result

    def algExtEuclides(self, num1, num2):
        print("mandando a calcular el algoritmo extendido de euclides de " + str(num1) + " y " +str(num2))

        result = self.client.algExtEuclides(num1,num2)
        return result

    def congLineal(self, num1, num2, num3):
        print("mandando a calcular congruencia lineal con formato ax cong b (mod m) con a=" + str(num1) + ", b=" +str(num2) + "y m="+str(num3))

        result = self.client.congLineal(num1,num2,num3)
        return result

    def ecuDiofantica(self, num1, num2, num3):
        print("mandando a calcular ecuación diofántica con formato ax + by = c siendo a=" + str(num1) + ", b=" +str(num2) + "y c="+str(num3))

        result = self.client.ecuDiofantica(num1,num2,num3)
        return result
    
    def sumaVectores(self, v1, v2):
        print("mandando a calcular suma de vectores " + str(v1) + " y " + str(v2))

        result = Calculadora.result_vector()
        noErrorVector(result)

        print(type(v1))

        if len(v1) != len(v2):
            result.errnum=1
            result.msg="Los vectores deben tener la misma longitud"
        else:
            result.data = [x + y for x, y in zip(v1, v2)]
            result.msg= "La suma de los vectores " + str(v1) + " y " + str(v2) + " es: " + str(result.data)

        return result

    def productoEscalar(self, v1, v2):
        print("mandando a calcular producto escalar de vectores " + str(v1) + " y " + str(v2))

        result = Calculadora.result()
        noError(result)

        if len(v1) != len(v2):
            result.errnum = 1
            result.msg = "Los vectores deben tener la misma longitud"
        else:
            result.data = sum([x * y for x, y in zip(v1, v2)])
            result.msg = "El producto escalar de los vectores " + str(v1) + " y " + str(v2) + " es: " + str(result.data)

        return result

    def productoCruz(self, v1, v2):
        print("mandando a calcular producto cruz de vectores " + str(v1) + " y " + str(v2))

        result = Calculadora.result_vector()
        noErrorVector(result)

        if len(v1) != 3 or len(v2) != 3:
            result.errnum = 1
            result.msg = "Los vectores deben tener longitud 3"
        else:
            result.data = [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]
            result.msg = "El producto cruz de los vectores " + str(v1) + " y " + str(v2) + " es: " + str(result.data)

        return result

if __name__ == "__main__":
    main()
    
