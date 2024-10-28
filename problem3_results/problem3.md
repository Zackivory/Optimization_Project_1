# problem 2
# binary decision variable for new facility

$` b_{r, \text{small}}, \quad \forall r \in R`$

$` b_{r, \text{medium}}, \quad \forall r \in R`$

$` b_{r, \text{large}} , \quad \forall r \in R`$

$`R \in\{2,3,\dots ,215401\} \text{ is the set contain all row number of potential\_locations.csv exculde row 1 which is the heading}`$

save all decision variable for new facility in a dictionary called
decision_variables_new_facilities

the sum of three binary decision variable for each row is less equal to 1,

$`b_{facility\_id}, \quad \forall \text{facility\_id} \in F`$
# continious decision variable for expansion
### fixed on Oct. 27 7pm: uperbond fix from 120 to 0.2 
$`0 \leq x_{\text{facility\_id}} \leq 0.2, \quad \forall \text{facility\_id} \in F`$

$`F \text{ is the set of all facility id in child\_care\_regulated.csv }`$



save all decision variable for expansion in a dictionary called 
decision_variables_expansion

# constrain 
## new facility type constrain 
$`b_{r, \text{small}} + b_{r, \text{medium}} + b_{r, \text{large}} \leq 1, \quad \forall r \in R`$

## piecewise expansion constrain
$`0\leq x_{\text{level 1, facility\_id}} \leq 0.1`$

$`0\leq x_{\text{level 2, facility\_id}} \leq 0.05`$

$`0\leq x_{\text{level 3, facility\_id}} \leq 0.05`$

$`x_{\text{level 1, facility\_id}}+x_{\text{level 2, facility\_id}}+x_{\text{level 3, facility\_id}} = x_{\text{facility\_id}},  \forall \text{facility\_id} \in F`$


## required capacity constrain
$`\delta_z \quad \text{Required increase in child care capacity for zipcode $z$}`$

$`\delta_z^{0-5} \quad \text{Required increase in 0-5(years old)capacity for zipcode $z$}`$

$`R_z \text{ contain all row number that belong to zip code z}`$

$`F_z \text{ contain all facility\_id that the coresbonding facility is within zip code z}`$

$`C_{facility\_id} \text{ original total capacity of the facility with given id}`$

$`C^{0-5}_{facility\_id} \text{ original 0-5 years old care capacity of the facility with given id}`$
### child care capacity 
$`\sum_{f \in F_z} x_f \cdot C_{facility\_id} + \sum_{r \in R_z} (b_{r, \text{small}}\times 100 + b_{r, \text{medium}} \times 200 + b_{r, \text{large}}\times 400) \geq \delta_z \quad \forall z`$

### 0-5 years old care capacity
$`\sum_{f \in F_z} x_f \cdot C^{0-5}_{facility\_id} + \sum_{r \in R_z} (b_{r, \text{small}}\times 50 + b_{r, \text{medium}} \times 100 + b_{r, \text{large}}\times 200) \geq \delta_z^{0-5} \quad \forall z`$

## minimum distance constrain
### Minimum Distance Constraint
$`\forall z, \forall r_i, r_j \in R_z, \text{if } \text{distance}(r_i, r_j) < 0.06 \text{ then } b_{r_i, \text{small}} + b_{r_i, \text{medium}} + b_{r_i, \text{large}} + b_{r_j, \text{small}} + b_{r_j, \text{medium}} + b_{r_j, \text{large}} \leq 1`$

## social coverage ratio constrain 
$`SCR_z =\text{ social coverage ratio of region with zip code z}`$

$`SCR_z=\frac {\sum_{f \in F_z} (1+x_f) \cdot C_{facility\_id} + \sum_{r \in R_z} (b_{r, \text{small}}\times 100 + b_{r, \text{medium}} \times 200 + b_{r, \text{large}}\times 400)}{p_z}`$


$`p_z \text{ is the population of region with zip code z}`$


difference of social coverage ratio between any zip is less or equal to 0.1
we assume the max social converage ratio of all zips is 1,


$`0.9 \leq SCR_z \leq 1 \quad \forall z`$

### for social converage ratio of younger children(0-5) no constrain
$`SCR_z^{0-5} =\text{ social coverage ratio of region with zip code z}`$

$`SCR_z^{0-5}=\frac {\sum_{f \in F_z} (1+x_f) \cdot C_{facility\_id}^{0-5} + \sum_{r \in R_z} (b_{r, \text{small}}\times 50 + b_{r, \text{medium}} \times 100 + b_{r, \text{large}}\times 200)}{p_z}`$






## budge constrain 
$`C_1= \sum_{r \in R}b_{r, \text{small}}\times 65,000 + b_{r, \text{medium}} \times 95,000 + b_{r, \text{large}}\times 115,000`$

$`C_2=\sum_{f \in F}\left(20000 + 200 \times C_{facility\_id} \times x_{\text{level 1, facility\_id}} + 400 \times C_{facility\_id} \times x_{\text{level 2, facility\_id}} + 1000 \times C_{facility\_id} \times x_{\text{level 3, facility\_id}}\right)`$

$`C_1+C_2 \leq 100,000,000 `$
# objective
$`SCI_z=\text{social coverage index of zip code z}`$

$`SCI_z= \frac {2 \times SCR_z^{0-5}+SCR_z}{3}`$

$`max \sum_zSCI_z`$ 