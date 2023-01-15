import models
import requests
import json
from datetime import datetime, timedelta

MINIMUM_MAINTAINERS_NUMBER = 2
MAXIMUM_LAST_VERSION_DAYS_AGE = 30
MAXIMUM_LAST_COMMIT_DAYS_AGE = 14


def check_health_of_packages(packages: models.Packages) -> dict[bool, str]:
    return {package_name: _check_health_of_package(package_data) for
            package_name, package_data in {package_name: _get_package_data(package_name) for
            package_name in packages.packages_names_list}.items()}


def _check_health_of_package(package_data: dict) -> bool:
    return _check_health_by_maintainers(package_data) and _check_health_by_last_version_date(
        package_data) and _check_health_by_last_commit_date(package_data)


def _get_package_data(package_name: str) -> dict:
    url = f'https://api.npms.io/v2/package/{package_name}'
    response = requests.get(url)
    package_data = json.loads(response.content)
    return package_data


def check_health_by_last_version_date(package_data: dict) -> bool:
    healthy_date = datetime.today() - timedelta(days=MAXIMUM_LAST_VERSION_DAYS_AGE)
    last_version_date = datetime.strptime(
        package_data["collected"]["metadata"]["date"], '%Y-%m-%dT%H:%M:%S.%fZ')
    return True if last_version_date >= healthy_date else False


def check_health_by_maintainers(package_data: dict) -> bool:
    package_maintainers_number = len(
        package_data["collected"]["metadata"]["maintainers"])
    return True if package_maintainers_number >= MINIMUM_MAINTAINERS_NUMBER else False


def _check_health_by_last_commit_date(package_data: dict) -> bool:
    healthy_date = datetime.today() - timedelta(days=MAXIMUM_LAST_COMMIT_DAYS_AGE)
    return True if _get_last_commit_date(package_data) >= healthy_date else False


def _get_last_commit_date(package_data: dict):
    github_link_splited = package_data["collected"]["metadata"]["links"]["repository"].split(
        '/')
    repo = github_link_splited[len(github_link_splited) - 1]
    owner = github_link_splited[len(github_link_splited) - 2]
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    response = requests.get(url)
    commits = response.json()
    last_commit_date = datetime.strptime(
        commits[0]["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ")
    return last_commit_date
