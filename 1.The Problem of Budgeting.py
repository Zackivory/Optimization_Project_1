import json
from pprint import pprint
import csv
import gurobipy as gp
from gurobipy import GRB
import time
import sys
import os
import folium

"""
in high-demand areas—defined as regions where at least 60% of parents are employed or the average income is $60,000 or less per year—an area is considered a child care desert
if the number of available slots is less than or equal to half the population of children aged two
weeks to 12 years.
"""

"""
In normal-demand areas, where employment and income levels do not meet
the high-demand criteria, the threshold is lower: an area is classified as a child care desert if the
available slots are less than or equal to one-third of the population of children within the same age
range
"""

"""
children under the age of 5 have sufficient access
to care. This means that the number of available slots for children in this age group must be at
least two-thirds of the population of children aged 0-5.
"""

# TODO find child care deserts


# Start timing
overall_start_time = time.time()

# Load population data
population_data = {}
population_start_time = time.time()
with open('data/population.csv', 'r', encoding="UTF-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        zipcode = row[0]
        total_population = int(row[1])
        children_population = int(row[2]) + int(row[3]) + int(row[4]) // 2
        children_0_5_population = int(row[2])  # Use column 2 for children aged 0-5
        population_data[zipcode] = {
            "total_population": total_population,
            "children_population": children_population,
            "children_0_5_population": children_0_5_population
        }
population_end_time = time.time()
print(f"Population data loading time: {population_end_time - population_start_time:.2f} seconds")

# Load employment rate data
employment_rate_data = {}
employment_start_time = time.time()
with open('data/employment_rate.csv', 'r', encoding="UTF-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        zipcode = row[0]
        employment_rate = float(row[1])
        employment_rate_data[zipcode] = employment_rate
employment_end_time = time.time()
print(f"Employment rate data loading time: {employment_end_time - employment_start_time:.2f} seconds")

# Load average income data
average_income_data = {}
income_start_time = time.time()
with open('data/avg_individual_income.csv', 'r', encoding="UTF-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        zipcode = row[0]
        average_income = float(row[1])
        average_income_data[zipcode] = average_income
income_end_time = time.time()
print(f"Average income data loading time: {income_end_time - income_start_time:.2f} seconds")

# Load child care capacity data
child_care_capacity_data = {}
care_0_5_capacity_data = {}
capacity_start_time = time.time()
with open('data/child_care_regulated.csv', 'r', encoding="UTF-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        zipcode = row[5]
        infant_capacity = int(row[7]) if row[7] else 0
        toddler_capacity = int(row[8]) if row[8] else 0
        preschool_capacity = int(row[9]) if row[9] else 0
        school_age_capacity = int(row[10]) if row[10] else 0
        children_capacity = int(row[11]) if row[11] else 0
        total_capacity = int(row[12]) if row[12] else 0
        # TODO:check the age range for each type
        if zipcode in child_care_capacity_data:
            child_care_capacity_data[zipcode] += total_capacity
        else:
            child_care_capacity_data[zipcode] = total_capacity

        # Calculate 0-5 capacity
        capacity_0_5 = infant_capacity + toddler_capacity
        if zipcode in care_0_5_capacity_data:
            care_0_5_capacity_data[zipcode] += capacity_0_5
        else:
            care_0_5_capacity_data[zipcode] = capacity_0_5
# Export child_care_capacity_data into temp
with open('temp/child_care_capacity_data.json', 'w', encoding="UTF-8") as file:
    json.dump(child_care_capacity_data, file, ensure_ascii=False, indent=4)
# Export care_0_5_capacity_data into temp
with open('temp/care_0_5_capacity_data.json', 'w', encoding="UTF-8") as file:
    json.dump(care_0_5_capacity_data, file, ensure_ascii=False, indent=4)

capacity_end_time = time.time()
print(f"Child care capacity data loading time: {capacity_end_time - capacity_start_time:.2f} seconds")

# Determine child care deserts and create decision variables
deserts_start_time = time.time()
child_care_deserts = {}
for zipcode, data in population_data.items():
    employment_rate = employment_rate_data.get(zipcode, 0)
    average_income = average_income_data.get(zipcode, 0)
    child_care_capacity = child_care_capacity_data.get(zipcode, 0)
    care_0_5_capacity = care_0_5_capacity_data.get(zipcode, 0)
    high_demand = employment_rate >= 0.6 or average_income <= 60000
    if high_demand:
        threshold = data["children_population"] / 2
    else:
        threshold = data["children_population"] / 3

    threshold_0_5 = data["children_0_5_population"] * (2 / 3)
    if child_care_capacity <= threshold or child_care_capacity <= threshold_0_5:

        child_care_deserts_info = {
            "is_high_demand": high_demand,
            "children_population": data["children_population"],
            "children_0_5_population": data["children_0_5_population"],
            "current_child_care_capacity": child_care_capacity,
            "current_0_5_capacity": care_0_5_capacity,
            "required_child_care_capacity": threshold,
            "required_0_5_capacity": threshold_0_5,
            "difference_child_care_capacity": threshold - child_care_capacity,
            "difference_0_5_capacity": threshold_0_5 - care_0_5_capacity
        }

        if zipcode not in child_care_deserts:
            child_care_deserts[zipcode] = child_care_deserts_info
deserts_end_time = time.time()
print(f"Child care deserts determination time: {deserts_end_time - deserts_start_time:.2f} seconds")

# Create decision variables for each potential location for new facilities
new_facilities_start_time = time.time()
decision_variables_new_facilities = {}
model = gp.Model("LP")
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
new_facilities_end_time = time.time()
print(
    f"New facilities decision variables creation time: {new_facilities_end_time - new_facilities_start_time:.2f} seconds")

# Create decision variables for each facility for expansion
expansion_start_time = time.time()
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
expansion_end_time = time.time()
print(f"Expansion decision variables creation time: {expansion_end_time - expansion_start_time:.2f} seconds")

# Define the cost of expansion
expansion_costs = {}
# Define the cost and size of new facilities
new_facility_info = {
    "small": {"total_slots": 100, "slots_0_5": 50, "cost": 65000},
    "medium": {"total_slots": 200, "slots_0_5": 100, "cost": 95000},
    "large": {"total_slots": 400, "slots_0_5": 200, "cost": 115000}
}

for facility_id, (info_list, var) in decision_variables_expansion.items():
    zipcode, original_0_5_capacity, original_total_capacity, latitude, longitude = info_list
    expansion_costs[facility_id] = 20000 + (200 * original_total_capacity)

# Add constraints to satisfy the increase of child care capacity and 0-5 capacity
constraints_start_time = time.time()


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total:
        print()


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
    print_progress_bar(current_desert, total_deserts, prefix='Progress:', suffix='Complete', length=50)

print("Finished adding constraints.")
constraints_end_time = time.time()
print(f"Constraints addition time: {constraints_end_time - constraints_start_time:.2f} seconds")

# Set the objective function
objective_start_time = time.time()
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
objective_end_time = time.time()
print(f"Objective function setup time: {objective_end_time - objective_start_time:.2f} seconds")

if __name__ == '__main__':
    optimization_start_time = time.time()
    model.optimize()
    optimization_end_time = time.time()
    print(f"Optimization time: {optimization_end_time - optimization_start_time:.2f} seconds")

    if model.status == GRB.OPTIMAL:
        var_values = {}
        for var in model.getVars():
            var_values[var.varName] = var.x

        with open('var_values.json', 'w') as f:
            json.dump(var_values, f)

        print(f'Optimal Objective Value: {model.objVal}')
    else:
        print("No optimal solution found")

    # End timing
    overall_end_time = time.time()
    print(f"Total execution time: {overall_end_time - overall_start_time:.2f} seconds")
