"""Azure Cosmos DB ``RegistryStore`` (NoSQL API, async SDK).

Design notes (per the repo's Cosmos DB guidance):
* One container per resource kind keeps items small and queries targeted.
* Partition key ``/partition_key`` is set to the publisher id — high cardinality
  and aligned with the most common query ("my org's resources").
* Auth prefers ``DefaultAzureCredential`` (managed identity in Azure) so no keys
  are stored; a key is only used if ``COSMOS_KEY`` is explicitly provided.
* A single ``CosmosClient`` is reused for the process lifetime.
"""

from __future__ import annotations

from azure.cosmos.aio import CosmosClient, DatabaseProxy
from azure.cosmos import PartitionKey, exceptions
from azure.identity.aio import DefaultAzureCredential

from ..config import Settings
from ..models import Agent, MCPServer, ResourceKind, Skill, Visibility
from .base import StoredResource

_CONTAINERS: dict[ResourceKind, str] = {
    ResourceKind.agent: "agents",
    ResourceKind.mcp_server: "mcpservers",
    ResourceKind.skill: "skills",
}

_MODELS = {
    ResourceKind.agent: Agent,
    ResourceKind.mcp_server: MCPServer,
    ResourceKind.skill: Skill,
}


class CosmosStore:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._credential: DefaultAzureCredential | None = None
        if settings.cosmos_key:
            self._client = CosmosClient(settings.cosmos_endpoint, settings.cosmos_key)
        else:
            self._credential = DefaultAzureCredential()
            self._client = CosmosClient(
                settings.cosmos_endpoint, credential=self._credential
            )
        self._db: DatabaseProxy | None = None

    async def init(self) -> None:
        self._db = await self._client.create_database_if_not_exists(
            self._settings.cosmos_database
        )
        for name in _CONTAINERS.values():
            await self._db.create_container_if_not_exists(
                id=name,
                partition_key=PartitionKey(path="/partition_key"),
            )

    async def close(self) -> None:
        await self._client.close()
        if self._credential is not None:
            await self._credential.close()

    def _container(self, kind: ResourceKind):
        assert self._db is not None, "init() not called"
        return self._db.get_container_client(_CONTAINERS[kind])

    @staticmethod
    def _to_item(resource: StoredResource) -> dict:
        # mode="json" makes HttpUrl/datetime/enum JSON-serializable.
        return resource.model_dump(mode="json")

    @staticmethod
    def _from_item(kind: ResourceKind, item: dict) -> StoredResource:
        return _MODELS[kind].model_validate(item)

    async def create(self, resource: StoredResource) -> StoredResource:
        await self._container(resource.kind).create_item(self._to_item(resource))
        return resource

    async def get(
        self, kind: ResourceKind, resource_id: str
    ) -> StoredResource | None:
        # We don't know the partition key from the id alone, so do a point query.
        query = "SELECT * FROM c WHERE c.id = @id"
        params = [{"name": "@id", "value": resource_id}]
        async for item in self._container(kind).query_items(
            query=query, parameters=params
        ):
            return self._from_item(kind, item)
        return None

    async def replace(self, resource: StoredResource) -> StoredResource:
        await self._container(resource.kind).upsert_item(self._to_item(resource))
        return resource

    async def delete(self, kind: ResourceKind, resource_id: str) -> bool:
        existing = await self.get(kind, resource_id)
        if existing is None:
            return False
        try:
            await self._container(kind).delete_item(
                item=resource_id, partition_key=existing.partition_key
            )
            return True
        except exceptions.CosmosResourceNotFoundError:
            return False

    async def list(
        self,
        kind: ResourceKind,
        *,
        query: str | None = None,
        tags: list[str] | None = None,
        publisher_id: str | None = None,
        visible_to_org: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> tuple[list[StoredResource], int]:
        clauses: list[str] = []
        params: list[dict] = []

        if publisher_id:
            clauses.append("c.partition_key = @pub")
            params.append({"name": "@pub", "value": publisher_id})

        if visible_to_org is not None:
            clauses.append("(c.visibility = @pub_vis OR c.partition_key = @org)")
            params.append({"name": "@pub_vis", "value": Visibility.public.value})
            params.append({"name": "@org", "value": visible_to_org})

        if query:
            clauses.append(
                "(CONTAINS(LOWER(c.name), @q) OR CONTAINS(LOWER(c.summary), @q) "
                "OR CONTAINS(LOWER(c.description), @q))"
            )
            params.append({"name": "@q", "value": query.lower()})

        if tags:
            for i, tag in enumerate(tags):
                clauses.append(f"ARRAY_CONTAINS(c.tags, @tag{i})")
                params.append({"name": f"@tag{i}", "value": tag})

        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        container = self._container(kind)

        # Total count for paging.
        total = 0
        async for row in container.query_items(
            query=f"SELECT VALUE COUNT(1) FROM c{where}", parameters=params
        ):
            total = row

        sql = (
            f"SELECT * FROM c{where} ORDER BY c.updated_at DESC "
            f"OFFSET {int(offset)} LIMIT {int(limit)}"
        )
        items = [
            self._from_item(kind, item)
            async for item in container.query_items(query=sql, parameters=params)
        ]
        return items, total
