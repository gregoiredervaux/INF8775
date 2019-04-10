# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 15:01:31 2019

@author: Marc
"""

import pandas as pd
import numpy as np
import math
import os
import time

data = pd.read_csv("./exemplaires/LEGO_50_100_1000", sep = "\n|  | ",
                   skiprows=1, header = None, engine='python')



nbTypesLegos = len(data.iloc[0, :])
nbModels = int(data.iloc[2,0])

myLegos = np.array(data.iloc[0,:])
models = np.array(data.iloc[3:,:])

def gluttonFunction(myLegos, models, nbModels, nbTypesLegos):
    priceList = np.array(data.iloc[1,:])
    #pricebyModel = np.dot(models, priceList)/np.sum(models, axis = 1)
    bestSolution = None
    bestPrice = float('inf')
    
    #pricebyModel = np.dot(models, priceList)
    
    for j in range(25):
        currentLegos = myLegos[:]    
        totalRemaining = float('inf')
        for repetition in range(10):
            
            #selectionOrder = np.random.choice(range(len(pricebyModel)), 
                                          #size =len(pricebyModel), 
                                          #p = (pricebyModel)/sum(pricebyModel),
                                          #replace = False)
            
            selectionOrder = np.random.choice(range(nbModels), size =nbModels,
                                              p = np.sum(models, axis = 1)/
                                              sum(np.sum(models, axis = 1)))
            
            solution = []
            currentLegos = myLegos[:]
        
            while len(selectionOrder) > 0:
                for idx in selectionOrder:
                    if sum((currentLegos - models[idx,:]) < 0) < 1 :
                        currentLegos = currentLegos - models[idx,:]
                        solution.append(idx)
                    else: 
                        selectionOrder = np.delete(selectionOrder, 
                                                   np.where(selectionOrder == idx)[0])
                        pass
            if sum(currentLegos) < totalRemaining:
                totalRemaining = sum(currentLegos)
                partialSolution = solution[:]
                remainingLegos = currentLegos[:]
        
        currentLegos = remainingLegos[:]
        solution = partialSolution[:]     
        
        while sum(currentLegos) > 0:        
            #print(solution, sum(currentLegos))
            minCostRatio = float('inf')     
            for idx in range(nbModels):
                diff = (currentLegos[:] - models[idx,])
                nbReduced = np.array(diff[:])
                nbReduced[nbReduced < 0] = 0
                nbReduced = sum(currentLegos - nbReduced)
                if nbReduced > 0:
                    for i in range(len(diff)):
                        if diff[i] > 0:
                            diff[i] = 0
                        else:
                            diff[i] = np.abs(diff[i])
                    additionalCost = np.dot(diff, priceList) 
                    costRatio = additionalCost/nbReduced
                    if math.isnan(costRatio):
                        costRatio = float('inf')
                    if costRatio < minCostRatio:
                        new_idx = idx
                        minCostRatio = costRatio
            solution.append(new_idx)
            currentLegos = currentLegos[:] - models[new_idx,]
            currentLegos[currentLegos < 0] = 0
    
        test = myLegos[:]
    
        for idx in solution:
            test = test - models[idx,] 
    
        totalPrice = np.dot(abs(test), priceList)
        #nbLegos = sum(np.abs(test))
        if totalPrice < bestPrice:
            bestPrice = totalPrice
            bestSolution = solution
            print(bestSolution, bestPrice)
        
    return(bestSolution, bestPrice)



def heuristicFunction (current_solution, myLegos, models, nbModels, 
                       nbTypesLegos):
    
    overallTime = time.time()
    priceList = np.array(data.iloc[1,:])
    pricebyModel = np.dot(models, priceList)/np.sum(models, axis = 1)
    solution = current_solution[0]
    
    startT = time.time()
    replacementSize = int(len(solution)/2)
    
    while True: 
        
        latency = time.time() - startT
        if latency > 10: 
            replacementSize = int(replacementSize*0.80)
            startT = time.time()
            if replacementSize < 4:
                replacementSize = int(len(solution)/2)
            print(replacementSize)
        totalLegos = np.zeros(nbTypesLegos)
        
        for idx in solution: 
            totalLegos = totalLegos + models[idx,]        
        bestPrice = np.dot((totalLegos - myLegos), priceList)
        toRemove = np.random.choice(len(solution), size = replacementSize, 
            replace = False) 
       
        idxToRemove = [] 
        for i in toRemove: 
            idxToRemove.append(solution[i])
        
        removedLegos = np.sum(models[idxToRemove,], axis = 0)
        
        tempLegos = totalLegos - myLegos - removedLegos

        for i in range(len(tempLegos)):
            if tempLegos[i] >= 0:
                tempLegos[i] = 0
            else:
                tempLegos[i] = np.abs(tempLegos[i])
        currentLegos = np.array(tempLegos[:])
        
        new_solution = []
        while sum(currentLegos) > 0:        
            minCostRatio = float('inf')     
            for idx in range(nbModels):
                diff = (currentLegos[:] - models[idx,])
                nbReduced = np.array(diff[:])
                nbReduced[nbReduced < 0] = 0
                nbReduced = sum(currentLegos - nbReduced)
                if nbReduced > 0:
                    for i in range(len(diff)):
                        if diff[i] > 0:
                            diff[i] = 0
                        else:
                            diff[i] = np.abs(diff[i])
                    additionalCost = np.dot(diff, priceList) 
                    costRatio = additionalCost/nbReduced
                    if math.isnan(costRatio):
                        costRatio = float('inf')
                    if costRatio < minCostRatio:
                        new_idx = idx
                        minCostRatio = costRatio
            new_solution.append(new_idx)
            currentLegos = currentLegos[:] - models[new_idx,]
            currentLegos[currentLegos < 0] = 0

        new_solution = np.append(new_solution, np.delete(solution, toRemove))
        
        newTotalLegos = np.zeros(nbTypesLegos)
        for idx in new_solution: 
            newTotalLegos = newTotalLegos + models[idx,]
        
        newPrice = np.dot((newTotalLegos - myLegos), priceList)
        
        if newPrice < bestPrice:
            startT = time.time()
            bestPrice = newPrice
            solution = new_solution[:]
            print(solution, bestPrice)
       
        if time.time() - overallTime > 180:
            break
        
s_time = time.time()      
glutton_solution = gluttonFunction(myLegos, models, nbModels, nbTypesLegos)
time.time() - s_time

heuristicFunction(glutton_solution, myLegos, models, nbModels, nbTypesLegos)

#[ 6 25 62 62 32 48  4 94  1  1 48 95  4  6 15 36  1 73 57  2 31 97 62 69
# 28 93 40 68 89 11 31 61 51 12 20] 598.0