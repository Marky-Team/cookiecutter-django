from uuid import UUID
from uuid import uuid4

import boto3
from common_template.test_helper_utils import TestSentinels
from common_template.test_helper_utils import inject_test_counter
from services.dynamo import DynamoTableNames
from users.tests.db_helpers import create_test_user


def _create_dynamo_table_if_not_exists(
    dynamodb: boto3.client,
    table_name: str,
    primary_key: str,
    read_capacity: int,
    write_capacity: int,
    gsi: dict[str, list[dict[str, str]]] | None = None,
) -> None:
    try:
        dynamodb.describe_table(TableName=table_name)
    except Exception:  # noqa: BLE001, S110
        pass  # Table doesn't exist, expected
    else:
        return  # Table already exists (probably)

    table_definition = {
        "TableName": table_name,
        "KeySchema": [{"AttributeName": primary_key, "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": primary_key, "AttributeType": "S"}],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": read_capacity,
            "WriteCapacityUnits": write_capacity,
        },
    }

    if gsi:
        table_definition["GlobalSecondaryIndexes"] = []
        table_definition["AttributeDefinitions"].extend(gsi["attributes"])
        for index in gsi["indices"]:
            key_schema = [{"AttributeName": index["key"], "KeyType": "HASH"}]
            if "sort_key" in index:
                key_schema.append(
                    {"AttributeName": index["sort_key"], "KeyType": "RANGE"},
                )
            table_definition["GlobalSecondaryIndexes"].append(
                {
                    "IndexName": index["name"],
                    "KeySchema": key_schema,
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": read_capacity,
                        "WriteCapacityUnits": write_capacity,
                    },
                },
            )

    dynamodb.create_table(**table_definition)


def _create_businesses_dynamo_db_table_if_not_exists():
    client = boto3.client("dynamodb")

    _create_dynamo_table_if_not_exists(
        dynamodb=client,
        table_name=DynamoTableNames.BUSINESSES,
        primary_key="id",
        read_capacity=5,
        write_capacity=5,
        gsi={
            "attributes": [{"AttributeName": "user_id", "AttributeType": "S"}],
            "indices": [
                {"name": "user_id-index", "key": "user_id"},
            ],
        },
    )


def _create_user_business_roles_dynamo_db_table_if_not_exists():
    client = boto3.client("dynamodb")

    _create_dynamo_table_if_not_exists(
        dynamodb=client,
        table_name=DynamoTableNames.USER_BUSINESS_ROLES,
        primary_key="id",
        read_capacity=5,
        write_capacity=5,
        gsi={
            "attributes": [
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "business_id", "AttributeType": "S"},
            ],
            "indices": [
                {"name": "user_id-index", "key": "user_id"},
                {"name": "business_id-index", "key": "business_id"},
                {
                    "name": "user_id-business_id-index",
                    "key": "user_id",
                    "sort_key": "business_id",
                },
            ],
        },
    )


def _create_post_dynamo_db_table_if_not_exists():
    client = boto3.client("dynamodb")

    _create_dynamo_table_if_not_exists(
        dynamodb=client,
        table_name=DynamoTableNames.POSTS,
        primary_key="id",
        read_capacity=5,
        write_capacity=5,
        gsi={
            "attributes": [{"AttributeName": "business_id", "AttributeType": "S"}],
            "indices": [{"name": "business_id-index", "key": "business_id"}],
        },
    )


@inject_test_counter
def create_test_business_id(
    counter,
    owning_user_id: str = TestSentinels.NOT_SET,
) -> UUID:
    if owning_user_id is TestSentinels.NOT_SET:
        owning_user_id = str(create_test_user().id)

    business_id = uuid4()

    client = boto3.client("dynamodb")
    _create_businesses_dynamo_db_table_if_not_exists()
    client.put_item(
        TableName=DynamoTableNames.BUSINESSES,
        Item={"id": {"S": str(business_id)}, "user_id": {"S": str(owning_user_id)}},
    )

    return business_id


def add_user_to_business(
    user_id: str,
    business_id: str,
) -> None:
    _create_user_business_roles_dynamo_db_table_if_not_exists()
    client = boto3.client("dynamodb")
    client.put_item(
        TableName=DynamoTableNames.USER_BUSINESS_ROLES,
        Item={
            "id": {"S": str(uuid4())},
            "user_id": {"S": str(user_id)},
            "business_id": {"S": str(business_id)},
        },
    )


def create_test_post(
    business_id: str | None = None,
    media_rendering_status: str | None = "FAILED",
    video_url: str | None = None,
    template: dict | None = None,
) -> dict:
    client = boto3.resource("dynamodb")
    table = client.Table(DynamoTableNames.POSTS)
    if business_id is None:
        business_id = str(create_test_business_id())

    post_id = str(uuid4())

    item = {
        "id": post_id,
        "business_id": business_id,
        "media_rendering_status": media_rendering_status,
    }
    if template is None:
        template = {
            "id": "not_an_id",
            "pages": [
                {
                    "id": "not_an_id",
                    "custom": {"image_url": "not_an_image.png"},
                },
            ],
        }

    item["template"] = template

    if video_url is not None:
        item["template"]["video_url"] = video_url

    table.put_item(
        TableName=DynamoTableNames.POSTS,
        Item=item,
    )

    return item
