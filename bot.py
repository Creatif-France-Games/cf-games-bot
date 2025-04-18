from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import asyncio
from discord import ui
from discord import app_commands
import wikipediaapi

# Initialisation de Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot actif !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Charger le token depuis le fichier .env
load_dotenv()

# Configuration des intents
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Connecté en tant que {bot.user} (commandes slash synchronisées)')

# Configuration des IDs (à remplacer par vos vrais IDs)
CHANNEL_ANNONCES_ID = os.getenv('CHANNEL_ANNONCES_ID')  # Utilisez une variable d'environnement
ROLE_NOTIFS_ID = os.getenv('ROLE_NOTIFS_ID')  # Utilisez une variable d'environnement


# Liste des compliments
COMPLIMENTS = [
    "{member.display_name}, tu es une personne incroyable ! 😄",
    "{member.display_name}, tu illumines la journée de tout le monde ! ✨",
    "{member.display_name}, tu as un sourire qui réchauffe le cœur ! 😊",
    "{member.display_name}, tu es un rayon de soleil dans ce monde ! 🌞",
    "{member.display_name}, tes idées sont toujours brillantes ! 💡",
    "{member.display_name}, tu as un grand cœur ! ❤️",
    "{member.display_name}, t'es vraiment une source d'inspiration ! 🌟",
    "{member.display_name}, ton énergie est contagieuse ! ⚡",
    "{member.display_name}, t'es une personne vraiment cool et positive ! 😎"
]

#Commande /wikipedia (en test, marche pas trop je crois)
@bot.tree.command(name='wikipedia', description='Fais une recherche sur Wikipédia.')
async def wikipedia(interaction: discord.Interaction, recherche: str):
    wiki = wikipediaapi.Wikipedia('fr')  # ou 'en' pour anglais

    page = wiki.page(recherche)

    if not page.exists():
        await interaction.response.send_message(f"Aucune page trouvée pour : **{recherche}**", ephemeral=True)
        return

    extrait = page.summary[0:1000]  # Coupe à 1000 caractères max
    url = page.fullurl

    await interaction.response.send_message(f"**{page.title}**\n{extrait}...\n[Lire plus ici]({url})")


# Commande Slash pour lancer un dé
@bot.tree.command(name='de', description='Lance un dé avec un nombre de faces de ton choix.')
async def de(interaction: discord.Interaction, faces: int = 6):
    roll_result = random.randint(1, faces)
    await interaction.response.send_message(f"Tu as lancé un dé à {faces} faces et tu as obtenu : {roll_result}")

# Lire les blagues depuis le blagues.txt
def lire_blagues():
    with open('blagues.txt', 'r') as f:
        blagues = f.readlines()
    return [blague.strip() for blague in blagues]

# Commande Slash pour dire une blague
@bot.tree.command(name='blague', description='Dis une blague drôle.')
async def blague(interaction: discord.Interaction):
    blagues = lire_blagues()  # Lit la blague
    joke = random.choice(blagues)  # Choisir aléatoiremetn
    await interaction.response.send_message(joke)  # Envoie la blague

# Commande Slash pour changer le statut du bot
@bot.tree.command(name='statusbot', description='Change le statut du bot avec un message personnalisé.')
async def statusbot(interaction: discord.Interaction, statut: str):
    activity = discord.Game(name=statut)
    await bot.change_presence(activity=activity)
    await interaction.response.send_message(f"Le statut du bot a été changé en : {statut}")

# Commande Slash pour envoyer un compliment
@bot.tree.command(name='compliment', description='Envoie un compliment à un utilisateur !')
async def compliment(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    compliment_message = random.choice(COMPLIMENTS).format(member=member)
    await interaction.response.send_message(compliment_message)

# Commande Slash pour afficher la latence
@bot.tree.command(name="ping", description="Affiche la latence du bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # En ms
    await interaction.response.send_message(f"Pong ! Latence : `{latency}ms`")

# Code déjà initialisé pour la gestion des messages
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    salutations = ["salut", "bonjour", "coucou", "hi", "hola", "hello", "yo", "bonsoir"]
    depart = ["au revoir", "bye", "a+", "ciao", "see ya", "à bientôt", "adieu", "bonne nuit", "bn", "tchao"]
    faim = ["j'ai faim", "faim", "j’ai la dalle", "je crève de faim", "trop faim", "je crève la dalle"]
    quoifeur = ["quoi"]


    if any(word in content for word in salutations):
        await message.reply(f"Salut {message.author.mention} !")
        return
    elif any(word in content for word in depart):
        await message.reply(f"Bye {message.author.mention} !")
        return
    elif any(word in content for word in faim):
        await message.reply("Tiens une bonne assiette de pâtes carbonara :\nhttps://cdn.pixabay.com/photo/2011/04/29/11/20/spaghetti-7113_1280.jpg")
        return
    elif any(word in content for word in quoifeur):
        await message.reply("Feur !")
        return

    await bot.process_commands(message)


# Code pour envoyer une news (fonctionnel avec permissions administrateur)
@bot.tree.command(name="envoyer_news", description="Envoyer une news dans le salon annonces")
@app_commands.checks.has_permissions(administrator=True)
async def envoyer_news(interaction: discord.Interaction):
    await interaction.response.send_message("Que souhaitez-vous inclure ?", ephemeral=True)

    def check(m):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    try:
        msg = await bot.wait_for("message", check=check, timeout=60)

        view = ConfirmationView(interaction.user, msg.content)
        await interaction.followup.send("Clique pour confirmer ou annuler :", view=view, ephemeral=True)

        await view.wait()

        if view.confirmed:
            salon = bot.get_channel(CHANNEL_ANNONCES_ID)
            role = interaction.guild.get_role(ROLE_NOTIFS_ID)

            if salon and role:
                embed = discord.Embed(
                    title="NEWS",
                    description=msg.content,
                    color=discord.Color.from_rgb(88, 101, 242)
                )
                await salon.send(f"{role.mention}", embed=embed)
                await interaction.followup.send("News envoyée !", ephemeral=True)
            else:
                await interaction.followup.send("Erreur : salon ou rôle introuvable.", ephemeral=True)
        else:
            await interaction.followup.send("Envoi annulé.", ephemeral=True)

    except asyncio.TimeoutError:
        await interaction.followup.send("Temps écoulé, veuillez recommencer la commande.", ephemeral=True)

# Code déjà initialisé pour garder le bot actif via Flask
keep_alive()

# Lancer le bot Discord
bot.run(os.getenv('DISCORD_TOKEN'))

