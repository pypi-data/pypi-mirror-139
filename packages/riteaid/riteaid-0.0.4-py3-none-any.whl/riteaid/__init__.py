"""Main API for Rite Aid."""
import aiohttp
import json
from urllib.parse import quote

from .const import GET_STORES_URL, REFILL_RX_URL
from .exceptions import RiteAidError

class RiteAidAPI:
    """Object for making requests to Rite Aid."""
    def __init__(self):
        pass

    @staticmethod
    async def get_stores(zip):
        """Get stores near a zip code."""
        async with aiohttp.ClientSession() as session:
            async with session.get(GET_STORES_URL.format(zip=zip)) as resp:
                if resp.status != 200:
                    raise RiteAidError("Error getting stores.")
                return await resp.json()

    @staticmethod
    async def refill_rx(prescription_nums, store_id, date, time, phone):
        """Refill a prescription."""
        # Using application/x-www-form-urlencoded
        form = "refillPrescriptions={}&location={}&pickUpDate={}&pickUpTime={}&phone={}".format(
            quote(json.dumps(prescription_nums)).replace("%20", ""),
            quote(str(store_id)),
            quote(date).replace("-", "%\2F"),
            quote(time).replace("%20", "+"),
            quote(phone),
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(REFILL_RX_URL, data=form) as resp:
                return await resp.json()