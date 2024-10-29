```text
Gurobi Optimizer version 11.0.3 build v11.0.3rc0 (win64 - Windows 11.0 (22631.2))

CPU model: 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, instruction set [SSE2|AVX|AVX2|AVX512]
Thread count: 8 physical cores, 16 logical processors, using up to 16 threads

Optimize a model with 343116 rows, 708616 columns and 2091547 nonzeros
Model fingerprint: 0x4d450193
Model has 46812 quadratic objective terms
Variable types: 15604 continuous, 693012 integer (693012 binary)
Coefficient statistics:
  Matrix range     [1e-01, 9e+02]
  Objective range  [7e+04, 1e+05]
  QObjective range [4e+04, 2e+06]
  Bounds range     [2e-01, 1e+00]
  RHS range        [3e-01, 1e+04]
Found heuristic solution: objective 6.487111e+08
Presolve removed 317313 rows and 632189 columns (presolve time = 22s) ...
Presolve removed 317312 rows and 632188 columns
Presolve time: 22.47s
Presolved: 27673 rows, 78297 columns, 170395 nonzeros
Variable types: 2492 continuous, 75805 integer (75805 binary)
Deterministic concurrent LP optimizer: primal and dual simplex
Showing primal log only...


Root simplex log...

Iteration    Objective       Primal Inf.    Dual Inf.      Time
       0    1.9190410e+08   1.039709e+02   2.547014e+08     23s
Concurrent spin time: 0.00s

Solved with dual simplex

Root simplex log...

Iteration    Objective       Primal Inf.    Dual Inf.      Time
    2794    4.1300388e+08   0.000000e+00   0.000000e+00     23s

Use crossover to convert LP symmetric solution to basic solution...

Root crossover log...

       0 DPushes remaining with DInf 0.0000000e+00                23s

   19253 PPushes remaining with PInf 0.0000000e+00                23s
       0 PPushes remaining with PInf 0.0000000e+00                23s

  Push phase complete: Pinf 0.0000000e+00, Dinf 5.0670045e+04     23s


Root simplex log...

Iteration    Objective       Primal Inf.    Dual Inf.      Time
   24123    4.1300388e+08   0.000000e+00   5.067005e+04     23s
   24130    4.1300388e+08   0.000000e+00   0.000000e+00     23s

Root relaxation: objective 4.130039e+08, 24130 iterations, 0.19 seconds (0.14 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 4.1300e+08    0 1950 6.4871e+08 4.1300e+08  36.3%     -   26s
H    0     0                    4.272428e+08 4.1300e+08  3.33%     -   26s
H    0     0                    4.251636e+08 4.1300e+08  2.86%     -   26s
H    0     0                    4.251544e+08 4.1300e+08  2.86%     -   26s
H    0     0                    4.228206e+08 4.1300e+08  2.32%     -   28s
H    0     0                    4.227637e+08 4.1300e+08  2.31%     -   29s
H    0     0                    4.227079e+08 4.1300e+08  2.30%     -   29s
     0     0 4.2240e+08    0  465 4.2271e+08 4.2240e+08  0.07%     -   29s
H    0     0                    4.226394e+08 4.2240e+08  0.06%     -   30s
     0     0 4.2240e+08    0  395 4.2264e+08 4.2240e+08  0.06%     -   30s
     0     0 4.2240e+08    0  290 4.2264e+08 4.2240e+08  0.06%     -   30s
     0     0 4.2240e+08    0  297 4.2264e+08 4.2240e+08  0.06%     -   30s
     0     0 4.2240e+08    0  224 4.2264e+08 4.2240e+08  0.06%     -   30s
     0     0 4.2240e+08    0  178 4.2264e+08 4.2240e+08  0.06%     -   30s
     0     0 4.2243e+08    0  110 4.2264e+08 4.2243e+08  0.05%     -   30s
     0     0 4.2248e+08    0   98 4.2264e+08 4.2248e+08  0.04%     -   31s
     0     0 4.2249e+08    0   95 4.2264e+08 4.2249e+08  0.04%     -   31s
     0     0 4.2250e+08    0  117 4.2264e+08 4.2250e+08  0.03%     -   31s
     0     0 4.2252e+08    0  117 4.2264e+08 4.2252e+08  0.03%     -   31s
     0     0 4.2252e+08    0  110 4.2264e+08 4.2252e+08  0.03%     -   32s
     0     0 4.2252e+08    0  104 4.2264e+08 4.2252e+08  0.03%     -   34s
H    0     0                    4.226262e+08 4.2252e+08  0.03%     -   35s
H    0     0                    4.225798e+08 4.2252e+08  0.01%     -   35s
H    0     0                    4.225786e+08 4.2252e+08  0.01%     -   37s
     0     0 4.2252e+08    0  104 4.2258e+08 4.2252e+08  0.01%     -   38s

Cutting planes:
  Learned: 283
  Gomory: 33
  Lift-and-project: 4
  Cover: 73
  Implied bound: 4
  MIR: 198
  StrongCG: 89
  Flow cover: 18
  GUB cover: 13
  RLT: 536
  Relax-and-lift: 21
  BQP: 55

Explored 1 nodes (29998 simplex iterations) in 38.89 seconds (21.54 work units)
Thread count was 16 (of 16 available processors)

Solution count 10: 4.22579e+08 4.2258e+08 4.22626e+08 ... 4.27243e+08

Optimal solution found (tolerance 1.00e-04)
Best objective 4.225785837541e+08, best bound 4.225785837541e+08, gap 0.0000%
Optimal objective value: 422578583.75411177
```