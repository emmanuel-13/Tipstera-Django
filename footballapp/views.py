import requests

from django.http import JsonResponse
from django.conf import settings

from .models import Area, Competition, Team, Match

BASE_URL = 'https://api.football-data.org/v2'
API_KEY = settings.FOOTBALL_DATA_API_TOKEN


def populate_areas(request):
    url = f'{BASE_URL}/areas'

    headers = {
        'X-Auth-Token': API_KEY,  # Replace with your actual API key
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        areas_data = response.json()['areas']

        for area_data in areas_data:
            area_id = area_data['id']
            name = area_data['name']
            code = area_data.get('code')
            flag = area_data['ensignUrl']

            Area.objects.update_or_create(
                id=area_id,
                defaults={
                    'name': name,
                    'code': code,
                    'flag': flag
                }
            )

        return JsonResponse({'message': 'Areas populated successfully'})

    return JsonResponse({'error': 'Failed to fetch areas'}, status=response.status_code)


def populate_competitions(request):
    url = f'{BASE_URL}/competitions'

    headers = {
        'X-Auth-Token': API_KEY,  # Replace with your actual API key
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        competitions_data = response.json()['competitions']

        for competition_data in competitions_data:
            competition_id = competition_data['id']
            area_id = competition_data['area']['id']
            name = competition_data['name']
            code = competition_data['code']
            emblem = competition_data.get('emblemUrl', '')

            area = Area.objects.get(id=area_id)

            Competition.objects.update_or_create(
                id=competition_id,
                defaults={
                    'area': area,
                    'name': name,
                    'code': code,
                    'emblem': emblem
                }
            )

        return JsonResponse({'message': 'Competitions populated successfully'})

    return JsonResponse({'error': 'Failed to fetch competitions'}, status=response.status_code)


def populate_teams(request):
    teams_url = f'{BASE_URL}/teams'
    areas_url = f'{BASE_URL}/areas'

    headers = {
        'X-Auth-Token': API_KEY,  # Replace with your actual API key
        'Accept': 'application/json',
    }

    response = requests.get(areas_url, headers=headers)

    if response.status_code == 200:
        areas_data = response.json()['areas']

        for area_data in areas_data:
            area_id = area_data['id']
            teams_url_with_area = f'{teams_url}?areas={area_id}'

            teams_response = requests.get(teams_url_with_area, headers=headers)

            if teams_response.status_code == 200:
                teams_data = teams_response.json()['teams']

                for team_data in teams_data:
                    team_id = team_data['id']
                    name = team_data['name']
                    short_name = team_data.get('shortName', '')
                    tla = team_data.get('tla', '')
                    crest = team_data.get('crestUrl', '')

                    area = Area.objects.get(id=area_id)

                    Team.objects.update_or_create(
                        id=team_id,
                        defaults={
                            'area': area,
                            'name': name,
                            'shortName': short_name,
                            'tla': tla,
                            'crest': crest
                        }
                    )

        return JsonResponse({'message': 'Teams populated successfully'})

    return JsonResponse({'error': 'Failed to fetch areas'}, status=response.status_code)


# def populate_matches(request):
#     url = f'{BASE_URL}/matches'

#     headers = {
#         'X-Auth-Token': API_KEY,  # Replace with your actual API key
#         'Accept': 'application/json',
#     }

#     params = {
#         'season': '2023',  # Replace with the desired season
#     }

#     response = requests.get(url, headers=headers, params=params)

#     if response.status_code == 200:
#         matches_data = response.json()['matches']

#         for match_data in matches_data:
#             match_id = match_data['id']
#             utc_date = match_data['utcDate']
#             status = match_data['status']
#             minute = match_data.get('minute')
#             injury_time = match_data.get('injuryTime')
#             attendance = match_data.get('attendance')
#             venue = match_data.get('venue')
#             match_day = match_data['matchday']
#             stage = match_data.get('stage', '')
#             group = match_data.get('group', '')
#             home_team_id = match_data['homeTeam']['id']
#             away_team_id = match_data['awayTeam']['id']
#             score_home = match_data['score']['fullTime'].get('homeTeam')
#             score_away = match_data['score']['fullTime'].get('awayTeam')

#             competition_id = match_data['competition']['id']
#             competition = Competition.objects.get(id=competition_id)

#             home_team = Team.objects.get_or_create(id=home_team_id)
#             away_team = Team.objects.get_or_create(id=away_team_id)

#             Match.objects.update_or_create(
#                 id=match_id,
#                 defaults={
#                     'competition': competition,
#                     'utcDate': utc_date,
#                     'status': status,
#                     'minute': minute,
#                     'injuryTime': injury_time,
#                     'attendance': attendance,
#                     'venue': venue,
#                     'matchDay': match_day,
#                     'stage': stage,
#                     'group': group,
#                     'homeTeam': home_team,
#                     'awayTeam': away_team,
#                     'scoreHome': score_home,
#                     'scoreAway': score_away,
#                 }
#             )

#         return JsonResponse({'message': 'Matches populated successfully'})

#     return JsonResponse({'error': 'Failed to fetch matches'}, status=response.status_code)
