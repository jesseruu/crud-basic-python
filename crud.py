import psycopg2 as pg 
from datetime import datetime
import os

conn = pg.connect(database = "postgres", user = "postgres", password = "")
enl = conn.cursor()

pretty_Bar = "================================================"

def center_Titles(self):
    return self.center(80)

def cleanT(operatingSystem):
    if operatingSystem == 'nt':
        return os.system("cls")
    else:
        return os.system("clear")

def create_table():
    sql = '''CREATE TABLE ESTUDIANTES(
        Codigo VARCHAR(15),
        nombre VARCHAR(20),
        Apellido VARCHAR(20),
        Edad INT,
        Programa VARCHAR(20))'''

    try:
        enl.execute(sql)
        enl.execute("ALTER TABLE ESTUDIANTES ADD PRIMARY KEY(codigo)")
        conn.commit()
        print("Tabla estudiantes creada correctamente")
    except:
        conn.rollback()
        print("La tabla estudiantes ya habia sido creada")
        
op = 0

def code_generator(program):
    aux = datetime.now()

    if program == "SISTEMAS":
        code = "55"
    elif program == "MECANICA":
        code = "66"
    elif program == "INDUSTRIAL":
        code = "77"
    elif program == "AMBIENTAL":
        code = "88"

    code = code + aux.strftime("%y%H%d%S")
    return code

def pg_read():

    global sql_select, code_search
    option = input('\t\tT = Todos \n\t\tU= Uno'
                   '\n¿Que registros desea mostrar? [T/u]:')

    if option == 'T' or option =='t':
        sql_select = "SELECT * FROM ESTUDIANTES"
        enl.execute(sql_select)

    elif option == 'U' or option == 'u':
        sql_select = "SELECT * FROM ESTUDIANTES WHERE codigo = %s;"
        code_search = input("Ingrese el codigo del estudiante a consultar:")
        enl.execute(sql_select,(code_search,))


    imprim_regist = enl.fetchall()

    if imprim_regist:
        for i in imprim_regist:
            print(i) 
    if not imprim_regist:
        print("El estudiante no existe")
    
    

def pg_create(name, lastname, age, program):
    sql_insert = '''INSERT INTO ESTUDIANTES (codigo, nombre, apellido, edad, programa)
                    VALUES (%s, %s, %s, %s, %s);'''
    
    codigoG = code_generator(program)

    enl.execute(sql_insert, (codigoG, name,lastname,age,program))
    conn.commit()
    print("\n",center_Titles(pretty_Bar))
    print("\t\t Estudiante registrado")

def pg_update():

    global sql_update, modi

    cod = input("\t\t Digite el codigo del estudiante:")
    print("\n",center_Titles(pretty_Bar))

    sql_select = "SELECT * FROM ESTUDIANTES WHERE codigo =%s"
    enl.execute(sql_select, (cod,))

    exist_or_not = enl.fetchall()

    if exist_or_not:

        option = input('\t\t N = Nombre \n\t\t A = Apellido \n\t\t E = Edad \n\t\t P = Programa'
                '\n\n\t\t Seleccione una opcion a actualizar: [N,A,E,P]: ')
        print("\n",center_Titles(pretty_Bar))            
        
        if option == 'n' or option == 'N':
            sql_update = "UPDATE ESTUDIANTES SET nombre = %s WHERE codigo = %s;"
            modi = input("\t\t Actualice el nombre del estudiante:").capitalize()

        elif option == 'A' or option == 'a':
            sql_update = "UPDATE ESTUDIANTES SET apellido = %s WHERE codigo = %s;"
            modi = input("\t\t Actualice el apellido de estudiante:").capitalize

        elif option == 'E' or option == 'e':
            sql_update = "UPDATE ESTUDIANTES SET edad = %s WHERE codigo = %s;"
            modi = int(input("\t\t Actualice la edad del estudiante:"))

        elif option == 'P' or option == 'p':
            sql_update = "UPDATE ESTUDIANTES SET programa = %s WHERE codigo = %s;"
            modi = input("\t\t Actualice el programa:").upper()

        else:
            print("\t\tOpcion no valida")
            print("\n",center_Titles(pretty_Bar))
            pg_update()

        enl.execute(sql_update, (modi, cod,))
        conn.commit()

    if not exist_or_not:
        print("\t\t El estudiante no existe")
    

def pg_delete():
    sql_select_elim = "DELETE FROM ESTUDIANTES WHERE codigo = %s;"
    select_registro = input("Ingrese el codigo del registro a eliminar:")

    enl.execute(sql_select_elim,(select_registro,))
    
    try:
        enl.fetchone()
        conn.commit()
    except:
        conn.rollback()
        print("El registro no existe")   

while op != 6:

    print("\n",center_Titles(pretty_Bar),"\n")
    title = "CRUD BASICO CON POSTGRES".upper()
    print(center_Titles(title),"\n")
    print("\t\t1. Crear o reestablecer nueva tabla")
    print("\t\t2. Ingresar un nuevo registro")
    print("\t\t3. Mostrar tabla completa o registro unico")
    print("\t\t4. Actualizar un registro de la tabla")
    print("\t\t5. Eliminar un registro de la tabla")
    print("\t\t6. Salir\n")
    print(center_Titles(pretty_Bar),"\n")
    op = int(input("\t\tSeleccione una opcion: "))
    cleanT(os.name)

    if op == 1:
        create_table()

    elif op == 2:

        titleDos = "Ingresar un nuevo registro".upper()
        print("\n",center_Titles(titleDos),"\n")
        name = input("\t\tIngrese el nombre:").capitalize()
        lastname = input("\t\tIngrese el apellido:").capitalize()
        age = int(input("\t\tIngrese la edad:"))
        program = input("\t\tIngrese el programa:").upper()

        cleanT(os.name)
        pg_create(name,lastname,age,program)


    elif op == 3:
        titleTres = "Mostrar tabla completa o registro unico".upper()
        print(center_Titles(titleTres),"\n")
        #code_search = input("Ingrese el codigo del registro a consultar:")
        pg_read()

    elif op == 4:
        titleCua = "Ingresar un nuevo registro".upper()
        print(center_Titles(titleCua),"\n")
        pg_update()

    elif op == 5:
        titleCin = "Ingresar un nuevo registro".upper()
        print(center_Titles(titleCin),"\n")
        pg_delete()

    elif op == 6:
        conn.close()
        print("Cerrando conexion con la base de datos...")

    else:
        title_default = "ERROR"
        print(center_Titles(titleDos),"\n")
        print("Digite una opcion valida")

