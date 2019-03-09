from pyexcel_ods3 import get_data
import json


def create_dict():
    df = get_data("as_dict.ods")
    f = open("slovnyk.json", 'w')
    f.write(json.dumps(df, ensure_ascii=False, indent=2))
    f.close()

    dct = {}
    for row in df["Sheet1"]:
        if row[0] != "":
            current_key = row[0]
            # check which if the word has male and/or female associations
            try:
                male_present = True
                row[1]
            except IndexError:
                male_present = False
            try:
                female_present = True
                row[5]
            except IndexError:
                female_present = False

            if male_present and female_present:
                dct[current_key] = ([row[3], (row[1], row[2])], [row[7], (row[5], row[6])])
            elif male_present:
                dct[current_key] = ([row[3], (row[1], row[2])], [])
            else:
                dct[current_key] = ([], [row[7], (row[5], row[6])])

        else:
            try:
                dct[current_key][0].append((row[1], row[2]))
            except IndexError:
                pass
            try:
                dct[current_key][1].append((row[5], row[6]))
            except IndexError:
                pass

    return dct


if __name__ == '__main__':
    thedict = create_dict()
    for element in thedict:
        print(element, thedict[element], sep='   ')