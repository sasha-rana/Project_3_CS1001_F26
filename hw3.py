from data import CountyDemographics


POVERTY_KEY = 'Persons Below Poverty Level'


# Part 1

# Compute the total 2014 population of the given counties.
# input: a list of CountyDemographics objects
# output: the sum of each county's '2014 Population' value as an int
def population_total(counties: list[CountyDemographics]) -> int:
    total = 0
    for county in counties:
        total += county.population['2014 Population']
    return int(total)


# Part 2

# Select the counties that belong to the given state.
# input: a list of CountyDemographics objects
# input: a two-letter state abbreviation, such as 'CA'
# output: a list of the CountyDemographics objects whose state matches
def filter_by_state(counties: list[CountyDemographics],
                    state: str) -> list[CountyDemographics]:
    result = []
    for county in counties:
        if county.state == state:
            result.append(county)
    return result


# Part 3

# Helper: estimate the 2014 sub-population for a percentage stored in one
# of each county's dictionaries.
# input: a list of CountyDemographics objects
# input: the name of the attribute holding the dictionary ('education', ...)
# input: the dictionary key whose percentage should be used
# output: the summed estimate (population * percent / 100); counties that
#         lack the key contribute 0
def _sub_population(counties: list[CountyDemographics], attribute: str,
                    key: str) -> float:
    total = 0.0
    for county in counties:
        values = getattr(county, attribute)
        if key in values:
            total += county.population['2014 Population'] * values[key] / 100
    return total


# Estimate the total 2014 sub-population for an education key.
# input: a list of CountyDemographics objects
# input: an education key, such as "Bachelor's Degree or Higher"
# output: the estimated number of people as a float (0 if key is missing)
def population_by_education(counties: list[CountyDemographics],
                            key: str) -> float:
    return _sub_population(counties, 'education', key)


# Estimate the total 2014 sub-population for an ethnicity key.
# input: a list of CountyDemographics objects
# input: an ethnicities key, such as 'Two or More Races'
# output: the estimated number of people as a float (0 if key is missing)
def population_by_ethnicity(counties: list[CountyDemographics],
                            key: str) -> float:
    return _sub_population(counties, 'ethnicities', key)


# Estimate the total 2014 sub-population below the poverty level.
# input: a list of CountyDemographics objects
# output: the estimated number of people below the poverty level as a float
def population_below_poverty_level(
        counties: list[CountyDemographics]) -> float:
    return _sub_population(counties, 'income', POVERTY_KEY)


# Part 4

# Helper: convert a sub-population into a percentage of the total
# 2014 population of the counties.
# input: the sub-population total
# input: a list of CountyDemographics objects
# output: 100 * sub_population / total population (0 for an empty total)
def _percent_of_total(sub_population: float,
                      counties: list[CountyDemographics]) -> float:
    total = population_total(counties)
    if total == 0:
        return 0
    return 100 * sub_population / total


# Compute the population-weighted percentage for an education key.
# input: a list of CountyDemographics objects
# input: an education key, such as "Bachelor's Degree or Higher"
# output: the overall percentage as a float (0 if key is missing)
def percent_by_education(counties: list[CountyDemographics],
                         key: str) -> float:
    return _percent_of_total(population_by_education(counties, key), counties)


# Compute the population-weighted percentage for an ethnicity key.
# input: a list of CountyDemographics objects
# input: an ethnicities key, such as 'Hispanic or Latino'
# output: the overall percentage as a float (0 if key is missing)
def percent_by_ethnicity(counties: list[CountyDemographics],
                         key: str) -> float:
    return _percent_of_total(population_by_ethnicity(counties, key), counties)


# Compute the population-weighted percentage below the poverty level.
# input: a list of CountyDemographics objects
# output: the overall percentage below the poverty level as a float
def percent_below_poverty_level(counties: list[CountyDemographics]) -> float:
    return _percent_of_total(population_below_poverty_level(counties),
                             counties)


# Part 5

# Helper: select counties whose stored percentage for a key is strictly
# above (above=True) or strictly below (above=False) a threshold.
# input: a list of CountyDemographics objects
# input: the name of the attribute holding the dictionary
# input: the dictionary key to compare
# input: the percentage threshold
# input: True for 'greater than', False for 'less than'
# output: the matching CountyDemographics objects (counties lacking the key
#         are skipped)
def _filter_threshold(counties: list[CountyDemographics], attribute: str,
                      key: str, threshold: float,
                      above: bool) -> list[CountyDemographics]:
    result = []
    for county in counties:
        values = getattr(county, attribute)
        if key in values:
            value = values[key]
            if (above and value > threshold) or \
                    (not above and value < threshold):
                result.append(county)
    return result


# Select counties whose education percentage is greater than a threshold.
# input: a list of CountyDemographics objects
# input: an education key
# input: the percentage threshold
# output: the counties whose education[key] > threshold
def education_greater_than(counties: list[CountyDemographics], key: str,
                           threshold: float) -> list[CountyDemographics]:
    return _filter_threshold(counties, 'education', key, threshold, True)


# Select counties whose education percentage is less than a threshold.
# input: a list of CountyDemographics objects
# input: an education key
# input: the percentage threshold
# output: the counties whose education[key] < threshold
def education_less_than(counties: list[CountyDemographics], key: str,
                        threshold: float) -> list[CountyDemographics]:
    return _filter_threshold(counties, 'education', key, threshold, False)


# Select counties whose ethnicity percentage is greater than a threshold.
# input: a list of CountyDemographics objects
# input: an ethnicities key
# input: the percentage threshold
# output: the counties whose ethnicities[key] > threshold
def ethnicity_greater_than(counties: list[CountyDemographics], key: str,
                           threshold: float) -> list[CountyDemographics]:
    return _filter_threshold(counties, 'ethnicities', key, threshold, True)


# Select counties whose ethnicity percentage is less than a threshold.
# input: a list of CountyDemographics objects
# input: an ethnicities key
# input: the percentage threshold
# output: the counties whose ethnicities[key] < threshold
def ethnicity_less_than(counties: list[CountyDemographics], key: str,
                        threshold: float) -> list[CountyDemographics]:
    return _filter_threshold(counties, 'ethnicities', key, threshold, False)


# Select counties whose poverty-level percentage is greater than a threshold.
# input: a list of CountyDemographics objects
# input: the percentage threshold
# output: the counties whose 'Persons Below Poverty Level' > threshold
def below_poverty_level_greater_than(counties: list[CountyDemographics],
                                     threshold: float
                                     ) -> list[CountyDemographics]:
    return _filter_threshold(counties, 'income', POVERTY_KEY, threshold, True)


# Select counties whose poverty-level percentage is less than a threshold.
# input: a list of CountyDemographics objects
# input: the percentage threshold
# output: the counties whose 'Persons Below Poverty Level' < threshold
def below_poverty_level_less_than(counties: list[CountyDemographics],
                                  threshold: float
                                  ) -> list[CountyDemographics]:
    return _filter_threshold(counties, 'income', POVERTY_KEY, threshold,
                             False)
