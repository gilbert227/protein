import random

protein = "HHPHHHPH"
configs = []
no_of_duplicates = 0
max_duplicates   = 100

max_iter = 200000

for i in range(max_iter):
    while no_of_duplicates < max_duplicates:
        
        config = {}
        
        for number, amino in enumerate(protein):
        
            if number in (0,1):
                # set starting conditions
                config[number] = [amino, (number, 0)]
            else:
                prev_coordinate = config[number-1][1]
        
                options = [(prev_coordinate[0] + 1, prev_coordinate[1]), (prev_coordinate[0] - 1, prev_coordinate[1]),
                (prev_coordinate[0], prev_coordinate[1] + 1), (prev_coordinate[0], prev_coordinate[1] - 1)]
        
                for j in config.values():
                    if j[1] in options:
                         options.remove(j[1])
        
                if options == []:
                    break
                
                new_coordinate = random.choice(options)
                config[number] = [amino, new_coordinate]
        if config not in configs:
            configs.append(config)
        else:
            no_of_duplicates += 1
print(len(configs))
