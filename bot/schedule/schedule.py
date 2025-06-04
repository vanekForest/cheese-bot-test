import asyncio
from datetime import datetime
from typing import Callable, Awaitable, List, Tuple

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class ScheduledTask:
    def __init__(self, tasks: List[Tuple[Callable[[], Awaitable[None]], int]]) -> None:
        """
        Инициализация ScheduledTask.

        :param tasks: Список кортежей (асинхронная_функция, интервал_в_минутах)
        """
        self.tasks = tasks
        self.scheduler = AsyncIOScheduler()

    async def start(self) -> None:
        """
        Запуск всех задач из списка.
        """
        for func, interval in self.tasks:
            self.scheduler.add_job(
                self._wrap_task(func),
                'interval',
                minutes=interval,
                next_run_time=datetime.now(),
            )

        self.scheduler.start()

        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

    def _wrap_task(
        self, func: Callable[[], Awaitable[None]]
    ) -> Callable[[], Awaitable[None]]:
        """
        Оборачивает асинхронную функцию в job.

        :param func: Асинхронная функция.
        :return: Обёрнутая асинхронная функция.
        """

        async def wrapper() -> None:
            await func()

        return wrapper
