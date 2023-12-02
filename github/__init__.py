import json
from logging import getLogger, Logger
from os import getenv as os_getenv
import azure.functions as func
from hemera.notifications import send_slack_message

LOGGER = getLogger(__name__)


def main(
    req: func.HttpRequest,
    logger: Logger = LOGGER,
) -> func.HttpResponse:
    logger.info("Python HTTP trigger function processed a request.")
    json_data = json.dumps(
        {
            "method": req.method,
            "url": req.url,
            "headers": dict(req.headers),
            "params": dict(req.params),
            "get_body": req.get_body().decode(),
        }
    )
    logger.info(json_data)

    send_slack_message(
        slack_api_token=os_getenv("SLACK_API_TOKEN"),
        channel="#hemera-test",
        message="Hello from Azure Functions!",
    )
    return func.HttpResponse(json_data)
