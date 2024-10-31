import csv
import json
import gurobipy as gp
from gurobipy import GRB
import math
from util import create_decision_variables_for_expansion_problem2and3, create_decision_variables_for_new_facilities, \
    new_facility_info
from haversine import haversine, Unit

# Load the data
with open('temp/child_care_deserts.json', 'r') as file:
    child_care_deserts = json.load(file)
with open('temp/child_care_capacity_data.json', 'r') as file:
    child_care_capacity_data = json.load(file)
with open('temp/care_0_5_capacity_data.json', 'r') as file:
    care_0_5_capacity_data = json.load(file)
with open('temp/location_that_in_child_care_deserts.json', 'r') as file:
    location_that_in_child_care_deserts = json.load(file)



decision_variables_expansion = {}
decision_variables_new_facilities = {}
model = gp.Model("Child_Care_Desert_Expansion_and_Distance")
create_decision_variables_for_new_facilities(model, decision_variables_new_facilities)
create_decision_variables_for_expansion_problem2and3(model, decision_variables_expansion)



# Step 3: Define expansion costs using the piecewise expansions
expansion_cost = {}
for facility_id, (details, x,z, y1, y2, y3) in decision_variables_expansion.items():
    original_capacity = details[2]  # original_total_capacity is at index 2
    original_0_5_capacity = details[1]
    expansion_cost[facility_id] = (
        y1 * ((20000 + 200 * original_capacity) * x + 100 * z) +
        y2 * ((20000 + 400 * original_capacity) * x + 100 *z) +
        y3 * ((20000 + 1000 * original_capacity) * x + 100 *z)
    )



print("Starting to add constraints to satisfy the increase of child care capacity and 0-5 capacity...")
total_deserts = len(child_care_deserts)
current_desert = 0
for child_care_desert_zipcode, child_care_desert_info in child_care_deserts.items():
    sum_of_increase_child_care_capacity = 0
    sum_of_increase_0_5_capacity = 0

    for facility_id, (info_list, x,z,_,_,_) in decision_variables_expansion.items():

        zipcode, original_0_5_capacity, original_total_capacity, _, _ = info_list
        print(f"Processing facility_id: {facility_id}, zipcode: {zipcode}")
        print(f"Original 0-5 capacity: {original_0_5_capacity}, Original total capacity: {original_total_capacity}")

        if zipcode == child_care_desert_zipcode:
            sum_of_increase_child_care_capacity += x * original_total_capacity
            sum_of_increase_0_5_capacity += z

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

print("Finished adding constraints.")





from itertools import combinations

# Create a list of locations with their coordinates
locations = [(row_number, lat_lon['latitude'], lat_lon['longitude']) for row_number, lat_lon in location_that_in_child_care_deserts.items()]
# Append latitude, longitude from the csv with row number of -1
with open('data/new_child_care.csv', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])
            locations.append((-1, latitude, longitude))
        except ValueError:
            print(f"Skipping row with invalid data: {row}")

# Sort locations by latitude
locations.sort(key=lambda x: x[1])

# Use a spatial index for efficient range queries
from rtree import index

# Create an R-tree index
idx = index.Index()
for pos, (row_number, lat, lon) in enumerate(locations):
    idx.insert(pos, (lat, lon, lat, lon))

# Iterate through the sorted locations
for i in range(len(locations)):
    row_number_i, lat_i, lon_i = locations[i]

    # Query the R-tree for nearby locations
    nearby = list(idx.intersection((lat_i - 0.06 / 69.0, lon_i - 0.06 / 69.0, lat_i + 0.06 / 69.0, lon_i + 0.06 / 69.0)))

    for j in nearby:
        if i >= j:
            continue

        row_number_j, lat_j, lon_j = locations[j]

        if abs(lon_i - lon_j) < 0.06 / 69.0:

            distance = haversine((lat_i, lon_i), (lat_j, lon_j), unit=Unit.MILES)

            if distance < 0.06:
                # Add constraint that at most one facility can be built/expanded if they're too close
                if row_number_i == -1 or row_number_j == -1 or (row_number_i == -1 and row_number_j == -1):
                    continue
                print(f"{i}-{j}")
                model.addConstr(
                    decision_variables_new_facilities[f"{row_number_i}_small"][1] +
                    decision_variables_new_facilities[f"{row_number_i}_medium"][1] +
                    decision_variables_new_facilities[f"{row_number_i}_large"][1] +
                    decision_variables_new_facilities[f"{row_number_j}_small"][1] +
                    decision_variables_new_facilities[f"{row_number_j}_medium"][1] +
                    decision_variables_new_facilities[f"{row_number_j}_large"][1] <= 1,
                    name=f"distance_constraint_{row_number_i}_{row_number_j}"
                )

model.setObjective(
    gp.quicksum(new_facility_info["small"]["cost"] * var for rowNumber_type, (zipcode, var) in
                decision_variables_new_facilities.items() if rowNumber_type.endswith("_small")) +
    gp.quicksum(new_facility_info["medium"]["cost"] * var for rowNumber_type, (zipcode, var) in
                decision_variables_new_facilities.items() if rowNumber_type.endswith("_medium")) +
    gp.quicksum(new_facility_info["large"]["cost"] * var for rowNumber_type, (zipcode, var) in
                decision_variables_new_facilities.items() if rowNumber_type.endswith("_large")) +
    gp.quicksum(expansion_cost[facility_id] for facility_id in decision_variables_expansion),
    GRB.MINIMIZE
)




if __name__ == '__main__':
    model.optimize()

    if model.status == GRB.OPTIMAL:
        var_values = {}
        for var in model.getVars():
            var_values[var.varName] = var.x

        with open('problem2_results/decision_variable_results.json', 'w') as f:
            json.dump(var_values, f)

        print(f'Optimal Objective Value: {model.objVal}')
    else:
        print("No optimal solution found")
