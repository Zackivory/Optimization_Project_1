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

$`0 \leq x_{\text{facility\_id}} \leq 120, \quad \forall \text{facility\_id} \in F`$

$`F \text{ is the set of all facility id in child\_care\_regulated.csv }`$



save all decision variable for expansion in a dictionary called 
decision_variables_expansion

# constrain 
## new facility type constrain 
$`b_{r, \text{small}} + b_{r, \text{medium}} + b_{r, \text{large}} \leq 1, \quad \forall r \in R`$

## piecewise expansion constrain
$`0\leq x_{\text{level 1, facility\_id}} \leq 10`$

$`0\leq x_{\text{level 2, facility\_id}} \leq 5`$

$`0\leq x_{\text{level 3, facility\_id}} \leq 5`$

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



```python
for child_care_desert_zipcode, child_care_desert_info in child_care_deserts.items():
    sum_of_increase_child_care_capacity = 0
    sum_of_increase_0_5_capacity = 0

    for facility_id, (info_list, var) in decision_variables_expansion.items():
        zipcode, original_0_5_capacity,original_total_capacity, _, _ = info_list

        if zipcode == child_care_desert_zipcode:
            sum_of_increase_child_care_capacity += var * original_total_capacity
            sum_of_increase_0_5_capacity += var * original_0_5_capacity

    for rowNumber_type, (zipcode, var) in decision_variables_new_facilities.items():
        facility_type = rowNumber_type.split('_')[-1]

        if zipcode == child_care_desert_zipcode:
            if facility_type == "small":
                sum_of_increase_child_care_capacity += new_facility_info["small"]["total_slots"] * var
                sum_of_increase_0_5_capacity += new_facility_info["small"]["slots_0_5"] * var
            elif facility_type == "medium":
                sum_of_increase_child_care_capacity += new_facility_info["medium"]["total_slots"] * var
                sum_of_increase_0_5_capacity += new_facility_info["medium"]["slots_0_5"] * var
            elif facility_type == "large":
                sum_of_increase_child_care_capacity += new_facility_info["large"]["total_slots"] * var
                sum_of_increase_0_5_capacity += new_facility_info["large"]["slots_0_5"] * var

    model.addConstr(sum_of_increase_child_care_capacity >= child_care_desert_info["difference_child_care_capacity"], name=f"increase_child_care_capacity_{child_care_desert_zipcode}")
    model.addConstr(sum_of_increase_0_5_capacity >= child_care_desert_info["difference_0_5_capacity"], name=f"increase_0_5_capacity_{child_care_desert_zipcode}")
```

## minimum distance constrain
### Minimum Distance Constraint
$`\forall z, \forall r_i, r_j \in R_z, \text{if } \text{distance}(r_i, r_j) < 0.06 \text{ then } b_{r_i, \text{small}} + b_{r_i, \text{medium}} + b_{r_i, \text{large}} + b_{r_j, \text{small}} + b_{r_j, \text{medium}} + b_{r_j, \text{large}} \leq 1`$

# objective
$`C_1= \sum_{r \in R}b_{r, \text{small}}\times 65,000 + b_{r, \text{medium}} \times 95,000 + b_{r, \text{large}}\times 115,000`$

$`C_2=\sum_{f \in F}\left(20000 + 200 \times C_{facility\_id} \times x_{\text{level 1, facility\_id}} + 400 \times C_{facility\_id} \times x_{\text{level 2, facility\_id}} + 1000 \times C_{facility\_id} \times x_{\text{level 3, facility\_id}}\right)`$

$`\min C_1+C_2 `$
``` python
for facility_id, (info_list, var) in decision_variables_expansion.items():
    zipcode, original_0_5_capacity, original_total_capacity, latitude, longitude = info_list
    expansion_costs[facility_id] = 20000 + (200 * original_total_capacity)
    
model.setObjective(
    gp.quicksum(new_facility_info["small"]["cost"] * var for rowNumber_type, (zipcode, var) in decision_variables_new_facilities.items() if rowNumber_type.endswith("_small")) +
    gp.quicksum(new_facility_info["medium"]["cost"] * var for rowNumber_type, (zipcode, var) in decision_variables_new_facilities.items() if rowNumber_type.endswith("_medium")) +
    gp.quicksum(new_facility_info["large"]["cost"] * var for rowNumber_type, (zipcode, var) in decision_variables_new_facilities.items() if rowNumber_type.endswith("_large")) +
    gp.quicksum(expansion_costs[facility_id] for facility_id in decision_variables_expansion),
    GRB.MINIMIZE
)
```