#-*- coding:utf-8 -*-
from pulp import *

Ingredients = ['CHICKEN', 'BEEF', 'MUTTON', 'RICE', 'WHEAT', 'GEL']
costs = {'CHICKEN': 0.013, 
         'BEEF': 0.008, 
         'MUTTON': 0.010, 
         'RICE': 0.002, 
         'WHEAT': 0.005, 
         'GEL': 0.001}

proteinPercent = {'CHICKEN': 0.100, 
                  'BEEF': 0.200, 
                  'MUTTON': 0.150, 
                  'RICE': 0.000, 
                  'WHEAT': 0.040, 
                  'GEL': 0.000}

fatPercent = {'CHICKEN': 0.080, 
              'BEEF': 0.100, 
              'MUTTON': 0.110, 
              'RICE': 0.010, 
              'WHEAT': 0.010, 
              'GEL': 0.000}

fibrePercent = {'CHICKEN': 0.001, 
                'BEEF': 0.005, 
                'MUTTON': 0.003, 
                'RICE': 0.100, 
                'WHEAT': 0.150, 
                'GEL': 0.000}

saltPercent = {'CHICKEN': 0.002, 
               'BEEF': 0.005, 
               'MUTTON': 0.007, 
               'RICE': 0.002, 
               'WHEAT': 0.008, 
               'GEL': 0.000}

#定義問題
prob = LpProblem("The Whiskas Problem", LpMinimize)

#利用dictionary 加入變數
ingredient_vars = LpVariable.dicts("Ingr",Ingredients,0)

#加入目標式
prob += lpSum([costs[i]*ingredient_vars[i] for i in Ingredients])

#加入限制式
prob += lpSum([ingredient_vars[i] for i in Ingredients]) == 100 #總共100g
prob += lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 8.0 #至少有8g protein
prob += lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 6.0 #至少有6g fat
prob += lpSum([fibrePercent[i] * ingredient_vars[i] for i in Ingredients]) <= 2.0 #fibre不超過2g
prob += lpSum([saltPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.4 #salt不超過0.4g

#求解
prob.solve()

#查看目前解的狀態
print("Status:", LpStatus[prob.status])


#印出解及目標值
for v in prob.variables():
    print(v.name, "=", v.varValue)
print('obj=',value(prob.objective))
#印出解的另一種方式
# for i in Ingredients:
#   print(ingredient_vars[i],"=",ingredient_vars[i].value())

