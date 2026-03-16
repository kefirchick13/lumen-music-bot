from utils import os, load_dotenv, dataclass, field, asyncio
from telethon import TelegramClient


@dataclass
class UserState:
    admin_message_to_send: str = None
    admin_broadcast: bool = False
    send_to_specified_flag: bool = False
    search_result: str = None


class BotState:
    # Список обязательных каналов теперь задаётся в config.env
    # через переменную REQUIRED_CHANNELS, например:
    # REQUIRED_CHANNELS=channel1,channel2
    channel_usernames = []
    user_states = {}
    lock = asyncio.Lock()

    load_dotenv('config.env')

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")

    _admin_ids_raw = os.getenv('ADMIN_USER_IDS')
    _required_channels_raw = os.getenv('REQUIRED_CHANNELS', '')

    if not all([BOT_TOKEN, API_ID, API_HASH, _admin_ids_raw]):
        raise ValueError("Required environment variables are missing.")

    ADMIN_USER_IDS = [int(id) for id in _admin_ids_raw.split(',')]

    # REQUIRED_CHANNELS может быть пустой строкой — тогда обязательных каналов нет
    if _required_channels_raw.strip():
        channel_usernames = [c.strip() for c in _required_channels_raw.split(',') if c.strip()]
    else:
        channel_usernames = []

    BOT_CLIENT = TelegramClient('bot', int(API_ID), API_HASH)

    # @staticmethod #[DEPRECATED]
    # def initialize_user_state(user_id):
    #     if user_id not in BotState.user_states:
    #         BotState.user_states[user_id] = {
    #             'admin_message_to_send': None,
    #             'admin_broadcast': False,
    #             'send_to_specified_flag': False,
    #             'messages': {},no
    #             'search_result': None,
    #             'tweet_screenshot': None,
    #             'youtube_search': None,
    #             'waiting_message': None
    #         }

    @staticmethod
    async def initialize_user_state(user_id):
        if user_id not in BotState.user_states:
            BotState.user_states[user_id] = UserState()

    @staticmethod
    async def get_user_state(user_id):
        async with BotState.lock:
            await BotState.initialize_user_state(user_id)
            return BotState.user_states[user_id]

    @staticmethod
    async def get_admin_message_to_send(user_id):
        user_state = await BotState.get_user_state(user_id)
        return user_state.admin_message_to_send

    @staticmethod
    async def get_admin_broadcast(user_id):
        user_state = await BotState.get_user_state(user_id)
        return user_state.admin_broadcast

    @staticmethod
    async def get_send_to_specified_flag(user_id):
        user_state = await BotState.get_user_state(user_id)
        return user_state.send_to_specified_flag

    @staticmethod
    async def set_admin_message_to_send(user_id, message):
        user_state = await BotState.get_user_state(user_id)
        user_state.admin_message_to_send = message

    @staticmethod
    async def set_admin_broadcast(user_id, value):
        user_state = await BotState.get_user_state(user_id)
        user_state.admin_broadcast = value

    @staticmethod
    async def set_send_to_specified_flag(user_id, value):
        user_state = await BotState.get_user_state(user_id)
        user_state.send_to_specified_flag = value
