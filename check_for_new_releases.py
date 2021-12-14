import os
import yaml
from github import Github
from utils import replace_relative_paths, DATETIME_FORMAT


def get_subdirectories(d: str) -> list:
    """Gets all the subdirectors of directory d"""
    # https://stackoverflow.com/a/973492
    return [o for o in os.listdir(d)
            if os.path.isdir(os.path.join(d, o))]


def get_repo_url(artifacthub_config) -> str:
    """Gets the repository url from the ArtifactHub config"""
    if 'links' in artifacthub_config:
        for link in artifacthub_config['links']:
            if link['name'] == 'Source':
                return link['url'].replace('https://github.com/', '').partition('/tree')[0]
    else:
        return None


if __name__ == '__main__':
    directories = get_subdirectories('./')
    directories = [d for d in directories if not d.startswith(
        '.') and not d in ['workflow', '__pycache__']]

    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        g = Github(github_token)
    else:
        g = Github()

    for d in directories:
        try:
            latest_version = get_subdirectories(d)[-1]
        except:
            print(f'{d} directory doesn\'t have a version yet')
            continue

        with open(os.path.join(d, latest_version, 'artifacthub-pkg.yml'), 'r') as stream:
            try:
                artifacthub_config = yaml.safe_load(stream)
                repository_name = get_repo_url(artifacthub_config)

                try:
                    repo = g.get_repo(repository_name)
                except Exception as e:
                    print(f'{d} has no public Github repository. Skipping!')
                    continue

                try:
                    release = repo.get_latest_release()
                except:
                    print(f'{d} has no release. Skipping!')
                    continue

                release_version = release.tag_name.strip().replace('release-', '')

                if release_version not in get_subdirectories(d):
                    release_folder = os.path.join(d, release_version)
                    os.makedirs(release_folder)

                    branch_name = release.target_commitish

                    # https://github.com/PyGithub/PyGithub/issues/1157#issuecomment-507498931
                    readme = repo.get_contents(
                        'README.md', ref=branch_name).decoded_content.decode('utf-8')

                    # Replace relative image paths with absolute paths pointing to the github repo
                    readme = replace_relative_paths(
                        readme, repository_name, branch_name)

                    with open(os.path.join(release_folder, 'README.md'), 'w') as f:
                        f.write(readme)

                    artifacthub_config['version'] = release_version
                    artifacthub_config['createdAt'] = release.created_at.strftime(
                        DATETIME_FORMAT)
                    artifacthub_config['digest'] = release.created_at.strftime(
                        DATETIME_FORMAT)

                    with open(os.path.join(release_folder, 'artifacthub-pkg.yml'), 'w') as f:
                        yaml.dump(artifacthub_config, f, sort_keys=False)

            except yaml.YAMLError as exc:
                print(exc)
