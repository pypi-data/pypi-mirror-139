from __future__ import annotations

import asyncio
import json
import logging
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass
from typing import AsyncIterator

import aiohttp.web
from neuro_admin_client import AdminClient
from neuro_config_client import ConfigClient

logger = logging.getLogger(__name__)


class UnknownClusterError(aiohttp.web.HTTPServiceUnavailable):
    def __init__(self, cluster_name: str, org_name: str | None = None) -> None:
        if org_name is None:
            error_payload = {"error": f"Cluster '{cluster_name}' is not found."}
        else:
            error_payload = {
                "error": f"OrgCluster '{cluster_name}/{org_name}' is not found."
            }
        data = json.dumps(error_payload)
        super().__init__(text=data, content_type="application/json")


class InMaintenanceError(aiohttp.web.HTTPServiceUnavailable):
    def __init__(self, cluster_name: str, org_name: str | None = None) -> None:
        if org_name is None:
            error_payload = {
                "error": f"Cluster '{cluster_name}' is under maintenance, please wait."
            }
        else:
            error_payload = {
                "error": f"OrgCluster '{cluster_name}/{org_name}' is under maintenance, please wait."
            }
        data = json.dumps(error_payload)
        super().__init__(text=data, content_type="application/json")


@dataclass
class ClusterState:
    on_maintenance: bool
    storage_ready: bool


class MaintenanceChecker:
    _clusters: dict[str | tuple[str, str], ClusterState]

    def __init__(
        self,
        admin_client: AdminClient,
        config_client: ConfigClient,
    ) -> None:
        self._admin_client = admin_client
        self._config_client = config_client
        self._fetched_once = asyncio.Event()

    async def _do_reload(self) -> None:
        new_clusters: dict[str | tuple[str, str], ClusterState] = {}
        for admin_cluster in await self._admin_client.list_clusters():
            config_cluster = await self._config_client.get_cluster(admin_cluster.name)

            def _get_storage_ready(org_name: str | None) -> bool:
                if (
                    config_cluster.cloud_provider is None
                    or config_cluster.cloud_provider.storage is None
                ):
                    return True
                for instance in config_cluster.cloud_provider.storage.instances:
                    if instance.name == org_name:
                        return instance.ready
                return False

            new_clusters[admin_cluster.name] = ClusterState(
                on_maintenance=admin_cluster.maintenance,
                storage_ready=_get_storage_ready(None),
            )
            for org_cluster in await self._admin_client.list_org_clusters(
                admin_cluster.name
            ):
                new_clusters[
                    (org_cluster.cluster_name, org_cluster.org_name)
                ] = ClusterState(
                    on_maintenance=org_cluster.maintenance,
                    storage_ready=_get_storage_ready(org_cluster.org_name),
                )
        self._clusters = new_clusters
        self._fetched_once.set()

    async def _poller_task(self, interval_sec: int) -> None:
        while True:
            try:
                await self._do_reload()
            except Exception:
                logger.exception("Failed to update maintenance state, ignoring...")
            await asyncio.sleep(interval_sec)

    @asynccontextmanager
    async def run_poller(self, interval_sec: int = 60) -> AsyncIterator[None]:
        task = asyncio.create_task(self._poller_task(interval_sec))
        try:
            yield
        finally:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

    def _check_for_maintenance(
        self,
        key: str | tuple[str, str],
        *,
        check_storage: bool = True,
    ) -> None:
        cluster_state = self._clusters.get(key)
        args = key if isinstance(key, tuple) else (key,)
        if cluster_state is None:
            raise UnknownClusterError(*args)
        if cluster_state.on_maintenance or (
            check_storage and not cluster_state.storage_ready
        ):
            raise InMaintenanceError(*args)

    async def check_for_maintenance(
        self,
        cluster_name: str,
        org_name: str | None,
        *,
        check_storage: bool = True,
    ) -> None:
        await self._fetched_once.wait()
        self._check_for_maintenance(
            cluster_name, check_storage=check_storage if org_name is None else False
        )
        if org_name:
            self._check_for_maintenance(
                (cluster_name, org_name), check_storage=check_storage
            )
