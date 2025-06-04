import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class ScheduledTask:
    def __init__(self, func, interval_minutes):
        """
        Инициализация ScheduledTask.

        :param func: Асинхронная функция для выполнения.
        :param interval_minutes: Интервал в минутах между запусками функции.
        """
        self.func = func
        self.interval_minutes = interval_minutes
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """
        Запуск планировщика задач.
        """
        self.scheduler.add_job(self._run_task, 'interval', minutes=self.interval_minutes,
                               next_run_time=datetime.now())
        self.scheduler.start()

        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

    async def _run_task(self):
        """
        Запуск асинхронной функции.
        """
        await self.func()