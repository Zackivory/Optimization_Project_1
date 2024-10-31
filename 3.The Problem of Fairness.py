import csv
import json
import gurobipy as gp
import numpy as np
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
with open('temp/population_data.json', 'r') as file:
    population_data = json.load(file)


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
        y2 * ((20000 + 400 * original_capacity) * x + 100 * z) +
        y3 * ((20000 + 1000 * original_capacity) * x + 100 * z)
    )

# calculate social coverage ratio for all zips
# Calculate social coverage ratio for all zips
social_coverage_ratios = {}

for zipcode, data in population_data.items():
    children_population = data["children_population"]
    child_care_capacity = child_care_capacity_data.get(zipcode, 0)
    
    if children_population > 0:
        social_coverage_ratio = child_care_capacity / children_population
    else:
        social_coverage_ratio = 0
    
    social_coverage_ratios[zipcode] = social_coverage_ratio

# Export social_coverage_ratios to JSON
with open('temp/social_coverage_ratios.json', 'w', encoding="UTF-8") as file:
    json.dump(social_coverage_ratios, file, ensure_ascii=False, indent=4)

# Print max social coverage ratios
max_social_coverage_ratio = max(social_coverage_ratios.values())
print(f"Max social coverage ratio: {max_social_coverage_ratio}")
import matplotlib.pyplot as plt

# Plot histogram of social coverage ratios
plt.hist(social_coverage_ratios.values(), bins=np.arange(0, max(social_coverage_ratios.values()) + 0.1, 0.1), edgecolor='black')
plt.xlabel('Social Coverage Ratio')
plt.ylabel('Frequency')
plt.title('Histogram of Social Coverage Ratios')
plt.grid(True)
plt.show()
# assume social coverage ratio larger than 1 is caused by data error drop zipcode
# Filter out zip codes with social coverage ratio larger than 1
filtered_social_coverage_ratios = {zipcode: ratio for zipcode, ratio in social_coverage_ratios.items() if ratio <= 1}

# Check if any zip code in child_care_deserts.json was not in filtered zip
missing_zipcodes = [zipcode for zipcode in child_care_deserts if zipcode not in filtered_social_coverage_ratios]
if missing_zipcodes:
    print(f"Zip codes in child_care_deserts.json not found in filtered zip codes: {missing_zipcodes}")
else:
    print("All zip codes in child_care_deserts.json are present in the filtered zip codes.")



print("Starting to add constraints to satisfy the increase of child care capacity and 0-5 capacity...")
total_deserts = len(child_care_deserts)
current_desert = 0
social_coverage_indices=[]
for child_care_desert_zipcode, child_care_desert_info in child_care_deserts.items():
    sum_of_increase_child_care_capacity = 0
    sum_of_increase_0_5_capacity = 0

    for facility_id, (info_list, x, z, _, _, _) in decision_variables_expansion.items():

        zipcode, original_0_5_capacity, original_total_capacity, _, _ = info_list
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

    # problem3: specific
    new_child_care_capacity = original_total_capacity + sum_of_increase_child_care_capacity
    new_0_5_capacity = original_0_5_capacity + sum_of_increase_0_5_capacity
    if child_care_desert_info["children_population"] != 0:
        all_child_social_coverage_ratio = new_child_care_capacity / child_care_desert_info["children_population"]
        model.addConstr(all_child_social_coverage_ratio>=0.9,name="social_coverage_ratio_lower_bound")
        model.addConstr(all_child_social_coverage_ratio<=1,name="social_coverage_ratio_upper_bound")
    else:
        all_child_social_coverage_ratio = 0
    
    if child_care_desert_info["children_0_5_population"] != 0:
        all_0_5_social_coverage_ratio = new_0_5_capacity / child_care_desert_info["children_0_5_population"]
    else:
        all_0_5_social_coverage_ratio = 0
    #calculate social coverage index
    social_coverage_index = (2 * all_0_5_social_coverage_ratio + all_child_social_coverage_ratio) / 3
    social_coverage_indices.append(social_coverage_index)
    
    current_desert += 1
    print(current_desert)

