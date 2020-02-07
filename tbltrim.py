import json

CHAR_LOC = "character_table.json"
ITEM_LOC = "item_table.json"
FORMULA_LOC = "building_data.json"

FTYPE='formulaType'

FCT = 'manufactFormulas'
CHIP = "F_ASC"
FCT_REMOVE = ('weight', 'costPoint', 'formulaType', 'buffType', 'requireRooms', 'requireStages')

WRK = 'workshopFormulas'
ELITE = "F_EVOLVE"
WRK_REMOVE = ('apCost', 'formulaType', 'buffType', 'extraOutcomeRate', 'extraOutcomeGroup', 'requireRooms', 'requireStages')

ITM = 'items'
ITM_REMOVE = ('description', 'iconId', 'overrideBkg', 'stackIconId', 'sortId', 'usage', 'obtainApproach',
              'classifyType', 'itemType', 'stageDropList')
FMLINK = 'buildingProductList'
#ITM_VALS = list(range(3211, 3283)) + list(range(30011, 32001))

RARE = 'rarity'
CHAR_REMOVE = ('description', 'canUseGeneralPotentialItem', 'potentialItemId', 'team', 'displayNumber',
               'tokenKey', 'appellation', 'position', 'tagList', 'displayLogo', 'itemUsage', 'itemDesc',
               'itemObtainApproach', 'maxPotentialLevel', 'profession', 'trait', 'talents', 'potentialRanks',
               'favorKeyFrames')

RM = "roomType"
CONVRM = {"MANUFACTURE":"manufactFormulas", "WORKSHOP":"workshopFormulas"}
FMID = "formulaId"
NM = 'name'

COST = 'costs'

def pruneFormulas():
    try:
        with open(FORMULA_LOC, "r") as fmfile:
            fmdata = (json.loads(fmfile.read()))
    except Exception:
        return IOError("Failed to read file.")

    [fmdata.pop(datadesc) for datadesc in list(fmdata.keys()) if datadesc not in [FCT, WRK]]

    toRmv = []
    for fnum in fmdata[FCT].keys():
        if fmdata[FCT][fnum][FTYPE] == CHIP: # Keep formulas related to dualchip production (only in factories)
            [fmdata[FCT][fnum].pop(datarow) for datarow in FCT_REMOVE]
        else:
            toRmv.append(fnum)
    [fmdata[FCT].pop(fct_fnum) for fct_fnum in toRmv]

    toRmv = []
    for fnum in fmdata[WRK].keys():
        if fmdata[WRK][fnum][FTYPE] == ELITE:
            [fmdata[WRK][fnum].pop(datarow) for datarow in WRK_REMOVE]
        else:
            toRmv.append(fnum)
    [fmdata[WRK].pop(wrk_fnum) for wrk_fnum in toRmv]

    return fmdata

def pruneItems():
    try:
        with open(ITEM_LOC, "r") as itemfile:
            itemdata = (json.loads(itemfile.read()))
    except Exception:
        return IOError("Failed to read file.")

    [itemdata.pop(datadesc) for datadesc in list(itemdata.keys()) if datadesc != ITM]

    toRmv = []
    for fnum in itemdata[ITM].keys():
        if fnum.isdigit() and \
            ((int(fnum) >= 3211 and int(fnum) <= 3303) or (int(fnum) >= 30011 and int(fnum) <= 32001)):
            [itemdata[ITM][fnum].pop(datarow) for datarow in ITM_REMOVE]
            if (int(fnum) >= 3211 and int(fnum) <= 3303 and (int(fnum) % 10 != 3 or int(fnum) == 3303)):
                itemdata[ITM][fnum][FMLINK] = []
        else:
            toRmv.append(fnum)
    [itemdata[ITM].pop(itm_fnum) for itm_fnum in toRmv]

    return itemdata[ITM]

def pruneChars():
    try:
        with open(CHAR_LOC, "r") as charfile:
            chardata = (json.loads(charfile.read()))
    except Exception:
        return IOError("Failed to read file.")

    [chardata.pop(char) for char in list(chardata.keys()) if chardata[char][RARE] < 3 or char.startswith("token_")]

    for charnum in chardata.keys():
        [chardata[charnum].pop(datarow) for datarow in CHAR_REMOVE]

    return chardata

def itemmapper(itemdata, formulas):
    namedict = {}
    for inum in itemdata.keys():
        if len(itemdata[inum][FMLINK]) == 0:
            itemdata[inum][COST] = []
            itemdata[inum].pop(FMLINK)
        else:
            itemdata[inum][COST] = formulas[CONVRM[itemdata[inum][FMLINK][0][RM]]][itemdata[inum][FMLINK][0][FMID]][COST]
            itemdata[inum].pop(FMLINK)
        namedict[itemdata[inum][NM]] = inum
    return itemdata, namedict

def main(write = False):
    itemdata, namedict = itemmapper(pruneItems(), pruneFormulas())
    if write:
        with open('chardata.json', 'w', encoding='utf-8') as charw:
            json.dump(pruneChars(), charw, ensure_ascii=False, indent=4)
        with open('formulas.json', 'w', encoding='utf-8') as fmw:
            json.dump(itemdata, fmw, ensure_ascii=False, indent=4)
        with open('itemnames.json', 'w', encoding='utf-8') as inamew:
            json.dump(namedict, inamew, ensure_ascii=False, indent=4)
        with open('itemids.json', 'w', encoding='utf-8') as iidw:
            json.dump({itemid:itemname for itemname, itemid in namedict.items()}, iidw, ensure_ascii=False, indent=4)
    else:
        return [pruneChars(), itemdata, namedict]

if __name__ == '__main__':
    main(True)