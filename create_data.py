import simulacrum as sm

test = {'names': {'type': 'name'},
        'scores': {'type': 'norm', 'mean': .5, 'sd': .2}
        }

res = sm.create(100, coltypes=test)

print(res)