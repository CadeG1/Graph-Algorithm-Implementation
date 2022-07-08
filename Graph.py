#Assignment 3: Graph Search!
#Author: Cade Gallenstein


#Define class vertice
class Vertice:
    def __init__(self,key):
        self.key = key
        self.index = -1
        self.next = None
        self.visited = False
        self.prev = None
        self.distance = 0;

#Define class Edge
class Edge:
    def __init__(self, key, distance):
        self.key = key
        self.distance = distance
        self.point = None 
        self.next = None

#Insert Initial Values into Vertice
def insertVertice(Hashtable, key, index):
    for i in Hashtable:
        if i.key == None:
            i.key = key
            i.index = index
            return None

#Insert Edges into given vertice based on conditions below
def insertEdge(Hashtable, vKey, eKey, length):
    ins = Edge(eKey, length)
    
    #Go through Hash and find where to much Edge
    for i in Hashtable:
        if(vKey == i.key):
            currentNode = i
            
            #Go until there is an empty edge
            while(currentNode.next != None):
                currentNode = currentNode.next
            currentNode.next = ins
            return
      
       
#Print full graph
def printGraph(Hashtable):
    for edge in Hashtable:
        if edge.key is not None:
            print(edge.key, end = ' ---> ')
            currVert = edge.next
            while currVert is not None:    
                print(currVert.key, end = ', ')
                currVert = currVert.next
            print()
        else:
            return

#Open vertice file and put it into a list
def openVertice(fileName):

    file = open(fileName, "r")
    vertices = file.readlines()

    for i in range(len(vertices)):
        vertices[i] = vertices[i].rstrip("\n")
    return vertices


#Open edge file and put it into a list
def openEdge(fileName):
    
    file = open(fileName, "r")
    line = file.readlines()
    
    edges = []
    for i in range(len(line)):
        line[i] = line[i].rstrip("\n")
        line[i] = line[i].split(",")
        line[i][2] = int(line[i][2])
        edges.append(line[i])
        
    return edges


#Find all edge instances of a vertice and give it a pointer to itself
def giveSelf(Hashtable, toSelf):
    for i in Hashtable:
        curr = i.next
        while curr is not None:
            if curr.key == toSelf.key:
                curr.point = toSelf
            curr = curr.next
    
 
#Implementation of unweighted Breadth first search
def BFS(Hashtable, source, end):
    
    queue = []
    queue.append(Hashtable[source])
    Hashtable[source].visited = True
    
    while queue:
        cn = queue.pop(0)
    
        curr = cn.next
        while curr is not None:
            if curr.point.visited == False:
                queue.append(curr.point)
                curr.point.visited = True
                curr.point.prev = cn
            curr = curr.next
            
    PrintPath(Hashtable, source, end)
    
   
#Print Path defined at the end to the start using previous pointers
#NOTE: For both BFS and Dijkstra's
def PrintPath(Hashtable, start,end):
    node = Hashtable[end]
    route = []
    
    while node is not None:
        route.append(node.key)
        node = node.prev
     
    route.reverse()
    print(Hashtable[start].key, "to", Hashtable[end].key, end= ' ')
    for city in route:
        print("---> ", city, end = ' ')
    print()
    
    clearVisits(Hashtable)
 
 
#Clear visits of every vertice so they can search once again
def clearVisits(Hashtable):
    for edge in Hashtable:
        edge.visited = False
 
    
#Implementation of weighted graph search via Dijkstra's algorithm
def Dijkstra(Hashtable, source, end):
    InitSource(Hashtable, source)
    queue = [Vertice(None)]*20
    num = 0
    
    for i in Hashtable:
        queue[num] = i 
        num = num + 1

    while queue:
        u = minDistance(queue)
        
        for j in range(len(queue)):
            if queue[j].key == u.key:
                queue.pop(j)
                break
        
        curr = u.next
        while curr is not None:
            relax(u,curr)
            curr = curr.next
      
    
    PrintPath(Hashtable, source, end)
    
#Relax the current node, helper for Dijkstra
def relax(u, v):
    if v.point.distance > u.distance + v.distance:
        v.point.distance = u.distance + v.distance
        v.point.prev = u

#Initial conditions for Dijkstra's algorithm defined at a source
def InitSource(Hashtable, source):
    for i in Hashtable:
        i.distance = 99999
        i.prev = None
    Hashtable[source].distance = 0


#Find the minimum distance in the current queue
def minDistance(queue):
    minVert = queue[0]
    for i in queue:
        if i.distance < minVert.distance:
            minVert = i
    
    return minVert
 

#Find a vertice given its key
def findVertice(Hashtable, find):
    for i in Hashtable:
        if i.key == find:
            print(i.index)
            return i.index



def PrimMST(Hashtable, source):
    for vert in Hashtable:
        vert.distance = 99999
        vert.prev = None
        
    Span = []  
    cn = Hashtable[source]
    cn.distance = 0

    queue = [Vertice(None)]*20
    num = 0
    for i in Hashtable:
        queue[num] = i 
        num = num + 1
    
    while queue:
        u = minDistance(queue)
        Span.append(u)
        for j in range(len(queue)):
            if queue[j].key == u.key:
                queue.pop(j)
                break
        
        curr = u.next
        while curr is not None:
            check = 0
            for i in queue:
                if curr.key == i.key:
                    check = 1
   
            if check == 1 and (curr.distance < curr.point.distance):
                    curr.point.prev = u
                    curr.point.distance = curr.distance
                                  
            curr = curr.next
    
    #Print MST from Source
    print("MST", end = "")
    for i in Span:
        print(" -->",i.key, end = "")



def main():
    
    #Define max value of vertices
    maxV = 20
    
    #Create Hashmap to represent graph
    HashTable = [Vertice(None)]*maxV
    for i in range(maxV):
        HashTable[i] = Vertice(None)
    
    #Open file that holds the names of the vertices and insert into the Hashtable
    file = openVertice("RomaniaVertices.txt")
    num = 0
    for i in file:
        insertVertice(HashTable, i, num)
        num = num + 1
    
    
    #Open file that holds the edges and insert into the specified Vertice within the Hashtable
    file = openEdge("RomaniaEdges.txt")
    num= 0
    for i in file:
        insertEdge(HashTable, file[num][0], file[num][1], file[num][2])
        insertEdge(HashTable, file[num][1], file[num][0], file[num][2])
        num = num + 1
    
    
    #Find all the edge's corresponding vertice's and point to it
    for i in HashTable:
        giveSelf(HashTable, i)
    

    arad = findVertice(HashTable, 'Arad')
    sibiu = findVertice(HashTable, 'Sibiu')
    craiova = findVertice(HashTable, 'Craiova')
    bucharest = findVertice(HashTable, 'Bucharest')
    

    print("BFS Search:")
    BFS(HashTable, arad, sibiu)
    BFS(HashTable, arad, craiova)
    BFS(HashTable, arad, bucharest)
    print()
    print("Dijkstra Search:")
    Dijkstra(HashTable, arad, sibiu)
    Dijkstra(HashTable, arad, craiova)
    Dijkstra(HashTable, arad, bucharest)
    print()
    print("Prims Search:")
    PrimMST(HashTable, arad)
    print()
    print()
    print("Full Map of Romania:")
    printGraph(HashTable)
  
    
main()
