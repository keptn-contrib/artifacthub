# Asana Integration

> This integration is for Keptn v1. It is no longer supported.
>
> Users are advised to use Keptn instead: https://keptn.sh

[Asana](https://asana.com) is a project management and task tracking platform. This page describes how to integrate Keptn with Asana.

![tagged user](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/asana/1.0.0/assets/tagged-user.png)

## Overview
The [keptn webhook service](https://github.com/keptn/keptn/tree/master/webhook-service), which comes "out of the box" with Keptn, will be used to listen for Keptn events and trigger webhooks into Asana. In this way new Asana projects, tasks or anything else in Asana are created in response to a Keptn cloudevent.

Examples:
  - Create a new task every time a deployment occurs. Include the pass / fail status of the deployment
  - Create a new task every time a load test or evaluation is finished. Include the results and any output of the test / evaluation
  - Tag Asana users in tasks to notify them that action is required

## Step 1: Gather Asana Details

1. Log in to Asana.com and visit: `https://app.asana.com/api/1.0/users/me/workspaces` make a note of the `gid`. This is the unique Asana workspace ID
1. Go to the project and grab the project ID from the URL. In `https://app.asana.com/0/1213480328994600/list` the project ID is `1213480328994600`
1. In a browser, go to `https://app.asana.com/api/1.0/projects/ASANA-PROJECT-ID-HERE/sections?limit=50&opt_pretty=true` make a note of the `gid` for the section under which Keptn tasks should appear
1. Create an Asana PAT by following instructions [here](https://developers.asana.com/docs/authentication-quick-start#app-or-pat)

## Step 2: Keptn Webhook Setup
> This can be done programmatically or via the Keptn's bridge

1. Navigate to a keptn project and to go the integrations screen
1. Click the webhook-service and setup the task subscription
1. Set the method as `POST`
1. Set the URL as `https://app.asana.com/api/1.0/tasks`
1. Set the `Content-Type` header to `application/json`
1. Set the `Authorization` header to `Bearer ASANA-PAT-TOKEN-HERE` eg. `Bearer 1/1234567:1a2b3c4d`
1. Modify the payload below to your liking and use it as the `body` content

`name` is the title of the task. Use `html_notes` or `notes`. Asana doesn't support every HTML tag. See [here](https://developers.asana.com/docs/rich-text) for the supported tags.

```
{
  "data": {
    "name": "Keptn Evaluation: pass",
    "projects": "ASANA-PROJECT-gid-HERE",
    "html_notes": "<body><strong>Result: pass</strong>\nProject: project-1\nService: service-1\nStage: stage-1</body>",
    "memberships": [{
      "project": "ASANA-PROJECT-gid-HERE",
      "section": "ASANA-SECTION-gid-HERE"
    }]
  }
}
```

That's it! Execute the sequence and an Asana task will be automatically created.

## Bonus: Tagging Asana Users

It is possible to automatically tag Asana users when a task is created.

1. Ask the user to provide their `gid`. When logged in, ask them to go to `https://app.asana.com/api/1.0/users/me`
1. Modify the above webhook body to use `html_notes` and include a specially formatted hyperlink like: `<a data-asana-gid=\"THEIR-USER-gid-HERE\"/>`

For example:

```
{
    "data": {
        "name": "Keptn Evaluation: pass",
        "projects": "1234654328998765",
        "html_notes": "<body><strong>Result: pass</strong>\nProject: project-1\nService: service-1\nStage: stage-1\nResponsible:<a data-asana-gid=\"1234123423456789\"/></body>",
        "memberships": [{
            "project": "1234654328998765",
            "section": "9999280328991234"
        }]
    }
}
```

![tagged user](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/asana/1.0.0/assets/tagged-user.png)
