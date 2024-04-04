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
    handler = AlgebraicaHandler()
    processor = Calculadora.Processor(handler)
    transport = TSocket.TServerSocket(host="127.0.0.1", port=9091)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print("iniciando servidor...")
    server.serve()
    print("fin")


def noError(result):
    result.errnum = 0
    result.msg = ""
    result.data = 0


def noError2(result):
    result.errnum = 0
    result.msg = ""
    result.data = []


class AlgebraicaHandler:
    def __init__(self):
        self.log = {}

    def ping(self):
        print("estoy atento...")

    def algEuclides(self, num1, num2):
        print("calculando el algoritmo de euclides de " + str(num1) + " y " + str(num2))
        #ejemplo algEuclides(15,5) -> 5

        result = Calculadora.result()
        noError(result)

        num1_or = num1
        num2_or = num2

        if type(num1) != int or type(num2) != int:
            result.errnum=1
            result.msg="Los datos deben ser enteros para trabajar con esta operación"
        else:
            if num1 < num2:
                num1, num2 = num2, num1  # swap a and b, a=b and b=a
            while num2 != 0:
                num1, num2 = num2, num1 % num2

            result.data = num1
            result.msg = "El MCD(" +str(num1_or)+","+str(num2_or)+") calculado mediante el Algoritmo de Euclides es "+str(result.data)

        return result

    def algExtEuclides(self, num1, num2):
        print("calculando el algoritmo extendido de euclides de " + str(num1) + " y " + str(num2))
        #ejemplo algExteEuclides(196,121) -> 1, -50, 81

        result = Calculadora.result2()
        noError2(result)

        num1_or = num1
        num2_or = num2

        if type(num1) != int or type(num2) != int:
            result.errnum=1
            result.msg="Los datos deben ser enteros para trabajar con esta operación"
        else:
            swap_u_v = False
            if num1 < num2:
                num1, num2 = num2, num1
                swap_u_v = True

            s, old_s = 0, 1
            t, old_t = 1, 0
            r, old_r = num2, num1

            while r > 0:
                quotient = old_r // r
                old_r, r = r, old_r - quotient * r
                old_s, s = s, old_s - quotient * s
                old_t, t = t, old_t - quotient * t

            if swap_u_v:
                old_s, old_t = old_t, old_s
                result.data = [ old_r, old_s, old_t ]
                result.msg = f'El MCD({num1_or},{num2_or}) es igual a {result.data[0]}, además u y v tal que {num1_or}*u+{num2_or}*v=1 son u={result.data[1]}, y v={result.data[2]}'
            else:
                result.data = [ old_r, old_s, old_t ]
                result.msg = f'El MCD({num1_or},{num2_or}) es igual a {result.data[0]}, además u y v tal que {num2_or}*u+{num1_or}*v=1 son u={result.data[1]}, y v={result.data[2]}'

        return result

    def congLineal(self, num1, num2, num3):
        print("calculando congruencia lineal con formato ax cong b (mod m) con a=" + str(num1) + ", b=" +str(num2) + "y m="+str(num3))
        #Ejemplo 54x cong 2 (mod 4) -> 1+2k

        result = Calculadora.result2()
        noError2(result)

        if type(num1) != int or type(num2) != int or type(num3) != int:
            result.errnum=1
            result.msg="Los datos deben ser enteros para trabajar con esta operación"
        else:
            mcd = self.algEuclides(num1, num2)
            mcd = mcd.data

            if num2 % mcd == 0:
                num1 = num1 // mcd
                num2 = num2 // mcd
                num3 = num3 // mcd

                num1 = num1 % num3
                num2 = num2 % num3

                r_s_t = self.algExtEuclides(num1,num3)
                r, s, t = r_s_t.data[0], r_s_t.data[1], r_s_t.data[2]
                x = (num2 * s) % num3

                result.data = [x,num3]
                result.msg= "{El conjunto de todas las soluciones es x = " + str(x) + " + " + str(num3) + "k, con k ∈ Z}\n"

            else:
                result.errnum = 2
                result.msg = f'No es posible solucionar la congruencia ya que {num2}%{mcd} != 0'

        return result

    def ecuDiofantica(self, num1, num2, num3):
        print("calculando ecuación diofántica con formato ax + by = c siendo a=" + str(num1) + ", b=" +str(num2) + "y c="+str(num3))
        #Ejemplo 123x +93y = 6 -> x=25 + 31 k, y= 33+41k

        result = Calculadora.result2()
        noError2(result)

        if type(num1) != int or type(num2) != int or type(num3) != int:
            result.errnum=1
            result.msg="Los datos deben ser enteros para trabajar con esta operación"
        else:
            if (num2 < 0):
                num2 = num2 * -1

            mcd = self.algEuclides(num1,num2)
            mcd = mcd.data
            if num3 % mcd == 0:
                x_m = self.congLineal(num1,num3,num2)
                x, m = x_m.data[0], x_m.data[1]

                aux1 = num1 * x
                aux2 = num1 * m

                aux1 = aux1 - num3

                aux1 = aux1 // num2
                aux2 = aux2 // num2

                y = aux1
                n = aux2

                result.data = [m,n]
                result.msg="{El conjunto de todas las soluciones es (x,y) = (" + str(x) + " + (" + str(m) + ")k, " + str(
                    y) + " + (" + str(n) + ")k), con k ∈ Z}\n"
            else:
                result.errnum=2
                result.msg="La ecuación no tiene solución: " + str(num1) + "x + " + str(num2) + "y = " + str(num3) + "\n"

        return result

if __name__ == "__main__":
    main()
