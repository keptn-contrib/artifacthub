# Run k6 with Keptn

  [k6](https://k6.io) is an open source load generation tool. Keptn can be used to trigger k6 by using the [Job Executor Service](https://github.com/keptn-contrib/job-executor-service).

  1. At the root of your stage branch, create two folders. `files` and `job`
  1. Inside the `files` folder, create a folder to hold your k6 files called `k6`
  1. Inside `files/k6` drop your k6 load test `.js` file (eg. `test.js`)
  1. Inside the `job` folder, create a file called `config.yaml`

  ```
  apiVersion: v2
  actions:
    - name: "Run k6"
      events:
        - name: "sh.keptn.event.test.triggered"
      tasks:
        - name: "Run k6 with Keptn"
          files:
            - /k6
          image: "loadimpact/k6"
          cmd: ["k6"]
          args: ["run", "--duration", "30s", "--vus", "60", "/keptn/k6/test.js"]
  ```