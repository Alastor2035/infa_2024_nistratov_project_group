def drawed(graf, edges, m, v, siz):
    for color in range(1, m+1):
        maybe = True
        for i in range(len(graf)):
            if edges[v][i] == 1 and graf[i] == color:
                maybe = False
                break
        if maybe:
            graf[v] = color
            if v == siz:
                return True
            if drawed(graf, edges, m, v+1, siz):
                return True
            graf[v] = 0
    return False
v, e  = map(int, input().split())
graf = [0] * v
edges = []
for i in range(v):
    edges.append([0]*v)
for _ in range(e):
    i, j = map(int, input().split())
    edges[i][j] = 1
    edges[j][i] = 1
m = int(input())
print(str(drawed(graf, edges, m, 0, v-1)).lower())


# первая строка кол-во вершин и рёбер
#  далее рёбра в виде двух вершин, каждое ребро в своей строке 
# далее число цветов
