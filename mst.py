import random
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer


class List:
    def __init__(self, x):
        self.list = []
        self.list.append(x)
        self.rep = x


class Arch:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight


class UnionFind:
    def __init__(self):
        self.list = []

    def make_set(self, v):
        self.list.append(List(v))

    def union(self, u, v):
        if len(self.list[self.list[u].rep].list) > len(self.list[self.list[v].rep].list):
            new_rep = self.list[u].rep
            old_rep = self.list[v].rep
            self.list[new_rep].list.extend(self.list[old_rep].list)
            for i in range(len(self.list[old_rep].list)):
                self.list[old_rep].list.pop()
            for i in range(len(self.list)):
                if self.list[i].rep == old_rep:
                    self.list[i].rep = new_rep
        else:
            new_rep = self.list[v].rep
            old_rep = self.list[u].rep
            self.list[new_rep].list.extend(self.list[old_rep].list)
            for i in range(len(self.list[old_rep].list)):
                self.list[old_rep].list.pop()
            for i in range(len(self.list)):
                if self.list[i].rep == old_rep:
                    self.list[i].rep = new_rep

    def find_set(self, v):
        return self.list[v].rep


def connected_components(dim, arches):
    union_find = UnionFind()
    for v in range(dim):
        union_find.make_set(v)
    for i in range(len(arches)):
        u = arches[i].u
        v = arches[i].v
        if union_find.find_set(u) != union_find.find_set(v):
            union_find.union(union_find.find_set(u), union_find.find_set(v))
    count = 0
    for i in range(len(union_find.list)):
        union_find.list[i].list.sort()
        if len(union_find.list[i].list) != 0:
            print("{}^a componente connessa:".format(count + 1))
            print(union_find.list[i].list)
            count += 1
    return count


def mst_kruskal(dim, arches):
    mst = []
    union_find = UnionFind()
    for v in range(dim):
        union_find.make_set(v)
    arches.sort(key=lambda x: x.weight)
    for i in range(len(arches)):
        u = arches[i].u
        v = arches[i].v
        if union_find.find_set(u) != union_find.find_set(v):
            mst.append((u, v))
            # print "nodo", u, " con rappresentante", union_find.find_set(
            # u), "e nodo", v, "con rappresentante", union_find.find_set(v)
            union_find.union(union_find.find_set(u), union_find.find_set(v))
            # print "nodo", u, " con nuovo rappresentante", union_find.find_set(
            # u), "e nodo", v, "con nuovo rappresentante", union_find.find_set(v)
    print("MST:", mst)


def connected_components_test(dim, arches):
    start = timer()
    count = connected_components(dim, arches)
    end = timer()
    time_c = end - start
    print("Tempo componenti connesse:", time_c)
    return count


def mst_kruskal_test(dim, arches):
    start = timer()
    mst_kruskal(dim, arches)
    end = timer()
    time_k = end - start
    print("Tempo Kruskal:", time_k, "\n")
    return time_k


def graph_creation(dim, prob, arches):
    matrix = np.zeros((dim, dim))
    max_weight = 20
    for i in range(dim):
        for j in range(i):
            if random.randint(1, 100) <= prob and matrix[i][j] == 0:
                matrix[i][j] = random.randint(1, max_weight)
                matrix[j][i] = matrix[i][j]
                arches.append(Arch(j, i, matrix[i][j]))
    print(matrix)


def avg(array):
    avg = 0
    for i in range(len(array)):
        avg += array[i]
    return avg / len(array)


def main():
    dim = 100
    mst_times = []
    cc_num = []
    probability = []
    for prob in range(0, 51):
        probability.append(prob)
        mst_single = []
        cc_single = []
        print("Dimensione:", dim, "Probabilita:", prob)
        for n in range(0, 10):
            arches = []
            graph_creation(dim, prob, arches)
            arches_copy = arches[:]
            cc_single.append(connected_components_test(dim, arches))
            mst_single.append(mst_kruskal_test(dim, arches_copy))
        mst_times.append(avg(mst_single))
        cc_num.append(avg(cc_single))

    plt.plot(probability, cc_num)
    plt.xlabel('Probabilita')
    plt.ylabel('Numero componenti connesse')
    plt.legend(['Componenti connesse'])
    plt.savefig('Componenti_Connesse')
    plt.clf()
    plt.plot(probability, mst_times)
    plt.xlabel('Probabilita')
    plt.ylabel('Tempo di esecuzione')
    plt.legend(['MST con Kruskal'])
    plt.savefig('MST_Kruscal')
    plt.clf()


if __name__ == '__main__':
    main()
