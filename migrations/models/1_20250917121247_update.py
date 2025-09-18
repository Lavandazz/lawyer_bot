from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "phone" TYPE BIGINT USING "phone"::BIGINT;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_users_phone_f72cc5" ON "users" ("phone");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_users_phone_f72cc5";
        ALTER TABLE "users" ALTER COLUMN "phone" TYPE INT USING "phone"::INT;"""
