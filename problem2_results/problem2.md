# problem 2
# todo check problem 5 ip exercise 
# binary decision variable for new facility

$` b_{r, \text{small}}, \quad \forall r \in R`$

$` b_{r, \text{medium}}, \quad \forall r \in R`$

$` b_{r, \text{large}} , \quad \forall r \in R`$

$`R \in\{2,3,\dots ,215401\} \text{ is the set contain all row number of potential\_locations.csv exculde row 1 which is the heading}`$

save all decision variable for new facility in a dictionary called
decision_variables_new_facilities

# integer decision variable for the 0-5 capacity increased for each facility_id

$`0 \leq n_{\text{facility\_id,0-5 capacity}}\leq 0.2 \times C_{facility\_id}, \quad \forall \text{facility\_id} \in F`$


# continious decision variable for total capacity expansion for each facility_id

$`0 \leq x_{\text{facility\_id}} \leq 0.2, \quad \forall \text{facility\_id} \in F`$

$`F \text{ is the set of all facility id in child\_care\_regulated.csv }`$

# piecewise decision variable and constraint
- $` y_{1,\text{facility\_id}} `$: Equals 1 if the facility is assigned to **Level 1** (i.e., $` 0 \leq x_{\text{facility\_id}} \leq 0.1 `$), and 0 otherwise.
- $` y_{2,\text{facility\_id}} `$: Equals 1 if the facility is assigned to **Level 2** (i.e., $` 0.1 \leq x_{\text{facility\_id}} \leq 0.15 `$), and 0 otherwise.
- $` y_{3,\text{facility\_id}} `$: Equals 1 if the facility is assigned to **Level 3** (i.e., $` 0.15 \leq x_{\text{facility\_id}} \leq 0.2 `$), and 0 otherwise.

$`y_{1,\text{facility\_id}} + y_{2,\text{facility\_id}} + y_{3,\text{facility\_id}} = 1 \quad \forall \text{facility\_id} \in F`$



# constraint
## new facility type constraint 
$`b_{r, \text{small}} + b_{r, \text{medium}} + b_{r, \text{large}} \leq 1, \quad \forall r \in R`$

$`x_{\text{facility\_id}} \geq 0 \times y_{1,\text{facility\_id}} + 0.1 \times y_{2,\text{facility\_id}} + 0.15 \times y_{3,\text{facility\_id}} \quad \forall \text{facility\_id} \in F`$

$`x_{\text{facility\_id}} \leq 0.1 \times y_{1,\text{facility\_id}} + 0.15 \times y_{2,\text{facility\_id}} + 0.2 \times y_{3,\text{facility\_id}} \quad \forall \text{facility\_id} \in F`$

## required capacity constraint
$`\delta_z \quad \text{Required increase in child care capacity for zipcode $z$}`$

$`\delta_z^{0-5} \quad \text{Required increase in 0-5(years old)capacity for zipcode $z$}`$

$`R_z \text{ contain all row number that belong to zip code z}`$

$`F_z \text{ contain all facility\_id that the coresbonding facility is within zip code z}`$

$`C_{facility\_id} \text{ original total capacity of the facility with given id}`$

$`C^{0-5}_{facility\_id} \text{ original 0-5 years old care capacity of the facility with given id}`$
### child care capacity 
$`\sum_{facility\_id \in F_z} x_f \cdot C_{facility\_id} + \sum_{r \in R_z} (b_{r, \text{small}}\times 100 + b_{r, \text{medium}} \times 200 + b_{r, \text{large}}\times 400) \geq \delta_z \quad \forall z`$

### 0-5 years old care capacity
$`\sum_{facility\_id \in F_z} n_{\text{facility\_id,0-5 capacity}} + \sum_{r \in R_z} (b_{r, \text{small}}\times 50 + b_{r, \text{medium}} \times 100 + b_{r, \text{large}}\times 200) \geq \delta_z^{0-5} \quad \forall z`$





## minimum distance constraint
$`b_{r, \text{small}} + b_{r, \text{medium}} + b_{r, \text{large}} \leq 1, \quad \forall r \in R`$

$`\forall z, \forall r_i, r_j \in R_z, \text{if } \text{distance}(r_i, r_j) < 0.06 \text{ then } b_{r_i, \text{small}} + b_{r_i, \text{medium}} + b_{r_i, \text{large}} + b_{r_j, \text{small}} + b_{r_j, \text{medium}} + b_{r_j, \text{large}} + c_{r_i}+ c_{r_j} \leq 1`$

$`where`$

$`c_{r_i}  =1 \text{ if a exist facility within 0.06 mile of potential location } r_i`$

$`c_{r_i} =0 \text{ otherwise} `$


# objective
$`C_1= \sum_{z \in Z}d_{z,small}\times 65,000 + d_{z,medium} \times 95,000 + d_{z,large}\times 115,000`$

$`C_2 = \sum_{\text{facility\_id} \in F} \left[ y_{1,\text{facility\_id}} \left( (20000 + 200 \times C_{\text{facility\_id}}) \times x_{\text{facility\_id}} + 100 \times n_{\text{facility\_id}}  \right) \right.`$

$` + y_{2,\text{facility\_id}} \left( (20000 + 400 \times C_{\text{facility\_id}}) \times x_{\text{facility\_id}} + 100 \times n_{\text{facility\_id}} \right) `$

$`+ y_{3,\text{facility\_id}} \left( (20000 + 1000 \times C_{\text{facility\_id}}) \times x_{\text{facility\_id}} + 100 \times n_{\text{facility\_id}}  \right) ]`$

$`\min C_1+C_{2}`$
