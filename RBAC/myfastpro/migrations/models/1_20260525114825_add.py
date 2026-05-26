from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `resource` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL,
    `path` VARCHAR(20),
    `pid_id` INT,
    CONSTRAINT `fk_resource_resource_7943f904` FOREIGN KEY (`pid_id`) REFERENCES `resource` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `role` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL,
    `mobile` VARCHAR(11) NOT NULL,
    `password` VARCHAR(20) NOT NULL,
    `role_id` INT NOT NULL COMMENT '所属角色',
    CONSTRAINT `fk_user_role_68c1d370` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE `role_resource` (
    `resource_id` INT NOT NULL REFERENCES `resource` (`id`) ON DELETE CASCADE,
    `role_id` INT NOT NULL REFERENCES `role` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `user`;
        DROP TABLE IF EXISTS `role_resource`;
        DROP TABLE IF EXISTS `role`;
        DROP TABLE IF EXISTS `resource`;"""


MODELS_STATE = (
    "eJztmFFv2jAQx79KladNYhNk0HZ7o2zVuq6tRNtpUltFJjEhIrFT21mLKr77bCfGIQlZAn"
    "QKFS+0nM/J3Y+7/C9+MQLsQJ9+HEKKI2JD48vBi4FAIP7JrbUODBCGekUYGBj50pmkvUaU"
    "EWAzbh8Dn0JuciC1iRcyDyNuRZHvCyO2uaOHXG2KkPcYQYthF7IJJHzh7oGbPeTAZ0jV13"
    "BqjT3oO0vheo64t7RbbBZK2xlip9JR3G1k2diPAqSdwxmbYLTw9hATVhciSACD4vKMRCJ8"
    "EV2SqcoojlS7xCGm9jhwDCKfpdKtyMDGSPDj0VCZoCvu8sHsdI+6x58Ou8fcRUaysBzN4/"
    "R07vFGSeDyxpjLdcBA7CExam7yb47cYAJIMTrln4HHQ87CU6jK6CmDxqdLZkv8AvBs+RC5"
    "bCKgtUtg/eoPB9/7w3dm+73IBfMijqv7Mlkx5ZLgqfmFgF+4Bj/lvxa/pLbeEj7PsWq1rt"
    "7w7/ZtBsEtNLB46o2nhf0bFtE7xQR6LjqHMwnxjAcEkF3UtwVP+cYRnKsaUFYdBQFPCy1I"
    "lQZPkKcFWdyL/etB/+s3Q1IcAXv6BIhjrcCphIzmoZ4kW0/Ph9AHMom3xVMCwiZOgVlCll"
    "8KzKCYIvaLCF4ANLvB4rNqWfLrrCMrry3KJRUpI7eyQ1SSBxGFAx2ruNowkZincKYYJuW8"
    "+AXUUrItWWYTgiN3stiUHsYKO4HbreyYI3/8ACDgSpPIe95aTqBoOkwSK5kMlcd+KmyYqO"
    "ynwu2ONTmRrqI3EYVkQ6255Zf4r5SN++jQ7Lbvo57dg/fR8WfH5J/mkWk0RX5Wi3h9Caqu"
    "5M2XoVQuOSlaSHZGhpa1JidFWqU2liHJr1yHZK0X6JDqgdU6FCmPvQ7tdehN61BrqT1Gnl"
    "+LoN6xmww7nQoMO52VDMVS9oSH0idMCjq47JRH79lNjtuvxZRUVHwQpnasddjTmJHnlc+A"
    "1DvWpodAa75tN22QbGXOhVJlVPdgaMORtHSW6UPi2ZOiaSZZKZ1ngPbZTzQ7NNH84e97ye"
    "tcVTFJbdlRLen1qohJr7daTcTaspyI1qgBMXHfTYCddhU15l6rx5p2To/5HRmMe3AZ4o/r"
    "q8tiiKktGZC3iCd453g2ax34HmUPzcRaQlFkLYIOKH300/DeXfR/Z7kOfl6dSAqYMpfIq8"
    "gLnNQ7B9q+vMz/AqkvPpk="
)
