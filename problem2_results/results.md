```text
Gurobi Optimizer version 11.0.3 build v11.0.3rc0 (win64 - Windows 11.0 (22631.2))

CPU model: 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, instruction set [SSE2|AVX|AVX2|AVX512]
Thread count: 8 physical cores, 16 logical processors, using up to 16 threads

Optimize a model with 208736 rows, 380680 columns and 1188557 nonzeros
Model fingerprint: 0xdb01ad1e
Model has 6138 quadratic objective terms
Variable types: 14756 continuous, 365924 integer (351168 binary)
Coefficient statistics:
  Matrix range     [1e-01, 5e+02]
  Objective range  [7e+04, 1e+05]
  QObjective range [2e+02, 1e+06]
  Bounds range     [2e-01, 1e+00]
  RHS range        [3e-01, 1e+04]
Found heuristic solution: objective 4.712713e+08
Presolve removed 203962 rows and 364674 columns (presolve time = 5s) ...
Presolve removed 203960 rows and 364672 columns
Presolve time: 5.28s
Presolved: 4878 rows, 16110 columns, 34748 nonzeros
Found heuristic solution: objective 3.638524e+08
Variable types: 68 continuous, 16042 integer (15972 binary)
Found heuristic solution: objective 3.626224e+08

Root simplex log...

Iteration    Objective       Primal Inf.    Dual Inf.      Time
       0    2.5216361e+08   2.885375e+03   0.000000e+00      6s
     205    3.3604406e+08   0.000000e+00   0.000000e+00      6s

Root relaxation: objective 3.360441e+08, 205 iterations, 0.00 seconds (0.00 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 3.3604e+08    0   67 3.6262e+08 3.3604e+08  7.33%     -    5s
H    0     0                    3.381595e+08 3.3604e+08  0.63%     -    5s
H    0     0                    3.381462e+08 3.3604e+08  0.62%     -    5s
H    0     0                    3.381447e+08 3.3604e+08  0.62%     -    5s
H    0     0                    3.381398e+08 3.3604e+08  0.62%     -    5s
H    0     0                    3.381157e+08 3.3761e+08  0.15%     -    5s
     0     0 3.3808e+08    0   56 3.3812e+08 3.3808e+08  0.01%     -    5s

Cutting planes:
  Learned: 2
  Cover: 17
  MIR: 20
  StrongCG: 6
  Flow cover: 1
  RLT: 4

Explored 1 nodes (600 simplex iterations) in 5.79 seconds (4.89 work units)
Thread count was 16 (of 16 available processors)

Solution count 8: 3.38116e+08 3.3814e+08 3.38145e+08 ... 4.71271e+08

Optimal solution found (tolerance 1.00e-04)
Best objective 3.381157058074e+08, best bound 3.380848267376e+08, gap 0.0091%
Optimal Objective Value: 338115705.80735344

```