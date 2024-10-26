import json

import gurobipy as gp
from gurobipy import GRB
import math
import json

# Start building the optimization model
model = gp.Model("Child_Care_Desert_Expansion_and_Distance")
# Load the data
with open('temp/child_care_deserts.json', 'r') as file:
    child_care_deserts = json.load(file)
with open('temp/child_care_capacity_data.json', 'r') as file:
    child_care_capacity_data = json.load(file)
with open('temp/care_0_5_capacity_data.json', 'r') as file:
    care_0_5_capacity_data = json.load(file)
import csv

location_data = {}
with open('data/potential_locations.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row_number, row in enumerate(reader, start=1):
        zipcode = row['zipcode']
        latitude = float(row['latitude'])
        longitude = float(row['longitude'])
        location_data[row_number] = {'latitude': latitude, 'longitude': longitude, 'zipcode': zipcode}
# Filter locations that are in child care deserts
location_that_in_child_care_deserts = {
    row_number: {'zipcode': lat_lon['zipcode'], 'latitude': lat_lon['latitude'], 'longitude': lat_lon['longitude']}
    for row_number, lat_lon in location_data.items()
    if lat_lon['zipcode'] in child_care_deserts
}
# Save the filtered locations to a new JSON file
with open('temp/location_that_in_child_care_deserts.json', 'w') as f:
    json.dump(location_that_in_child_care_deserts, f, indent=4)
decision_variables_expansion = {}
with open('data/child_care_regulated.csv', 'r', encoding="UTF-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        facility_id = row[0]
        zipcode = row[5]

        original_infant_capacity = int(row[7]) if row[7] else 0
        original_toddler_capacity = int(row[8]) if row[8] else 0
        original_preschool_capacity = int(row[9]) if row[9] else 0
        original_school_age_capacity = int(row[10]) if row[10] else 0
        original_children_capacity = int(row[11]) if row[11] else 0
        original_total_capacity = int(row[12]) if row[12] else 0  # total_capacity
        latitude = float(row[13]) if row[13] else 0.0
        longitude = float(row[14]) if row[14] else 0.0
        original_0_5_capacity = original_infant_capacity + original_toddler_capacity

        decision_variables_expansion[facility_id] = (
        [zipcode, original_0_5_capacity, original_total_capacity, latitude, longitude],
        model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_percentage_{facility_id}", lb=0, ub=120))

        # Add constraints for expansion
        if original_total_capacity <= 500:
            model.addConstr((original_total_capacity * (decision_variables_expansion[facility_id][1] / 100)) <= 500,
                            name=f"max_capacity_{facility_id}")

# THE NEW FACILITY IS SELECTED FROM POTENTIAL_LOCATIONS.CSV NOT CHILD_CARE_DESERTS ZIP CODES
# Decision variables for new facilities (small, medium, large) in each zip code
#new_facilities = {}
# for zip_code in child_care_deserts:
#     new_facilities[f"{zip_code}_small"] = model.addVar(vtype=GRB.BINARY, name=f"new_small_{zip_code}")
#     new_facilities[f"{zip_code}_medium"] = model.addVar(vtype=GRB.BINARY, name=f"new_medium_{zip_code}")
#     new_facilities[f"{zip_code}_large"] = model.addVar(vtype=GRB.BINARY, name=f"new_large_{zip_code}")
decision_variables_new_facilities = {}
with open('data/potential_locations.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row_number, row in enumerate(reader, start=1):
        zipcode = row[0]
        latitude = float(row[1])
        longitude = float(row[2])
        decision_variables_new_facilities[f"{row_number}_small"] = (
        zipcode, model.addVar(vtype=GRB.BINARY, name=f"location_{row_number}_small"))
        decision_variables_new_facilities[f"{row_number}_medium"] = (
        zipcode, model.addVar(vtype=GRB.BINARY, name=f"location_{row_number}_medium"))
        decision_variables_new_facilities[f"{row_number}_large"] = (
        zipcode, model.addVar(vtype=GRB.BINARY, name=f"location_{row_number}_large"))
        # TODO check
        model.addConstr(decision_variables_new_facilities[f"{row_number}_small"][1] +
                        decision_variables_new_facilities[f"{row_number}_medium"][1] +
                        decision_variables_new_facilities[f"{row_number}_large"][1] <= 1,
                        name=f"at_most_one_facility_at_{row_number}")
# Step 2: Define decision variables for expansion and auxiliary variables for piecewise cost
expansions = {}
piecewise_expansion = {}
for facility_id, info in decision_variables_expansion.items():
    expansions[facility_id] = model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_{facility_id}", lb=0,
                                           ub=0.2)  # Max 20% expansion

    # Define auxiliary variables for the three expansion ranges
    piecewise_expansion[facility_id] = {
        'x1': model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_x1_{facility_id}", lb=0, ub=0.1),  # 0-10%
        'x2': model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_x2_{facility_id}", lb=0, ub=0.05),  # 10-15%
        'x3': model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_x3_{facility_id}", lb=0, ub=0.05)  # 15-20%
    }

    # Ensure that the total expansion is the sum of expansions in each piece
    model.addConstr(expansions[facility_id] == piecewise_expansion[facility_id]['x1'] +
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

# Objective: Minimize the total cost of building new facilities and expanding existing ones
# total_cost = gp.quicksum(
#     65000 * new_facilities[f"{zip_code}_small"] +
#     95000 * new_facilities[f"{zip_code}_medium"] +
#     115000 * new_facilities[f"{zip_code}_large"]
#     for zip_code in child_care_deserts
# )

# Add the cost of expansion based on the piecewise linear cost
# total_cost += gp.quicksum(expansion_cost[facility_id] for facility_id in expansion_cost)
#
# model.setObjective(total_cost, GRB.MINIMIZE)
new_facility_info = {
    "small": {"total_slots": 100, "slots_0_5": 50, "cost": 65000},
    "medium": {"total_slots": 200, "slots_0_5": 100, "cost": 95000},
    "large": {"total_slots": 400, "slots_0_5": 200, "cost": 115000}
}
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


# # Add constraints to ensure enough slots are added to meet demand
# for zip_code, desert_info in child_care_deserts.items():
#     required_capacity = desert_info["difference_child_care_capacity"]
#     required_0_5_capacity = desert_info["difference_0_5_capacity"]
#
#     # Total new slots added (small, medium, large facilities)
#     total_new_capacity = (100 * new_facilities[f"{zip_code}_small"] +
#                           200 * new_facilities[f"{zip_code}_medium"] +
#                           400 * new_facilities[f"{zip_code}_large"])
#
#     # Total expansion capacity added
#     total_expansion_capacity = gp.quicksum(
#         expansions[facility_id] * child_care_capacity_data[facility_id]
#         for facility_id in child_care_capacity_data if facility_id == zip_code
#     )
#
#     # Add constraint for total capacity (new + expansion) >= required capacity
#     model.addConstr(total_new_capacity + total_expansion_capacity >= required_capacity,
#                     name=f"capacity_constraint_{zip_code}")

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
                model.addConstr(
                    decision_variables_new_facilities[f"{row_number_i}_small"][1] +
                    decision_variables_new_facilities[f"{row_number_i}_medium"][1] +
                    decision_variables_new_facilities[f"{row_number_i}_large"][1] +
                    decision_variables_new_facilities[f"{row_number_j}_small"][1] +
                    decision_variables_new_facilities[f"{row_number_j}_medium"][1] +
                    decision_variables_new_facilities[f"{row_number_j}_large"][1] <= 1,
                    name=f"distance_constraint_{row_number_i}_{row_number_j}"
                )

# Solve the model
model.optimize()

# Output the result
if model.status == GRB.OPTIMAL:
    print(f'Optimal objective value: {model.objVal}')
    for v in model.getVars():
        print(f'{v.varName}: {v.x}')
else:
    print("No optimal solution found")
