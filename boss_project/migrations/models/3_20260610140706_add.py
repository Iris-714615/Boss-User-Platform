from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `message_category` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL DEFAULT '新对话',
    `create_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_message__user_53f2800e` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `message` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `content` LONGTEXT NOT NULL,
    `role` VARCHAR(100) NOT NULL,
    `create_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `message_category_id` INT NOT NULL,
    CONSTRAINT `fk_message_message__a202078b` FOREIGN KEY (`message_category_id`) REFERENCES `message_category` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `message_category`;
        DROP TABLE IF EXISTS `message`;"""


MODELS_STATE = (
    "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"
)
