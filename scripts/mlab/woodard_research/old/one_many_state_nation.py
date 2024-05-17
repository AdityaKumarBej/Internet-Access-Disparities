import csv

def get_states_with_multiple_nations(csv_file):
    states = {}
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            state_name = row['state_name']
            nation_name = row['WOODARD NATION NAME']
            if state_name not in states:
                states[state_name] = set()
            states[state_name].add(nation_name)
    
    states_with_multiple_nations = [state for state, nations in states.items() if len(nations) > 1]
    
    return states_with_multiple_nations

csv_file = '../../../results/mlab/US/Woodard_research/mlab_woodard_w_popcount_hhincome_education_age.csv'

states = get_states_with_multiple_nations(csv_file)
print("States with counties belonging to more than one nation:")
for state in states:
    print(state)
print(len(states))