from utils import Shazam, os, asyncio


class ShazamHelper:

    @classmethod
    def initialize(cls):
        cls.Shazam = Shazam()

        cls.voice_repository_dir = "repository/Voices"
        if not os.path.isdir(cls.voice_repository_dir):
            os.makedirs(cls.voice_repository_dir, exist_ok=True)

    @staticmethod
    async def recognize(file):
        """
        Распознавание трека по файлу с таймаутом.
        Если Shazam зависает или отвечает слишком долго, возвращаем пустую строку,
        чтобы бот не "висел" бесконечно.
        """

        async def _do_recognize():
            try:
                return await ShazamHelper.Shazam.recognize(file)
            except Exception:
                return await ShazamHelper.Shazam.recognize_song(file)

        try:
            # таймаут 20 секунд на работу Shazam
            out = await asyncio.wait_for(_do_recognize(), timeout=20)
        except asyncio.TimeoutError:
            print("Shazam recognize timeout for file:", file)
            return ""
        except Exception as e:
            print("Shazam recognize error:", e)
            return ""

        # Логируем статус и message ответа Shazam (если есть)
        try:
            status = out.get('status')
            message = out.get('message') or out.get('status', {}).get('msg')
            print("Shazam raw status:", status)
            print("Shazam message:", message)
        except Exception:
            print("Shazam response (raw):", out)

        return ShazamHelper.extract_song_details(out)

    # Function to extract the Spotify link
    @staticmethod
    def extract_spotify_link(data):
        for provider in data['track']['hub']['providers']:
            if provider['type'] == 'SPOTIFY':
                for action in provider['actions']:
                    if action['type'] == 'uri':
                        return action['uri']
        return None

    @staticmethod
    def extract_song_details(data):

        try:
            music_name = data['track']['title']
            artists_name = data['track']['subtitle']
        except:
            return ""

        song_details = {
            'music_name': music_name,
            'artists_name': artists_name
        }
        song_details_string = ", ".join(f"{value}" for value in song_details.values())
        return song_details_string
