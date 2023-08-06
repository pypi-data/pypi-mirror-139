

def addTreatments(design, mainEffects):
    """ Add treatments information to design matrix 

    design is a pandas dataframe with the design matrix as created by the doepy package
    mainEffects is a list of the columns that define main effects
    """
    design = design.copy()
    mainEffects = mainEffects
    treatments = []
    for _, row in design.iterrows():
        treatment = ''.join([effect for effect in mainEffects if row[effect] == 1])
        if not treatment:
            treatment = '(1)'
        treatments.append(treatment)
    design.insert(0, 'Treatments', treatments)
    return design
