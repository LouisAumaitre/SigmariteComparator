from sigmar.compendium.stormcast_eternals import liberators

warscrolls = [
    liberators
]

for ws in warscrolls:
    for w_c_n, w_c_s in ws.stats().items():
        damage, health = w_c_s
        print(f'{ws.name} with {w_c_n}: {round(damage, 2)} dpt / {round(health, 2)} hp')

for ws in warscrolls:
    ws.simplest_stats()
