from calculadora import Calculadora

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:

    transport = TSocket.TSocket("localhost", 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = Calculadora.Client(protocol)

    transport.open()

    # TIPOS DE OPERACIONES ------------------------------------------------------

    operaciones_binarias_int = [10, 11]
    operaciones_binarias = [1, 2, 3, 4]
    operaciones_unarias = [5, 6, 7, 8, 9]
    operaciones_tres_int = [12, 13]
    operaciones_vectores = [14,15,16]

    operaciones = {
        1: "suma",
        2: "resta",
        3: "multiplicacion",
        4: "division",
        5: "seno",
        6: "coseno",
        7: "tangente",
        8: "convGradosRadianes",
        9: "convRadianesGrados",
        10: "algEuclides",
        11: "algExtEuclides",
        12: "congLineal",
        13: "ecuDiofantica",
        14: "sumaVectores",
        15: "productoEscalar",
        16: "productoCruz"
    }

    # PING Y MOSTRAMOS TIPO DE OPERACIONES ------------------------------------------------------

    print("Hacemos ping al server...")
    client.ping()

    print("Hacemos ping al server algebraico...")
    client.pingAlgebraica()

    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    print("5. Seno (grad)")
    print("6. Coseno (grad)")
    print("7. Tangente (grad)")
    print("8. Conversión Grados-Radianes")
    print("9. Conversión Radianes-Grados")
    print("10. Algoritmo de Euclides (a, b)")
    print("11. Algoritmo Extendido de Euclides (a, b)")
    print("12. Congruencia Lineal (a*x cong b (mod m)")
    print("13. Ecuación diofántica ( a*x + b*y = c)")
    print("14. Suma de los vectores (v1 + v2)")
    print("15. Producto escalar de los vectores (v1 . v2)")
    print("16. Producto cruz de los vectores (v1 x v2)")

    # RECOGER OPERACIONES Y OPERANDOS ---------------------------------------------

    operacion = None

    while operacion not in operaciones:
        try:
            print("Introduce una de las operaciones presentadas:")
            operacion = int(input("Operación: "))
        except ValueError:
            print("Se espera una de las operaciones de muestra.")

    while True:
        if operacion in operaciones_binarias:
            try:
                num1 = float(input("Primer número: "))
                num2 = float(input("Segundo número: "))
                break
            except ValueError:
                print("Se espera un número válido")
        elif operacion in operaciones_binarias_int:
            try:
                num1 = int(input("Primer número: "))
                num2 = int(input("Segundo número: "))
                break
            except ValueError:
                print("Se espera un número válido, es decir, un entero")
        elif operacion in operaciones_unarias:
            try:
                num1 = float(input("Número: "))
                break
            except ValueError:
                print("Se espera un número válido")
        elif operacion in operaciones_tres_int:
            try:
                num1 = int(input("Primer número: "))
                num2 = int(input("Segundo número: "))
                num3 = int(input("Tercer número:  "))
                break
            except ValueError:
                print("Se espera un número válido, es decir, un entero")
        elif operacion in operaciones_vectores:
            try:
                print ("Introduce los vectores en formato de lista [x,y,z]")
                v1 = input("Primer vector: ")
                v2 = input("Segundo vector: ")
                num1 = list(map(float, v1.strip('[]').split(',')))
                num2 = list(map(float, v2.strip('[]').split(',')))

                break
            except ValueError:
                print("Se esperan vectores válidos con el formato requerido")

    # LLAMADA A PROCEDIMIENTOS REMOTOS SEGÚN OPERACIÓN---------------------------------------------

    if operacion in operaciones_binarias or operacion in operaciones_binarias_int or operacion in operaciones_vectores:
        resultado = getattr(client, operaciones[operacion])(num1, num2)
        if resultado.errnum == 0:
            print(resultado.msg)
        else:
            print(f"Ocurrió un error con código {resultado.errnum}, que refiere al problema: {resultado.msg}")

    elif operacion in operaciones_unarias:
        resultado = getattr(client, operaciones[operacion])(num1)
        if resultado.errnum == 0:
            print(resultado.msg)
        else:
            print(f"Ocurrió un error con código {resultado.errnum}, que refiere al problema: {resultado.msg}")

    elif operacion in operaciones_tres_int:
        resultado = getattr(client, operaciones[operacion])(num1, num2, num3)
        if resultado.errnum == 0:
            print(resultado.msg)
        else:
            print(f"Ocurrió un error con código {resultado.errnum}, que refiere al problema: {resultado.msg}")

except TTransport.TTransportException as ex:
    print(f"Error de transporte: {ex}")
    # Manejo de la excepción de transporte, por ejemplo, la caída del servidor

except TBinaryProtocol.TProtocolException as ex:
    print(f"Error de protocolo: {ex}")
    # Manejo de la excepción de protocolo, por ejemplo, problemas de deserialización

except Exception as ex:
    print(f"Error inesperado: {ex}")

finally:
    # Siempre cerrar la conexión
    if 'transport' in locals():
        transport.close()
