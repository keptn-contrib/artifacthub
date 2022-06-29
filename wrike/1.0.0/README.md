# Wrike.com Integration

[Wrike](https://wrike.com) is a described as a "work management platform". Create Wrike tasks on certain keptn events (eg. `deployment.finished`).

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/wrike/1.0.0/assets/wrike1.png)


## Retrieve Required Details from Wrike

Create a Wrike app to retrieve an API token. Go to `https://www.wrike.com/frontend/apps/index.html` and create an app.

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/wrike/1.0.0/assets/assets/wrike_create_app.png)

Click `configure`, scroll down to `Permanent Access Token` and click `Create token`. Make a note of the generated token.

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/wrike/1.0.0/assets/assets/wrike_create_token.png)
![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/wrike/1.0.0/assets/assets/wrike_pat.png)

A folder ID will be needed which tells Wrike under which folder to create tasks. Perform a `GET` request to `http://www.rike.com/api/v4/folders` with an `Authorization` header set to `Bearer {WRIKE-API-TOKEN}`

```
curl -X GET 'https://www.wrike.com/api/v4/folders' ^
-H 'Authorization: Bearer ey******.*******'
```

Returns JSON like this where `IEAABCDEF123HRA4` is the ID required for tasks to appear under `Product Launch`.

```
{
    "kind": "folderTree",
    "data": [{
            "id": "IEAABCDEF123HRA4",
            "title": "Product Launch"
            ...
        }, ...]
}
```

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/wrike/1.0.0/assets/wrike_folders_get.png)

## Configure Keptn Webhook Service

In the Keptn's bridge, create a secret to store the Wrike API token.

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/wrike/1.0.0/assets/keptn_secret.png)

In the bridge, navigate to `Settings > Uniform > Integrations` and add a subscription for the webhook service.

- Request Method: `POST`
- Request URL: `https://www.wrike.com/api/v4/folders/{WRIKE-FOLDER-NAME-HERE}/tasks`

```
https://www.wrike.com/api/v4/folders//{WRIKE-FOLDER-NAME-HERE}/tasks?title=Deployment ({{.data.project}} / {{.data.service}} / {{.data.stage}}) ({{.data.result}})&description=<h2>Result: {{.data.result}}</h2>Project: <strong>{{.data.project}}</strong><br />Service: <strong>{{.data.service}}</strong><br />Stage: <strong>{{.data.stage}}</strong>
```

In a more readable form, this is the URL:

```
https://www.wrike.com/api/v4/folders/{WRIKE-FOLDER-ID}/tasks
```
With the following URL parameters:

```
"title": "Your Title Here..."
"description": "Task description here (supports HTML)..."
```

Full documentation for allowed fields is found on the [Wrike Developer Portal](https://developers.wrike.com/api/v4/tasks/#create-task).