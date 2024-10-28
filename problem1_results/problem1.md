 problem 1
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

## required capacity constrain
$`\delta_z \quad \text{Required increase in child care capacity for zipcode $z$}`$

$`\delta_z^{0-5} \quad \text{Required increase in 0-5(years old)capacity for zipcode $z$}`$

$`R_z \text{ contain all row number that belong to zip code z}`$

$`F_z \text{ contain all facility\_id that the coresbonding facility is within zip code z}`$

$`C_{facility\_id} \text{ original total capacity of the facility with given id}`$

$`C^{0-5}_{facility\_id} \text{ original 0-5 years old care capacity of the facility with given id}`$

### child care capacity 
$`\sum_{f \in F_z} x_{\text{facility\_id}} \cdot C_{facility\_id} + \sum_{r \in R_z} (b_{r, \text{small}}\times 100 + b_{r, \text{medium}} \times 200 + b_{r, \text{large}}\times 400) \geq \delta_z \quad \forall z`$

### 0-5 years old care capacity
$`\sum_{f \in F_z} x_{\text{facility\_id}} \cdot C^{0-5}_{facility\_id} + \sum_{r \in R_z} (b_{r, \text{small}}\times 50 + b_{r, \text{medium}} \times 100 + b_{r, \text{large}}\times 200) \geq \delta_z^{0-5} \quad \forall z`$




# objective
$`C_1= \sum_{r \in R}b_{r, \text{small}}\times 65,000 + b_{r, \text{medium}} \times 95,000 + b_{r, \text{large}}\times 115,000`$

$`C_2=\sum_{f \in F}(20000+200\times C_{facility\_id})\times b_{facility\_id}`$

$`\min C_1+C_2 `$