# Hemera

Hemera is a Python library for handling HTTP requests in a serverless environment.
It was designed to send a notification to a Slack channel when a new GitHub Pull Request is created and make my lights blink by sending a request to my Home Assistant instance.

## Using the Docker Image

The Docker image for Hemera is available on GitHub packages You can pull and run the image with the following commands:

```bash
docker pull ghcr.io/rterluun/hemera:latest
docker run -p 80:80 ghcr.io/rterluun/hemera:latest
```

## Configuration Environment Variables

The following environment variables are required to run Hemera:
| Environment Variable     | Description                                                                                           |
|--------------------------|-------------------------------------------------------------------------------------------------------|
| `SLACK_API_TOKEN`        | The Slack API token to use for sending messages to Slack. [More info](https://api.slack.com/tutorials/tracks/getting-a-token) |
| `SLACK_CHANNEL`          | The Slack channel to send messages to.                                                                |
| `HOMEAUTOMATION_WEBHOOK` | The webhook URL to use for sending requests to Home Assistant. [More info](https://www.home-assistant.io/docs/automation/trigger/#webhook-trigger) |
| `ALLOWED_USERNAME`       | The username of the GitHub user that is allowed to trigger the action.                               |

## Running Hemera

Hemera can be run using the following command:

```bash
docker run -p 80:80 \
-e SLACK_API_TOKEN=... \
-e SLACK_CHANNEL=... \
-e HOMEAUTOMATION_WEBHOOK=... \
-e ALLOWED_USERNAME=... \
ghcr.io/rterluun/hemera:latest
```

## Configuring GitHub webhooks for Pull Requests

To configure GitHub webhooks for Pull Requests, go to the settings of your repository and click on "Webhooks". Click on "Add webhook" and enter the following information:

| Parameter    | Value                  |
|--------------|------------------------|
| Payload URL  | `http://<your-ip>/api/github` |
| Content type | `application/json`    |
| Events       | `Pull requests`        |
