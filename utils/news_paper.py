import logging
import requests
from settings.config import GOOGLE_NEWS

logger = logging.getLogger(__name__)


class News:
    """
    Get the information in IBGE API.
    """
    _url = f'{GOOGLE_NEWS["url"]}top-headlines?'\
        f'sources={",".join(GOOGLE_NEWS["sources"])}'\
        f'&apiKey={GOOGLE_NEWS["token"]}'

    def __init__(self, quantity: int=5) -> None:
        """
        Constructor.
        """
        self.quantity = int(quantity)

    def news(self) -> list:
        """
        Get the information based in self.quantity attribute.
        """
        _response = requests.get(url=self._url)
        content, status = _response.json(), _response.status_code

        if not status == 200:
            logger.error(content)
            raise Exception(content)

        return content['articles'][:self.quantity]

    def filter(self, phrase: str) -> list:
        """
        Filter content by keywords.
        """
        _url = f'{self._url}&q={phrase if phrase else ""}'
        _response = requests.get(url=_url)
        content, status = _response.json(), _response.status_code

        if not status == 200:
            logger.error(content)
            raise Exception(content)

        return content['articles'][:self.quantity]
