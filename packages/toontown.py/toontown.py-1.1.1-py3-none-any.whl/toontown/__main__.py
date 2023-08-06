import asyncio

import toontown
import toontown.models


async def main():
    async with toontown.AsyncToontownClient() as client:
        doodles = await client.doodles()

        for doodle in doodles:
            print(doodle.district, doodle.playground, doodle.dna, doodle.rendition, doodle.traits, doodle.cost)

        status = await client.status()
        print(status)


asyncio.run(main())
