# Superpaws

Flask app serving webhook for a Slack application that provides pictures of animals from APIs and Google Photos albums.

Provides Python example for
* Google Photos API
* Slack app webhook integration.


## Setup

Uses a google cloud project with photos api enabled, a slack app enabled in a workspace, and a host for the flask application (Heroku, etc.)

* Set up Slack app following this [tutorial](https://renzo.lucioni.xyz/serverless-slash-commands-with-python/)
    * Token and team_id are stored in `config.yaml`
    * Webhook endpoint is `http://yourhost/superpaws`. App is deployable to Heroku in the current configuration
* Follow instructions in `google_auth.py` to authenticate Google Photos album access and add any album ids to `config.yaml`

## Usage
Set up as a slash command in Slack, takes args mapped to 
* API endpoints that return an image url (api map in app)
* Google Photo album ids (config file)