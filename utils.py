import re
from urllib.parse import urljoin


IMAGE_REGEX = r'(?:\[(?P<caption>.*?)\])\((?P<path>.*?)\)'
DATETIME_FORMAT = '%Y-%m-%mT%H:%M:%SZ'


def replace_relative_paths(readme: str, repository: str, branch_name: str) -> str:
    """Replace relative image paths with absolute paths pointing to the github repo"""
    for match in re.finditer(IMAGE_REGEX, readme, re.IGNORECASE | re.MULTILINE):
        m = match.group()
        _, path = match.group('caption', 'path')
        if path.startswith('#'):
            absolute_path = urljoin(
                f'https://github.com/{repository}/blob/{branch_name}/README.md', path)
        else:
            absolute_path = urljoin(
                f'https://raw.githubusercontent.com/{repository}/{branch_name}/', path)
        readme = readme.replace(m, m.replace(path, absolute_path))
    return readme
