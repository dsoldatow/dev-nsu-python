import vk_api
import getpass

from password import PASSWORD
pswd = PASSWORD

vk_session = vk_api.VkApi('+79134636437', pswd)
vk_session.auth()

vk = vk_session.get_api()


# a = vk.users.get(user_ids=['dsoldatow'], fields=['last_seen'])
# print(a)
#
# groups = ['abiturient_ef_nsu', 'mmfnsu2018', 'nsuabiturient', 'ef_nsu', 'mathematics_mechanics_department']
# groups_names = vk.groups.getById(group_ids=groups)
#
# members = vk.groups.getMembers(group_id='mmfnsu2018')
# print(members['count'])
# [print(mem) for mem in members['items']]

# for i, group in enumerate(groups):
#     id_users_in_group = vk.groups.getMembers(group_id=group)['items']
#     users = vk.users.get(user_ids=id_users_in_group, fields=['last_seen'])
#     count_all = 0
#     count_ios = 0
#     for user in users:
#         if user.get('last_seen') is None:
#             continue
#         # print(user)
#         platform = user['last_seen'].get('platform')
#
#         if platform in [2, 3]:
#             count_ios += 1
#
#         if platform in [2, 3, 4]:
#             count_all += 1
#
#     print('*' * 50)
#     print(group, groups_names[i]['name'])
#     print('IOS: ', count_ios)
#     print('ALL: ', count_all)
#     print('%:   ', count_ios / count_all)
#     print('*' * 15)


