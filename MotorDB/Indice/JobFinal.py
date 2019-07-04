import time
import arbolAVL
import csv
from parse import *
import sys
import os


class CMotorDB:
    create_table = ''
    insert = ''
    select = ''
    eraser = ''
    update = ''

    table = {}

    def __init__(self):
        self.select = 'select_table_idx'

        f = open('info.txt', 'r')
        m = f.readline()
        while m:
            m = parse('{}:{}', m)
            self.table[m[0].strip()] = m[1].strip()
            m = f.readline()

    def func_select(self, cad):
        temp = parse('{}WHERE{}', cad)
        if temp:            # Si encuentra WHERE
            st = time.time()
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

    def check(self, chain):
        cad = parse(self.select + '{}', chain)
        if cad:
            cad = cad[0].strip()
            self.func_select(cad)
            return

        print('__-- SYNTAX ERROR --__')
        return

    def program(self):
        follow = True
        while follow:
            cad = input()
            if cad == 'exit' or cad == 'Exit' or cad == 'EXIT':
                follow = False
            else:
                self.check(cad)

#sys.setrecursionlimit(100000)

#select_table_idx alumnoUM (id = 999556, idx = IDX_id)
#select_table_idx alumnotest (edad = 17, idx = IDX_edad)
list_type_query = ['create_table','insert_table','select_table','delete_table','up_date_table','select','create_index']

def create_index(nameTxt, table, campo):
    a = arbolAVL.AVLTree()
    with open(table+'.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            a.insert(int(line.get(campo)), int(int(line.get('id'))))   # int(line.get('id')))

    t = a.display()
    f = open(nameTxt+'.txt', 'w')
    for i in t:
        f.write(str(t.get(i)) + '\n')
    f.close()

def a_ram(nameTxt):
    tree = arbolAVL.AVLTree()
    f = open(nameTxt + '.txt', 'r')
    for i in f:
        i = i.replace(' ', '')
        i = i[1:len(i)-2]
        i = i.split('],')
        for j in range(0,len(i)):
            if i[j].find(']'):
                i[j] = i[j].replace(']', '')
            i[j] = i[j].split(',[')
        for j in range(0, len(i)):
            i[j][1] = i[j][1].split(',')
        for j in range(0, len(i)):
            for k in range(0, len(i[j][1])):
                tree.insert(int(i[j][0]), int(i[j][1][k]))

    print("__-- SUCCESSFUL a_ram --__")
    return tree

def select_table_idx(name_table, direction):
    with open(name_table+'.csv') as csvfile:
        for i in range(direction * 2): #direccion*2
            csvfile.readline()
        reader = csv.DictReader(csvfile)
        print(reader.fieldnames)

def run(query):
    split_query = query.split(' ')
    if split_query[0] == 'create_index':
        split_query[4]=split_query[4][1:len(split_query[4])-1]
        create_index(split_query[1],split_query[3],split_query[4])

def menu():
    treeEdad = arbolAVL.AVLTree()
    treeId = arbolAVL.AVLTree()
    tree = arbolAVL.AVLTree()
    while True:
        query = input()
        if query != 'exit' and query != 'Exit' and query != 'EXIT':
            split_query = query.split(' ')
            if split_query[0] == 'a_ram':
                split_query[1] = split_query[1][1:len(split_query[1])-1]
                if split_query[1] == 'IDX_edad':
                    treeEdad = a_ram(split_query[1])
                elif split_query[1] == 'IDX_id':
                    treeId = a_ram(split_query[1])
                else:
                    tree = a_ram(split_query[1])
            if split_query[0] == 'select_table_idx':
                A = CMotorDB()
                query = parse(A.select + '{}', query)
                query = parse('{}' + ', ' + '{}', query[0])
                if query[1] == 'idx = IDX_id' or query[1] == 'idx = IDX_edad':
                    query = query[0].strip()
                    A.func_select(query)
                # A.func_select(query)
                # split_query = query.split(' ',2)
                # parameters = split_query[2]
                # parameters = split_query[2][1:len(parameters)-1]
                # parameters = parameters.replace(' ', '')
                # parameters = parameters.replace('=', ',')
                # split_parameters = parameters.split(',')
                # if split_parameters[3] == 'IDX_id':
                #     aux = treeId.find(int(split_parameters[1]))
                #     if aux[0] == True:
                #         for i in aux[1]:
                #             select_table_idx(split_query[1],i)
                #     else:
                #         print('nose encontro',split_parameters[1])
                # elif split_parameters[3] == 'IDX_edad':
                #     aux = treeEdad.find(int(split_parameters[1]))
                #     if aux[0] == True:
                #         for i in aux[1]:
                #             select_table_idx(split_query[1],i)
                #     else:
                #         print('nose encontro',split_parameters[1])
        else:
            break

# select_table_idx tb_akumno (edad = 17, idx = IDX_edad)
# select_table_idx tb_alumno (id = 99556, idx = IDX_id)


if __name__ == "__main__":
    a_ram('IDX_id')
    # select_table_idx tb_alumno WHERE id = 99966, idx = IDX_id
    a_ram('IDX_edad')
    # select_table_idx tb_alumno WHERE edad = 19, idx = IDX_edad

    menu()
