# Keptn NeoLoad Service

This service is designed to use NeoLoad for executing various Load testing tasks. 

To trigger a NeoLoad test, the service has subscriptions to event channels. In more details, the current implementation of the service listens to CloudEvents from type:
* `sh.keptn.event.test.triggered`: When receiving this event, the service executes a test for a deployed application. This event would be replace by the start test event

## Secret for credentials
During the setup of NeoLaod, a secret is created that contains key-value pairs for the NeoLoad  URL, NeoLoad apiKey:
   * NL_WEB_HOST 
   * NL_API_HOST 
   * NL_UPLOAD_HOST
   * NL_API_TOKEN
   * NL_WEB_ZONEID 

## Install service

1. To install the service, you need to run :
 * installer/defineNeoLoadWebCredentials.sh to configure the required parameters :
    1. NL_WEB_HOST : host of the web ui of NeoLoad web
    1. NL_API_HOST : host of the api of NeoLoad web
    1. NL_UPLOAD_HOST : host of upload api of NeoLoad Web
    1. NL_API_TOKEN: api token of your NeoLoad account
    1. NL_WEB_ZONEID : NeoLoad Web Zone id that would be used by Keptn

you can also take advantage of the native dyntrace integration by running the dedicated installer.*

2. Run the installer script
 * there are 2 type of installation
   1. installing the neoload-service with dynatrace
   If the dynatrace-service has been previously installed then you can run:
`installer/deployNeoLoadWebWithDynatrace.sh <args>`    
    Once deployed the neoload-service will had the right project settings to run a test with the dynatrace integration.
    The Enduser will still need to configure the tags in each scenario.
    
    2. Installing the neoload-service
`installer/deployNeoLoadWeb.sh <Args>`    
    
    
  * Here are the following parameters for the deployment bash scripts :
   1.  -n : namespace name where Keptn is installed ( default value : keptn)
   2.  -c : custom NeoLoad Controller image name ( by default keptn will pick the latest version)
   3.  -l : custom NeoLoad LoadGenerator image name 
   4.  -u : git login user ( if the git repository require authentification with user/password)
   5.  -p : git password ( if the git repository require authentification with user/password)
    
## The NeoLoad Service requires to store the workload.yaml file in the ressources of keptn

1. Create your keptn.neoload.engine.yaml file describing the test and the infrastructure

```yaml
workloads:
- teststrategy: performance
  script:
    repository: https://github.com/yourREPO.git
    issecured: true
    project:
    - path: /test/cart_basic.yaml
    - path: /test/load_template/load_template.nlp
  description: CartLoad
  properties:
    scenario: CartLoad
    constant_variables:
    - name: server_host
      value: carts.sockshop-dev.svc
  infrastructure:
    managedbyKeptn: false
    numberOfMachine: 4
    zoneId : rest
    
 ```
   Here is a template of a [workload.yaml](/template/workload.yaml) file
   The ```repository``` needs to have the url of your source control repo containing your NeoLoad tests.
   The property ```project``` will have the list of the relative path of your neoload project files.
   A NeoLoad project can be combined of a NeoLoad gui project ( nlp) , yaml files, or both.
   
   ```constant_variables``` is the object allowing you to replace the value of constant variable defined in your project.
   
   ```infrastructure``` is the object describing the Load testing infrastructure required for this test.
  
2. Once your workload.yaml file created , you will need to store in keptn by sending the following command :

   ```keptn add-resource --project=your-project --service=my-service --stage=your stage --resource=workload.yaml```
   
    [here](https://keptn.sh/docs/0.6.0/installation/setup-keptn/) is the ling to keptn's documentation. 


###How to uninstall the NeoLoad-service

Run the following script
* if Neoload-service with dynatrace
`installer/uninstallNeoLoadServiceWithDynatrace.sh -n <name of you keptn namespace>`    

* if NeoLoad-service installed without dynatrace
`installer/uninstallNeoLoadService.sh -n <name of you keptn namespace>` 

### Deploy the service by using custom NeoLoad docker images
* if Neoload-service with dynatrace
`installer/uninstallNeoLoadServiceWithDynatrace.sh -n <name of you keptn namespace> -c <controller image> -l <lg image>`    

* if NeoLoad-service installed without dynatrace
`installer/uninstallNeoLoadService.sh -n <name of you keptn namespace> -c <controller image> -l <lg image>` 
   