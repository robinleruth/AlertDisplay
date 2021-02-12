import asyncio
import queue

from app.domain.services.task_service import TaskService
from app.infrastructure.log import logger
from app.interface.gui.gui_launcher import GuiLauncher

sync_queue = queue.Queue()
out_sync_queue = queue.Queue()
async_queue = asyncio.Queue()
task_service = TaskService(sync_queue, async_queue)

GuiLauncher(sync_queue, out_sync_queue).start()


async def populate_queue():
    logger.info("populate_queue")
    while True:
        try:
            alert = out_sync_queue.get_nowait()
            await async_queue.put(alert)
        except queue.Empty:
            await asyncio.sleep(1)


async def process():
    while True:
        await task_service.wait()
        await task_service.process_messages()


loop = asyncio.get_event_loop()
loop.create_task(populate_queue())
loop.create_task(process())

loop.run_forever()
