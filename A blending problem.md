# A blending problem

 ##### ※參考資料: https://pythonhosted.org/PuLP/CaseStudies/a_blending_problem.html 
  
 ## (一)問題描述
此為Pulp的官網範例，在此加以整理介紹。

 ### ● 題目:
 有一家公司要生產貓飼料，希望能在滿足營養的情況下，成本越低越好，貓的飼料中含有Chicken、Beef、MUTTON、Rice、Wheat bran、Gel六種配料。它們的成本分別為$ 0.013, $ 0.008, $ 0.010, $ 0.002, $ 0.005, $ 0.001(All costs are per gram.) ，每100g的貓飼料成品中，至少需要有8g protein、6g fat，但是fibre不能超過2g、salt不能超過0.4g。
 
 ### ● 已知:
|Stuff|Protein|fat|Fibre|Salt
|-----|-----|-----|-----|-----|
|Chicken|0.1|0.08|0.001|0.002|
|Beef|0.2|0.1|0.005|0.005|
|Rice|0|0.01|0.1|0.002|
|Wheat bran|0.04|0.01|0.15|0.008|
  
 ### ● 目標:
 - 最小化總成本

### ● 限制:
 每100g的貓飼料成品中，
 - 至少需要有8g protein
 - 至少需要有6g fat
 - fibre不能超過2g
 - salt不能超過0.4g
 

  
 ## (二)數學模型
 
 ### ● 參數設定
 - proteinPercent_i : 配料 i 中的proteinPercent
 - fatPercent_i : 配料 i 中的fatPercent
 - fibrePercent_i : 配料 i 中的fibrePercent
 - saltPercent_i : 配料 i 中的saltPercent
 
 ### ● 決策變數
 - Ingr_i : 每100g貓飼料中，配料 i 的含量
 
 ### ● 數學式

- 目標式 : Min:Σcost_i * Ingr_i

- 限制式:
- 總重為100g : ΣIngr_i=100
- 至少需要有8g protein : ΣproteinPercent_i * Ingr_i ≧ 8
- 至少需要有6g fat : ΣfatPercent_i * Ingr_i ≧ 6
- fibre不能超過2g : ΣfibrePercent_i * Ingr_i ≦ 2
- salt不能超過0.4g : ΣsaltPercent_i * Ingr_i ≦ 0.4
 






## (三)Python+Pulp


## Import pulp


```python
from pulp import *
```

## Add parameters

- 定義六種配料
- 利用dictionary將價錢以及各營養素比例存入



```python
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
```




## Model

- 定義問題
```python
prob = LpProblem("The Whiskas Problem", LpMinimize)
```

## Add decision variables

- 創建字典來儲存決策變數

```python
ingredient_vars = LpVariable.dicts("Ingr",Ingredients,0)
```

## Add objective function

```python
#加入目標式
prob += lpSum([costs[i]*ingredient_vars[i] for i in Ingredients])
```

## Add constraints


```python
prob += lpSum([ingredient_vars[i] for i in Ingredients]) == 100 #總共100g
prob += lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 8.0 #至少有8g protein
prob += lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 6.0 #至少有6g fat
prob += lpSum([fibrePercent[i] * ingredient_vars[i] for i in Ingredients]) <= 2.0 #fibre不超過2g
prob += lpSum([saltPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.4 #salt不超過0.4g

```


## solve

```python
prob.solve()
```

##  Show Result


```python
#查看目前解的狀態
print("Status:", LpStatus[prob.status])


#印出解及目標值
for v in prob.variables():
    print(v.name, "=", v.varValue)
print('obj=',value(prob.objective))
#解的另一種方式
# for i in Ingredients:
#   print(ingredient_vars[i],"=",ingredient_vars[i].value())

```
```python
 Status: Optimal
 Ingr_BEEF = 60.0
 Ingr_CHICKEN = 0.0
 Ingr_GEL = 40.0
 Ingr_MUTTON = 0.0
 Ingr_RICE = 0.0
 Ingr_WHEAT = 0.0
 obj= 0.52

```

  
    

  

