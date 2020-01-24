def csv_compiler(protein):
    '''
    makes an csv file with protein stats
    '''

    directions = get_path_directions(protein)

    with open('protein.csv', 'w') as csvfile:
        fieldnames = ['amino', 'direction', 'coordinates']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for number, amino in enumerate(protein.sequence):
            writer.writerow({'amino': amino, 'direction': directions[number], 'coordinates': protein.path[number][1]})

def csv_reader():
    '''
    creates a protein object where the path is defined in the csv file as made by csv_compiler where the filename is protein.csv and information is given as:
    amino, direction, coordinate
    '''
    sequence = ""
    coordinates = []
    with open('protein.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                sequence += row[0]
                coordinates.append(ast.literal_eval(row[2]))
            line_count += 1

    if coordinates == [] or sequence == "":
        return f"No data found"


    if len(coordinates[0]) == 2:
        protein = Protein(sequence)
    else:
        protein = Protein(sequence, dim3=True)

    number = 2
    for amino in protein.sequence[2:]:
        protein.add_step(amino, coordinates[number])
        number += 1

    return protein

def get_path_directions(protein):
    '''
    converts path into format as specified by case assignment
    directions between subsequent aminoacids are signified by numbers, where:
       -1, 1 represent unit steps along the x-axis
       -2, 2 represent unit steps along the y-axis
       -3, 3 represent unit steps along the z-axis if protein in 3D
       0 terminates the sequence
    '''
    # obtain positions from path
    positions = [point[1] for point in protein.path]

    directions = []
    for i in range(len(positions)-1):
        # append appropriate number for each step's direction
        if not protein.dim3:
            directions.append(
                1 * (positions[i + 1][0] - positions[i][0]) +
                2 * (positions[i + 1][1] - positions[i][1])
            )
        else:
            directions.append(
                1 * (positions[i + 1][0] - positions[i][0]) +
                2 * (positions[i + 1][1] - positions[i][1]) +
                3 * (positions[i + 1][2] - positions[i][2])
            )
    # append 0 to terminate the sequence
    directions.append(0)
    return directions
