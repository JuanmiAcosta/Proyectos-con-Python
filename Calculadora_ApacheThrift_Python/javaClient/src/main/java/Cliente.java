
import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;

import calculadora.Calculadora;
import calculadora.result;


public class Cliente {
    public static void main(String[] args) {
        TTransport tTransport = null;
        TBinaryProtocol protocol = null;
        try {

            tTransport  = new TSocket("localhost", 9090);
            protocol = new TBinaryProtocol(tTransport);

            Calculadora.Client client = new Calculadora.Client(protocol);
            tTransport.open();


            // TIPOS DE OPERACIONES ------------------------------------------------------

            int[] operaciones_binarias = {1, 2, 3, 4};
            int[] operaciones_unarias = {5, 6, 7, 8, 9};

            int[] operaciones = new int[operaciones_unarias.length + operaciones_binarias.length];

            System.arraycopy(operaciones_unarias, 0, operaciones, 0, operaciones_unarias.length);
            System.arraycopy(operaciones_binarias, 0, operaciones, operaciones_unarias.length, operaciones_binarias.length);

            String[] operacionesStr = {"suma", "resta", "multiplicacion", "division", "seno", "coseno", "tangente",
                    "convGradosRadianes", "convRadianesGrados"};

            // PING Y MOSTRAMOS TIPO DE OPERACIONES ------------------------------------------------------

            System.out.println("Hacemos ping al server...");
            client.ping();

            System.out.println("Hacemos ping al server algebraico...");
            client.pingAlgebraica();

            for (int i = 0; i < operacionesStr.length; i++) {
                System.out.println((i + 1) + ". " + operacionesStr[i]);
            }

            // RECOGER OPERACIONES Y OPERANDOS ---------------------------------------------

            int operacion = -1;
            java.util.Scanner scanner = new java.util.Scanner(System.in);

            while (!contains(operaciones, operacion)) {
                try {
                    System.out.println("Introduce una de las operaciones presentadas:");
                    operacion = Integer.parseInt(scanner.nextLine().trim());
                } catch (NumberFormatException e) {
                    System.out.println("Se espera una de las operaciones de muestra.");
                }
            }

            double num1 = 0, num2 = 0;

            switch (operacion) {
                case 1:
                case 2:
                case 3:
                case 4:
                    System.out.print("Primer número: ");
                    num1 = Double.parseDouble(scanner.nextLine().trim());
                    System.out.print("Segundo número: ");
                    num2 = Double.parseDouble(scanner.nextLine().trim());
                    break;
                case 5:
                case 6:
                case 7:
                case 8:
                case 9:
                    System.out.print("Número: ");
                    num1 = Double.parseDouble(scanner.nextLine().trim());
                    break;
            }


            // LLAMADA A PROCEDIMIENTOS REMOTOS SEGÚN OPERACIÓN---------------------------------------------

            switch (operacion){
                case 1:
                    result result = client.suma(num1, num2);
                    if (result.errnum == 0)
                        System.out.println(result.msg);
                    else
                        System.out.println("Ocurrió un error con código " + result.errnum + " que refiere al problema: " + result.msg);
                    break;
                case 2:
                    result = client.resta(num1, num2);
                    if (result.errnum == 0)
                        System.out.println(result.msg);
                    else
                        System.out.println("Ocurrió un error con código " + result.errnum + " que refiere al problema: " + result.msg);
                    break;

                case 3:
                    result = client.multiplicacion(num1, num2);
                    if (result.errnum == 0)
                        System.out.println(result.msg);
                    else
                        System.out.println("Ocurrió un error con código " + result.errnum + " que refiere al problema: " + result.msg);
                    break;

                case 4:
                    result = client.division(num1, num2);
                    if (result.errnum == 0)
                        System.out.println(result.msg);
                    else
                        System.out.println("Ocurrió un error con código " + result.errnum + " que refiere al problema: " + result.msg);
                    break;

                case 5:
                    result = client.seno(num1);
                    if (result.errnum == 0)
                        System.out.println(result.msg);
                    else
                        System.out.println("Ocurrió un error con código " + result.errnum + " que refiere al problema: " + result.msg);
                    break;

                case 6:

                    result = client.coseno(num1);
                    if (result.errnum == 0)
                        System.out.println(result.msg);
                    else
                        System.out.println("Ocurrió un error con código " + result.errnum + " que refiere al problema: " + result.msg);
                    break;

                case 7:

                    result = client.tangente(num1);
                    if (result.errnum == 0)
                        System.out.println(result.msg);
                    else
                        System.out.println("Ocurrió un error con código " + result.errnum + " que refiere al problema: " + result.msg);
                    break;

                case 8:

                    result = client.convGradosRadianes(num1);
                    if (result.errnum == 0)
                        System.out.println(result.msg);
                    else
                        System.out.println("Ocurrió un error con código " + result.errnum + " que refiere al problema: " + result.msg);
                    break;

                case 9:
                    
                    result = client.convRadianesGrados(num1);
                    if (result.errnum == 0)
                        System.out.println(result.msg);
                    else
                        System.out.println("Ocurrió un error con código " + result.errnum + " que refiere al problema: " + result.msg);
                    break;
                    

            }

        } catch (TTransportException ex) {
            System.out.println("Error de transporte: " + ex.getMessage());
            // Manejar excepción de transporte, como la caída del servidor

        } catch (TException ex) {
            System.out.println("Error de Thrift: " + ex.getMessage());
            // Manejar excepción de Thrift, que puede ocurrir durante la comunicación con el servidor

        } finally {
            // Cerrar la conexión
            if (tTransport != null) {
                tTransport.close();
            }
        }
    }

    static boolean contains(int[] array, int key) {
        for (int i : array) {
            if (i == key) {
                return true;
            }
        }
        return false;
    }
}