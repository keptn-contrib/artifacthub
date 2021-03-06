import os
import yaml
import argparse
from github import Github
import datetime
from utils import replace_relative_paths, DATETIME_FORMAT


def get_yaml_content(repo, release):
    content = {
        'version': release.tag_name,
        'name': repo.name,
        'displayName': repo.name,
        'createdAt': release.created_at.strftime(DATETIME_FORMAT),
        'description': repo.description,
        'digest': datetime.datetime.now().strftime(DATETIME_FORMAT),
        'license': repo.get_license().license.spdx_id,
        'homeURL': 'https://keptn.sh/docs/integrations/',
        'keywords': ['keptn', repo.owner.login.split('-')[1]],
        'links': [{
            'name': 'Source',
            'url': f'https://github.com/{repo.owner.login}/{repo.name}/tree/{release.target_commitish}'
        }],
        'annotations': {
            'keptn/org': repo.owner.login.split('-')[1]
        }
    }

    return content


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repository', type=str,
                        required=True, help='Name of Github repository')
    parser.add_argument('-v', '--version', type=str,
                        default='', help='Version (default=latest)')
    args = parser.parse_args()

    g = Github()

    repo = g.get_repo(args.repository)

    if args.version == '':
        if repo.get_releases().totalCount != 0:
            release = repo.get_latest_release()
        else:
            raise Exception('No release available')
    else:
        try:
            release = repo.get_release(args.version)
        except:
            raise Exception(f'Release {args.version} not found.')

    folder_path = os.path.join(repo.name, release.tag_name)

    os.makedirs(repo.name, exist_ok=True)
    os.makedirs(folder_path, exist_ok=True)

    branch_name = release.target_commitish

    # https://github.com/PyGithub/PyGithub/issues/1157#issuecomment-507498931
    readme = repo.get_contents(
        'README.md', ref=branch_name).decoded_content.decode('utf-8')

    # Replace relative image paths with absolute paths pointing to the github repo
    readme = replace_relative_paths(readme, args.repository, branch_name)

    with open(os.path.join(folder_path, 'README.md'), 'w') as f:
        f.write(readme)

    with open(os.path.join(folder_path, 'artifacthub-pkg.yml'), 'w') as f:
        yaml.dump(get_yaml_content(repo, release), f, sort_keys=False)
