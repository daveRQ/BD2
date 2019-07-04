# import random, math
import csv

class Node():
    def __init__(self, date, dir):
        self.date = date
        self.dir = dir
        self.listPos = []
        self.left = None
        self.right = None

class AVLTree():
    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0;

    def height(self):
        if self.node:
            return self.node.height
        else:
            return 0

    def is_leaf(self):
        return (self.height == 0)

    def insert(self, date,dir):
        tree = self.node

        newnode = Node(date,dir)

        if tree == None:
            self.node = newnode
            self.node.listPos.append(self.node.dir)
            self.node.left = AVLTree()
            self.node.right = AVLTree()

        elif date < tree.date:
            self.node.left.insert(date,dir)

        elif date > tree.date:
            self.node.right.insert(date,dir)

        else:
            self.node.listPos.append(dir)
        self.rebalance()

    def rebalance(self):
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.lrotate()  # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rrotate()  # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()

    def rrotate(self):
        # Rotate left pivoting on self
        A = self.node
        B = self.node.left.node
        T = B.right.node

        self.node = B
        B.right.node = A
        A.left.node = T

    def lrotate(self):
        # Rotate left pivoting on self
        A = self.node
        B = self.node.right.node
        T = B.left.node

        self.node = B
        B.left.node = A
        A.right.node = T

    def update_heights(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()

            self.height = max(self.node.left.height,
                              self.node.right.height) + 1
        else:
            self.height = -1

    def update_balances(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def delete(self, date):
        # debug("Trying to delete at node: " + str(self.node.date))
        if self.node != None:
            if self.node.date == date:
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None  # leaves can be killed at will
                # if only one subtree, take that 
                elif self.node.left.node == None:
                    self.node = self.node.right.node
                elif self.node.right.node == None:
                    self.node = self.node.left.node

                # worst-case: both children present. Find logical successor
                else:
                    replacement = self.logical_successor(self.node)
                    if replacement != None:  # sanity check
                        self.node.date = replacement.date

                        # replaced. Now delete the date from right child 
                        self.node.right.delete(replacement.date)

                self.rebalance()
                return
            elif date < self.node.date:
                self.node.left.delete(date)
            else:# date > self.node.date:
                self.node.right.delete(date)

            self.rebalance()
        else:
            return

    def logical_predecessor(self, node):
        ''' 
        Find the biggest valued node in LEFT child
        '''
        node = node.left.node
        if node != None:
            while node.right != None:
                if node.right.node == None:
                    return node
                else:
                    node = node.right.node
        return node

    def logical_successor(self, node):
        ''' 
        Find the smallese valued node in RIGHT child
        '''
        node = node.right.node
        if node != None:  # just a sanity check

            while node.left != None:
                if node.left.node == None:
                    return node
                else:
                    node = node.left.node
        return node

    def check_balanced(self):
        if self == None or self.node == None:
            return True

        # We always need to make sure we are balanced 
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())

    def inorder_traverse(self):
        if self.node == None:
            return []

        inlist = []
        l = self.node.left.inorder_traverse()
        for i in l:
            inlist.append(i)
        inlist.append(self.node.date)
        inlist.append(self.node.listPos)
        l = self.node.right.inorder_traverse()
        for i in l:
            inlist.append(i)

        return inlist

    def display(self, level=0, pref=',',dicc = {}):
        self.update_heights()
        self.update_balances()

        if (self.node != None):
            list = []
            list.append(self.node.date)
            list.append(self.node.listPos)
            if dicc.get(level) != None:
                aux = dicc.setdefault(level)
                aux.append(self.node.date)
                aux.append(self.node.listPos)
                dicc[level] = aux
            else:
                dicc[level] = list

            if self.node.left != None:
                self.node.left.display(level + 1, ',',dicc)
            if self.node.left != None:
                self.node.right.display(level + 1, ',',dicc)
        return dicc

    def display1(self, level=0, pref=''):
        if (self.node != None):
            print('-' * level * 2, pref, self.node.date, "[" + str(self.height) + ":" + str(
                self.balance) + "]", 'L' if self.is_leaf() else 'N')
            if self.node.left != None:
                self.node.left.display1(level + 1, '<')
            if self.node.left != None:
                self.node.right.display1(level + 1, '>')

    def find(self, date):
        tree = self.node
        if tree != None:
            if date == tree.date:
                return  (True,tree.listPos)
            elif date < tree.date:
                return  tree.left.find(date)
            elif date > tree.date:
                return tree.right.find(date)
        return (False,[])
