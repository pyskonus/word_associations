from pyexcel_ods3 import get_data
import json

def m_f_present(row):
    """
    This function checks if male or female associations are present in the given row.
    If, for example, female associations are present, and male are not, it returns
    (False, True).
    :param row: list, which represents the row
    :return: tuple, that has two boolean values
    """
    try:
        male_present = True
        if not row[1]:
            raise IndexError
    except IndexError:
        male_present = False
    try:
        female_present = True
        if not row[5]:
            raise IndexError
    except IndexError:
        female_present = False

    return male_present, female_present


def create_dict():
    df = get_data("dict.ods")
    # f = open("slovnyk.json", 'w')
    # f.write(json.dumps(df, ensure_ascii=False, indent=2))
    # f.close()

    dct = {}
    current_key = ''
    for row in df["Sheet1"]:
        # check if reached the end of the document
        if not row:
            break
        # check if the word has any more male and/or female associations
        m_f = m_f_present(row)
        if row[0] != "":
            current_key = row[0]

            if m_f == (True, True):
                dct[current_key] = ([row[3], (row[1], row[2])], [row[7], (row[5], row[6])])
            elif m_f == (True, False):
                dct[current_key] = ([row[3], (row[1], row[2])], [])
            else:
                dct[current_key] = ([], [row[7], (row[5], row[6])])

        else:
            if m_f[0]:
                dct[current_key][0].append((row[1], row[2]))
            if m_f[1]:
                dct[current_key][1].append((row[5], row[6]))

    f = open("slovnyk.json", 'w')
    f.write(json.dumps(dct, ensure_ascii=False, indent=2))
    f.close()

    return dct


if __name__ == '__main__':
    thedict = create_dict()
    cntr = 0
    for element in thedict:
        if cntr == 5:
            break
        print(element, thedict[element], sep='   ')
        cntr += 1
