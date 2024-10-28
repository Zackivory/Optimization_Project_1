```text
Gurobi Optimizer version 11.0.3 build v11.0.3rc0 (win64 - Windows 11.0 (22631.2))

CPU model: 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, instruction set [SSE2|AVX|AVX2|AVX512]
Thread count: 8 physical cores, 16 logical processors, using up to 16 threads

Optimize a model with 304443 rows, 708616 columns and 1953133 nonzeros
Model fingerprint: 0x7440eedd
Variable types: 62416 continuous, 646200 integer (646200 binary)
Coefficient statistics:
  Matrix range     [3e-02, 9e+02]
  Objective range  [6e+02, 9e+05]
  Bounds range     [5e-02, 1e+00]
  RHS range        [3e-01, 1e+04]
Presolve removed 269916 rows and 601482 columns (presolve time = 12s) ...
Presolve removed 269916 rows and 601482 columns
Presolve time: 11.97s
Presolved: 34527 rows, 107134 columns, 222670 nonzeros
Variable types: 1808 continuous, 105326 integer (105326 binary)
Found heuristic solution: objective 7.367027e+08
Deterministic concurrent LP optimizer: primal and dual simplex
Showing primal log only...

Concurrent spin time: 0.00s

Solved with dual simplex

Root simplex log...

Iteration    Objective       Primal Inf.    Dual Inf.      Time
     724    7.2341502e+08   0.000000e+00   0.000000e+00     13s

Use crossover to convert LP symmetric solution to basic solution...

Root crossover log...

       0 DPushes remaining with DInf 0.0000000e+00                13s

   29961 PPushes remaining with PInf 0.0000000e+00                13s
       0 PPushes remaining with PInf 0.0000000e+00                13s

  Push phase complete: Pinf 0.0000000e+00, Dinf 1.1949963e+05     13s


Root simplex log...

Iteration    Objective       Primal Inf.    Dual Inf.      Time
   30937    7.2341502e+08   0.000000e+00   1.194996e+05     13s
   30941    7.2341502e+08   0.000000e+00   0.000000e+00     13s

Root relaxation: objective 7.234150e+08, 30941 iterations, 0.25 seconds (0.16 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 7.2342e+08    0  345 7.3670e+08 7.2342e+08  1.80%     -   13s
H    0     0                    7.356340e+08 7.2342e+08  1.66%     -   13s
H    0     0                    7.344134e+08 7.2342e+08  1.50%     -   14s
H    0     0                    7.342276e+08 7.2542e+08  1.20%     -   14s
     0     0 7.3179e+08    0  358 7.3423e+08 7.3179e+08  0.33%     -   14s
H    0     0                    7.339846e+08 7.3179e+08  0.30%     -   15s
H    0     0                    7.339565e+08 7.3179e+08  0.29%     -   15s
H    0     0                    7.338389e+08 7.3179e+08  0.28%     -   15s
     0     0 7.3380e+08    0  338 7.3384e+08 7.3380e+08  0.01%     -   15s

Cutting planes:
  Cover: 80
  Implied bound: 41
  MIR: 23
  StrongCG: 10
  GUB cover: 5

Explored 1 nodes (32393 simplex iterations) in 15.49 seconds (11.29 work units)
Thread count was 16 (of 16 available processors)

Solution count 7: 7.33839e+08 7.33957e+08 7.33985e+08 ... 7.36703e+08

Optimal solution found (tolerance 1.00e-04)
Best objective 7.338389409945e+08, best bound 7.337979082508e+08, gap 0.0056%
Optimal objective value: 733838940.9945325
```