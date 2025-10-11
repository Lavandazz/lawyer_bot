from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salary_requests" RENAME COLUMN "approved" TO "deleted";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salary_requests" RENAME COLUMN "deleted" TO "approved";"""
