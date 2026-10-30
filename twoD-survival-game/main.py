# NOTE:
# Keep this import for pygbag build.
# In some environments, the build did not work when pygame was not imported in main.py.
import pygame
import asyncio

from game.package.core.engine import Engine


async def main():
    e = Engine()
    await e.start()
     
if __name__ == "__main__":
    asyncio.run(main())