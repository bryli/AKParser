import json
from collections import Counter

ALLSKL = 'allSkillLvlup' # Key for character dictionary to get 2-7 level up mats
LVCOST = 'lvlUpCost'
MCOSTC = 'levelUpCostCond' # Key for mastery level cost upgrades.
MCOST = 'levelUpCost'
SKILLS = 'skills'
ELITE = 'phases'
PROMOTE = 'evolveCost'
RARE = 'rarity'
ID = 'id'
CT = 'count'
CHAR_LOC = "chardata.json"
FORMULAS = "formulas.json"
ITEMNAMES = "itemnames.json"
ITEMIDS = "itemids.json"
MASTERY = "masterylist.json"
NM = 'name'
COST = 'costs'

def main():
    try:
        with open(CHAR_LOC, "r") as charfile:
            chardata = (json.loads(charfile.read()))
        with open(FORMULAS, "r") as fmfile:
            formulas = (json.loads(fmfile.read()))
        with open(ITEMNAMES, "r") as inmfile:
            itemnames = (json.loads(inmfile.read()))
        with open(ITEMIDS, "r") as iidfile:
            itemids = (json.loads(iidfile.read()))
        with open(MASTERY, "r") as mstrfile:
            masterylist = (json.loads(mstrfile.read()))
    except Exception:
        return IOError("Failed to read files.")
    compiled_mats = {}
    [chardata.pop(char) for char in list(chardata.keys()) if chardata[char][RARE] < 2]
    for char in chardata.keys():
        compiled_mats.update(charCost(char, chardata, formulas, itemnames, itemids,
                                      masterylist.get(chardata[char][NM])))
    return(compiled_mats)


def charCost(char, chardata, formulas, itemnames, itemids, mastery = None, reduce = ['Loxic Kohl', 'Grindstone']):
    rarity = chardata[char][RARE]
    if mastery is None:
        if rarity < 5:
            mastery = [1, 2]
        else:
            mastery = [1, 2, 3]
    elitemats = eliteCost(char, chardata)
    skillmats = skillCost(char, chardata, mastery)
    if reduce is not None:
        if rarity > 2:
            elitemats = reduceMaterials(elitemats, formulas, itemnames, reduce)
        skillmats = reduceMaterials(skillmats, formulas, itemnames, reduce)
    elitemats = dict((itemids[itemid], count) for (itemid, count) in elitemats.items())
    skillmats = dict((itemids[itemid], count) for (itemid, count) in skillmats.items())
    # Combines elitemats and skillmats by adding the values corresponding to keys in both sets.
    totmats = Counter(elitemats)
    totmats.update(Counter(skillmats))
    return {chardata[char][NM]:[mastery, elitemats, skillmats, totmats]}

def skillCost(char, chardata, toMaster):
    # chardata[char] -> char info
    # chardata[char]['allSkillLvlup'] -> list of list of dictionaries of items for skill level up costs 2-7
    # for sklv in chardata[char]['allSkillLvlup']: Unlock info and level up cost for each skill level
    #     for mats in sklv['lvlUpCost']: mats for unlock
    #         mats['id'] id of item
    #         mats['count'] # of item
    rarity = chardata[char][RARE]
    skillmats = {}
    for sklv in chardata[char][ALLSKL]:
        for mats in sklv[LVCOST]:
            skillmats[mats[ID]] = mats[CT]
    if rarity > 2:
        for skill in toMaster:
            for sklv in chardata[char][SKILLS][skill - 1][MCOSTC]:
                for mats in sklv[MCOST]:
                    if mats[ID] in skillmats:
                        skillmats[mats[ID]] += mats[CT]
                    else:
                        skillmats[mats[ID]] = mats[CT]
    return skillmats

def eliteCost(char, chardata):
    elitemats = {}
    rarity = chardata[char][RARE]
    if rarity > 2:
        for eliteStgNum in range(len(chardata[char][ELITE])):
            if eliteStgNum > 0:
                for mats in chardata[char][ELITE][eliteStgNum][PROMOTE]:
                    if mats[ID] in elitemats:
                        elitemats[mats[ID]] += mats[CT]
                    else:
                        elitemats[mats[ID]] = mats[CT]
        return elitemats
    else:
        return None

def reduceMaterials(mats, formulas, itemnames, reducemats):
    toReduce = []
    for item in reducemats:
        toReduce.append(itemnames[item])
    result = {item:0 for item in toReduce}
    for mat in mats.keys():
        reduced = reduce({mat:mats[mat]}, formulas, toReduce)
        for itemid in reduced.keys():
            result[itemid] += reduced[itemid]
    return(result)


def reduce(mat, formulas, reducemats):
    result = {item: 0 for item in reducemats}
    key = list(mat.keys())[0]
    if key in result:
        result[key] += mat[key]
        return result
    elif len(formulas[key][COST]) == 0:
        return result
    else:
        for item in formulas[key][COST]:
            reduced = reduce({item[ID]:item[CT]}, formulas, reducemats)
            for itemid in reduced.keys():
                    result[itemid] += reduced[itemid] * mat[key]
        return result

if __name__ == '__main__':
    main()