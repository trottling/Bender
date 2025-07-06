import httpx
from loguru import logger


def check_vulners_key_request(self):
    try:
        resp = httpx.post(url=f"https://vulners.com/api/v3/apiKey/valid/?keyID={self.ui.api_key.text().strip()}")
        if resp.status_code != 200:
            logger.debug(f"check_vulners_key_request: resp.status_code {resp.status_code}")
            return False
        if resp.json()['data']['valid']:
            logger.debug("check_vulners_key_request: key valid")
            return True
        else:
            logger.debug(f"check_vulners_key_request: key invalid: {resp.json()}")
            return False
    except Exception as e:
        logger.error(f"check_vulners_key_request: {e}")
        return False
