  # Keptn Trello Integration

  ## Step 1: Gather Trello Information

  1. Go to `https://trello.com/app-key` and make a note of your api-key
  2. Click on the `Token` link and follow the wizard. Then make a note of your `api-token`
  3. Make a note of the `board id` from the URL
  4. Make a note of the (case sensitive) list name on your board. (eg. `To Do`)
  5. Execute a curl request to get the IDs for the lists. This is the list under which you want the cards to be created
  ```
  curl -X GET https://api.trello.com/1/boards/<BOARD_ID>/lists?key=<TRELLO_API_KEY>&token=<TRELLO_API_TOKEN>
  ```
  The output should look like this. Make a note of the `id` field (eg. `12342044e670786dbbd21234`)
  ```
  [{
    "id": "12342044e670786dbbd21234",
    "name": "To Do",
    "closed": false,
    "idBoard": "12342044e670786dbbd21234",
    "pos": 16384,
    "subscribed": false,
    "softLimit": null
  }]
  ```

  ## Step 2: Save as Keptn Secret
  Save the above details as a Keptn secret with the scope set to `keptn-webhook-service`

  ![keptn secret](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/trello/1.0.0/assets/1.png)

  ## Step 3: Create Webhook
  This is the raw curl request you will recreate in the Keptn webhook.

  Note: Be sure to properly URL encode your fields (eg. name and desc). Usually this is easy: just replace each space character with `%20`
  ```
  curl -X POST 'https://api.trello.com/1/cards?key=<API_KEY>&token=<API_TOKEN>&idList=<LIST_ID>&name=Keptn%20List%20Item&desc=description%20here...'
  ```

  ![keptn webhook](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/trello/1.0.0/assets/2.png)

  ## Step 4: Run a Sequence and Get a Card

  ![trello card](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/trello/1.0.0/assets/3.png)
