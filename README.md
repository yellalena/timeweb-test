# Timeweb test assignment

A web application to parse and download a website data. 

## Preparing for run

create a 'secrets' directory in project root and put there contents of 'secrets.zip' file you've received from developer (me)

## Running

To run the service, you should have docker-compose installed on your machine. Enter in terminal:
```
docker-compose up
```

After all parts are up and listening, the app is ready to accept requests.

## API usage examples

#### POST to create a task
* the 'url' is a link to a site you want to be parsed. 
* returns task's id

```shell
http POST http://127.0.0.1:8000/parse url="http://biba.com/"

{
    "id": "80495a8d-d85c-4853-b4bc-01a64ccfc78d"
}
```

#### GET to retrieve the result (a link to an archive containing parsed data) and/or task status
* use id from POST request response
* returns a link to download the archive if task is complete
* returns only task status if task is still being processed or something went wrong
```shell
http GET http://127.0.0.1:8000/result/80495a8d-d85c-4853-b4bc-01a64ccfc78d

{"result":
{
    "url_to_download":"http://biba.com"
}
}
```