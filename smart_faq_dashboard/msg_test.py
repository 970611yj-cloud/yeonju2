from thefuzz import fuzz

query = "액티브 에너지젤"
target = "에너지젤"
print(f"Query: {query}, Target: {target}")
print(f"Token Set Ratio: {fuzz.token_set_ratio(query, target)}")
print(f"Partial Ratio: {fuzz.partial_ratio(query, target)}")
print(f"Token Sort Ratio: {fuzz.token_sort_ratio(query, target)}")

query2 = "단백지쉐이크"
target2 = "단백질 쉐이크"
print(f"Query: {query2}, Target: {target2}")
print(f"Token Set Ratio: {fuzz.token_set_ratio(query2, target2)}")
print(f"Partial Ratio: {fuzz.partial_ratio(query2, target2)}")
