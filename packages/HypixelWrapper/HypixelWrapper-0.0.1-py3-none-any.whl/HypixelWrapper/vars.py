from errors import *
HYPIXELAPIURL = "https://api.hypixel.net/{}?key={}"
KEY = []

ERRORS = {
    403: APIKeyError("Invalid API key"),
    429: APIKeyError("Request limit reached"),
    400: HypixelAPIError("Missing field"),
    422: PlayerNotFoundError("Couldn't find player")
}