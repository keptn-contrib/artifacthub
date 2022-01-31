# Artifact Integration

This repository holds the metadata for Keptn integrations to be listed on the [ArtifactHub](https://artifacthub.io). Each Keptn integration that's listed needs to have a [`artifacthub-pkg.yml` file](https://github.com/artifacthub/hub/blob/master/docs/metadata/artifacthub-pkg.yml) and a `README.md` file.

## Generate draft from repository

To quickly generate a draft of the `README.md` and `artifacthub-pkg.yml` for a new service use the [`generate_config.py` file](generate_config.py).

```
usage: generate_config.py [-h] -r REPOSITORY [-v VERSION]

optional arguments:
  -h, --help            show this help message and exit
  -r REPOSITORY, --repository REPOSITORY
                        Name of Github repository
  -v VERSION, --version VERSION
                        Version (default=latest)
```

## Update existing version of a service

In order for updates of an existing version to take effect on Artifacthub the `digest` parameter needs to be updated or added to the `artifacthub-pkg.yml` file of that version. A change of the digest parameter signals the Artifacthub backend to reprocess that version. To make sure the new `digest` value is unqiue we use the current date of the change with the same format as the `createdAt` argument (RFC3339).