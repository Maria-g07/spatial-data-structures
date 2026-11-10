from operator import itemgetter
import math
import csv
from timeit import default_timer as timer
from os import chdir

from lshash import LSHash



class Kdtree:
    
    def __init__(self,point_list):
        
        self.kdtree = self.build(point_list, 0)
        
        
        
    def build(self, point_list, depth: int = 0):
        if not point_list:
            return []
 
        k = len(point_list[0])
        
        axis = depth % k
        
        point_list.sort(key=itemgetter(axis))
        
        median = len(point_list) // 2
           
        return [point_list[median], 
                self.build(point_list[:median], depth + 1),
                self.build(point_list[median + 1:], depth + 1)]
    
    
    
    def search(self, key):
    
        depth = 0

        current = self.kdtree

        while(len(current)>0):
            node = current[0]
            if ((key[0] == node[0]) and (key[1]==node[1]) and (key[2]==node[2])):
                #key found!
                return True   
       
            dim = depth % 3

            if (key[dim] <= current[0][dim]):
                current = current[1] 
            else:
                current = current[2] 
            
            depth += 1

        return False
    
    
    
    def insert(self, key):
        
        new_node = [key,[],[]]

        depth = 0
        current = self.kdtree
        
        flag = True
        while(flag):
            dim = depth % 3

            if (key[dim] < current[0][dim]):
                if (current[1]):
                    current = current[1]
                else:
                    current[1] = new_node
                    return
            else:
                if (current[2]):
                    current = current[2]
                else:
                    current[2] = new_node
                    return
            depth += 1
            
            
    
    def delete(self, key):
        depth = 0   
        current = self.kdtree   
        while(current):
            node = current[0]
            if ((key[0] == node[0]) and (key[1]==node[1]) and (key[2]==node[2])):
                if ((not current[1]) and (not current[2])):
                    current.clear()
                    return True
                    
                else:
                    point_list = self.get_children(current)
                    subtree = self.build(point_list, depth)
                    current[0] = subtree[0]
                    current[1] = subtree[1]
                    current[2] = subtree[2] 
                    return True          
            dim = depth % 3
            if (key[dim] < current[0][dim]):
                current = current[1]
            else:
                current = current[2]
            depth += 1
        return False 
    
    
    
    def get_children(self, node):
        
        children = []
        queue = []
        if (node[1]):
            queue.append(node[1])
        if (node[2]):
            queue.append(node[2])

        while (len(queue)>0):
            current = queue[0]

            children.append(current[0])
            if (current[1]):
                queue.append(current[1])
            if (current[2]):
                queue.append(current[2])
            del queue[0]            
        return children
    
    
    
    def update(self, key, value):
        if(self.search(key)):
            self.delete(key)
            self.insert(value)
            return True
        else:
            return False
    
    
    
    def find_nearest(self, key):
        
        lsh = LSHash(4, 3)
        
        root = self.kdtree
        
        
        root_str = ''.join([str(i) for i in root[0]])
        root_ascii = []        
        for x in root_str:
            root_ascii.append(ord(x))
       
        lsh.index(root_ascii)
        
        
        rest_nodes = self.get_children(root)
        
        
        for x in rest_nodes:
            x_str = ''.join([str(i) for i in x])
            
            x_ascii = []
            
            for y in x_str:
                x_ascii.append(ord(y))
            lsh.index(x_ascii)
        
        
        key_str = ''.join([str(i) for i in key])
        key_ascii = []        
        for x in key_str:
            key_ascii.append(ord(x))
          
        
        result = lsh.query(key_ascii,1)

        nearest = result[0][0]
        
        mystr=""
        
        for x in nearest:
            mystr = mystr + chr(x)
            
        print(mystr)
        



point_list = []
        
with open("test.txt") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    
for line in lines:
    point = list(line)
    point_list.append(point)
    
  
start = timer()              
tree = Kdtree(point_list)
end = timer()

elapsed = end - start

print("Time for construction of Kd-Tree:"+str(elapsed))

print(tree.kdtree)



points_to_search = []

points_to_search.append(['k','c','b'])

points_to_search.append(['t','c','a'])

points_to_search.append(['z','u','o'])

points_to_search.append(['t','r','c'])

points_to_search.append(['p','o','i'])

sum_time = 0

for i in range(5):
    start = timer()
    
    tree.search(points_to_search[i])
    
    end = timer()
    
    elapsed = end - start
    
    sum_time = sum_time + elapsed
    
    
    
print("Average Time for searching in Kd-Tree:"+str(sum_time/5))



points_to_insert=[]

points_to_insert.append(['r','r','r'])

points_to_insert.append(['q','a','z'])

points_to_insert.append(['x','y','z'])

points_to_insert.append(['c','e','o'])

points_to_insert.append(['e','r','t'])


sum_time = 0


for i in range(5):
    start  = timer()
    
    tree.insert(points_to_insert[i])
    
    end = timer()
    
    elapsed = end - start
    
    sum_time = sum_time+elapsed
    
    
print("Average Time for inserting in Kd-Tree:"+str(sum_time/5))



points_to_delete = []

points_to_delete.append(['r','r','r'])

points_to_delete.append(['q','a','z'])

points_to_delete.append(['x','y','z'])

points_to_delete.append(['c','e','o'])

points_to_delete.append(['e','r','t'])


sum_time = 0
for i in range(5):
    start = timer()
    tree.delete(points_to_delete[i])
    end = timer()
    elapsed = end - start
    sum_time=sum_time+elapsed
    


print("Average Time for deleting in Kd-Tree:"+str(sum_time/5))



old_points = []

new_points = []

old_points.append(['x','c','v'])

old_points.append(['s','a','s'])

old_points.append(['z','a','l'])

old_points.append(['r','a','s'])

old_points.append(['b','m','n'])


new_points.append(['n','g','a'])

new_points.append(['e','r','j'])

new_points.append(['r','e','u'])

new_points.append(['a','e','p'])

new_points.append(['m','k','i'])

sum_time = 0


for i in range(5):
    start=timer()
    tree.update(old_points[i],new_points[i])
    end=timer()
    elapsed = end - start
    sum_time = sum_time+elapsed
    
    


print("Average Time for updating in Kd-Tree:"+str(sum_time/5))



lsh_points = []


lsh_points.append(['z','w','y'])

lsh_points.append(['d','a','d'])

lsh_points.append(['g','h','a'])

lsh_points.append(['b','b','c'])

lsh_points.append(['r','a','t'])


sum_time = 0


for i in range(5):
    start=timer()
    tree.find_nearest(lsh_points[i])
    end=timer()
    elapsed = end - start
    sum_time = sum_time+elapsed

print("Average Time for LSH  in Kd-Tree:"+str(sum_time/5))

