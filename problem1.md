# binary decision variable for new facility

location_{row_number}_small,

location_{row_number}_medium,

location_{row_number}_large

#### save all decision variable for new facility in a dictionary called 

decision_variables_new_facilities

the sum of three binary decision variable for each row is less equal to 1,
# continious decision variable for expansion
decision variable for each facility id is f"expansion_percentage_{facility_id}",
lower bound=0
higer bound=120

#### save all decision variable for expansion in a dictionary called 
decision_variables_expansion
# constrain 
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
# objective
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