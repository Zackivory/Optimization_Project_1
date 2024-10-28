import json
import gurobipy as gp
import numpy as np
from gurobipy import GRB
import math
from util import create_decision_variables_for_expansion, create_decision_variables_for_new_facilities, \
    new_facility_info

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
create_decision_variables_for_expansion(model, decision_variables_expansion)


# Step 2: Define decision variables for expansion and auxiliary variables for piecewise cost
piecewise_expansion = {}
for facility_id, (info_list, var) in decision_variables_expansion.items():
    # Define auxiliary variables for the three expansion ranges
    piecewise_expansion[facility_id] = {
        'x1': model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_x1_{facility_id}", lb=0, ub=0.1),  # 0-10%
        'x2': model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_x2_{facility_id}", lb=0, ub=0.05),  # 10-15%
        'x3': model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_x3_{facility_id}", lb=0, ub=0.05)  # 15-20%
    }

    # Ensure that the total expansion is the sum of expansions in each piece
    model.addConstr(var == piecewise_expansion[facility_id]['x1'] +
                    piecewise_expansion[facility_id]['x2'] +
                    piecewise_expansion[facility_id]['x3'], name=f"expansion_split_{facility_id}")

# Step 3: Define expansion costs using the piecewise expansions
expansion_cost = {}
for facility_id, (details, var) in decision_variables_expansion.items():
    original_capacity = details[2]  # original_total_capacity is at index 2

    # Calculate the cost for each expansion range
    cost_x1 = 20000 + 200 * original_capacity * piecewise_expansion[facility_id]['x1']  # Up to 10%
    cost_x2 = 400 * original_capacity * piecewise_expansion[facility_id]['x2']  # 10-15%
    cost_x3 = 1000 * original_capacity * piecewise_expansion[facility_id]['x3']  # 15-20%

    # Total cost for expansion
    expansion_cost[facility_id] = cost_x1 + cost_x2 + cost_x3

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
    # problem3: specific
    new_child_care_capacity = original_total_capacity + sum_of_increase_child_care_capacity
    new_0_5_capacity = original_0_5_capacity + sum_of_increase_0_5_capacity
    all_child_social_coverage_ratio=new_child_care_capacity/child_care_desert_info["children_population"]
    model.addConstr(all_child_social_coverage_ratio>=0.9,name="social_coverage_ratio_lower_bound")
    model.addConstr(all_child_social_coverage_ratio<=1,name="social_coverage_ratio_upper_bound")
    all_0_5_social_coverage_ratio=new_0_5_capacity/child_care_desert_info["children_0_5_population"]
    #calculate 
    
    
    
    current_desert += 1
    print(current_desert)

print("Finished adding constraints.")



# Step 5: Distance constraint - Ensure no two facilities are within 0.06 miles of each other
def haversine(lat1, lon1, lat2, lon2):
    R = 3959.87433  # Radius of Earth in miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in miles

def l2_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to miles
    lat1_miles = lat1 * 69.0
    lon1_miles = lon1 * 69.0
    lat2_miles = lat2 * 69.0
    lon2_miles = lon2 * 69.0
    return math.sqrt((lat2_miles - lat1_miles) ** 2 + (lon2_miles - lon1_miles) ** 2)


from itertools import combinations

# Create a list of locations with their coordinates
locations = [(row_number, lat_lon['latitude'], lat_lon['longitude']) for row_number, lat_lon in location_that_in_child_care_deserts.items()]

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
            distance_l2 = l2_distance(lat_i, lon_i, lat_j, lon_j)
            if distance_l2 < 0.06:
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
    # Solve the model
    model.optimize()

    # Output the result
    if model.status == GRB.OPTIMAL:
        print(f'Optimal objective value: {model.objVal}')

    else:
        print("No optimal solution found")