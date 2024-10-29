# Problem 1 math formulation
# discrete decision variable for new facility number in each child chare deserts,enoted using zip code 

$` d_{z,\text{small}},\quad \forall z \in Z`$

$` d_{z,\text{medium}},\quad \forall z \in Z`$

$` d_{z,\text{large}} , \quad \forall z \in Z`$



# continious decision variable for expansion

$`1.2=+120\%`$

$`0 \leq x_{\text{facility\_id}} \leq 1.2, \quad \forall \text{facility\_id} \in F`$

$`F \text{ is the set of all facility id in child\_care\_regulated.csv }`$



save all decision variable for expansion in a dictionary called 
decision_variables_expansion

# constrain 

## required capacity constrain
$`\delta_z \quad \text{Required increase in child care capacity for zipcode $z$}`$

$`\delta_z^{0-5} \quad \text{Required increase in 0-5(years old)capacity for zipcode $z$}`$

$`R_z \text{ contain all row number that belong to zip code z}`$

$`F_z \text{ contain all facility\_id that the coresbonding facility is within zip code z}`$

$`C_{facility\_id} \text{ original total capacity of the facility with given id}`$

$`C^{0-5}_{facility\_id} \text{ original 0-5 years old care capacity of the facility with given id}`$

### child care capacity 
$`\sum_{f \in F_z} x_{\text{facility\_id}} \cdot C_{facility\_id} + d_{z,small}\times 100 + d_{z,medium} \times 200 + d_{z,large}\times 400) \geq \delta_z \quad \forall z`$

### 0-5 years old care capacity
$`\sum_{f \in F_z} x_{\text{facility\_id}} \cdot C^{0-5}_{facility\_id} + d_{z,small}\times 50 + d_{z,medium} \times 100 + d_{z,large}\times 200) \geq \delta_z^{0-5} \quad \forall z`$




# objective
   (baseline cost + capacity-based cost * existing capacity) * expansion rate + (addtional cost per slot for children under 5) * slots expanded for children under 5

$`C_1= \sum_{z \in Z}d_{z,small}\times 65,000 + d_{z,medium} \times 95,000 + d_{z,large}\times 115,000`$

$`C_2=\sum_{f \in F}(20000+200\times C_{facility\_id}) \times x_{\text{facility\_id}}+100\times x_{\text{facility\_id}} \times C^{0-5}_{facility\_id} `$
# todo update to the ed cost        

$`\min C_1+C_2 `$
