import pickle
import pickletools
import zlib
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import psutil
from anyio import open_file
from loguru import logger
from nonebot.utils import run_sync
from pydantic import parse_obj_as

from ..exceptions import AccountAlreadyExists
from ..plugin_config import AccountConfig
from ..plugin_config import config as plugin_config
from .download import ACCOUNTS_DATA_PATH, BINARY_DIR, BINARY_PATH
from .models import ProcessAccountsStore
from .process import GoCQProcess

ACCOUNTS_SAVE_PATH = BINARY_DIR / "accounts.pkl"


class ProcessesManager:
    _processes: Dict[int, GoCQProcess] = {}

    @staticmethod
    @lru_cache
    def is_predefined(uin: int) -> Optional[AccountConfig]:
        account = next(
            (account for account in plugin_config.ACCOUNTS if account.uin == uin), None
        )
        return account

    get = _processes.get

    @classmethod
    def add(cls, process: GoCQProcess, uin: Optional[int] = None):
        uin = uin or process.account.uin
        if uin in cls._processes:
            raise AccountAlreadyExists
        cls._processes[uin] = process

    @classmethod
    def create(cls, account: AccountConfig):
        return GoCQProcess(account, **plugin_config.PROCESS_KWARGS)

    @classmethod
    async def remove(cls, uin: int):
        process = cls._processes.pop(uin)
        process.logs.listeners.clear()
        await process.stop()
        return

    @classmethod
    def all(cls) -> List[GoCQProcess]:
        return [*cls._processes.copy().values()]

    @classmethod
    async def save(cls, save_path: Path = ACCOUNTS_SAVE_PATH) -> int:
        store = ProcessAccountsStore(
            accounts=[process.account.source for process in cls.all()]
        )
        dumped = pickle.dumps(store)
        dumped = pickletools.optimize(dumped)
        compressed = zlib.compress(dumped, level=zlib.Z_BEST_COMPRESSION)
        async with await open_file(save_path, "wb") as f:
            size = await f.write(compressed)
        return size

    @classmethod
    def load_config(cls, *, ignore_loaded: bool = False) -> List[GoCQProcess]:
        return [
            GoCQProcess(account, **plugin_config.PROCESS_KWARGS)
            for account in plugin_config.ACCOUNTS
            if not ignore_loaded or account.uin not in cls._processes
        ]

    @classmethod
    async def load_saved(
        cls,
        save_path: Path = ACCOUNTS_SAVE_PATH,
        ignore_loaded: bool = False,
    ) -> List[GoCQProcess]:
        try:
            async with await open_file(save_path, "rb") as f:
                compressed = await f.read()
            decompressed = zlib.decompress(compressed)
            store = parse_obj_as(ProcessAccountsStore, pickle.loads(decompressed))
        except Exception as e:
            raise RuntimeError(
                f"Failed to load saved accounts from {save_path!r}"
            ) from e
        return [
            GoCQProcess(account, **plugin_config.PROCESS_KWARGS)
            for account in store.accounts
            if (
                not cls.is_predefined(account.uin)
                or not ignore_loaded
                or account.uin not in cls._processes
            )
        ]


@run_sync
def kill_duplicated_processes():
    killed: List[int] = []
    for process in psutil.process_iter():
        try:
            with process.oneshot():
                pid = process.pid
                cwd = process.cwd()
                exe = process.exe()
        except psutil.Error:
            continue

        if (
            Path(exe).is_file()
            and BINARY_PATH.samefile(exe)
            and ACCOUNTS_DATA_PATH in Path(cwd).parents
        ):
            process.terminate()
            killed.append(pid)
            logger.warning(f"Duplicate running process {pid=} detected, killed.")

    return killed
