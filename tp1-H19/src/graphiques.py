import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

os.chdir("S:/OneDrive - Universite de Montreal/DESS/INF8775/tp1-H19/")
data = pd.read_csv("tableau.csv")

sortingNames = ["Counting", "Quick", "QuickSeuil", "QuickRandomSeuil"]
colors = ["b", "r", "g"]

#Tests de puissances
for i in range(4):
    plt.clf()
    fig = plt.figure()   
    ax = fig.add_subplot(111)
    ax.set_xlabel('log n')
    ax.set_ylabel('log (temps)')
    for j in range(3):
        x = np.array(np.log(data.iloc[:,0]))
        y = np.array(np.log(data.iloc[:,(i*3+j+1)]))
        ax.scatter(x, y, c = colors[j], label = list(data)[i*3+j+1])
        try:
            ax.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),\
                    c= colors[j])
        except:
            pass
    ax.legend(loc="lower right")
    plt.show()
    fig.savefig("Puissance"+ str(sortingNames[i]))

#Tests de rapport  

nModif = [data.iloc[:,0], data.iloc[:,0]*np.log(data.iloc[:,0]),\
           data.iloc[:,0]**2]
nNames = ["n","nlog(n)", "n**2"]

#Meilleur cas et cas moyen
targetN1 = [[0,None,0],[1,1,1],[1,1,1], [1,1,1]]

for i in range(4):
    plt.clf()
    fig = plt.figure()   
    ax = fig.add_subplot(111)
    ax.set_xlabel("Taille des exemplaires (n)")
    ax.set_ylabel('Temps / ' + str(nNames[targetN1[i][0]])) 
    maxY = 0
    for j in range(3):
        if targetN1[i][j] != None:
            x = np.array(data.iloc[:,0])
            y = np.array(data.iloc[:,(i*3+j+1)]/nModif[targetN1[i][j]])
            ax.scatter(x, y, c = colors[j], label = list(data)[i*3+j+1])
        if max(y) > maxY:
            maxY = max(y)
    ax.set_ylim(ymax = 1.5*maxY, ymin = 0)
    ax.legend(loc="lower right")
    plt.show()
    fig.savefig("Rapport"+ str(sortingNames[i]))

#Counting2 rapport
plt.clf()
fig = plt.figure()   
ax = fig.add_subplot(111)
ax.set_xlabel("Taille des exemplaires (n)")
ax.set_ylabel('Temps / n') #+ str(nNames[targetN1[i]]))
x = np.array(data.iloc[:,0])
y = np.array(data.iloc[:,2]/nModif[0])
ax.scatter(x, y, c = colors[1], label = list(data)[2])
ax.set_ylim(ymax = 1.5*max(y), ymin = 0)
ax.legend(loc="lower right")
plt.show()
fig.savefig("RapportCounting2")

#Pire cas

targetN1 = [[0,0,0],[2,2,2],[2,2,2], [2,2,2]]

for i in range(1,4):
    plt.clf()
    fig = plt.figure()   
    ax = fig.add_subplot(111)
    ax.set_xlabel("Taille des exemplaires (n)")
    ax.set_ylabel('Temps / ' + str(nNames[targetN1[i][0]])) 
    maxY = 0
    for j in range(3):
        if targetN1[i][j] != None:
            x = np.array(data.iloc[:,0])
            y = np.array(data.iloc[:,(i*3+j+1)]/nModif[targetN1[i][j]])
            ax.scatter(x, y, c = colors[j], label = list(data)[i*3+j+1])
        if max(y) > maxY:
            maxY = max(y)
    ax.set_ylim(ymax = 1.5*maxY, ymin = 0)
    ax.legend(loc="lower right")
    plt.show()
    fig.savefig("RapportPire"+ str(sortingNames[i]))



#Tests de constance
targetN3 = [[0,None,0],[1,1,1],[1,1,1], [1,1,1]]

for i in range(4):
    plt.clf()
    fig = plt.figure()   
    ax = fig.add_subplot(111)
    ax.set_xlabel(nNames[targetN3[i][0]])
    ax.set_ylabel('Temps')
    for j in range(3):
        if targetN3[i][j] != None:
            x = np.array(nModif[targetN3[i][j]])
            y = np.array(data.iloc[:,(i*3+j+1)])
            ax.scatter(x, y, c = colors[j], label = list(data)[i*3+j+1])
            try:
                ax.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))\
                        (np.unique(x)), c= colors[j])
            except:
                pass
    ax.legend(loc="lower right")
    plt.show()  
    fig.savefig("Constante"+ str(sortingNames[i]))

#Counting2 constance
plt.clf()
fig = plt.figure()   
ax = fig.add_subplot(111)
ax.set_xlabel("n")
ax.set_ylabel('Temps')
x = np.array(nModif[0])
y = np.array(data.iloc[:,2])
ax.scatter(x, y, c = colors[1], label = list(data)[2])
ax.legend(loc="lower right")
plt.show()  
fig.savefig("ConstanteCounting2")


    
