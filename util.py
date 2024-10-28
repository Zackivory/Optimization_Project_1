import csv
import gurobipy as gp
from gurobipy import GRB

new_facility_info = {
    "small": {"total_slots": 100, "slots_0_5": 50, "cost": 65000},
    "medium": {"total_slots": 200, "slots_0_5": 100, "cost": 95000},
    "large": {"total_slots": 400, "slots_0_5": 200, "cost": 115000}
}

def create_decision_variables_for_new_facilities(model, decision_variables_new_facilities):
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

def create_decision_variables_for_expansion_probelm1(model, decision_variables_expansion):
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
                model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_percentage_{facility_id}", lb=0, ub=1.2))

            # Add constraints for expansion
            if original_total_capacity <= 500:
                model.addConstr((original_total_capacity * (decision_variables_expansion[facility_id][1] / 100)) <= 500,
                                name=f"max_capacity_{facility_id}")


def create_decision_variables_for_expansion(model, decision_variables_expansion):
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
                model.addVar(vtype=GRB.CONTINUOUS, name=f"expansion_percentage_{facility_id}", lb=0, ub=0.2))

            # Add constraints for expansion
            if original_total_capacity <= 500:
                model.addConstr((original_total_capacity * (decision_variables_expansion[facility_id][1] / 100)) <= 500,
                                name=f"max_capacity_{facility_id}")
