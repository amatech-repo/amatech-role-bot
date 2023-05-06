import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
GUILD_ID = os.getenv('GUILD_ID')
MESSAGE_ID = os.getenv('MESSAGE_ID')

# Discord botのコマンドプレフィックス
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    # メッセージを送信するチャンネルを取得
    channel = bot.get_channel(CHANNEL_ID)

    # メッセージを送信
    message = await channel.send('こんにちは！以下のリアクションをクリックすると、あなたにロールを付与します。\n\nスマブラ部 :video_game:\nスプラ部 :art:\n甘てく :cake:\n麻雀部 :mahjong:\nテッペン部 :trophy:\nモンスト部 :dragon:')

    # リアクションを付与
    reactions = ['🎮', '🎨', '🍰', '🀄', '🏆', '🐲']
    for reaction in reactions:
        await message.add_reaction(reaction)


# リアクションを付与したときに実行されるイベント
@bot.event
async def on_raw_reaction_add(payload):
    print('リアクションを付与します')

    # ロールの名前とIDの辞書
    roles = {
        '🎮': 1104336563153932298,
        '🎨': 1104278806107279372,
        '🍰': 1104337324621439129,
        '🀄': 1104338437798113390,
        '🏆': 1104338556236865586,
        '🐲': 1104338615200403558
    }

    # リアクションを付与するときの絵文字とロールの名前の辞書
    reactions = {
        '🎮': 'スマブラ部',
        '🎨': 'スプラ部',
        '🍰': '甘てく',
        '🀄': '麻雀部',
        '🏆': 'テッペン部',
        '🐲': 'モンスト部'
    }

    message_id = payload.message_id
    if message_id == MESSAGE_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        if guild is not None:
            role_name = str(payload.emoji)
            if role_name in roles:
                role_id = roles[role_name]
                role = guild.get_role(role_id)
                if role is not None:
                    member = await guild.fetch_member(payload.user_id)
                    if member is not None:
                        await member.add_roles(role)
                        print(f"ロール {role.name} をユーザー {member.display_name} に付与しました")
                    else:
                        print(f"メンバーが見つかりませんでした")
                else:
                    print(f"ロールが見つかりませんでした")
            else:
                print(f"リアクションに対応するロールがありません")
        else:
            print(f"サーバーが見つかりませんでした")

# Discord botを起動する
bot.run(TOKEN)