# for zipcodes not in child_care_deserts, we need to add constraints to ensure the social coverage ratio is between 0.9 and 1

zipcodes_not_in_child_care_deserts = {zipcode: info for zipcode, info in population_data.items() if zipcode not in child_care_deserts}
for zipcode, population_info in zipcodes_not_in_child_care_deserts.items():
    sum_of_increase_child_care_capacity = 0
    sum_of_increase_0_5_capacity = 0

    for facility_id, (info_list, x,z,_,_,_) in decision_variables_expansion.items():
        facility_zipcode, original_0_5_capacity, original_total_capacity, _, _ = info_list

        if facility_zipcode == zipcode:
            sum_of_increase_child_care_capacity += x * original_total_capacity
            sum_of_increase_0_5_capacity += z

    for rowNumber_type, (facility_zipcode, var) in decision_variables_new_facilities.items():
        facility_type = rowNumber_type.split('_')[-1]

        if facility_zipcode == zipcode:
            if facility_type == "small":
                sum_of_increase_child_care_capacity += new_facility_info["small"]["total_slots"] * var
                sum_of_increase_0_5_capacity += new_facility_info["small"]["slots_0_5"] * var
            elif facility_type == "medium":
                sum_of_increase_child_care_capacity += new_facility_info["medium"]["total_slots"] * var
                sum_of_increase_0_5_capacity += new_facility_info["medium"]["slots_0_5"] * var
            elif facility_type == "large":
                sum_of_increase_child_care_capacity += new_facility_info["large"]["total_slots"] * var
                sum_of_increase_0_5_capacity += new_facility_info["large"]["slots_0_5"] * var

    new_child_care_capacity = original_total_capacity + sum_of_increase_child_care_capacity
    new_0_5_capacity = original_0_5_capacity + sum_of_increase_0_5_capacity
    if population_info["children_population"] != 0:
        all_child_social_coverage_ratio = new_child_care_capacity / population_info["children_population"]
        model.addConstr(all_child_social_coverage_ratio >= 0.9, name=f"social_coverage_ratio_lower_bound_{zipcode}")
        model.addConstr(all_child_social_coverage_ratio <= 1, name=f"social_coverage_ratio_upper_bound_{zipcode}")
    else:
        all_child_social_coverage_ratio = 0
    
    if population_info["children_0_5_population"] != 0:
        all_0_5_social_coverage_ratio = new_0_5_capacity / population_info["children_0_5_population"]
        model.addConstr(all_0_5_social_coverage_ratio >= 0.9, name=f"social_coverage_ratio_0_5_lower_bound_{zipcode}")
        model.addConstr(all_0_5_social_coverage_ratio <= 1, name=f"social_coverage_ratio_0_5_upper_bound_{zipcode}")
    else:
        all_0_5_social_coverage_ratio = 0
    #calculate social coverage index
    social_coverage_index = (2 * all_0_5_social_coverage_ratio + all_child_social_coverage_ratio) / 3
    social_coverage_indices.append(social_coverage_index)

# Step 4: Define the objective function to maximize the sum of social coverage indices
model.setObjective(gp.quicksum(social_coverage_indices), GRB.MAXIMIZE)




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
                if row_number_i == -1 or row_number_j == -1 or (row_number_i == -1 and row_number_j == -1):
                    continue
                # Add constraint that at most one facility can be built/expanded if they're too close
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



if __name__ == '__main__':
    model.optimize()

    if model.status == GRB.OPTIMAL:
        var_values = {}
        for var in model.getVars():
            var_values[var.varName] = var.x

        with open('problem3_results/decision_variable_results.json', 'w') as f:
            json.dump(var_values, f)

        print(f'Optimal Objective Value: {model.objVal}')
    else:
        print("No optimal solution found")
