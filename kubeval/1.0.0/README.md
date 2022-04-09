# Kubeval Execution

Use kubeval to validate Kubernetes YAML files inside a Keptn sequence. More info on [kubeval.com](https://kubeval.com)

Whenever valid files are provided, the Keptn task passes:

![valid evaluation](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/kubeval/1.0.0/assets/valid.png)

Invalid YAML files cause the task to fail (as they should because kubeval is providing the error):

![invalid evaluation](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/kubeval/1.0.0/assets/invalid.png)



Inside the stage folder on the correct stage branch, create a subfolder called `files` and store all YAML files to be validated. Files are copied into `/keptn/` so these files will be available at `/keptn/files/*`

Below is the equivalent of:

```
docker run -it -v `pwd`/files:/files garethr/kubeval -d /files -o json
```

Validate all YAML files inside `files` directory:
```
apiVersion: v2
actions:
  - name: "Run kubeval to validate files"
    events:
      - name: "sh.keptn.event.validate.triggered"
    tasks:
      - name: "Run Kubeval"
        files:
          - '/files'
        image: "garethr/kubeval:0.15.0"
        args:
          - '-d'
          - '/keptn/files'
          - '-o'
          - 'json'
```