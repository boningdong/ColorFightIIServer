import aiohttp
from aiohttp import web
import asyncio
import aiohttp_jinja2
from colorfight import Colorfight
import time

def clean_gameroom(request):
    delete_rooms = []
    for name, gameroom in request.app['game'].items():
        # clear the rooms that's inactivate for more than 10 minutes
        if name != 'public' and time.time() - gameroom.last_update > 10 * 60:
            delete_rooms.append(name)
    for name in delete_rooms:
        if name in request.app['game']:
            request.app['game'].pop(name)


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}

@aiohttp_jinja2.template('gameroom.html')
async def game_room(request):
    return {}

@aiohttp_jinja2.template('gameroom_list.html')
async def gameroom_list(request):
    clean_gameroom(request)
    headers = ['Name', 'Players', 'Turns']
    gamerooms = []
    for name, game in request.app['game'].items():
        gameroom = {}
        gameroom['Name'] = '<a href="/gameroom/{0}">{0}</a>'.format(name)
        gameroom['Players'] = len(game.users)
        gameroom['Turns'] = '{} / {}'.format(game.turn, game.max_turn)
        gamerooms.append(gameroom)
    return {'gamerooms': gamerooms, 'headers': headers}

@aiohttp_jinja2.template('get_started.html')
async def get_started(request):
    return {}

@aiohttp_jinja2.template('game_rules.html')
async def game_rules(request):
    return {}

@aiohttp_jinja2.template('api.html')
async def api_documentation(request):
    return {}

@aiohttp_jinja2.template('contact.html')
async def contact(request):
    return {}

async def game_channel(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    curr_turn = 0 
    gameroom_id = request.match_info['gameroom_id']

    if gameroom_id in request.app['game']:
        game = request.app['game'][gameroom_id]

        try:
            while True:
                game.update()
                if curr_turn != game.turn:
                    curr_turn = game.turn
                    await ws.send_json(game.get_game_info())
                await asyncio.sleep(0.1)
        finally:
            pass
    return ws

async def action_channel(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    uid = None

    gameroom_id = request.match_info['gameroom_id']

    if gameroom_id in request.app['game']:
        game = request.app['game'][gameroom_id]

        try:
            request.app['game_sockets'].append(ws)
            while True:
                msg = await ws.receive()
                if msg.type == aiohttp.WSMsgType.text:
                    result = game.parse_action(uid, msg.data)
                    uid = result.get('uid', uid)
                    await ws.send_json(result)
                else:
                    break
        finally:
            pass
    return ws

async def restart(request):
    data = await request.json()
    result, err_msg = request.app['game'].config(data)
    if result:
        request.app['game'].restart()
        return web.json_response({"success": True})
    else:
        return web.json_response({"success": False, "err_msg": err_msg})

async def create_gameroom(request):
    data = await request.json()
    try:
        gameroom_id = data['gameroom_id']
        if gameroom_id in request.app['game']:
            return web.json_response({"success": False, "err_msg": "Same id exists"})
        request.app['game'][gameroom_id] = Colorfight()
    except Exception as e:
        return web.json_response({"success": False, "err_msg": str(e)})

    return web.json_response({"success": True})
