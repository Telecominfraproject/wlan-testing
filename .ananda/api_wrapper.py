#!/usr/bin/env python

import json
import requests
import argparse

ananda_api = 'https://api.ananda.net'


def get_bearer_token():
    authHeader = {"Authorization": args.token}
    r = requests.post(
        f'{ananda_api}/login-accounts/v1.2/auths/apis/oauth/token',
        headers=authHeader)

    try:
        org_id = r.json()['meta']['orgId']
        token = r.json()['access_token']
    except Exception:
        print('Error: could not get bearer token.')
        exit(1)

    return org_id, token


def logout():
    authHeader = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f'{ananda_api}/login-accounts/v1.2/auths/logout',
        headers=authHeader)


def get_user_id():
    authHeader = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f'{ananda_api}/manage-accounts/v1.2/api/orgs/{org_id}/users',
        headers=authHeader)

    try:
        for key in r.json():
            user_data = key
            if user_data['email'] == args.user or user_data['name'] == args.user:
                user_id = user_data['userId']
                break
    except Exception:
        print('Error: user was not found')
        exit(1)

    return user_id


def get_group_id():
    authHeader = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f'{ananda_api}/manage-accounts/v1.2/api/orgs/{org_id}/groups',
        headers=authHeader)

    try:
        for key in r.json():
            group_data = key
            if group_data['name'] == args.group:
                group_id = group_data['groupId']
                break
    except Exception:
        print('Error: group was not found')
        exit(1)

    return group_id


def get_user_groups():
    user_id = get_user_id()

    authHeader = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f'{ananda_api}/manage-accounts/v1.2/api/orgs/{org_id}/users/{user_id}',
        headers=authHeader)

    try:
        user_groups = r.json()['groupIds']
    except Exception:
        print('Error: user was not found')
        exit(1)

    return user_groups


def list_resource(resource):
    authHeader = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f'{ananda_api}/manage-accounts/v1.2/api/orgs/{org_id}/{resource}',
        headers=authHeader)

    print(json.dumps(r.json(), indent=4, sort_keys=True))


def set_user_groups():
    user_id = get_user_id()
    group_id = get_group_id()
    user_groups = get_user_groups()

    authHeader = {"Authorization": f"Bearer {token}"}

    if args.api_call == 'add_user_to_group':
        data = user_groups + [group_id]
    elif args.api_call == 'remove_user_from_group':
        try:
            user_groups.remove(group_id)
        except Exception:
            print('Error: user is not in group')
            exit(1)
        data = user_groups

    r = requests.post(
        f'{ananda_api}/manage-accounts/v1.2/api/orgs/{org_id}/users/{user_id}/groups',
        json=data,
        headers=authHeader)


def main():
    if args.api_call == 'list_users':
        list_resource('users')
    if args.api_call == 'list_groups':
        list_resource('groups')
    if args.api_call == 'add_user_to_group' or args.api_call == 'remove_user_from_group':
        set_user_groups()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'api_call',
        help='The API call you want to make, currently supported are: '
             'list_users, '
             'list_groups, '
             'add_user_to_group, '
             'remove_user_from_group')
    parser.add_argument('--token', help='your Ananda API token')
    parser.add_argument(
        '--user',
        help='user you want to add to or remove from group, '
             'you can either specify email address or first and last name')
    parser.add_argument('--group', help='name of the group you want to add or remove a user from')
    args = parser.parse_args()

    org_id, token = get_bearer_token()
    main()
    logout()
