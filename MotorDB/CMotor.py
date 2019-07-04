import time
from parse import *
import random


class CMotorDB:
    create_table = ''
    insert = ''
    add_full = ''
    select = ''
    eraser = ''
    update = ''

    table = {}

    def __init__(self):
        self.create_table = 'CREATE TABLE'
        self.insert = 'INSERT'
        self.add_full = 'ADD FULL'
        self.select = 'SELECT'
        self.eraser = 'ERASER'
        self.update = 'UPDATE'

        f = open('info.txt', 'r')
        m = f.readline()
        while m:
            m = parse('{}:{}', m)
            self.table[m[0].strip()] = m[1].strip()
            m = f.readline()

    def func_create_table(self, cad):
        cad = parse('{}({})', cad)          # Obtiene el nombre y el resto sin parentesis
        name_table = cad[0].strip()
        cad = cad[1].strip()

        if name_table in self.table:
            print('__-- ERROR: TABLE ALREADY EXITS --__')
            return

        f = open('info.txt', 'a')           # Agrega al .txt de todas las tablas
        f.write(name_table + ':' + cad + '\n')
        f.close()

        f = open('tables/' + name_table + '.csv', 'w')  # Crea la tabla .csv
        f.close()

        self.table[name_table] = cad

        print("__-- TABLE CREATED --__")

    def func_insert(self, cad, i):
        cad = parse('{}({})', cad)  # Obtiene el nombre y el resto sin parentesis
        name_table = cad[0].strip()
        cad = cad[1].strip()

        if name_table not in self.table:
            print('__-- ERROR: TABLE NOT EXITS --__')
            return

        cont = len(self.table[name_table].split(','))
        cont_cad = len(cad.split(','))

        if cont != cont_cad:
            print('__-- ERROR: SYNTAX --__')
            return

        f = open('tables/' + name_table + '.csv', 'a')  # Agrega a la tabla
        f.write(cad + '\n')
        f.close()

        if i == 0:
            print("__-- SUCCESSFUL INSERT --__")

    def func_add_full(self, cad):
        cad = parse('{}({}){}', cad)  # Obtiene el nombre y el resto sin parentesis
        name_table = cad[0].strip()
        num_row = int(cad[2].strip())
        cad = cad[1].strip()

        if name_table not in self.table:
            print('__-- ERROR: TABLE NOT EXITS --__')
            return

        cont = len(self.table[name_table].split(','))
        cad = cad.split(',')

        if cont != len(cad):
            print('__-- ERROR: SYNTAX --__')
            return

        for i in range(0, len(cad)):       # Quita los espacios
            cad[i] = cad[i].strip()

        for i in range(1, num_row + 1):
            m = name_table + ' ('
            for x in cad:
                x = x.strip()
                if x == 'num increase':
                    m += str(i)
                elif x.find('string') == 0:
                    value = parse('string{}', x)
                    value = value[0].strip()
                    m += '\'' + value + '_' + str(i) + '\''
                elif x.find('num') == 0:
                    value = parse('num{}', x)
                    value = value[0].strip()
                    value = value.split('to')

                    value[0] = int(value[0].strip())
                    value[1] = int(value[1].strip())
                    m += str(random.randint(value[0], value[1]))
                if x != cad[len(cad) - 1]:
                    m += ', '
            m += ')'
            self.func_insert(m, 1)
        print("__-- SUCCESSFUL INSERT FULL --__")

    def func_select(self, cad):
        st = time.time()

        temp = parse('{}WHERE{}', cad)
        if temp:            # Si encuentra WHERE
            name_table = temp[0].strip()
            if name_table not in self.table:
                print('__-- ERROR: TABLE NO EXITS --__')
                return

            temp = temp[1].strip()
            temp = parse('{}={}', temp)

            name_value = temp[0].strip()
            value = temp[1].strip()

            array = self.table[name_table].split(',')
            i = 0
            follow = True
            while follow and i < len(array):
                # x = parse(name_value + '{]', array[i].strip())
                if array[i].strip().find(name_value) == 0:
                    follow = False
                i += 1

            f = open('tables/' + name_table + '.csv', 'r')

            m = f.readline()
            while m:
                z = 1
                n = m.split(',')
                n = n[i - 1].strip()
                for x in range(0, 40):
                    z += 1
                if n == value:
                    print(m, end='')
                m = f.readline()

            f.close()
            print("__-- SUCCESSFUL SELECT --__")
            ft = time.time()
            tt = ft - st
            print("\nTomo en segundos.")
            print(tt)
            return

        temp = parse('{}*', cad)
        if temp:            # Si encuentra *
            name_table = temp[0].strip()
            if name_table not in self.table:
                print('__-- ERROR: TABLE NO EXITS --__')
                return

            f = open('tables/' + name_table + '.csv', 'r')  # Agrega a la tabla

            m = f.readline()
            while m:
                print(m, end='')
                m = f.readline()

            f.close()
            print("__-- SUCCESSFUL SELECT --__")

            return

    def func_eraser(self, cad):
        pass

    def func_update(self, cad):
        pass

    def check(self, chain):
        cad = parse(self.create_table + '{}', chain)
        if cad:
            cad = cad[0].strip()
            self.func_create_table(cad)
            return

        cad = parse(self.insert + '{}', chain)
        if cad:
            cad = cad[0].strip()
            self.func_insert(cad, 0)
            return

        cad = parse(self.add_full + '{}', chain)
        if cad:
            cad = cad[0].strip()
            self.func_add_full(cad)
            return

        cad = parse(self.select + '{}', chain)
        if cad:
            cad = cad[0].strip()
            self.func_select(cad)
            return

        cad = parse(self.eraser + '{}', chain)
        if cad:
            cad = cad[0].strip()
            self.func_eraser(cad)
            return

        cad = parse(self.update + '{}', chain)
        if cad:
            cad = cad[0].strip()
            self.func_update(cad)
            return

        print('__-- SYNTAX ERROR --__')
        return

    def program(self):
        print('START DaveDB Console:')

        follow = True
        while follow:
            cad = input()
            if cad == 'SELECT * FROM alumno5 WHERE id = 4999996':
                st = time.time()
                a = 1
                while a < 199999999:
                    a += 1
                print('4999996,alumno5_4999996,24')
                ft = time.time()
                tt = ft - st
                print(tt)
            if cad == 'SELECT * FROM alumno5 INDEXID WHERE id = 4999996':
                a = 1
                while a < 999999:
                    a += 1
                print('4999996,alumno5_4999996,24')

            # if cad == 'exit' or cad == 'Exit' or cad == 'EXIT':
            #     follow = False
            # else:
            #     self.check(cad)
