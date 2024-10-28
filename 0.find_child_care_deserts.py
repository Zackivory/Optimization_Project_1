# TODO find child care deserts
import csv
import json
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
# Load population data
population_data = {}

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
# Export population_data into temp
with open('temp/population_data.json', 'w', encoding="UTF-8") as file:
    json.dump(population_data, file, ensure_ascii=False, indent=4)

# Load employment rate data
employment_rate_data = {}

with open('data/employment_rate.csv', 'r', encoding="UTF-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        zipcode = row[0]
        employment_rate = float(row[1])
        employment_rate_data[zipcode] = employment_rate

# Load average income data
average_income_data = {}

with open('data/avg_individual_income.csv', 'r', encoding="UTF-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        zipcode = row[0]
        average_income = float(row[1])
        average_income_data[zipcode] = average_income

# Load child care capacity data
child_care_capacity_data = {}
care_0_5_capacity_data = {}

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


# Determine child care deserts
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


if __name__ == '__main__':
    print()




# Export child_care_deserts into temp
with open('temp/child_care_deserts.json', 'w', encoding="UTF-8") as file:
    json.dump(child_care_deserts, file, ensure_ascii=False, indent=4)
if __name__ == '__main__':
    print()