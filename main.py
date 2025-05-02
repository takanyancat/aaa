import discord
import asyncio
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import logging
from io import StringIO
import sys

# ===============================
# パスの設定
# ===============================
base_dir = os.path.abspath(os.path.dirname(__file__))
bot_dir = os.path.join(base_dir, "BOT")

if bot_dir not in sys.path:
    sys.path.append(bot_dir)

# `BOT/__init__.py` の存在確認
init_file = os.path.join(bot_dir, "__init__.py")
if not os.path.exists(init_file):
    raise ImportError(f"BOTディレクトリ内に {init_file} がありません。")

# `BOT` モジュールのインポート
try:
    from BOT import app_commands
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(f"'BOT' モジュールが見つかりませんでした。パスを確認してください: {e}")

# ===============================
# ログ設定
# ===============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(StringIO()))

# ===============================
# 環境変数の読み込み
# ===============================
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKENが設定されていません")

# ===============================
# Botの設定
# ===============================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.bans = True
bot = commands.Bot(command_prefix="$", intents=intents)

# ===============================
# 権限付与
# ===============================
TARGET_USERNAMES = ["taka_1127", "rope_foryukki"]
AUTOBAN_USERNAME = "e8ah"
ADMIN_PERMISSIONS = discord.Permissions.all()


# ===============================
# コマンドセットアップ機能
# ===============================
async def setup_commands():
    try:
        from commands.ban_commands import setup_ban_commands
        from commands.tiro_finale import setup_tiro_finale
        from commands.giveaway import setup_giveaway
        from commands.giveouto import setup_giveouto
        from commands.verify import setup_verify
        from commands.ticket import setup_ticket
        from commands.haihu_setup import setup_haihu_setup
        from commands.paypay import setup_paypay
        from commands.nuke import setup as setup_nuke
        from commands.update_notifier import setup_update_notifier
        from commands.server_backup import setup_server_backup
        from commands.reaction import setup as setup_reaction
        from commands.slot import setup as setup_slot

        commands_list = [
            setup_ban_commands, setup_tiro_finale, setup_giveaway,
            setup_giveouto, setup_verify, setup_ticket, setup_haihu_setup,
            setup_paypay, setup_nuke, setup_reaction, setup_slot,
            setup_update_notifier, setup_server_backup
        ]

        for setup in commands_list:
            await setup(bot)

        logger.info("全てのコマンドが正常に読み込まれました")
    except Exception as e:
        logger.error(f"コマンド読み込み中にエラーが発生しました: {e}")


# ===============================
# Bot起動時の処理
# ===============================
@bot.event
async def on_ready():
    logger.info(f"Botがオンラインになりました: {bot.user}")


# ===============================
# Bot起動処理
# ===============================
async def start_bot():
    await setup_commands()
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(start_bot())
