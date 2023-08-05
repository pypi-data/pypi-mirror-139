from IPython.display import SVG, display,HTML
import random as rd
import math
class Attr:
    deneme = []
    def __init__(self,name,features={}, oneTag=False, context= None):
        self.name = name
        self.features = features
        self.oneTag = oneTag
        self.altAttr = []
        self.context = context
    def add(self, nesne, onden=False):
        if onden:
            self.altAttr.insert(0,nesne)
        else:
            self.altAttr.append(nesne)

    def string(self,index=0):
        text = "\t"*index+"<" + self.name
        for i in self.features:
            text += " "+str(i)+"=\""+str(self.features[i])+"\""
        if self.oneTag: text += "/>\n"
        else:
            text += ">\n"
            if self.context != None: text += "\t"*(index+1)+self.context+"\n"
            for i in self.altAttr:
                text += i.string(index+1)
            text += "\t"*index+"</"+ self.name +">\n"
        return text
    def show(self): display(SVG(data=self.string()))
    def save(self, path):
        with open(path, 'w') as f:
            f.write(self.string())
        
class Svg:
    colors = ["rgb(212, 0, 255)"]
    def __init__(self,res):
        self.svg = Attr("svg",features={"version":"1.1","xmlns":"http://www.w3.org/2000/svg","width":str(res[0])+"px","height":str(res[1])+"px","style":"rgb(30,30,30"})

    def node(self, context, pos,color=(100,0,0), r=None):
        circ = Attr("circle",
            features={
                "cx":pos[0],
                "cy":pos[1],
                "r":r if r!= None else max(len(context)*4,30),
                "fill":"rgb"+str(color),
                "stroke":"black",
                "stroke-width":5,
            },oneTag=True
        )
        
        text = Attr("text",
            features={
                "x":pos[0],
                "y":pos[1],
                "fill":"white",
                "dominant-baseline":"middle",
                "text-anchor":"middle"
            }, context=context
        )
        self.svg.add(circ)
        self.svg.add(text)
        return circ

    def bag(self, pos1, pos2, color=(100,150,150), width=5, context=None):
        line = Attr("line",
            features={
                "x1":pos1[0],
                "y1":pos1[1],
                "x2":pos2[0],
                "y2":pos2[1],
                "style":"stroke:rgb"+str(color)+";stroke-width:"+str(width)
            }
        )
        self.svg.add(line, onden=True)
        if context != None:
            text = Attr("text",
                features={
                    "x":pos1[0] + (pos2[0] - pos1[0])/2,
                    "y":pos1[1] + (pos2[1] - pos1[1])/2,
                    "fill":"white",
                    "dominant-baseline":"middle",
                    "text-anchor":"middle"
                }, context=context
            )
            self.svg.add(text)

    def res(self):
        x,y=[],[]
        for i in self.svg.altAttr:
            if i.name == "circle":
                x.append(i.features["cx"]+i.features["r"])
                y.append(i.features["cy"]+i.features["r"])
        x = max(x)
        y = max(y)
        self.svg.features["width"] = x+20
        self.svg.features["height"] = y+20
                
    def show(self):
        self.res()
        self.svg.show()

    

    def graph(gr,iter=1000, distance = 200):
        #vector class to help vector calculations
        class vt:
            
            def ort(posses, neigbours):
                x,y=0,0
                for i in neigbours:
                    x += posses[i][0]
                    y += posses[i][1]
                x /= len(neigbours)
                y /= len(neigbours)
                return [x,y]
            
            def go(pos1,pos2,dist):
                x = pos1[0] - pos2[0]
                y = pos1[1] - pos2[1]
                length = math.sqrt(x**2+y**2)
                return [
                    pos1[0] - x/length * dist,
                    pos1[1] - y/length * dist
                ]
            def len(pos1,pos2):
                x = pos1[0] - pos2[0]
                y = pos1[1] - pos2[1]
                return math.sqrt(x**2+y**2)
                 
            def norm(pos1,pos2):
                x = pos1[0] - pos2[0]
                y = pos1[1] - pos2[1]
                length = math.sqrt(x**2+y**2)
                return [x/length, y/length]
        
        #create svg object and replace points randomly
        liste = []
        svg = Svg([0,0])
        for i in range(len(gr["points"])):
            pos = [rd.randint(500,600),rd.randint(500,600)]
            liste.append(pos)
        
        #add list of neigbours for every vertices
        gr["list"] = []
        for j in range(len(gr["points"])):
            jnci = []
            for i in gr["joints"]:
                if j in i:
                    if i[0] == j: jnci.append(i[1])
                    else: jnci.append(i[0])
            gr["list"].append(jnci)

        for asd in range(iter):
            for i in range(len(gr["points"])):
                for j in range(i+1,len(gr["points"])):
                    if j in gr["list"][i]:
                        if vt.len(liste[i], liste[j]) > distance+5:
                            temp = vt.norm(liste[i], liste[j])
                            liste[i][0] -= temp[0] * 4
                            liste[i][1] -= temp[1] * 4
                            liste[j][0] += temp[0] * 4
                            liste[j][1] += temp[1] * 4
                        if vt.len(liste[i], liste[j]) < distance:
                            temp = vt.norm(liste[i], liste[j])
                            liste[i][0] += temp[0] * 1
                            liste[i][1] += temp[1] * 1
                            liste[j][0] -= temp[0] * 1
                            liste[j][1] -= temp[1] * 1
                    else:
                        if vt.len(liste[i], liste[j]) < distance*2:
                            temp = vt.norm(liste[i], liste[j])
                            liste[i][0] += temp[0] * 1
                            liste[i][1] += temp[1] * 1
                            liste[j][0] -= temp[0] * 1
                            liste[j][1] -= temp[1] * 1
        for i in range(len(liste)):
            if liste[i][0] < 0:
                for j in range(len(liste)):
                    liste[j][0] -= liste[i][0]
            if liste[i][1] < 0:
                for j in range(len(liste)):
                    liste[j][1] -= liste[i][1]
        #add all vertices and edges in svg
        for i in range(len(gr["points"])):
            svg.node(gr["points"][i],liste[i])
        for i in gr["joints"]:
            svg.bag(liste[i[0]], liste[i[1]])
        gr["pos"] = liste

        #also show it
        svg.show()

        return svg
    def real_quick(gr):
        svg = Svg([0,0])
         #add all vertices and edges in svg
        for i in range(len(gr["points"])):
            svg.node(gr["points"][i],gr["pos"][i])
        for i in gr["joints"]:
            svg.bag(gr["pos"][i[0]], gr["pos"][i[1]])

        #also show it
        svg.show()

