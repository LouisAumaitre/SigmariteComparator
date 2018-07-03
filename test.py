from sigmar.compendium.stormcast_eternals import liberators

units = [
    liberators
]

for u in units:
    for w_c_n, w_c_d in u.average_damage().items():
        print(f'{u.name} with {w_c_n}: {round(w_c_d, 2)} dpt')
