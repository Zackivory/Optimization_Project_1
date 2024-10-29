# constrain choice 1
- assume all constrain from problem 2
- add budge constrain that is less than 100,000,000
- for the description in the problem,we drop the region with social coverage ratio that is larger than 1
![img.png](..%2Fvisuals%2Fimg.png)



```text
Gurobi Optimizer version 11.0.3 build v11.0.3rc0 (win64 - Windows 11.0 (22631.2))

CPU model: 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, instruction set [SSE2|AVX|AVX2|AVX512]
Thread count: 8 physical cores, 16 logical processors, using up to 16 threads

Optimize a model with 346412 rows, 708616 columns and 3109835 nonzeros
Model fingerprint: 0x3afa598e
Variable types: 15604 continuous, 693012 integer (693012 binary)
Coefficient statistics:
  Matrix range     [2e-04, 9e+02]
  Objective range  [7e-05, 2e+02]
  Bounds range     [2e-01, 1e+00]
  RHS range        [1e-02, 1e+04]
Presolve removed 68587 rows and 157800 columns
Presolve time: 0.15s

Explored 0 nodes (0 simplex iterations) in 0.48 seconds (0.56 work units)
Thread count was 1 (of 16 available processors)

Solution count 0
No other solutions better than -1e+100

Model is infeasible
Best objective -, best bound -, gap -
No optimal solution found
```

