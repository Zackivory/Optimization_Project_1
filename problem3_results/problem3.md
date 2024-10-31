# problem 2
# binary decision variable for new facility

$` b_{r, \text{small}}, \quad \forall r \in R`$

$` b_{r, \text{medium}}, \quad \forall r \in R`$

$` b_{r, \text{large}} , \quad \forall r \in R`$

$`R \in\{2,3,\dots ,215401\} \text{ is the set contain all row number of potential\_locations.csv exculde row 1 which is the heading}`$

# integer decision variable for the 0-5 capacity increased for each facility_id

$`0 \leq n_{\text{facility\_id,0-5 capacity}}\leq 0.2 \times C_{facility\_id}, \quad \forall \text{facility\_id} \in F`$


# continious decision variable for expansion
$`0 \leq x_{\text{facility\_id}} \leq 0.2, \quad \forall \text{facility\_id} \in F`$

$`F \text{ is the set of all facility id in child\_care\_regulated.csv }`$



save all decision variable for expansion in a dictionary called 
decision_variables_expansion

# constraint 
## new facility type constraint
$`b_{r, \text{small}} + b_{r, \text{medium}} + b_{r, \text{large}} \leq 1, \quad \forall r \in R`$

## piecewise decision variable and constraint
- $` y_{1,\text{facility\_id}} `$: Equals 1 if the facility is assigned to **Level 1** (i.e., $` 0 \leq x_{\text{facility\_id}} \leq 0.1 `$), and 0 otherwise.
- $` y_{2,\text{facility\_id}} `$: Equals 1 if the facility is assigned to **Level 2** (i.e., $` 0.1 \leq x_{\text{facility\_id}} \leq 0.15 `$), and 0 otherwise.
- $` y_{3,\text{facility\_id}} `$: Equals 1 if the facility is assigned to **Level 3** (i.e., $` 0.15 \leq x_{\text{facility\_id}} \leq 0.2 `$), and 0 otherwise.

$`y_{1,\text{facility\_id}} + y_{2,\text{facility\_id}} + y_{3,\text{facility\_id}} = 1 \quad \forall \text{facility\_id} \in F`$


## required capacity constraint
$`\delta_z \quad \text{Required increase in child care capacity for zipcode $z$}`$

$`\delta_z^{0-5} \quad \text{Required increase in 0-5(years old)capacity for zipcode $z$}`$

$`R_z \text{ contain all row number that belong to zip code z}`$

$`F_z \text{ contain all facility\_id that the coresbonding facility is within zip code z}`$

$`C_{facility\_id} \text{ original total capacity of the facility with given id}`$

$`C^{0-5}_{facility\_id} \text{ original 0-5 years old care capacity of the facility with given id}`$
### child care capacity 
$`\sum_{f \in F_z} x_f \cdot C_{facility\_id} + \sum_{r \in R_z} (b_{r, \text{small}}\times 100 + b_{r, \text{medium}} \times 200 + b_{r, \text{large}}\times 400) \geq \delta_z \quad \forall z`$

### 0-5 years old care capacity
$`\sum_{facility\_id \in F_z} n_{\text{facility\_id,0-5 capacity}} + \sum_{r \in R_z} (b_{r, \text{small}}\times 50 + b_{r, \text{medium}} \times 100 + b_{r, \text{large}}\times 200) \geq \delta_z^{0-5} \quad \forall z`$

## minimum distance constraint
$`b_{r, \text{small}} + b_{r, \text{medium}} + b_{r, \text{large}} \leq 1, \quad \forall r \in R`$

$`\forall z, \forall r_i, r_j \in R_z, \text{if } \text{distance}(r_i, r_j) < 0.06 \text{ then } b_{r_i, \text{small}} + b_{r_i, \text{medium}} + b_{r_i, \text{large}} + b_{r_j, \text{small}} + b_{r_j, \text{medium}} + b_{r_j, \text{large}} + c_{r_i}+ c_{r_j} \leq 1`$

$`where`$

$`c_{r_i}  =1 \text{ if a exist facility within 0.06 mile of potential location } r_i`$

$`c_{r_i} =0 \text{ otherwise} `$
## social coverage ratio constraint
$`SCR_z =\text{ social coverage ratio of region with zip code z}`$

$`SCR_z=max(1,\frac {\sum_{f \in F_z} (1+x_f) \cdot C_{facility\_id} + \sum_{r \in R_z} (b_{r, \text{small}}\times 100 + b_{r, \text{medium}} \times 200 + b_{r, \text{large}}\times 400)}{p_z})`$


difference of social coverage ratio between any zip is less or equal to 0.1
we assume the max social converage ratio of all zips is 1


$`p_z \text{ is the population of region with zip code z}`$

----

$`(SCR_{z1}-SCR_{z2})^2 \leq 0.01 \forall z1,z2 \in Z,z1 \neq z2 `$

$` Max(SCR_z)=1 \forall z \in Z`$

$` \Rightarrow 0.9 \leq SCR_z \leq 1 \quad \forall z \in Z`$

prove in [fairness_constraint_explain.md](fairness_constraint_explain.md)


## [IMPORTANT] Clarification and Supplementary Information/Instructions from ed discussion
https://edstem.org/us/courses/65260/discussion/5468625
```text
For the objective function in the problem 3, you can use any (or more than one) of following reasonable indices of child care coverage (since it is not clearly specified sorry): 

Child care coverage on a state-level; 

Average of child care coverage on a zipcode-level; 

Minimum of child care coverage on a zipcode-level. 

Please indicate which one(s) your group used in the final report. 
```
We used the average child care coverage at the ZIP code level, as we calculated the total capacity in a ZIP code region relative to its population.
### for social converage ratio of younger children(0-5) no constraint
$`SCR_z^{0-5} =\text{ social coverage ratio of region with zip code z}`$

$`SCR_z^{0-5}=\frac {\sum_{f \in F_z} (1+x_f) \cdot C_{facility\_id}^{0-5} + \sum_{r \in R_z} (b_{r, \text{small}}\times 50 + b_{r, \text{medium}} \times 100 + b_{r, \text{large}}\times 200)}{p_z}`$





## budge constraint 
$`C_1= \sum_{r \in R}b_{r, \text{small}}\times 65,000 + b_{r, \text{medium}} \times 95,000 + b_{r, \text{large}}\times 115,000`$

$`C_2 = \sum_{\text{facility\_id} \in F} \left[ y_{1,\text{facility\_id}} \left( (20000 + 200 \times C_{\text{facility\_id}}) \times x_{\text{facility\_id}} + 100 \times n_{\text{facility\_id}}  \right) \right.`$

$` + y_{2,\text{facility\_id}} \left( (20000 + 400 \times C_{\text{facility\_id}}) \times x_{\text{facility\_id}} + 100 \times n_{\text{facility\_id}} \right) `$

$`+ y_{3,\text{facility\_id}} \left( (20000 + 1000 \times C_{\text{facility\_id}}) \times x_{\text{facility\_id}} + 100 \times n_{\text{facility\_id}}  \right) ]`$

$`C_1+C_2 \leq 1,000,000,000 `$
# objective
$`SCI_z=\text{social coverage index of zip code z}`$

$`SCI_z= \frac {2 \times SCR_z^{0-5}+SCR_z}{3}`$

$`max \sum_zSCI_z`$ 