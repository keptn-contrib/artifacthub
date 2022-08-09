# Listing Your Integration

## Step 1: Tracking Progress / Contributing and Requesting Assistance

This file describe how to list your tool integration on the [Keptn Integrations page](https://keptn.sh/docs/integrations/).

If you have not done so already, [Create an issue](https://github.com/keptn/integrations/issues/new?assignees=&labels=integrations&template=integration_template.yaml&title=%5Bintegration%5D+) to track the development of this integration. This is also the place to look for integration requests raised by others. If you want to contribute to Keptn, this is a great place to start.

## Step 2: Integration is Ready

When your integration is ready and tested:

1. Fork this repository
2. Create a new branch on your fork
3. Copy the `aws_lambda` folder to use as a template
4. Rename the `aws_lambda` folder to match your integration name (eg. `myToolX`)
5. The 1.0.0 subfolder is used to version the artifact when it's a "full" keptn service. In most cases, contributors will be leveraging the job-executor-service or the webhook service to usually this can be left as 1.0.0 to denote that your integration is not versioned.
6. Modify the `artifacthub-pkg.yml` file with your details
7. Modify the `README.md` file with your instructions
8. If you have no screenshots, you can delete the assets folder
9. Create a PR back on the parent repo and someone will review

## A note on screenshots

If you include screenshots (by convention, saved into the `assets` folder), it would be natural to include them like this:

```
![an image](assets/image.jpg)
```

However, ArtifactHub cannot resolve relative paths so you **must** "figure out" the "real path" after the PR is merged which takes the form `https://github.com/keptn-contrib/artifacthub/{your-service-folder-name}/{version-subfolder}/assets/{image name}`. For example:

```
![alt text](https://github.com/keptn-contrib/artifacthub/myToolX/1.0.0/assets/image.jpg
```

## Stuck? Need Help?

Join us on the `#help-integrations` channel on [Keptn Slack](https://slack.keptn.sh) and we will help out.