import asyncio
from dataclasses import replace

import pytest
from neuro_admin_client import AdminClient
from neuro_config_client import ConfigClient
from neuro_config_client.models import StorageInstance

from neuro_maintenance_checker import (
    InMaintenanceError,
    MaintenanceChecker,
    UnknownClusterError,
)

from tests.conftest import MockConfigClient


@pytest.fixture
def checker(
    config_client: ConfigClient, admin_client: AdminClient
) -> MaintenanceChecker:
    return MaintenanceChecker(config_client=config_client, admin_client=admin_client)


async def test_unknown_cluster(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        with pytest.raises(UnknownClusterError):
            await checker.check_for_maintenance("not-exists", None)


async def test_unknown_org_cluster(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        with pytest.raises(UnknownClusterError):
            await checker.check_for_maintenance("test", "not-exists")


async def test_cluster_ok(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        await checker.check_for_maintenance("test", None)


async def test_cluster_ok_no_storage_info(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        await checker.check_for_maintenance("test-3", None)


async def test_org_cluster_ok(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        await checker.check_for_maintenance("test", "org1")


async def test_org_cluster_ok_cluster_not_ready(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        await checker.check_for_maintenance("test-2", "org1")


async def test_cluster_not_ready(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        with pytest.raises(InMaintenanceError):
            await checker.check_for_maintenance("test-2", None)


async def test_cluster_on_maintenance(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        with pytest.raises(InMaintenanceError):
            await checker.check_for_maintenance("test-4", None)


async def test_org_cluster_on_maintenance(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        with pytest.raises(InMaintenanceError):
            await checker.check_for_maintenance("test-5", "org1")


async def test_org_cluster_not_ready(checker: MaintenanceChecker) -> None:
    async with checker.run_poller():
        with pytest.raises(InMaintenanceError):
            await checker.check_for_maintenance("test", "org2")


async def test_refetch(
    checker: MaintenanceChecker, config_client: MockConfigClient
) -> None:
    async with checker.run_poller(interval_sec=1):
        with pytest.raises(InMaintenanceError):
            await checker.check_for_maintenance("test", "org2")
        cluster = config_client.mock_clusters[0]
        assert cluster.cloud_provider
        assert cluster.cloud_provider.storage
        config_client.mock_clusters[0] = replace(
            cluster,
            cloud_provider=replace(
                cluster.cloud_provider,
                storage=replace(
                    cluster.cloud_provider.storage,
                    instances=[
                        StorageInstance(
                            ready=True,
                            name=None,
                        ),
                        StorageInstance(
                            ready=True,
                            name="org1",
                        ),
                        StorageInstance(
                            ready=True,
                            name="org2",
                        ),
                    ],
                ),
            ),
        )
        await asyncio.sleep(1.5)
        await checker.check_for_maintenance("test", "org2")
