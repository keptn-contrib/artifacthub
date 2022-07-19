# Artifact Integration

This repository holds the metadata for Keptn integrations to be listed on the [ArtifactHub](https://artifacthub.io). Each Keptn integration listed needs to have an [`artifacthub-pkg.yml` file](https://github.com/artifacthub/hub/blob/master/docs/metadata/artifacthub-pkg.yml) and a `README.md` file.

## `artifacthub-pkg.yml` structure

For the integration to be displayed correctly, the `artifacthub-pkg.yml` file needs to meet the [syntax requirements described on the AH repository](https://github.com/artifacthub/hub/blob/master/docs/metadata/artifacthub-pkg.yml). The `version`, `name`, `displayName`, `createdAt`, and `description` attributes are required by AH. Additionally to the before-mentioned attributes, it's also recommended to add the `digest` as described in more detail in the ['Update existing version of a service' section](#update-existing-version-of-a-service).

## Adding images to the README or `artifacthub-pkg.yml` file

Images can be added to the README or `artifacthub-pkg.yml` file using [Markdown syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images). The link to the image needs to be absolute as Artifacthub doesn't currently support relative paths. The reason is that when processing packages AH currently only reads the metadata files (`README.md` and `artifacthub-pkg.yml`). They don't currently store or serve any other files. For more information, please refer to artifacthub/hub#629.

## Generate draft from a Github repository

To quickly generate a draft of the `README.md` and `artifacthub-pkg.yml` for a new service, use the [`generate_config.py` file](generate_config.py). 

```
usage: generate_config.py [-h] -r REPOSITORY [-v VERSION]

optional arguments:
  -h, --help            show this help message and exit
  -r REPOSITORY, --repository REPOSITORY
                        Name of Github repository
  -v VERSION, --version VERSION
                        Version (default=latest)
```

Before the script can be executed the first time, the required dependencies have to be installed via pip (should be executed from the root of the repository):

```bash
pip install -r requirements.txt 
```

Generate the config like this (should be executed from the root of the repository):
```bash
python3 generate_config.py -r keptn-sandbox/datadog-service -v 0.2.0
```

The script was tested with Python 3.8.10.


## Update existing version of a service

For updates of an existing version to take effect on Artifacthub, the `digest` parameter needs to be updated or added to the `artifacthub-pkg.yml` file of that version. A change of the digest parameter signals the Artifacthub backend to reprocess that version. To ensure the new `digest` value is unique, we use the current date of the change with the same format as the `createdAt` argument (RFC3339).