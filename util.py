import csv
import math

import gurobipy as gp
from gurobipy import GRB

new_facility_info = {
    "small": {"total_slots": 100, "slots_0_5": 50, "cost": 65000},
    "medium": {"total_slots": 200, "slots_0_5": 100, "cost": 95000},
    "large": {"total_slots": 400, "slots_0_5": 200, "cost": 115000}
}

def create_decision_variables_for_new_facilities_problem1(model, decision_variables_new_facilities):
    with open('data/new_population.csv', 'r', encoding="UTF-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        zipcodes = set(row[0] for row in reader)
        for zipcode in zipcodes:
            decision_variables_new_facilities[f"d_{zipcode}_small"] = (
                zipcode, model.addVar(vtype=GRB.INTEGER ,name=f"d_{zipcode}_small"))
            decision_variables_new_facilities[f"d_{zipcode}_medium"] = (
                zipcode, model.addVar(vtype=GRB.INTEGER,name=f"d_{zipcode}_medium"))
            decision_variables_new_facilities[f"d_{zipcode}_large"] = (
                zipcode, model.addVar(vtype=GRB.INTEGER,name=f"d_{zipcode}_large"))
  

def create_decision_variables_for_expansion_problem1(model, decision_variables_expansion):
    with open('data/new_child_care.csv', 'r', encoding="UTF-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            facility_id = row[0]
            zipcode = row[0]

            original_infant_capacity = int(row[7]) if row[7] else 0
            original_toddler_capacity = int(row[8]) if row[8] else 0
            original_preschool_capacity = int(row[9]) if row[9] else 0
            original_school_age_capacity = int(row[10]) if row[10] else 0
            original_children_capacity = int(row[11]) if row[11] else 0
            original_total_capacity = int(row[12]) if row[12] else 0  # total_capacity
            latitude = float(row[13]) if row[13] else 0.0
            longitude = float(row[14]) if row[14] else 0.0
            original_0_5_capacity = original_infant_capacity + original_toddler_capacity+original_preschool_capacity
            x=model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_percentage_of_total_capacity{facility_id}", lb=0, ub=0.2)
            z=model.addVar(vtype=GRB.INTEGER, name=f"expansion_amount_of_0_5_capacity{facility_id}", lb=0)
            decision_variables_expansion[facility_id] = (
                [zipcode, original_0_5_capacity, original_total_capacity, latitude, longitude],
            x,z)
            model.addConstr(z <= 0.2 * original_total_capacity)

            # Add constraints for expansion
            if original_total_capacity <= 500:
                model.addConstr((original_total_capacity * (1 + decision_variables_expansion[facility_id][1])) <= 500,
                                name=f"max_capacity_{facility_id}")
def create_decision_variables_for_new_facilities(model, decision_variables_new_facilities):
    with open('data/new_potential_loc.csv', 'r') as file:
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

def create_decision_variables_for_expansion_problem2and3(model, decision_variables_expansion):
    with open('data/new_child_care.csv', 'r', encoding="UTF-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            facility_id = row[0]
            zipcode = row[0]

            original_infant_capacity = int(row[7]) if row[7] else 0
            original_toddler_capacity = int(row[8]) if row[8] else 0
            original_preschool_capacity = int(row[9]) if row[9] else 0
            original_school_age_capacity = int(row[10]) if row[10] else 0
            original_children_capacity = int(row[11]) if row[11] else 0
            original_total_capacity = int(row[12]) if row[12] else 0  # total_capacity
            latitude = float(row[13]) if row[13] else 0.0
            longitude = float(row[14]) if row[14] else 0.0
            original_0_5_capacity = original_infant_capacity + original_toddler_capacity+original_preschool_capacity

            y1 = model.addVar(vtype=GRB.BINARY, name=f"y1_{facility_id}")
            y2 = model.addVar(vtype=GRB.BINARY, name=f"y2_{facility_id}")
            y3 = model.addVar(vtype=GRB.BINARY, name=f"y3_{facility_id}")
            x = model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_percentage_of_total_capacity{facility_id}", lb=0, ub=0.2)
            z= model.addVar(vtype=GRB.INTEGER, name=f"expansion_amount_of_0_5_capacity{facility_id}", lb=0)
            model.addConstr(y1 + y2 + y3 == 1, name=f"expansion_choice_{facility_id}")
            decision_variables_expansion[facility_id] = (
                [zipcode, original_0_5_capacity, original_total_capacity, latitude, longitude],
                x,z,y1,y2,y3)
            model.addConstr(z<=(0.2*original_total_capacity+original_0_5_capacity))
            model.addConstr(x >= 0 * y1 + 0.1 * y2 + 0.15 * y3, name=f"min_expansion_{facility_id}")
            model.addConstr(x <= 0.1 * y1 + 0.15 * y2 + 0.2 * y3, name=f"max_expansion_{facility_id}")





            # Add constraints for expansion
            if original_total_capacity <= 500:
                model.addConstr((original_total_capacity * (1 + x)) <= 500,
                                name=f"max_capacity_{facility_id}")
def l2_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to miles
    lat1_miles = lat1 * 69.0
    lon1_miles = lon1 * 69.0
    lat2_miles = lat2 * 69.0
    lon2_miles = lon2 * 69.0
    return math.sqrt((lat2_miles - lat1_miles) ** 2 + (lon2_miles - lon1_miles) ** 2)
