import json
import csv
import gurobipy as gp
from gurobipy import GRB
from util import create_decision_variables_for_new_facilities, create_decision_variables_for_expansion, \
    new_facility_info

# Read child_care_deserts from file
with open('temp/child_care_deserts.json', 'r', encoding="UTF-8") as file:
    child_care_deserts = json.load(file)



decision_variables_new_facilities = {}
decision_variables_expansion = {}
model = gp.Model("LP")
create_decision_variables_for_new_facilities(model, decision_variables_new_facilities)
create_decision_variables_for_expansion(model, decision_variables_expansion)


expansion_costs = {}
# Define the cost and size of new facilities


for facility_id, (info_list, var) in decision_variables_expansion.items():
    _, _, original_total_capacity,_,_ = info_list
    expansion_costs[facility_id] = 20000 + (200 * original_total_capacity)


# Add constraints to satisfy the increase of child care capacity and 0-5 capacity
print("Starting to add constraints to satisfy the increase of child care capacity and 0-5 capacity...")
total_deserts = len(child_care_deserts)
current_desert = 0
for child_care_desert_zipcode, child_care_desert_info in child_care_deserts.items():
    sum_of_increase_child_care_capacity = 0
    sum_of_increase_0_5_capacity = 0

    for facility_id, (info_list, var) in decision_variables_expansion.items():
        zipcode, original_0_5_capacity, original_total_capacity, _, _ = info_list

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

    model.addConstr(sum_of_increase_child_care_capacity >= child_care_desert_info["difference_child_care_capacity"],
                    name=f"increase_child_care_capacity_{child_care_desert_zipcode}")
    model.addConstr(sum_of_increase_0_5_capacity >= child_care_desert_info["difference_0_5_capacity"],
                    name=f"increase_0_5_capacity_{child_care_desert_zipcode}")

    current_desert += 1
    print(current_desert)




model.setObjective(
    gp.quicksum(new_facility_info["small"]["cost"] * var for rowNumber_type, (zipcode, var) in
                decision_variables_new_facilities.items() if rowNumber_type.endswith("_small")) +
    gp.quicksum(new_facility_info["medium"]["cost"] * var for rowNumber_type, (zipcode, var) in
                decision_variables_new_facilities.items() if rowNumber_type.endswith("_medium")) +
    gp.quicksum(new_facility_info["large"]["cost"] * var for rowNumber_type, (zipcode, var) in
                decision_variables_new_facilities.items() if rowNumber_type.endswith("_large")) +
    gp.quicksum(expansion_costs[facility_id] for facility_id in decision_variables_expansion),
    GRB.MINIMIZE
)

if __name__ == '__main__':

    model.optimize()

    if model.status == GRB.OPTIMAL:
        var_values = {}
        for var in model.getVars():
            var_values[var.varName] = var.x

        with open('var_values.json', 'w') as f:
            json.dump(var_values, f)

        print(f'Optimal Objective Value: {model.objVal}')
    else:
        print("No optimal solution found")
