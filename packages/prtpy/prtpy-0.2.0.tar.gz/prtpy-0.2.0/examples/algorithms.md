# Algorithms

## Approximate algorithms
Currently, `prtpy` supports a single approximate algorithm - `greedy` - based on [Greedy number partitioning](https://en.wikipedia.org/wiki/Greedy_number_partitioning).
It is very fast, and attains very good result on random instances with many items and bins.


```python
import prtpy
import numpy as np
from time import perf_counter

values = np.random.randint(1,10, 100000)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.approx.greedy, numbins=9, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[55551. 55551. 55551. 55551. 55551. 55550. 55550. 55550. 55550.]
         0.28302570000000005 seconds
```



## Exact algorithms
`prtpy` supports several exact algorithms. By far, the fastest of them uses integer linear programming.
It can handle a relatively large number of items when there are at most 4 bins.

```python
values = np.random.randint(1,10, 100)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.exact.integer_programming, numbins=4, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[132. 133. 116. 144.]
         0.6141641999999998 seconds
```



The default solver is CBC. You can choose another, potentially faster solver. 
For example, if you install the XPRESS solver, you can try the following (it will return an error if XPRESS is not installed):

```python
# import cvxpy
# print(prtpy.partition(algorithm=prtpy.exact.integer_programming, numbins=4, items=values, outputtype=prtpy.out.Sums, solver=cvxpy.XPRESS))
```



Another algorithm is dynamic programming. It is fast when there are few bins and the numbers are small, but quite slow otherwise.

```python
values = np.random.randint(1,10, 20)
start = perf_counter()
print(prtpy.partition(algorithm=prtpy.exact.dynamic_programming, numbins=3, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
(35, 35, 36)
         0.05837340000000024 seconds
```



The *complete greedy* algorithm (Korf, 1995) is also available, though it is not very useful without further heuristics and optimizations.

```python
start = perf_counter()
values = np.random.randint(1,10, 10)
print(prtpy.partition(algorithm=prtpy.exact.complete_greedy, numbins=2, items=values, outputtype=prtpy.out.Sums))
print(f"\t {perf_counter()-start} seconds")
```

```
[28. 28.]
         0.009200299999999828 seconds
```


---
Markdown generated automatically from [algorithms.py](algorithms.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-02-14.
