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
 
 ### ● 已知:
|Stuff|Protein|fat|Fibre|Salt

  
 ## (二)數學模型
  ### ● 符號設定
 - arcs:所有可能的運輸路線<br>
  
 - nodes:所有運輸路線上的城市<br>
  
 - commodities:所有等待運輸的產品<br>
  
 ### ● 參數設定
 - cost[h,i,j]:商品h從城市i到城市j的運輸成本<br>
  
 - capacity[i,j]:從城市i到城市j 的運能<br>
  
 - inflow[h,j]:商品h在城市j的生產量或需求量<br>
 
 ### ● 決策變數
 - flow[h,i,j]:商品h從城市i到城市j的運輸總量
 
 ### ● 數學式
 <img src="https://github.com/wurmen/Gurobi-Python/blob/master/python-gurobi%20%20model/picture/Netflow%20problem/netflow%20problem%20model.PNG"  width=750>







## (三)Python+Gurobi

#### ※完整程式碼可點擊[這裡](https://github.com/wurmen/Gurobi-Python/blob/master/python-gurobi%20%20model/Netflow%20problem.py)

## Import gurobipy


```python
from gurobipy import *
```

## Add parameters

- 定義兩種商品，以及包含五個節點六條路徑的網絡結構，形成commodities與nodes兩個列表
- 利用multidict函數初始化arcs與capacity，將arcs轉入tuplelist





```python
commodities = ['Pencils', 'Pens']
nodes = ['Detroit', 'Denver', 'Boston', 'New York', 'Seattle']

arcs, capacity = multidict({
  ('Detroit', 'Boston'):   100,
  ('Detroit', 'New York'):  80,
  ('Detroit', 'Seattle'):  120,
  ('Denver',  'Boston'):   120,
  ('Denver',  'New York'): 120,
  ('Denver',  'Seattle'):  120 })
arcs = tuplelist(arcs)
```

- 建立每個商品在每條路徑的運輸成本數據，以及每個節點的生產或需求量
- 透過cost[h,i,j]來索引運輸成本
- 透過inflow[h,j]來索引每個節點的生產或需求量


```python
cost = {
  ('Pencils', 'Detroit', 'Boston'):   10,
  ('Pencils', 'Detroit', 'New York'): 20,
  ('Pencils', 'Detroit', 'Seattle'):  60,
  ('Pencils', 'Denver',  'Boston'):   40,
  ('Pencils', 'Denver',  'New York'): 40,
  ('Pencils', 'Denver',  'Seattle'):  30,
  ('Pens',    'Detroit', 'Boston'):   20,
  ('Pens',    'Detroit', 'New York'): 20,
  ('Pens',    'Detroit', 'Seattle'):  80,
  ('Pens',    'Denver',  'Boston'):   60,
  ('Pens',    'Denver',  'New York'): 70,
  ('Pens',    'Denver',  'Seattle'):  30 }

inflow = {
  ('Pencils', 'Detroit'):   50,
  ('Pencils', 'Denver'):    60,
  ('Pencils', 'Boston'):   -50,
  ('Pencils', 'New York'): -50,
  ('Pencils', 'Seattle'):  -10,
  ('Pens',    'Detroit'):   60,
  ('Pens',    'Denver'):    40,
  ('Pens',    'Boston'):   -40,
  ('Pens',    'New York'): -30,
  ('Pens',    'Seattle'):  -30 }
```

## Model


```python
# Create optimization model
m = Model('netflow')
```

## Add decision variables

- 創建字典flow來儲存決策變數
- 透過obj參數來設定決策變數的目標係數


```python
# Create variables
flow = {}
for h in commodities:
    for i,j in arcs:
        flow[h,i,j] = m.addVar(ub=capacity[i,j], obj=cost[h,i,j],
                               name='flow_%s_%s_%s' % (h, i, j))
m.update()
```

## Update


```python
m.update()
```

## Add constraints

- 加入運輸容量限制式
- 加入流量守恆限制式


```python
# Arc capacity constraints
for i,j in arcs:
    m.addConstr(quicksum(flow[h,i,j] for h in commodities) <= capacity[i,j],
                'cap_%s_%s' % (i, j))

# Flow conservation constraints
for h in commodities:
    for j in nodes:
        m.addConstr(
          quicksum(flow[h,i,j] for i,j in arcs.select('*',j)) +
              inflow[h,j] ==
          quicksum(flow[h,j,k] for j,k in arcs.select(j,'*')),
                   'node_%s_%s' % (h, j))
```

## Result

- 透過getAttr()函數取得模型m中決策變數flow的屬性值x，也就是決策變數flow的最佳解
- getAttr()函數詳細內容可點擊[這裡](https://www.gurobi.com/documentation/7.0/refman/py_model_getattr.html)


```python
# Compute optimal solution
m.optimize()

# Print solution
if m.status == GRB.Status.OPTIMAL:
    solution = m.getAttr('x', flow)
    for h in commodities:
        print('\nOptimal flows for %s:' % h)
        for i,j in arcs:
            if solution[h,i,j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h,i,j]))

```

    Optimize a model with 16 rows, 12 columns and 36 nonzeros
    Coefficient statistics:
      Matrix range     [1e+00, 1e+00]
      Objective range  [1e+01, 8e+01]
      Bounds range     [8e+01, 1e+02]
      RHS range        [1e+01, 1e+02]
    Presolve removed 16 rows and 12 columns
    Presolve time: 0.00s
    Presolve: All rows and columns removed
    Iteration    Objective       Primal Inf.    Dual Inf.      Time
           0    5.5000000e+03   0.000000e+00   0.000000e+00      0s
    
    Solved in 0 iterations and 0.01 seconds
    Optimal objective  5.500000000e+03
    
    Optimal flows for Pencils:
    Denver -> Seattle: 10
    Denver -> New York: 50
    Detroit -> Boston: 50
    
    Optimal flows for Pens:
    Denver -> Seattle: 30
    Detroit -> New York: 30
    Detroit -> Boston: 30
    Denver -> Boston: 10
    
 <div align=center>
 <img src="https://github.com/wurmen/Gurobi-Python/blob/master/python-gurobi%20%20model/picture/Netflow%20problem/netflow%20problem%20picture_final.PNG"  width="614" height="356"/>
 </div>
  

