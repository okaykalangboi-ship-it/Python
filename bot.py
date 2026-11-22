

import discord
from discord.ext import commands
from mcstatus import JavaServer
import asyncio

# ==================================
# ECHOFALL SMP SERVER CONFIGURATION
# ==================================

TOKEN = "MTU3MzkxOTk2NzI5OTI0MDAwNg.G3melR.xF0anbhKjxeWhqL29gl-JleihaZzZZPa3z9UDY"

SERVER_IP = "EchoFallSMP.prism.baby"
SERVER_PORT = 25463

# ==================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print("==============================")
    print(f"Bot online: {bot.user}")
    print(f"Server: {SERVER_IP}:{SERVER_PORT}")
    print("==============================")


@bot.command()
async def ip(ctx):

    embed = discord.Embed(
        title="🌍 EchoFallSMP",
        description="Minecraft Java Server Information",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="🌐 Server IP",
        value=f"`{SERVER_IP}`",
        inline=False
    )

    embed.add_field(
        name="🔌 Port",
        value=f"`{SERVER_PORT}`",
        inline=True
    )

    try:
        server = JavaServer(
            SERVER_IP,
            SERVER_PORT,
            timeout=10
        )

        status = await asyncio.wait_for(
            server.async_status(),
            timeout=15
        )

        embed.color = discord.Color.green()

        embed.add_field(
            name="🟢 Server Status",
            value="ONLINE",
            inline=True
        )

        embed.add_field(
            name="👥 Players Online",
            value=f"{status.players.online}/{status.players.max}",
            inline=True
        )

        embed.add_field(
            name="📦 Minecraft Version",
            value=status.version.name,
            inline=True
        )

        players = status.players.sample or []

        if players:
            player_names = "\n".join(
                f"• {player.name}"
                for player in players
            )
        elif status.players.online > 0:
            player_names = (
                "Players are online, but names "
                "are not provided by the server."
            )
        else:
            player_names = "Nobody is online."

        embed.add_field(
            name="🎮 Online Players",
            value=player_names[:1024],
            inline=False
        )

    except asyncio.TimeoutError:
        embed.color = discord.Color.orange()
        embed.add_field(
            name="⚠️ Server Status",
            value="Status check timed out.",
            inline=False
        )

    except Exception as error:
        embed.color = discord.Color.red()
        embed.add_field(
            name="🔴 Server Status",
            value="Could not retrieve server status.",
            inline=False
        )

        print("Server error:", repr(error))

    embed.set_footer(
        text="EchoFallSMP • Minecraft Status Bot"
    )

    await ctx.send(embed=embed)


bot.run(TOKEN)

