import pytest
from neuro_admin_client import (
    AdminClient,
    Balance,
    Cluster as AdminCluster,
    OrgCluster,
    Quota,
)
from neuro_config_client import Cluster as ConfigCluster, ConfigClient
from neuro_config_client.models import (
    AWSCloudProvider,
    AWSCredentials,
    AWSStorage,
    EFSPerformanceMode,
    EFSThroughputMode,
    StorageInstance,
)


class MockAdminClient(AdminClient):
    mock_clusters: list[AdminCluster]
    mock_org_clusters: dict[str, list[OrgCluster]]

    def __new__(
        cls,
    ) -> "MockAdminClient":
        return object.__new__(cls)  # type: ignore

    def __init__(self) -> None:
        pass

    async def list_clusters(self) -> list[AdminCluster]:
        return self.mock_clusters

    async def list_org_clusters(self, cluster_name: str) -> list[OrgCluster]:
        return self.mock_org_clusters[cluster_name]


class MockConfigClient(ConfigClient):
    mock_clusters: list[ConfigCluster]

    def __init__(self) -> None:
        pass

    async def get_cluster(self, name: str) -> ConfigCluster:
        for cluster in self.mock_clusters:
            if cluster.name == name:
                return cluster
        raise AssertionError("cluster not found")


@pytest.fixture
def admin_client() -> MockAdminClient:
    res = MockAdminClient()
    res.mock_clusters = [
        AdminCluster("test", default_credits=None, default_quota=Quota()),
        AdminCluster("test-2", default_credits=None, default_quota=Quota()),
        AdminCluster("test-3", default_credits=None, default_quota=Quota()),
        AdminCluster(
            "test-4", default_credits=None, default_quota=Quota(), maintenance=True
        ),
        AdminCluster("test-5", default_credits=None, default_quota=Quota()),
    ]
    res.mock_org_clusters = {
        "test": [
            OrgCluster("org1", "test", balance=Balance(), quota=Quota()),
            OrgCluster("org2", "test", balance=Balance(), quota=Quota()),
        ],
        "test-2": [
            OrgCluster("org1", "test-2", balance=Balance(), quota=Quota()),
        ],
        "test-3": [],
        "test-4": [],
        "test-5": [
            OrgCluster(
                "org1", "test-5", balance=Balance(), quota=Quota(), maintenance=True
            ),
        ],
    }
    return res


@pytest.fixture
def config_client() -> MockConfigClient:
    res = MockConfigClient()
    res.mock_clusters = [
        ConfigCluster(
            name="test",
            cloud_provider=AWSCloudProvider(
                credentials=AWSCredentials(
                    access_key_id="any",
                    secret_access_key="any",
                ),
                node_pools=[],
                region="us-east-1",
                zones=[],
                storage=AWSStorage(
                    id="id",
                    description="info",
                    performance_mode=EFSPerformanceMode.GENERAL_PURPOSE,
                    throughput_mode=EFSThroughputMode.BURSTING,
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
                            ready=False,
                            name="org2",
                        ),
                    ],
                ),
            ),
        ),
        ConfigCluster(
            name="test-2",
            cloud_provider=AWSCloudProvider(
                credentials=AWSCredentials(
                    access_key_id="any",
                    secret_access_key="any",
                ),
                node_pools=[],
                region="us-east-1",
                zones=[],
                storage=AWSStorage(
                    id="id",
                    description="info",
                    performance_mode=EFSPerformanceMode.GENERAL_PURPOSE,
                    throughput_mode=EFSThroughputMode.BURSTING,
                    instances=[
                        StorageInstance(
                            ready=False,
                            name=None,
                        ),
                        StorageInstance(
                            ready=True,
                            name="org1",
                        ),
                    ],
                ),
            ),
        ),
        ConfigCluster(
            name="test-3",
            cloud_provider=AWSCloudProvider(
                credentials=AWSCredentials(
                    access_key_id="any",
                    secret_access_key="any",
                ),
                node_pools=[],
                region="us-east-1",
                zones=[],
                storage=None,
            ),
        ),
        ConfigCluster(
            name="test-4",
            cloud_provider=AWSCloudProvider(
                credentials=AWSCredentials(
                    access_key_id="any",
                    secret_access_key="any",
                ),
                node_pools=[],
                region="us-east-1",
                zones=[],
                storage=None,
            ),
        ),
        ConfigCluster(
            name="test-5",
            cloud_provider=AWSCloudProvider(
                credentials=AWSCredentials(
                    access_key_id="any",
                    secret_access_key="any",
                ),
                node_pools=[],
                region="us-east-1",
                zones=[],
                storage=None,
            ),
        ),
    ]
    return res
