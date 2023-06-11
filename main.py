import sys

accepted_supplier_lengths = [500, 1000, 1500, 2000]
cut_width = 3 # ~2.5mm blade width + .5mm tolerance

# tuple[supplier_length, waste, list[pice]]
Scenario = tuple[int, int, list[int]]

required_pices = [
  510, 510, 510, 510,
  300, 300, 300, 300,
  220, 220
]

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
  least_waste = None
  least_waste_id = None

  for i in range(0, len(collection)):
    current_waste = collection[i][1]

    if least_waste is None or least_waste > current_waste:
      least_waste = current_waste
      least_waste_id = i

  if least_waste_id is None:
    return None

  return collection[least_waste_id]

def main():
  resulting_scenarios: list[Scenario] = []

  print(f'Required pices: {",".join(map(str, required_pices))}')
  print(f'Accepted supplier lengths: {",".join(map(str, accepted_supplier_lengths))}')
  print(f'Cut width: {cut_width}')
  print()

  while len(required_pices) > 0:
    scenarios: list[Scenario] = []

    for i in range(0, len(required_pices)):
      i_pice = required_pices[i]

      pices = []
      pices.append(i_pice)
      append_scenario(pices, scenarios)

      for j in range(0, len(required_pices)):
        if i == j:
          continue

        j_pice = required_pices[j]
        pices.append(j_pice)
        append_scenario(pices, scenarios)

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