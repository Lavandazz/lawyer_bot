from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salary_requests" DROP CONSTRAINT IF EXISTS "fk_salary_r_users_d2efc3ff";
        ALTER TABLE "salary_requests" RENAME COLUMN "user_id_id" TO "user_id";
        ALTER TABLE "salary_requests" ADD CONSTRAINT "fk_salary_r_users_199f6d0c" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "salary_requests" DROP CONSTRAINT IF EXISTS "fk_salary_r_users_199f6d0c";
        ALTER TABLE "salary_requests" RENAME COLUMN "user_id" TO "user_id_id";
        ALTER TABLE "salary_requests" ADD CONSTRAINT "fk_salary_r_users_d2efc3ff" FOREIGN KEY ("user_id_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""
