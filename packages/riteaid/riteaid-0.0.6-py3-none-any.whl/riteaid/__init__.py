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
            quote(date),
            quote(time).replace("%20", "+"),
            quote(phone),
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(REFILL_RX_URL, data=form, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
                "Content-Type": "pplication/x-www-form-urlencoded; charset=UTF-8",
                "Referer": "https://www.riteaid.com/pharmacy/services/prescription-refills/online-prescription-refills"
            }) as resp:
                return await resp.json()