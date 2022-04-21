import pydot
import os
import sys

prefix=sys.path[0]
f = open(prefix+"/parser.out", "r")
Lines = f.readlines()

edges=[]
nodes=[]
k=' '

for x in Lines:
  a = x.split()
  if len(a)>0 and a[0]=='state' and len(a)==2:
    k=a[1]
    nodes.append(k)
  elif k!=' ' and len(a)==7 and a[3]=='go':
    edges.append([k,a[6],a[0]])

graph = pydot.Dot("my_graph", graph_type="digraph", bgcolor="yellow")

for node in nodes:
  graph.add_node(pydot.Node('I'+node, shape="circle"))

for edge in edges:
  graph.add_edge(pydot.Edge('I'+edge[0],'I'+edge[1], color="blue",label=edge[2]))

graph.write(prefix+'/graph.dot')
os.system(f"sfdp -x -Tpng '{prefix}/graph.dot' > '{prefix}/graph.png'")