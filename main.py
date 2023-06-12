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

def choose_best_scenario(collection: list[Scenario]) -> Scenario | None:
  min_waste = None
  min_waste_id = None

  for i in range(0, len(collection)):
    current_waste = collection[i][1]

    if min_waste is None or min_waste > current_waste:
      min_waste = current_waste
      min_waste_id = i

  if min_waste_id is None:
    return None

  return collection[min_waste_id]

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

def try_combine_scenarios(collection: list[Scenario]) -> bool:
  for i in range(0, len(collection)):
    for j in range(0, len(collection)):
      if i == j:
        continue

      a = collection[i]
      b = collection[j]

      pices_total = a[2].copy()
      pices_total.extend(b[2])

      scenario_buffer = []
      append_scenario(pices_total, scenario_buffer)

      result = scenario_buffer[0] if len(scenario_buffer) > 0 else None

      if result is None:
        continue

      # The resulting waste has to be smaller than or equal to the sum of
      # both a and b, in order to not make things worse
      if result[2] > a[2] + b[2]:
        continue

      # The resulting supplier length should be strictly bigger than
      # the previous length, as another pice has been added
      if result[1] <= max(a[1], b[1]):
        continue

      # Combined successfully, remove both i and j and append the result
      collection.remove(a)
      collection.remove(b)
      collection.append(result)
      return True

  return False

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

  while True:
    if not try_combine_scenarios(resulting_scenarios):
      break

  for scenario in resulting_scenarios:
    print(f'length={scenario[0]}, waste={scenario[1]}, pices={scenario[2]}')

if __name__ == '__main__':
  main()