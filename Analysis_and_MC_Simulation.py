# -*- coding: utf-8 -*-
# analysis of a drill path, for each operation there is one line in the file
# for each operation a couple of data are given:
# start depth, end depth, duration
# a couple of classifications: class type, operation, major operation, phase and error code
# compares costs for two alternating technical solutions
# 1st one: relatively low  costs, but long drilling time
# 2nd one: relatively high costs, but short drilling time

import numpy as np
import matplotlib.pyplot as plt
import scipy
import random

def opener(n): # opens file and read data, data are given as welln.csv
    f = open('well' + str(n) + '.csv','r')
    data = []
    for line in f:
        helper = []
        every = line.split('\n')[0].split(';')
        helper.append(float(every[0])) # start MD
        helper.append(float(every[1])) # end MD
        helper.append(float(every[2])) # duration
        helper.append(every[6]) # class
        helper.append(every[7]) # operation
        helper.append(every[8]) # major operation
        helper.append(every[9]) # phase
        helper.append(every[10]) # trouble type
        data.append(helper)
    f.close()
    return data

def a1(data): # for a well get ratio productive time/non-productive time
    prod = 0
    nonprod = 0
    for i in data:
        if i[0] == i[1]:
            nonprod += i[2]
        else:
            prod += i[2]
    print prod/nonprod

def a2(data): # average rate of penetration for each phase
    (min6H,max6H,max4H) = minmax(data)
    time6H = 0
    time4H = 0
    for i in data:
        if i[6] == '6H' and i[0] != max6H:
            time6H += i[2]
        if i[6] == '4H' and i[0] != max4H:
            time4H += i[2]
    print 1/(time6H/(max6H-min6H) *24)
    print 1/(time4H/(max4H-max6H) *24)

def minmax(data): # find minimum and maximum depth
    max6H = 0
    min6H = 500   
    for i in data:
        if i[6] == '6H' and i[1] > max6H:
            max6H = i[1]
        if i[6] == '6H' and i[0] < min6H:
            min6H = i[0]
    max4H = data[-1][1]
    return (min6H,max6H,max4H)


def a3(data): # find reaming time per meter of hole section
    (min6H,max6H,max4H) = minmax(data)
    ream6H = 0
    ream4H = 0
    for i in data:
        if i[6] == '6H' and i[4] == 'RW':
            ream6H += i[2]
        if i[6] == '4H' and i[4] == 'RW':
            ream4H += i[2]
    print ream6H/(max6H-min6H) *24
    print ream4H/(max4H-max6H) *24

def a4(data): # find top 5 of error codes and the related total time for 1 well
    dic = {}
    for i in data:
        if i[7] not in dic:
            dic[i[7]] = 0
        dic[i[7]] += i[2]
    rev = {}
    numbers = []
    for i in dic:
        if i != 'NT':
            rev[dic[i]] = i
            numbers.append(dic[i])
    numbers.sort()
    for i in range(1,6):
        print rev[numbers[-i]] + ': ' + str(24 * numbers[-i])
    return dic

def get(i): # do a1 - a4 for a specific well 
    data = opener(i)
    a1(data)
    a2(data)
    a3(data)
    a4(data)

def alltrouble(): # find top 5 of error codes and the related total time for all well
    data = opener(1) + opener(2) + opener(4) + opener(5) + opener(6)
    dic = a4(data)

def allROP(): # take ROP for both phases from all wells 
    ROP1 = []
    ROP2 = []
    data = opener(1) + opener(2) + opener(4) + opener(5) + opener(6)
    for i in data:
        if i[0] != i[1] and i[6] == '6H':
            ROP1.append(abs((i[1]-i[0])/i[2]/24))
        if i[0] != i[1] and i[6] == '4H':
            ROP2.append(abs((i[1]-i[0])/i[2]/24))
    x = np.asarray(ROP1)
    y = np.asarray(ROP2)
    #n, bins, patches = plt.hist(x, 20, range=(0,50))
    #plt.plot(n)
    #plt.xlabel('ROP [m/hr]')
    #plt.ylabel('PDF')
    #plt.title('distribution of ROP of DRLG1')
    #plt.show()  
    return (x,y)
        
(x,y) = allROP()
# estimate parameters according to distributions and build a generator
(ln11,ln12,ln13) = scipy.stats.triang.fit(x) #fitting parameters for ROP1
(ln21,ln22,ln23) = scipy.stats.lognorm.fit(y) #fitting parameters for ROP2
rop1 = scipy.stats.lognorm(ln11,ln12,ln13)
rop2 = scipy.stats.lognorm(ln21,ln22,ln23)

def problems(): #find number of problems that occur in a well 
    numprob = 0
    for i in (1,2,4,5,6):
        staying = {}
        data = opener(i)
        (min6H,max6H,max4H) = minmax(data)
        for j in data:
            if j[0] == j[1]:
                if j[0] not in staying:
                    staying[j[0]] = 0
                staying[j[0]] += j[2]
        for j in staying:
            if staying[j] != max6H and staying[j] != max4H and staying[j] > 2:
                numprob += 1
    return numprob-1 
        
def totaldepth(): #total depth
    counter = 0
    for i in (1,2,4,5,6):
        data = opener(i)
        (min6H,max6H,max4H) = minmax(data)
        counter += max4H - max6H
    return counter

