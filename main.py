import interactions
import boto3
from botocore.config import Config
from secrets import TOKEN, QUEUE_URL
from properties import GUILD_ID

sqs_config = Config(
    region_name='us-east-1',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

bot = interactions.Client(token=TOKEN)
sqs = boto3.client('sqs', config=sqs_config)


@bot.command(
    name="kms",
    description="Kenneth's Meta Strats",
    scope=GUILD_ID,
    options=[
        interactions.Option(
            name="build",
            description="Generate a recommended build",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
            options=[
                interactions.Option(
                    name="summoner",
                    description="Generate a recommended build for the specified user",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
                # interactions.Option(
                #     name="champion",
                #     description="Generate a recommended build for the specified champion",
                #     type=interactions.OptionType.STRING,
                #     required=False,
                # )
            ]
        ),
        # TODO: configure region, specify choice
        # TODO: generalize it to a set_properties command
    ]
)
async def cmd(
        ctx,
        sub_command,
        summoner="",
        # champion="",
):
    guild = ctx.get_guild()
    if sub_command == "build":  # generate a build recommendation
        msg = await get_build_from_summoner(summoner)
        await ctx.send(msg)


async def get_build_from_summoner(summoner):
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=summoner
    )
    return response


bot.start()
