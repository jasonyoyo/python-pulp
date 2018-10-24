# Python+Pulp建模



## (一)最佳化流程
<img src="https://github.com/wurmen/Gurobi-Python/blob/master/python-gurobi%20%20model/picture/Python%2Bgurobi%E5%BB%BA%E6%A8%A1/%E6%9C%80%E4%BD%B3%E5%8C%96%E6%B5%81%E7%A8%8B.png" width="650">

## (二)問題產生
● 有x、y、z三個活動想在同一天舉辦<br>
● 場地總時間只有四個小時可使用<br>
● 活動z的價值為活動x及y的兩倍<br>
● 活動x與活動y至少要選一個舉辦<br>
● 活動x需花費1小時<br>
● 活動y需花費2小時<br>
● 活動z需花費3小時<br>
● 舉辦哪幾個活動可以使價值最大化?<br>

## (三)數學模式

<img src="https://github.com/wurmen/Gurobi-Python/blob/master/python-gurobi%20%20model/picture/Python%2Bgurobi%E5%BB%BA%E6%A8%A1/%E5%BB%BA%E6%A8%A1%E7%AF%84%E4%BE%8B.png" width="850">


## (四)Python+Pulp建模求解
## 1.建模流程
<img src="https://github.com/wurmen/Gurobi-Python/blob/master/python-gurobi%20%20model/picture/Python%2Bgurobi%E5%BB%BA%E6%A8%A1%E6%B5%81%E7%A8%8B.png" width="750">

## 2.Python+Pulp建模

<img src="https://github.com/wurmen/Gurobi-Python/blob/master/python-gurobi%20%20model/picture/Python%2Bgurobi%E5%BB%BA%E6%A8%A1/example.png" width="450">

## Import pulp


```python
from pulp import* #導入pulp函式庫
```

## Model


```python
model = pulp.LpProblem("value max", pulp.LpMaximize) # 建立一個新的model，命名為model
```

## Add decision variable


```python
x = pulp.LpVariable('x',lowBound = 0, cat='Binary')  #  pulp.LpVariable()加入變數
y = pulp.LpVariable('y',lowBound = 0, cat='Binary')
z = pulp.LpVariable('z',lowBound = 0, cat='Binary')
```



## Add objective and constraints


```python
# model += 設置目標函數
model += x+y+2*z

# model += 加入限制式
model += x+2*y+3*z <= 4
model += x+y >= 1
```








## Result

```python
model.solve()  # mmodel.solve()求解

# 透過屬性varValue,name顯示決策變數名字及值
for v in model.variables():
    print(v.name, "=", v.varValue)
    
# 透過屬性value(model.objective)顯示最佳解
print('obj=',value(model.objective))
```
```
x = 1.0
y = 0.0
z = 1.0
obj= 3.0
```
