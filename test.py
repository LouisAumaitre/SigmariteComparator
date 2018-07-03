from sigmar.compendium.stormcast_eternals import liberators

units = [
    liberators
]

for u in units:
    for w_c in u.average_damage():
        print(f'{u.name}: {round(w_c, 2)} dpt')
