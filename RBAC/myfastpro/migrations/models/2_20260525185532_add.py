from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `mobile` VARCHAR(11);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `mobile` VARCHAR(11) NOT NULL;"""


MODELS_STATE = (
    "eJztmG1P2zAQx78KyqtN6qY2a4HtXemGxhggFZgmAYrcxE2jJnawnUGF+t1nO3Gdp2bpA1"
    "OK+qbQu3Ny9+s5/4tfjAA70Kcfh5DiiNjQ+HLwYiAQiH8KvtaBAcJQe4SBgZEvg0k6akQZ"
    "ATbj9jHwKeQmB1KbeCHzMOJWFPm+MGKbB3rI1aYIeY8RtBh2IZtAwh13D9zsIQc+Q6q+hl"
    "Nr7EHfyaTrOeLe0m6xWShtZ4idykBxt5FlYz8KkA4OZ2yC0SLaQ0xYXYggAQyKyzMSifRF"
    "dkmlqqI4Ux0Sp5ha48AxiHyWKrcmAxsjwY9nQ2WBrrjLB7PTPeoefzrsHvMQmcnCcjSPy9"
    "O1xwslgcsbYy79gIE4QmLU3OTfArnBBJBydCo+B4+nnIenUFXRUwaNT7fMlvgF4NnyIXLZ"
    "REBrV8D61R8OvveH78z2e1EL5k0cd/dl4jGlS/DU/ELAL7wCPxW/Fr+kt94SPs+xVtq6es"
    "G/t28zCG5hA4un3nhaun/DMnqnmEDPRedwJiGe8YQAssv2bclTvnEE56oHlFVnQcDTQgtS"
    "rcEL5GVBFu/F/vWg//WbISmOgD19AsSxluCk/CZFnifJqtPzIfSBzP9toZRssIlTTDK0iq"
    "7ADEoBEuzDEoIXAM1usPis25H8OusoymvrcUUzysyt/PyU1EFE40Bn4VYTU8wKE4l5CmeK"
    "YdLJi19AuZJliZtNCI7cyWJReg4r3QTcbuUnHPnjBwABV5pE3fNWtoCywTAprGIoVBH7gb"
    "BherIfCLc70RT0uY7URBSSDbXmll/iv1I27qNDs9u+j3p2D95Hx58dk3+aR6bRFPnJPFY3"
    "lKD6St58GUrVUpCihWTnZCirNQUp0iq1sQxJftU6JHu9RIfUHliuQ5GK2OvQXofetA61Mt"
    "tj5PkrEdQrdvJwotOpgbDTWYpQuPJnO5Q+YVKygavOd/SafStqgVntlCe1Yq1jnsZMPK98"
    "+qNesTY9/lnzZbtpc2QrdyKUaqNVj4Q2nEgrR5k+JJ49KRtmEk/lOAN0zH6g2aGB5g9/3U"
    "ve5uqKSWrJjmpJr1dHTHq95WoifFk5EVtjBYhJ+G4C7LTrqDGPWj7WtAt6zO/IYLwHsxB/"
    "XF9dlkNMLcmBvEW8wDvHs1nrwPcoe2gm1gqKomqRdEDpo5+G9+6i/zvPdfDz6kRSwJS5RF"
    "5FXuBktWOg7cvL/C+RcTw2"
)
