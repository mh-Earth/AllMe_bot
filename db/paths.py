from typing import Final
from configurations.settings import DB_PATH
TRACKINSTA = {
    'ADD':f'{DB_PATH}/trackinstas',
    'PUT':f'{DB_PATH}/trackinstas/:id',
    'DELETE':f'{DB_PATH}/trackinstas/:id',
    'GET':""
}