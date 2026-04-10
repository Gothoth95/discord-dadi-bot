import discord
from discord.ext import commands
import random
import asyncio
import os
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

lobby_title = "Partita Dadi"
players = []

FILE = "stats.json"

# 🔹 Carica stats
def load_stats():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

# 🔹 Salva stats
def save_stats(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

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

# 👥 GIOCATORI SENZA VIRGOLE
@bot.command()
async def giocatori(ctx, *, lista: str):
    global players

    players = lista.split()

    if len(players) == 0:
        await ctx.send("❌ Nessun giocatore valido!")
        return

    await ctx.send(
        f"👥 Giocatori:\n" +
        "\n".join([f"• {p}" for p in players])
    )

    await asyncio.sleep(1)
    await play_game(ctx)

# 🎲 GIOCO CON SPAREGGI
async def play_game(ctx):
    global players, lobby_title

    stats = load_stats()

    round_num = 1
    current_players = players.copy()

    await ctx.send(f"\n🎲 **{lobby_title}** 🎲\n")

    while True:
        scores = {}
        await ctx.send(f"🔁 **Round {round_num}**")

        for p in current_players:
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            total = d1 + d2

            scores[p] = total

            await ctx.send(f"🎲 {p}: {d1} + {d2} = **{total}**")
            await asyncio.sleep(0.3)

        max_score = max(scores.values())
        winners = [p for p, s in scores.items() if s == max_score]

        if len(winners) == 1:
            winner = winners[0]

            await ctx.send(
                f"\n🏆 **VINCITORE: {winner} con {max_score}!**"
            )

            # 💾 SALVATAGGIO
            if lobby_title not in stats:
                stats[lobby_title] = {}

            if winner not in stats[lobby_title]:
                stats[lobby_title][winner] = 0

            stats[lobby_title][winner] += 1

            save_stats(stats)

            break
        else:
            await ctx.send(
                f"\n⚔️ Pareggio tra: {' '.join(winners)} con {max_score}!"
            )
            await ctx.send("🔁 Spareggio in corso...\n")

            current_players = winners
            round_num += 1
            await asyncio.sleep(1)

# 📊 STORICO
@bot.command()
async def storico(ctx):
    stats = load_stats()

    if not stats:
        await ctx.send("❌ Nessuna statistica disponibile!")
        return

    msg = "📊 **Storico Vittorie**\n\n"

    for lobby, data in stats.items():
        msg += f"🎮 {lobby}\n"

        for name, wins in data.items():
            msg += f"• {name}: {wins}\n"

        msg += "\n"

    await ctx.send(msg)

# 🔒 AVVIO BOT
bot.run(os.getenv("DISCORD_TOKEN"))