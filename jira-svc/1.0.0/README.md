# Jira Integration

[Jira Software](https://www.atlassian.com/software/jira) is a project management and task tracking platform. This page describes how to integrate Keptn with Jira.

## Overview
The [keptn webhook service](https://github.com/keptn/keptn/tree/master/webhook-service), which comes "out of the box" with Keptn, will be used to listen for Keptn events and trigger webhooks into Jira. In this way new Jira projects, tasks or anything else in Jira are created in response to a Keptn cloudevent.

Examples:
  - Create a new task every time a deployment occurs. Include the pass / fail status of the deployment
  - Create a new task every time a load test or evaluation is finished. Include the results and any output of the test / evaluation
  - Assign Jira users in tasks to notify them that action is required

## Step 1: Gather Jira Details

1. Log in to `https://www.atlassian.com/software/jira` and visit: `https://your-site.atlassian.net/jira/projects?selectedProjectType=software` create a Project choosing any template of your choice and give a `project name`. e.g. `KEP6`. Then, create a [Backlog](https://confluence.atlassian.com/jirasoftwareserver/creating-your-backlog-938845071.html) depending upon your project board and make a note of the `project key name`. e.g. `KEP6-1`.
1. Go to the project setting and grab the project ID from the URL. In `https://your-site.atlassian.net/secure/project/EditProject!default.jspa?pid=10004` the project ID is `10004`
1. Now, in order to get an issue type, go to `https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-types/#api-rest-api-3-issuetype-project-get-example` get an issue type for your project using `curl` API request and make a note of the `id` for the section under which Jira tasks should appear e.g for Bug type the response will contain `"id":"10010","description":"Bugs track problems or errors."`
1. Ask the user to provide their `accountId`. When logged in, ask them to go to `Profile` of an account and grab the `id` from the `URL`. e.g. `https://keptn-sp.atlassian.net/jira/people/635dh86823h289373` where `accountId`: `635dh86823h289373`
1. Create an Jira API token by following instructions [here](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/) and create a PAT using `echo 'email@example.com:<api_token>' | base64`

![Backlog](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/jira/0.9.1/assets/j1.png)

## Step 2: Keptn Webhook Setup
> This can be done programmatically or via the Keptn's bridge

1. Navigate to a keptn project and to go the integrations screen
1. Click the webhook-service and setup the task subscription
1. Set the method as `POST`
1. Set the URL as `https://your-site.atlassian.net/rest/api/3/issue`
1. Set the `Accept` header to `application/json`
1. Set the `Content-Type` header to `application/json`
1. Set the `Authorization` header to `Basic Jira-PAT-TOKEN-HERE` eg. `Basic eGFyb3I3OTU1M0Bsb2RvcmVzLmNvbT`
1. Modify the payload below to your liking and use it as the `body` content

With Jira API support platform, you can now make an API request using webhook service. For more details about API, you can see [here](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post).

```
{
  "fields": {
    "summary": "Keptn Evaluation: myapp project in qa stage pass",
    "parent": {
      "key": "<project key name>"
    },
    "issuetype": {
      "id": "<issue id>"
    },
    "project": {
      "id": "<project ID>"
    },
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "text": "Testing delivery pipeline quality gate pass when passing through.",
              "type": "text"
            }
          ]
        }
      ]
    },
    "reporter": {
      "id": "<accountId>"
    },
    "labels": [
      "bugfix",
      "blitz_test"
    ]
  }
}
```

![Jira Tickets](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/jira/0.9.1/assets/j2.png)

## Step 3: See Ticket Output

That's it! Execute the sequence and an Jira ticket will be automatically created.

![Jira Ticket](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/jira/0.9.1/assets/j3.png)