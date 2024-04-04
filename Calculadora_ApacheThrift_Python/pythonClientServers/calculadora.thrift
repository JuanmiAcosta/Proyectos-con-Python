namespace java calculadora
namespace py calculadora

struct result {
    1: required double data;
    2: required i16 errnum;
    3: required string msg;
}

struct result2 {
    1: required list<i64> data;
    2: required i16 errnum;
    3: required string msg;
}

struct result_vector {
    1: required list<double> data;
    2: required i16 errnum;
    3: required string msg;
}

service Calculadora{
   void ping(),
   result suma(1:double num1, 2:double num2),
   result resta(1:double num1, 2:double num2),
   result multiplicacion(1:double num1, 2:double num2),
   result division(1:double num1, 2:double num2),
   result seno(1:double num),
   result coseno(1:double num),
   result tangente(1:double num),
   result convGradosRadianes(1:double grado),
   result convRadianesGrados(1:double radianes),
   void pingAlgebraica(),
   result algEuclides(1:i64 num1, 2:i64 num2),
   result2 algExtEuclides(1:i64 num1, 2:i64 num2),
   result2 congLineal(1:i64 num1, 2:i64 num2, 3:i64 num3),
   result2 ecuDiofantica(1:i64 num1, 2:i64 num2, 3:i64 num3),
   result_vector sumaVectores(1: list<double> vec1, 2: list<double> vec2),
   result_vector productoEscalar(1: list<double> vec1, 2: list<double> vec2),
   result_vector productoCruz(1: list<double> vec1, 2: list<double> vec2)
}

service Algebraica{
    void ping(),
    result algEuclides(1:i64 num1, 2:i64 num2),
    result2 algExtEuclides(1:i64 num1, 2:i64 num2),
    result2 congLineal(1:i64 num1, 2:i64 num2, 3:i64 num3),
    result2 ecuDiofantica(1:i64 num1, 2:i64 num2, 3:i64 num3)
}