def getMO1(): # read all values for MO1 from the data
    MO1 = []
    for i in (1,2,4,5,6):
        mo = 0
        data = opener(i)
        for j in data:
            if j[6] == 'COND' or j[6] == 'PS':
                mo += j[2]
        MO1.append(mo)
    x = np.asarray(MO1)
    #n, bins, patches = plt.hist(x, range=(0,4))
    #plt.plot(n)
    #plt.xlabel('MO1 [d]')
    #plt.ylabel('PDF')
    #plt.title('distribution of MO1')
    #plt.show()
    return(x) 

(tr1,tr2,tr3) = scipy.stats.triang.fit(getMO1()) #fitting parameters for MO1

def getMO2(): # read all values for MO2 from the data
    MO2 = []
    for i in (1,2,4,5,6):
        mo = 0
        data = opener(i)
        (min6H,max6H,max4H) = minmax(data)
        for j in data:
            if j[0] == max6H and j[1] == max6H:
                mo += j[2]
        MO2.append(mo)
    x = np.asarray(MO2)
    x[1] = 4.07
    #n, bins, patches = plt.hist(x)
    #plt.plot(n)
    #plt.xlabel('MO2 [d]')
    #plt.ylabel('PDF')
    #plt.title('distribution of MO2')
    #plt.show()
    return(x) 

(u11,u12) = scipy.stats.uniform.fit(getMO2()) #fitting parameters for MO2

def getMO3(): # read all values for MO3 from the data
    MO3 = []
    for i in (1,2,4,5,6):
        mo = 0
        data = opener(i)
        (min6H,max6H,max4H) = minmax(data)
        for j in data:
            if j[0] == max4H and j[1] == max4H:
                mo += j[2]
        MO3.append(mo)
    x = np.asarray(MO3)
    #n, bins, patches = plt.hist(x)
    #plt.plot(n)
    #plt.xlabel('MO3 [d]')
    #plt.ylabel('PDF')
    #plt.title('distribution of MO3')
    #plt.show()
    return(x) 

(u21,u22) = scipy.stats.uniform.fit(getMO3()) #fitting parameters for MO3

numbersimulations = 100 # how often is MC performed, time versus accuracy
s2s = scipy.stats.norm(loc =5.5*10**-4, scale =2.31*10**-6)
n1 = int(1100/18)
n2 = int(1500/18)
# calculate basis costs that occur at all drilling operations
casingcosts = (2600*110 + 1100*110)*1.1 # first section + second section
# (amount first section + amount second section)*price*safety/circulation factor
mudcosts = (1100*3.14*(5*0.0254)**2/4 + 1500*3.14*(4.75*0.0254)**2/4)*350*2 
# (amount first section + amount second section)*price*safety factor
cementcosts = (1100*3.14/4*(6.75*0.0254 - 5*0.0254)**2 + 2600*3.14/4*(4.75*0.0254 - 3.5*0.0254)**2)*420*1.5 
basecosts = casingcosts + mudcosts + cementcosts # sum of all basecosts

def montecarlo(): #MC simulation based on the distributions found above
    saver = []
    costs = [] # save costs for standard solutions
    costsalt = [] # save costs for alternative solution
    problems = [] # save number of problems for each run
    productive = []
    betteralt = 0
    for i in range(0,numbersimulations):
        prod = 0
        numberproblems = 0
        MO1 = scipy.stats.triang(tr1,tr2,tr3).rvs()
        MO2 = scipy.stats.uniform(u11,u12).rvs()
        MO3 = scipy.stats.uniform(u21,u22).rvs()
        total = MO1 + MO2 + MO3 
        totalalt = MO1 + MO2 + MO3 
        for j in range(0,n1): # 1st section
            total += 18/rop1.rvs()/24 + abs(s2s.rvs())
            totalalt += 0.8*18/rop1.rvs()/24 + abs(s2s.rvs())
            prod += 18/rop1.rvs()/24
        for j in range(0,n2): # 2nd section
             total += 18/rop2.rvs()/24 + abs(s2s.rvs())
             totalalt += 0.8*18/rop1.rvs()/24 + abs(s2s.rvs())
             rand = random.random()
             prod += 18/rop1.rvs()/24
             if rand < 0.0392: # problem
                 total += 2.0*1100/86400 + 2.0*(j+1)*18/86400/0.5 +1
                 for k in range(0,2*(n1+j+1)): #2S2 up- and downwards
                     total += abs(s2s.rvs())
                     totalalt += abs(s2s.rvs())
                 numberproblems += 1
        costs.append(43000.0*int(total)+12000+numberproblems*8000+basecosts) 
        costsalt.append(43000.0*int(totalalt)+23000+numberproblems*18000+basecosts)
        if costsalt[i] < costs[i]: # compare standard and alternative costs
             betteralt += 1.0
        saver.append(total)
        problems.append(numberproblems)
        productive.append(prod/(total-prod))
    return (saver,problems,costs,costsalt,betteralt)
    
(v,w,x,y,z) = montecarlo()

n, bins, patches = plt.hist(x,range = (0,3000000))
plt.plot(n)
plt.xlabel('costs [MU]')
plt.ylabel('PDF')
plt.title('distribution of alternative total costs')
plt.show()
