This repository contains the Machine Learning model that is used by [TipTracker](https://github.com/JIA-0302/TipTracker) for Analytics feature.

# Release Notes
>  ## v1.0.1 (03/12/2021)
>   - A script was added to generate datasets.
>   - Performance metrics for various Machine Learning algorithms has been compiled for comparisions.
>  - The Machine Learning algorithm was developed to make predictions for a given dataset.
>
>  ## v1.0.2 (04/02/2021)
>  - A Flask Application was created to access the Machine Learning algorithm to make predictions.
>  - MongoDB has been integrated to load the dataset for user.
>  - Rest API has been developed to allow requesting shift predictions for a given user.
>  - Access token has been added on the API routes to prevent unauthorized access of the resources.
> 
> ## v.1.0.3 (04/23/2021)
>   - CI/CD for the application has been configured to automatically deploy new changes on the source code.
> ### Bug Fixes
>   - Validations have been added to the dataset before making predictions.
>   - API routes return meaningful error messages.



# Install Guide

## Pre-prequisites
The following tools, software, and technologies are needed to run the application:

1. <b> Python </b>

    For the project, we are using Python 3.8+.
    To check if you already have Python installed, run the following command:
    ```
    $ python --version
    ```
    If successful, it will display the currently installed Python version (eg: `Python 3.8.1`).

    If you need to install Python, visit [here](https://www.python.org/downloads/).

2. <b>MongoDB</b>

   We are using `MongoDB` to store data for our Machine Learning model.
   
   If you do not have a MongoDB database, MongoDB provides free cloud database service [here](https://www.mongodb.com/cloud/atlas/signup).

<br />

## Download Instructions

The source code can be downloaded any one of the steps:

1. Cloning the repository

    To clone the repository using HTTPS, run the following command from the desired directory:
    ```
    $ git clone https://github.com/JIA-0302/Analytics.git
    ```
    This will download all the source code from the repository.
    

2. Download the ZIP file from [here](https://github.com/JIA-0302/Analytics/archive/refs/heads/master.zip)

<br />


## Installing dependent libraries


1. Setup virtual environment

    Run the following commands if the virtual environment has not been setup:
    ```    
    $ pip install virtualenv
    $ virtualenv venv
    ```

    This will create a virtual environment directory `venv`.

    To activate the virtual environment, run the following command:
    ```    
    . venv/Scripts/activate
    ```

    This allows us manage and resolve dependenices easily

2. Install dependencies:

    To install all the required dependencies, run the following command:
    ```
    pip install -r requirements.txt
    ```

<br />

## Build instructions

1. Setup environment variables

    - Create a new file `.env` in the root directory
    - Copy all the contents of `.env.example` into `.env`
    - Replace all the required fields (`xxxxxxx`) specific to your configurations.
    ```
    # Database Configurations
    MONGODB_URL=xxxxxxxxxx
    DATABASE_NAME=test
    DATASET_COLLECTION_NAME=future_trends

    # Token to be able to access protected routes
    ACCESS_TOKEN=xxxxxxxx

    # Parameters for Tip Prediction
    SHIFT_INTERVAL_MINUTES=30
    SHIFT_START_TIME = 10
    SHIFT_END_TIME = 23
    ```

    You can use any value for access token. However, make sure any other application making an request to this service uses the same access token.


## Installation

No addition steps are required for installation.

## Run Instructions

Simply run the following command to start the server:
```
python index.py
```

The terminal will return the URL on where the application is running. By default, it runs on `http://127.0.0.1:5000/`.

If other applications need to use this service, use the provided URL.
    
## Troubleshooting

1. `ModuleNotFoundError: No module named '...'`

    This is usually because the script could not find the dependent libraries.

    Make sure the [virtual environment](#installing-dependent-libraries) is running first.

    If the problem still persists, re-install all the dependencies:
    ```
    pip install -r requirements.txt
    ```

2. `socket.error: [Errno 98] Address already in use`

     By default, Flask application starts on port number 5000. Since only one process can run on a port number, we cannot run this new processing to this occupies port. To fix this issue there are two approaches:
      - Kill other process running on port number 5000
        - For Windows, view instructions [here](https://stackoverflow.com/questions/39632667/how-do-i-kill-the-process-currently-using-a-port-on-localhost-in-windows).
        - For Mac and Linux, view instructions [here](https://stackoverflow.com/questions/3855127/find-and-kill-process-locking-port-3000-on-mac)

      - Run the application on a different port

        To run application in a different unoccupied port, run the following command:
        ```
        $ flask run -h localhost -p <PORT_NUMBER>
        ```
        Note, the application will now be available on the specified port number.

# Developers Guide

Please see the [installation guide](#install-guide) to setup the project.

## Utils
### Generating Test Dataset
Use `test-data-gen.py` script to generate test dataset in `csv` format.

It accepts command line arguments to generate data as needed:
```
usage: test-data-gen.py [-h] [-s START_DATE] [-e END_DATE] [-f FILE_NAME]

Generate test dataset for a user

optional arguments:
  -h, --help            show this help message and exit
  -s START_DATE, --start-date START_DATE
                        First shift date in the dataset. Default: 1/1/2020
  -e END_DATE, --end-date END_DATE
                        Last shift date in the dataset. Default: 3/16/2021
  -f FILE_NAME, --file-name FILE_NAME
                        Name of the file to save the dataset. Default: shift_data.csv
```

An example usage would be:

`python test-data-gen.py -s 1/1/2021 -e 3/1/2021 -f test_dataset.csv`


### Playground
We need to continuously improve our ML model using different features, aggregating different data, different algorithms, and so much more.

We are using Google Colab as a playground. Use TipTracker account to access it [here](https://colab.research.google.com/drive/1yPToDJgMi_kc8ZymerYhxs888vZwFWlk).




## API Usage
These API endpoints are protected and only authorized apps are allowed access based on the token issued.

Access token must be added using Bearer authentication.
```
$ curl https://service-url/api/...
    -H "Authorization: Bearer ${access_token}" 
    -H "Accept: application/json"
```

The following API endpoints are available:

## `/predict_tips`

#### **POST** `/predict_tips`

This endpoint is used to predict tips for the user for the given days.
The body parameters to request the data are following:

| Parameter | Description | Required |
|-----------|-------------|----------|
| user_id | `id` assigned to the user for whom we need to predict tips | Yes |
| dates | List of dates for which we need to predict tips. Each date should be formatted as `yyyy-MM-dd`. | Yes |

Example Request Body:

```
{
    "user_id": 18,
    "dates": ["2021-02-20", "2021-02-21", "2021-02-22", "2021-02-23"]
}
```

If the request is successful, it returns the predicted values in a dictionary in following scheme:
```
{
    // Each day represents the date passed in the request
    day: [
        // For a given day, different intervals that are specified by start and end time are given with predicted tip values
        {
            cash_tips,
            credit_card_tips,
            end_time,
            start_time
        },
        ...
    ],
    ...
}

```
If for a given day, the value is set to `null`, it means there isn't sufficient data to make predictions for that day.

Example Response:

```
{
    "result": {
        "2021-02-20": [
            {
                "cash_tips": 10.9,
                "credit_card_tips": 17.16,
                "end_time": "2021-04-01 10:30:00",
                "start_time": "2021-04-01 10:00:00"
            },
            {
                "cash_tips": 10.87,
                "credit_card_tips": 17.29,
                "end_time": "2021-04-01 11:00:00",
                "start_time": "2021-04-01 10:30:00"
            },
            {
                "cash_tips": 11.23,
                "credit_card_tips": 20.53,
                "end_time": "2021-04-01 11:30:00",
                "start_time": "2021-04-01 11:00:00"
            },
            ...
        ],
        "2021-02-21": [
            {
                "cash_tips": 15.35,
                "credit_card_tips": 14.4,
                ...
            },
            ...
        ],
        "2021-02-22": null,
        ...
}
```

If there are any errors, the response will contain a description about the error. An example error response is:
```
{
    "error": "We do not have sufficient data to make accurate predictions. Please continue entering shift data."
}
```
