"""
We are using Google Cloud Build to automatically
trigger a build and deploy the application on merge to master

However, unlike other cloud service providers,
we cannot set the environment variables through the Console for the App Engine.

Since the not all environment variables are not pushed to the source control, we cannot set it
Hence we are using Google Datastore to store relevant environment variables and other keys

Credits @Martin Omander
https://stackoverflow.com/questions/22669528/securely-storing-environment-variables-in-gae-with-app-yaml/35261091#35261091

"""

import os
from google.cloud import ndb

class env_variables(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.StringProperty()

    @staticmethod
    def get(key):
        key_value_pair = env_variables.query(env_variables.name == key).get()
        if not key_value_pair:
            raise Exception(f'Environment Variable for {key} has not been set')
        return key_value_pair.value


def get_env_variable(key):
    if os.environ.get('FLASK_ENV') == 'production':
        client = ndb.Client()
        with client.context():
            return env_variables.get(key)
    else:
        # If in development environment, get user specified environment variables
        return os.environ.get(key)

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'D:\\analytics-credentials.json'
    os.environ['FLASK_ENV'] = 'production'

    print(get_env_variable('ACCESS_TOKEN'))
