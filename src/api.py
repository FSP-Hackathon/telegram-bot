import json
import requests
import os
import logging
import asyncio

from flask import Flask, request, jsonify

from bot import Alert, Bot
from monitoring_bot import MonitoringBot

app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)


ACCESS_SERVICE_BASE_URL_KEY = 'ACCESS_SERVICE_BASE_URL'


async def __notifyUsers(users: list, message: str):
    await Bot.notifyUsers(users=users, message=message)


def __getUsersToNotify(token: str) -> list:
    logger.debug(f'__getUsersToNotify(token = {token})')

    baseUrl = os.getenv(ACCESS_SERVICE_BASE_URL_KEY)
    response = requests.get(
        f'{baseUrl}/api/database/users',
        params={'name': token}
    )
    body = response.json()

    logger.debug(f'__getUsersToNotify(body = {body})')
    return body['users']


def __parseRequest(request) -> (str, str):
    logger.debug(f'__parseRequest(request = {request})')

    error_message = request.json.get('msg')
    token = request.headers.get('Authorization')

    logger.debug(f'__parseRequest(error_message = {error_message})')
    logger.debug(f'__parseRequest(token = {token})')

    return error_message, token


@app.route('/alert', methods=['POST'])
def alert():
    error_message, token = __parseRequest(request)
    users = __getUsersToNotify(token)
    MonitoringBot.sendMessageToUsers(msg=error_message, users=users)
    return ('', 200)


def runApi():
    app.run(host='0.0.0.0', port=1082, debug=True, use_reloader=False)


if __name__ == '__main__':
    runApi()