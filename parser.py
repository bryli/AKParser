import tbltrim
import calc

RETRIM = False

if (RETRIM): tbltrim.main()
compiled_mats = calc.main()

with open('results.csv', 'w', encoding='utf-8') as resfile:
    for char in compiled_mats.keys():
        mastery = compiled_mats[char][0]
        if len(mastery) > 0:
            mastery = "S" + "/".join(str(skill) for skill in mastery)
        else:
            mastery = "N/A"
        mats = compiled_mats[char][1].keys()
        matDetails = []
        for key in mats:
            matDetails.append([compiled_mats[char][1][key],
                         compiled_mats[char][2][key],
                         compiled_mats[char][3][key]])
        resfile.write(char+","+mastery+","+",".join(
            [str(item) for numNeeded in matDetails for item in numNeeded])+"\n")