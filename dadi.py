import discord
from discord.ext import commands
import random
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

lobby_title = "Partita Dadi"
players = []

@bot.event
async def on_ready():
    print(f"Bot online come {bot.user}")

# 🎮 CREA LOBBY
@bot.command()
async def lobby(ctx, *, titolo: str = "Partita Dadi"):
    global lobby_title, players
    lobby_title = titolo
    players = []

    await ctx.send(f"🎮 Lobby creata: **{lobby_title}**\nUsa `!giocatori nome1 nome2 nome3`")

# 👥 INSERISCI GIOCATORI (SENZA VIRGOLE)
@bot.command()
async def giocatori(ctx, *, lista: str):
    global players

    # Divide per spazi
    players = lista.split()

    if len(players) == 0:
        await ctx.send("❌ Nessun giocatore valido!")
        return

    await ctx.send(
        f"👥 Giocatori registrati:\n" +
        "\n".join([f"• {p}" for p in players])
    )

    await asyncio.sleep(1)
    await play_game(ctx)

# 🎲 GIOCO CON SPAREGGI
async def play_game(ctx):
    global players

    round_num = 1
    current_players = players.copy()

    await ctx.send(f"\n🎲 **{lobby_title}** 🎲\n")

    while True:
        scores = {}
        await ctx.send(f"🔁 **Round {round_num}**")

        for p in current_players:
            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
            totale = dado1 + dado2

            scores[p] = totale

            await ctx.send(f"🎲 {p}: {dado1} + {dado2} = **{totale}**")
            await asyncio.sleep(0.3)

        max_score = max(scores.values())

        winners = [p for p, s in scores.items() if s == max_score]

        if len(winners) == 1:
            await ctx.send(
                f"\n🏆 **VINCITORE: {winners[0]} con {max_score}!**"
            )
            break
        else:
            await ctx.send(
                f"\n⚔️ Pareggio tra: {' '.join(winners)} con {max_score}!"
            )
            await ctx.send("🔁 Spareggio in corso...\n")

            current_players = winners
            round_num += 1
            await asyncio.sleep(1)

# 🔒 AVVIO BOT (Railway / locale)
bot.run(os.getenv("DISCORD_TOKEN"))