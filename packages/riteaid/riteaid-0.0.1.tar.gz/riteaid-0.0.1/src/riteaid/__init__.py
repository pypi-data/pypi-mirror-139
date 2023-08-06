"""Main API for Rite Aid."""
import aiohttp
import json
import asyncio

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
        form = aiohttp.FormData()
        data = {
            "refillPrescriptions": json.dumps(prescription_nums),
            "location": store_id,
            "pickUpDate": date,
            "pickUpTime": time,
            "phoneNumber": phone
        }
        for key, value in data.items():
            form.add_field(key, value)
        async with aiohttp.ClientSession() as session:
            async with session.post(REFILL_RX_URL, data=form) as resp:
                return await resp.json()