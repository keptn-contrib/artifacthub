import os
import re
import yaml
from github import Github
from urllib.parse import urljoin


def get_subdirectories(d):
    # https://stackoverflow.com/a/973492
    return [o for o in os.listdir(d) 
                    if os.path.isdir(os.path.join(d,o))]

if __name__ == '__main__':
    directories = get_subdirectories('./')
    directories = [d for d in directories if not d.startswith('.') and not d == 'workflow']
    
    g = Github()
    
    for d in directories:
        latest_version = get_subdirectories(d)[-1]
        with open(os.path.join(d, latest_version, 'artifacthub-pkg.yml'), 'r') as stream:
            try:
                artifacthub_config = yaml.safe_load(stream)
                repository_name = [link['url'] for link in artifacthub_config['links'] if link['name'] == 'Source'][0].replace('https://github.com/', '').partition('/tree')[0]
                
                repo = g.get_repo(repository_name)
                
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

                    image_regex = r'(?:\[(?P<caption>.*?)\])\((?P<path>.*?)\)'

                    # Replace relative image paths with absolute paths pointing to the github repo
                    for match in re.finditer(image_regex, readme, re.IGNORECASE | re.MULTILINE):
                        caption, path = match.group('caption', 'path')
                        absolute_path = urljoin(
                            f'https://raw.githubusercontent.com/{repository_name}/{branch_name}/', path)
                        readme = readme.replace(path, absolute_path)

                    with open(os.path.join(release_folder, 'README.md'), 'w') as f:
                        f.write(readme)
                    
                    datetime_format = '%Y-%m-%mT%H:%M:%SZ'
                    
                    artifacthub_config['version'] = release_version
                    artifacthub_config['createdAt'] = release.created_at.strftime(datetime_format)
                    artifacthub_config['digest'] = release.created_at.strftime(datetime_format)
                    
                    with open(os.path.join(release_folder, 'artifacthub-pkg.yml'), 'w') as f:
                        yaml.dump(artifacthub_config, f, sort_keys=False)
                    
            except yaml.YAMLError as exc:
                print(exc)
