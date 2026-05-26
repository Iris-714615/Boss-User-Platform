from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `buser` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `phone` VARCHAR(11) NOT NULL,
    `username` VARCHAR(20) NOT NULL,
    `gender` VARCHAR(5) NOT NULL,
    `age` INT NOT NULL,
    `password` VARCHAR(20) NOT NULL,
    `email` VARCHAR(20) NOT NULL,
    `avatar` VARCHAR(20) NOT NULL,
    `total_money` INT NOT NULL,
    `status` VARCHAR(5) NOT NULL,
    `resume_complete` INT NOT NULL,
    `total_delivery` INT NOT NULL,
    `add_time` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmG1v2jAQx78KyqtO6irISlvtHbBO7TRgatmDWlWRSUyw6thp7JSiiu++s5PgEBJGJK"
    "SB2nfJ/+7iu5/ss+NXK+AepuKkGwscWZ8brxZDAYaHVcNxw0JhaGQlSDSm2nO8dBkLGSFX"
    "gjhBVGCQPCzciISScAYqiylVInfBkTDfSDEjTzF2JPexnOpM7h9AJszDL1hkr+GjMyGYei"
    "uJEk+NrXVHzkOtXTP5VTuq0caOy2kcMOMczuWUs6U3YVKpPmY4QhKrz8soVumr7NIys4qS"
    "TI1LkmIuxsMTFFOZK3dLBi5nih9kI3SBvhrlo906PT+9+HR2egEuOpOlcr5IyjO1J4GawG"
    "BkLbQdSZR4aIyGWwgI8Dq63hRF5eyWAQV8kHQRXwZrE79MMADNpNkRwQC9OBQzX07htdXa"
    "gOtX56Z31bk5arU+qFo4TONkcg9Si61NiqghqOa9fq4BMR9zmBzt5hYc7WYlR2Va5QgVe0"
    "kH2ZaiiThMhu0tELYrCbaLAJFfMgcre2Dq/e8muCfkdtIHc30PCTHjUcmusaH15WIOc8bt"
    "ftXiABFaB+Iy4J1gumyfYW+u1fdMxDvDhKHkElEngJPJvEYLLES91VYoJJKxqDMBTcRhTs"
    "Adb7wRFnGAgU8QUizrbMIlkW91FiaLEX4ryTOO6q/ifOBbRYg88CFlfyJfoG5lqdhPcnEF"
    "dl4aeJI97CfJDZhG1/3L21Gn/0NlHgjxRDWQzuhSWWytzgvq0Vlh8S8/0vh9PbpqqNfG3X"
    "BwqYlxIf1Ij2j8RneWygnFkjuMzxxAnCs7kzNpoa41Jo+5H3QljJH7OEOR56xZuM2rfNdN"
    "gR0UFcTg9O+lNFWe6TVPB0fEnVolF0Cp5XjTDRAyPu9XQHvXJqqvgKBtCpVSjQNALuQwTw"
    "B2e5szAHhVH0Lb6z/gsDTqHOMT98ME2Gpuc4gHr+qbtObaMR5GlDhZg6sQv90OB+UQcyEF"
    "kD8ZFHjvEVceNygR8mE/sW6gqKpe2bUyeEf9zp8i1973Ybe4HakPdIHxf91eFn8BedLBlA"
    "=="
)
