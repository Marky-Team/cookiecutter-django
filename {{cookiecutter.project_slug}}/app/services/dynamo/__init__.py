from enum import StrEnum

import boto3
from boto3.dynamodb.conditions import Key
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from factory import Dict


class DynamoTableNames(StrEnum):
    BUSINESSES = f"businesses-{settings.DYNAMO_DB_TABLE_POSTFIX}"
    USER_BUSINESS_ROLES = f"user-business-roles-{settings.DYNAMO_DB_TABLE_POSTFIX}"
    POSTS = f"posts-{settings.DYNAMO_DB_TABLE_POSTFIX}"


def is_user_a_part_of_business(user_id: str, business_id: str) -> bool:
    if settings.ALLOW_ALL_USERS_ON_ALL_BUSINESSES:
        return True

    if is_user_business_owner(user_id, business_id):
        return True
    if is_user_authorized_user_on_business(user_id, business_id):
        return True
    return False


def is_user_business_owner(user_id: str, business_id: str) -> bool:
    client = boto3.client("dynamodb")
    response = client.get_item(
        TableName=DynamoTableNames.BUSINESSES,
        Key={"id": {"S": business_id}},
    )

    if "Item" not in response:
        return False

    if str(response["Item"]["user_id"]["S"]) == str(user_id):
        return True
    return False


def is_user_authorized_user_on_business(user_id: str, business_id: str) -> bool:
    client = boto3.client("dynamodb")
    response = client.query(
        TableName=DynamoTableNames.USER_BUSINESS_ROLES,
        IndexName="user_id-business_id-index",
        Select="COUNT",
        ConsistentRead=False,
        KeyConditionExpression="user_id = :user_id AND business_id = :business_id",
        ExpressionAttributeValues={
            ":user_id": {"S": str(user_id)},
            ":business_id": {"S": str(business_id)},
        },
    )

    if response["Count"] > 0:
        return True
    return False


class PostNotFoundError(ObjectDoesNotExist):
    pass


def get_post(post_id: str):
    client = boto3.resource("dynamodb")
    table = client.Table(DynamoTableNames.POSTS)
    response = table.query(
        KeyConditionExpression=Key("id").eq(post_id),
        Select="ALL_ATTRIBUTES",
        ConsistentRead=True,
    )
    items = response.get("Items")
    if response["Count"] == 0:
        raise PostNotFoundError("Post not found")  # noqa: TRY003 EM101
    return items[0]


def put_post(item: Dict):
    client = boto3.resource("dynamodb")
    table = client.Table(DynamoTableNames.POSTS)
    table.put_item(TableName=DynamoTableNames.POSTS, Item=item)


def update_post_status_and_video_url(
    post_id: str,
    status: str,
    video_url: str | None = None,
):
    post = get_post(post_id)
    post["media_rendering_status"] = status
    if video_url:
        post["template"]["video_url"] = video_url
        post["template"]["media_urls"] = [video_url]
        post["media_urls"] = [video_url]
    put_post(post)
    return post

def update_post_template(
    post_id: str,
    template: dict
):
    post = get_post(post_id)
    post["template"] = template
    put_post(post)
