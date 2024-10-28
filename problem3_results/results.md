# constrain choice 1
- assume all constrain from problem 2
- add budge constrain that is less than 100,000,000
- for the description in the problem,we drop the region with social coverage ratio that is larger than 1
![img.png](..%2Fvisuals%2Fimg.png)



```text
CPU model: 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, instruction set [SSE2|AVX|AVX2|AVX512]
Thread count: 8 physical cores, 16 logical processors, using up to 16 threads

Optimize a model with 307739 rows, 708616 columns and 2971421 nonzeros
Model fingerprint: 0x2b139f3a
Variable types: 62416 continuous, 646200 integer (646200 binary)
Coefficient statistics:
  Matrix range     [2e-04, 9e+02]
  Objective range  [7e-05, 2e+02]
  Bounds range     [5e-02, 1e+00]
  RHS range        [1e-02, 1e+04]
Presolve removed 68620 rows and 157804 columns
Presolve time: 0.18s

Explored 0 nodes (0 simplex iterations) in 0.56 seconds (0.54 work units)
Thread count was 1 (of 16 available processors)

Solution count 0
No other solutions better than -1e+100

Model is infeasible
Best objective -, best bound -, gap -
No optimal solution found

```