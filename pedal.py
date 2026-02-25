import discord
from discord import app_commands
from discord.ext import commands
import re

# --- KONFIGURACJA ---
TOKEN = 'MTQ3NjE3MzYxNDQzOTk5MzM3Ng.GL9_0x.X75QUm_lnmtrW8zekz16NUvu6gxd1bn13ge26s'
ID_KANALU_LEGIT_CHECK = 1474442209444237506 # Wpisz ID swojego kanału

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Zalogowano jako {self.user} i zsynchronizowano komendy.")

bot = MyBot()

async def get_last_number(channel):
    """Pancerna funkcja szukania numeru - rozwiązuje błąd ze zdjęcia"""
    try:
        async for message in channel.history(limit=50):
            if message.author == bot.user and message.embeds:
                embed = message.embeds[0]
                for field in embed.fields:
                    if "LEGIT CHECK" in field.value:
                        # Szuka wszystkich cyfr w tekście pola
                        numbers = re.findall(r'\d+', field.value)
                        if numbers:
                            # Bierze ostatnią znalezioną liczbę
                            return int(numbers[-1])
    except Exception as e:
        print(f"Błąd podczas sprawdzania historii: {e}")
    
    return 7152 # Liczba startowa

async def send_legit_embed(interaction, screenshot, typ_transakcji):
    if interaction.channel_id != ID_KANALU_LEGIT_CHECK:
        await interaction.response.send_message("To nie ten kanał!", ephemeral=True)
        return

    # To rozwiązuje błąd "polecenie jest nieaktualne" (daje botowi czas)
    await interaction.response.defer()

    num = await get_last_number(interaction.channel)
    new_num = num + 1

    embed = discord.Embed(
        title=f"💸 {typ_transakcji} Anarchia <:anarchia:1476187656860864664> Lifesteal",
        color=0xffa500
    )
    
    # Format identyczny jak na screenie z pierwszego pytania
    embed.add_field(
        name="", 
        value=f"» × ✅ **LEGIT CHECK** → {new_num}\n"
              f"» × 💸 **Klient potwierdził udaną transakcję**\n"
              f"» ×  **XYZ|SHOP - Bezpieczne zakupy**", 
        inline=False
    )
    
    embed.set_image(url=screenshot.url)
    embed.set_footer(text=f"Przez: {interaction.user.display_name}")

    await interaction.followup.send(embed=embed)

@bot.tree.command(name="zakup", description="Dodaj legit check (zakup)")
async def zakup(interaction: discord.Interaction, screenshot: discord.Attachment):
    await send_legit_embed(interaction, screenshot, "Zakup")

@bot.tree.command(name="sprzedaz", description="Dodaj legit check (sprzedaż)")
async def sprzedaz(interaction: discord.Interaction, screenshot: discord.Attachment):
    await send_legit_embed(interaction, screenshot, "Sprzedaż")

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    if message.channel.id == ID_KANALU_LEGIT_CHECK:
        if not message.interaction:
            try:
                await message.delete()
            except:
                pass

bot.run(TOKEN)