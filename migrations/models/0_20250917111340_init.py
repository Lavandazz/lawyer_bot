from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "statistics" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "day" DATE NOT NULL UNIQUE,
    "new_user" INT NOT NULL DEFAULT 0,
    "event" INT NOT NULL DEFAULT 0
);
COMMENT ON TABLE "statistics" IS 'Класс хранит статистику по новым пользователям, а так же по количеству использований бота.';
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100),
    "first_name" VARCHAR(100),
    "second_name" VARCHAR(100),
    "phone" INT NOT NULL,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "role" VARCHAR(20) NOT NULL DEFAULT 'user',
    "registration_date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_activity" TIMESTAMPTZ,
    "status" VARCHAR(20) NOT NULL DEFAULT 'active'
);
COMMENT ON TABLE "users" IS 'Модель для сохранения пользователей.';
CREATE TABLE IF NOT EXISTS "admin_posts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "photo_file_id" VARCHAR(255),
    "text" TEXT NOT NULL,
    "date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" INT NOT NULL DEFAULT 0,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "admin_posts" IS 'Модель бд для отображения постов админа';
CREATE TABLE IF NOT EXISTS "salary_requests" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "contract" VARCHAR(255),
    "account_screenshot" VARCHAR(255),
    "a_pass" VARCHAR(255),
    "ndfl_reference" VARCHAR(255),
    "extract" VARCHAR(255),
    "employment_record" VARCHAR(255),
    "comment" TEXT,
    "approved" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "salary_requests" IS 'Модель для загрузки данных по вопросам отпускных.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
