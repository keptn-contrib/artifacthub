# Listing Your Integration

## Step 1: Tracking Progress / Contributing and Requesting Assistance

This file describe how to list your tool integration on the [Keptn Integrations page](https://keptn.sh/docs/integrations/).

If you have not done so already, [Create an issue](https://github.com/keptn/integrations/issues/new?assignees=&labels=integrations&template=integration_template.yaml&title=%5Bintegration%5D+) to track the development of this integration. This is also the place to look for integration requests raised by others. If you want to contribute to Keptn, this is a great place to start.

## Step 2: Integration is Ready

> Please sign all commits (eg. `git commit -sm "commit message"`)

When your integration is ready and tested:

1. Fork this repository
2. Create a new branch on your fork
3. Copy the `aws_lambda` folder to use as a template
4. Rename the `aws_lambda` folder to match your integration name (eg. `myToolX`)
5. The `1.0.0` subfolder is used to version the artifact when it's a "full" Keptn service. In most cases, contributors will be leveraging the job-executor-service or the webhook service. In which case, this can be left as `1.0.0` to denote that your integration is not versioned.
6. Modify the `artifacthub-pkg.yml` file with your details.
7. Modify the `README.md` file with your instructions.
8. If you have no screenshots, you can delete the `assets` folder.
9. Create a PR back on the parent repo and someone will review.

## `artifacthub-pkg.yml` structure

For the integration to be displayed correctly, the `artifacthub-pkg.yml` file needs to meet the [syntax requirements](https://github.com/artifacthub/hub/blob/master/docs/metadata/artifacthub-pkg.yml) described on the AH repository. The `version`, `name`, `displayName`, `createdAt`, and `description` attributes are required by AH. In addition, authors are also recommended to add the `digest` as described in more detail in the ['Update existing version of a service' section](#update-existing-version-of-a-service).

## Keptn Annotations

There are two Keptn specific annotations you must add to the `artifacthub-pkg.yml`: `keptn/kind` and `keptn/version`. Both properties and accepted values are documented [here](https://artifacthub.io/docs/topics/annotations/keptn).

## Update existing version of a service

For updates of an existing version to take effect on Artifacthub, the `digest` parameter needs to be updated or added to the `artifacthub-pkg.yml` file of that version. A change of the digest parameter signals the Artifacthub backend to reprocess that version. To ensure the new `digest` value is unique, use the current date of the change with the same format as the `createdAt` argument (RFC3339).

## A note on screenshots

Screenshots should be saved into the `assets` folder.

ArtifactHub cannot resolve relative paths so you must specify the "real path" the image will have after the PR is merged.

The path takes the form `https://github.com/keptn-contrib/artifacthub/{your-service-folder-name}/{version-subfolder}/assets/{image name}`. For example:

```
https://github.com/keptn-contrib/artifacthub/aws_lambda/1.0.0/assets/image.jpg
```

## Stuck? Need Help?

Join us on the `#help-integrations` channel on [Keptn Slack](https://slack.keptn.sh) and the Keptn community will help out.