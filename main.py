import sys
from parts_list import get_current_pices

accepted_supplier_lengths = [500, 1000, 1500, 2000]
cut_width = 3 # ~2.5mm blade width + .5mm tolerance

# tuple[supplier_length, waste, list[pice]]
Scenario = tuple[int, int, list[int]]

required_pices = get_current_pices()

def round_to_nearest_supplier_length(input: int) -> int | None:
  if input <= 0:
    return None

  for accepted_supplier_length in accepted_supplier_lengths:
    if input < accepted_supplier_length:
      return accepted_supplier_length

  return None

def append_scenario(pices: list[int], collection: list[Scenario]):
  # Sum of all pices plus n-1 times the cutting width (cuts inbetween pices)
  total_length = sum(pices) + (len(pices) - 1) * cut_width
  supplier_length = round_to_nearest_supplier_length(total_length)

  # Total length not within bounds, this scenario is invalid
  if supplier_length is None:
    return

  waste = supplier_length - total_length
  scenario = (supplier_length, waste, pices.copy())
  collection.append(scenario)

def calculate_score(scenario: Scenario) -> float:
  '''
  (length=1500, waste=31, pices=[220, 220, 510, 510])
  (length=2000, waste=228, pices=[220, 220, 510, 510, 300])

  TODO: Think about a way to give preference to groups with more members, to also
  lessen the supplier cut count, as this change does not add waste, but reduces costs
  '''

  # The lesser the waste, the better the score
  max_length = max(accepted_supplier_lengths)
  scenario_waste = scenario[1]
  waste_score = max_length - scenario_waste

  return waste_score

def choose_best_scenario(collection: list[Scenario]) -> Scenario | None:
  max_score = None
  max_score_id = None

  for i in range(0, len(collection)):
    current_score = calculate_score(collection[i])

    if max_score is None or max_score < current_score:
      max_score = current_score
      max_score_id = i

  if max_score_id is None:
    return None

  return collection[max_score_id]

def generate_scenarios(pices: list[int]) -> list[Scenario]:
  scenarios: list[Scenario] = []

  for i in range(0, len(pices)):
    current_pices = []
    current_pices.append(pices[i])
    append_scenario(pices, scenarios)

    for j in range(0, len(pices)):
      if i == j:
        continue

      current_pices.append(pices[j])
      append_scenario(current_pices, scenarios)

  return scenarios

def main():
  resulting_scenarios: list[Scenario] = []

  print(f'Required pices: {required_pices} ({sum(required_pices)} total)')
  print(f'Accepted supplier lengths: {accepted_supplier_lengths}')
  print(f'Cut width: {cut_width}')
  print()

  while len(required_pices) > 0:
    scenarios = generate_scenarios(required_pices)
    best_scenario = choose_best_scenario(scenarios)

    if best_scenario is None:
      print('Could not locate the best scenario within the current iteration!')
      sys.exit(1)

    # Remove all pices of this scenario, as they're now "taken"
    for pice in best_scenario[2]:
      if not pice in required_pices:
        print(f'Could not remove no longer available pice {pice}!')
        sys.exit(1)
      
      required_pices.remove(pice)

    resulting_scenarios.append(best_scenario)

  for scenario in resulting_scenarios:
    print(f'length={scenario[0]}, waste={scenario[1]}, pices={scenario[2]}')

if __name__ == '__main__':
  main()