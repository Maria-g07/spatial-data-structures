import math
import csv
from timeit import default_timer as timer
from os import chdir
from lshash import LSHash



class Octtree:
    
    def __init__(self,point_list):
            self.octtree = self.build(point_list)
    
    
    
    def get_dir(self, root, key):
        if (key[0] < root[0]):
            if (key[1] < root[1]):
                if (key[2] < root[2]):
                    #tha pame sto proto paidi
                    return 1
                
                else:
                    return 2
                
                
            else:
                if (key[2] < root[2]):
                    return 3
                
                else:
                    return 4
        
        else:
            if (key[1] < root[1]):
                if (key[2] < root[2]):
                    return 5
                
                else:
                    return 6
            else:
                if (key[2] < root[2]):
                    return 7
                else:
                    return 8
                
                
                
    def build(self, point_list):
        if not point_list:
            return []
    
        current = point_list[0]
        del point_list[0]
        
        l1 = []
        l2 = []
        l3 = []
        l4 = []
        l5 = []
        l6 = []
        l7 = []
        l8 = []
    
        for p in point_list:
            d = self.get_dir(current, p)
            if(d==1):
                l1.append(p)
                continue
            if(d==2):
                l2.append(p)
                continue
            if(d==3):
                l3.append(p)
                continue
            if(d==4):
                l4.append(p)
                continue
            if(d==5):
                l5.append(p)
                continue
            if(d==6):
                l6.append(p)
                continue
            if(d==7):
                l7.append(p)
                continue
            if(d==8):
                l8.append(p)
                continue
     
        # Create node and construct subtrees
        return [current,
                self.build(l1),
                self.build(l2),
                self.build(l3),
                self.build(l4),
                self.build(l5),
                self.build(l6),
                self.build(l7),
                self.build(l8)]
    
    
    
    def search(self, key):
          
        current = self.octtree
        
        while(len(current)>0):
            node = current[0]
            if ((key[0] == node[0]) and (key[1]==node[1]) and (key[2]==node[2])):
                #tote epistrefoume true
                return True
            
            d = self.get_dir(node, key)
            current = current[d]
             
        return False
    
    
    
    def insert(self, key):
        new_node = [key,[],[],[],[],[],[],[],[]]
        
        current = self.octtree
        flag = True
        while(flag):
            d = self.get_dir(current[0], key)
            if (current[d]):
                current = current[d]
            else:
                current[d] = new_node                
                return
            
            
    
    def delete(self, key): 
        current = self.octtree
        while(current):
            node = current[0]
            if ((key[0] == node[0]) and (key[1]==node[1]) and (key[2]==node[2])):
                
                if ((not current[1]) and (not current[2]) and (not current[3]) and (not current[4]) and (not current[5]) and (not current[6]) and (not current[7])and (not current[8])):
                    current.clear()
                    return True
                else:  
                    point_list = self.get_children(current)
                                       
                    subtree = self.build(point_list)
                    
                    current[0] = subtree[0] 
                    current[1] = subtree[1] 
                    current[2] = subtree[2] 
                    current[3] = subtree[3]
                    current[4] = subtree[4]
                    current[5] = subtree[5]
                    current[6] = subtree[6]
                    current[7] = subtree[7]
                    current[8] = subtree[8]
                    return True
            else:
                d = self.get_dir(node, key)
                current = current[d]
                
        return False 
    
    
    
    def get_children(self, node):
        
        children = []
        queue = []
        for i in range(8):
            if (node[i + 1]):
                queue.append(node[i + 1])
         
        while (len(queue)>0):
            current = queue[0] 
            children.append(current[0])
            for i in range(8):
                if (current[i + 1]):
                    queue.append(current[i + 1])
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
        
        root = self.octtree
        
        
        
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
tree = Octtree(point_list)
end = timer()

elapsed = end - start

print("Time for construction of Oct-Tree:"+str(elapsed))

print(tree.octtree)



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
    
    
    
print("Average Time for searching in Oct-Tree:"+str(sum_time/5))



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
    
    
print("Average Time for inserting in Oct-Tree:"+str(sum_time/5))



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
    


print("Average Time for deleting in Oct-Tree:"+str(sum_time/5))



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
    
    


print("Average Time for updating in Oct-Tree:"+str(sum_time/5))



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

print("Average Time for LSH  in Oct-Tree:"+str(sum_time/5))
