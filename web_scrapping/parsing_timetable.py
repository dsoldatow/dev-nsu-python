import requests as req
from bs4 import BeautifulSoup
import re


def get_text_from_attr_of_soup_find_all(attrs):
    for atr in attrs:
        yield atr.text


def get_groups():
    """
    :return:     {fac:[groups],}
    """
    faculties = ['ggf', 'gi', 'imp', 'iphp', 'mmf', 'fen', 'fit', 'ff', 'ef']
    groups = {}

    base_url_group = 'https://table.nsu.ru/faculty/'
    for fac in faculties:
        groups[fac] = []
        url = base_url_group + fac
        resp = req.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        groups[fac] += list(get_text_from_attr_of_soup_find_all(soup.findAll("a", {"class": "group"})))

    return groups


def get_params_from_cell(cell):
    params = cell.split('  ')
    for i in params.copy():
        new = re.sub("^\s+|\n|\r|\s+$", '', i)
        if not bool(new):
            params.remove(i)
    return params


def is_type_lesson(tp):
    return 'пр' in tp or 'лек' in tp


letters = {
    'а': 'a',
    'и': 'i',
    'б': 'b',
    'м': 'm',
    'c': 's',

}


def change_letter(tp):
    for i, j in letters.items():
        tp = tp.replace(i, j)

    return tp


def get_timetable_from_group(group, fac=None):
    days = {
        0: 'monday',
        1: 'tuesday',
        2: 'wednesday',
        3: 'thursday',
        4: 'friday',
        5: 'saturday',
        6: 'sunday'
    }
    try:
        int(group)
    except:
        group = change_letter(group)

    resp = req.get('https://table.nsu.ru/group/' + group)
    # with open('huy.html', 'w') as f:
    #     f.write(resp.text)
    soup = BeautifulSoup(resp.text, 'html.parser')
    subjects = soup.findAll("td")
    a = 3
    calend_v1 = {}
    for i in range(14, len(subjects)):
        if i % 7 == 0:
            calend_v1[subjects[i].text] = []
        else:
            calend_v1[subjects[(i // 7) * 7].text] += [subjects[i].text]

    calend = []
    time = list(calend_v1.keys())
    # print(time)
    if not (isinstance(time, list) and len(time) >= 7):
        # print(fac, group)
        return []
    for i in range(7):
        for j, cell in enumerate(calend_v1[time[i]]):
            params = get_params_from_cell(cell)
            l_par = len(params)
            week = type_lesson = cab = teacher = subject = ''
            try:
                if l_par >= 3:
                    if l_par > 5:
                        if l_par == 6:
                            week_f = ''
                            if is_type_lesson(params[3]):
                                type_lesson = params[3].split('')
                                teacher = ''
                            else:
                                type_lesson = ''
                                teacher = params[3]
                        elif l_par > 8:
                            week_f = params[4]
                            week = params[8]
                            type_lesson = params[4].split()[1]
                            teacher = params[3]

                        else:
                            week_f = ''
                            week = ''
                            type_lesson = params[4]
                            teacher = params[3]
                        type_lesson_f, subject, cab = params[0], params[1], params[2]
                        instance = {
                            'week': re.sub("^\s+|\n|\r|\s+$", '', week_f),
                            'type': re.sub("^\s+|\n|\r|\s+$", '', type_lesson_f),
                            'time': time[i],
                            'cab': re.sub("^\s+|\n|\r|\s+$", '', cab),
                            'teacher': re.sub("^\s+|\n|\r|\s+$", '', teacher),
                            'subject': re.sub("^\s+|\n|\r|\s+$", '', subject),
                            'day': days[j],
                            'group': group
                        }
                        calend.append(instance)

                        subject, cab, teacher = params[5], params[6], params[7]
                    if l_par == 5:
                        type_lesson, subject, cab, teacher, week = params[0], params[1], params[2], params[3], params[4]
                    if l_par == 4:
                        type_lesson, subject, cab, teacher, week = params[0], params[1], params[2], params[3], ''
                    if l_par < 4:
                        # print(params)
                        type_lesson, subject, cab = params
                # убрать if тогда будут даже пустые
                if True or subject:
                    instance = {
                        'week': re.sub("^\s+|\n|\r|\s+$", '', week),
                        'type': re.sub("^\s+|\n|\r|\s+$", '', type_lesson),
                        'time': time[i],
                        'cab': re.sub("^\s+|\n|\r|\s+$", '', cab),
                        'teacher': re.sub("^\s+|\n|\r|\s+$", '', teacher),
                        'subject': re.sub("^\s+|\n|\r|\s+$", '', subject),
                        'day': days[j],
                        'group': group
                    }
                    calend.append(instance)
            except:
                pass
    return calend


def get_all_time_table():
    groups = get_groups()
    all_time_table = []
    count = 0
    counter = 0
    for i, grps in groups.items():
        # print(i,grps)
        count += len(grps)
        for gr in grps:
            all_time_table += get_timetable_from_group(gr, fac=i)
            counter += 1
            print(counter)
    return all_time_table
print(get_timetable_from_group('20137'))