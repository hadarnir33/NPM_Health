import models
import requests
import json
from datetime import datetime, timedelta

MINIMUM_MAINTAINERS_NUMBER = 2
MAXIMUM_LAST_VERSION_DAYS_AGE = 30
MAXIMUM_LAST_COMMIT_DAYS_AGE = 14


def check_health_of_packages(packages: models.Packages) -> bool:
    packages_health_list = {}
    for package_name in packages.packages_names_list:
        package_data = get_package_data(package_name)
        health = check_health_by_maintainers(package_data) and check_health_by_last_version_date(package_data)
        packages_health_list[package_name] = health
    return packages_health_list


def get_package_data(package_name: str) -> dict:
    url = f'https://api.npms.io/v2/package/{package_name}'
    response = requests.get(url)
    package_data = json.loads(response.content)
    return package_data


def check_health_by_last_version_date(package_data: dict) ->bool:
    healthy_date = datetime.today() - timedelta(days=MAXIMUM_LAST_VERSION_DAYS_AGE)
    last_version_date = datetime.strptime(package_data["collected"]["metadata"]["date"], '%Y-%m-%dT%H:%M:%S.%fZ')
    return True if last_version_date >= healthy_date else False


def check_health_by_maintainers(package_data: str) -> bool:
    package_maintainers_number = len(package_data["collected"]["metadata"]["maintainers"])
    return True if package_maintainers_number >= MINIMUM_MAINTAINERS_NUMBER else False


def check_health_by_last_commit_date(packag_data: str) ->bool:
    pass