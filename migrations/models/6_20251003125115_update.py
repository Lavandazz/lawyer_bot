from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salary_requests" ADD "user_folder" VARCHAR(300);
        ALTER TABLE "salary_requests" ADD "date_to_delete" DATE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salary_requests" DROP COLUMN "user_folder";
        ALTER TABLE "salary_requests" DROP COLUMN "date_to_delete";"""
