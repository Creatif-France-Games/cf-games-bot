# Créé par la Team CF Games avec l'aide de GPT.
# Sous license CC-BY, voir le fichier LICENSE
# (c) Team CF Games 2025
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
import requests
from discord import ui
from discord import app_commands
import wikipediaapi
from discord.app_commands import MissingPermissions
from discord.ui import View, Button
from server import keep_alive
import youtube_dl  # Nécessaire pour gérer les streams audio


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
    
import debile
debile.setup(bot)
import quiz
quiz.setup(bot)
import mistralai
mistralai.setup(bot)
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
    recherche = recherche.strip()  # Nettoyer l'entrée utilisateur
    wiki = wikipedia-api.Wikipedia('fr')  # ou 'en' pour l'anglais

    page = wiki.page(recherche)

    if not page.exists():
        await interaction.response.send_message(
            f"Aucune page trouvée pour : **{recherche}**. Essayez un autre mot-clé ou vérifiez l'orthographe.",
            ephemeral=True
        )
        return

    extrait = page.summary[0:1000]
    if len(page.summary) > 1000:
        extrait += "..."

    url = page.fullurl

    await interaction.response.send_message(
        f"**{page.title}**\n{extrait}\n[Lire plus ici]({url})"
    )


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

    salutations = ["salut", "bonjour", "coucou", "hi", "hola", "hello", "yo ", " yo", "bonsoir", "cc", "slt", "bjr"]
    depart = ["au revoir", "bye", "a+", "ciao", "see ya", "à bientôt", "adieu", "bonne nuit", "bn", "tchao"]
    faim = ["j'ai faim", "faim", "j’ai la dalle", "je crève de faim", "trop faim", "je crève la dalle"]
    quoifeur = ["quoi"]
    cava = ["ca va?", "cv?", "ça va ?", "bien ou bien"]
    caca = ["caca", "crotte"]
    rigole = ["haha", "lol", "mdr", "ptdr"]
    musique = ["musique", "chanson", "playlist", "écouter", "chant"]
    triste = ["triste", "déprimé", "mélancolique", "morose"]


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
    elif any(word in content for word in cava):
        await message.reply("Moi je vait bien, comme toujours ! Et toi?")
        return
    elif any(word in content for word in caca):
        embed = discord.Embed()
        embed.set_image(url="https://cdn.pixabay.com/photo/2014/02/13/11/56/wc-265278_1280.jpg")
        await message.reply(embed=embed)
        return
    elif any(word in content for word in rigole):
        await message.reply("T'as l'air de bien rigoler 😄!")
        return
    elif any(word in content for word in musique):
        await message.reply("Moi j'en connais une ! Never gonna give you up !")
        return
    elif any(word in content for word in triste):
        await message.reply("Fait /blague pour te remonter le moral !")
        return
    await bot.process_commands(message)


# Définition de la classe ConfirmationView
class ConfirmationView(View):
    def __init__(self, user, content):
        super().__init__()
        self.user = user
        self.content = content
        self.confirmed = False

    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.user.id:
            self.confirmed = True
            self.stop()
        else:
            await interaction.response.send_message("Vous ne pouvez pas interagir avec cette confirmation.", ephemeral=True)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.user.id:
            self.confirmed = False
            self.stop()
        else:
            await interaction.response.send_message("Vous ne pouvez pas interagir avec cette confirmation.", ephemeral=True)

# Commande Slash pour envoyer une news
@bot.tree.command(name="envoyer_news", description="Envoyer une news dans le salon annonces")
@app_commands.checks.has_permissions(administrator=True)
async def envoyer_news(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)  # Réponse différée pour éviter les erreurs de délai
    await interaction.followup.send("Que souhaitez-vous inclure ?", ephemeral=True)

    def check(m):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    try:
        # Attente de la réponse de l'utilisateur
        msg = await bot.wait_for("message", check=check, timeout=600)

        # Création de la vue de confirmation
        view = ConfirmationView(interaction.user, msg.content)
        await interaction.followup.send("Cliquez pour confirmer ou annuler :", view=view, ephemeral=True)

        # Attente de l'interaction avec la vue
        await view.wait()

        if view.confirmed:
            # Récupération du salon et du rôle
            salon = bot.get_channel(int(os.getenv('CHANNEL_ANNONCES_ID')))
            role = interaction.guild.get_role(int(os.getenv('ROLE_NOTIFS_ID')))

            if not salon:
                await interaction.followup.send("Erreur : le salon des annonces est introuvable.", ephemeral=True)
                return
            if not role:
                await interaction.followup.send("Erreur : le rôle pour les notifications est introuvable.", ephemeral=True)
                return

            # Création et envoi de l'embed
            embed = discord.Embed(
                title="NEWS",
                description=msg.content,
                color=discord.Color.from_rgb(88, 101, 242)
            )
            await salon.send(f"{role.mention}", embed=embed)
            await interaction.followup.send("News envoyée !", ephemeral=True)
        else:
            await interaction.followup.send("Envoi annulé.", ephemeral=True)

    except asyncio.TimeoutError:
        await interaction.followup.send("Temps écoulé, veuillez recommencer la commande.", ephemeral=True)

# Gestion des erreurs de permissions
@envoyer_news.error
async def envoyer_news_error(interaction: discord.Interaction, error):
    if isinstance(error, MissingPermissions):
        await interaction.response.send_message(
            "Vous devez être administrateur pour utiliser cette commande.", ephemeral=True
        )
# embed des infos du bot
@bot.tree.command(name="infobot", description="Affiche les informations du bot.")
async def infobot(interaction):
    # Date de création fixée au 16 avril 2025
    creation_date = "16 avril 2025"

    embed = discord.Embed(
        title="CF Games Bot",
        description="Bot Discord Open-Source\n\nCode source : [GitHub Repository](https://github.com/Creatif-France-Games/cf-games-bot/)",
        color=discord.Color.blue() 
    )
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else "")  # Ajoute l'avatar du bot (si dispo)
    embed.add_field(name="Date de création", value=creation_date, inline=False)
    embed.set_footer(text="Merci d'utiliser CF Games Bot !")

    # Envoi de l'embed
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar", description="Affiche l'avatar d'un membre")
async def avatar(interaction: discord.Interaction, membre: discord.Member = None):
    membre = membre or interaction.user
    avatar_url = membre.avatar.url if membre.avatar else membre.default_avatar.url
    await interaction.response.send_message(f"Avatar de {membre.display_name} : {avatar_url}")

# Lancer un minuteur
@bot.tree.command(name="minuteur", description="Lance un minuteur avec un nom personnalisé")
async def minuteur(interaction: discord.Interaction, duree: int, nom: str):
    await interaction.response.send_message(
        f"⏳ Minuteur **{nom}** lancé pour {duree} minute(s), {interaction.user.mention} !"
    )

    async def timer_task():
        try:
            await asyncio.sleep(duree * 60)
            await interaction.followup.send(f"⏰ Le minuteur **{nom}** est terminé, {interaction.user.mention} !")
        except asyncio.CancelledError:
            await interaction.followup.send(f"❌ Le minuteur **{nom}** a été annulé, {interaction.user.mention}.")

    task = asyncio.create_task(timer_task())
    active_minuteurs[interaction.user.id] = task


@bot.tree.command(name="annule_minuteur", description="Annule ton minuteur en cours")
async def annule_minuteur(interaction: discord.Interaction):
    task = active_minuteurs.get(interaction.user.id)
    if task and not task.done():
        task.cancel()
        await interaction.response.send_message(f"🛑 Ton minuteur a été annulé, {interaction.user.mention}.")
        del active_minuteurs[interaction.user.id]
    else:
        await interaction.response.send_message("⚠️ Tu n’as pas de minuteur actif à annuler.")

# Commande /dire
@bot.tree.command(name="dire", description="Envoie un message personnalisé dans le canal.")
@app_commands.checks.has_permissions(administrator=True)
async def dire(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message) 

# Gestion des erreurs pour la commande /dire si l'utilisateur n'est pas admin
@dire.error
async def dire_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Désolé, vous devez être un administrateur pour utiliser cette commande.")

# Fonction asynchrone pour obtenir une blague en JSON
async def get_joke():
    url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous?lang=fr&blacklistFlags=nsfw,religious,racist,sexist,explicit"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("type") == "single":
                    return data.get("joke")
                elif data.get("type") == "twopart":
                    return f"{data.get('setup')}\n{data.get('delivery')}"
            return "Impossible de récupérer une blague."

# Slash command qui fonctionne vraiment
@bot.tree.command(name="blague", description="Obtiens une blague !")
async def blague(interaction: discord.Interaction):
    await interaction.response.defer()  # évite le timeout Discord
    joke = await get_joke()
    embed = discord.Embed(
        title="Blague du jour",
        description=joke,
        color=discord.Color.orange()
    )
    embed.set_footer(text="Via JokeAPI | /blague")
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="embed", description="Envoie un message sous forme d'embed avec une couleur bleue.")
@app_commands.checks.has_permissions(administrator=True)
async def embed(interaction: discord.Interaction, titre: str, description: str):
    # Crée un embed avec les informations fournies
    embed = discord.Embed(
        title=titre,
        description=description,
        color=discord.Color.blue()  # Couleur bleue
    )
    
    # Envoie l'embed dans le canal
    await interaction.response.send_message(embed=embed)

@embed.error
async def embed_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "Désolé, vous devez être un administrateur pour utiliser cette commande.",
            ephemeral=True  # Message visible uniquement par l'utilisateur
        )

@bot.tree.command(name="bannir", description="Bannir un utilisateur avec une raison.")
@app_commands.checks.has_permissions(administrator=True)
async def bannir(interaction: discord.Interaction, membre: discord.Member, raison: str):
    try:
        # Envoi du message privé à l'utilisateur banni
        await membre.send(f"Vous avez été banni du serveur **{interaction.guild.name}** pour la raison suivante : {raison}")
    except discord.Forbidden:
        # Si l'utilisateur a les MP désactivés ou bloqués
        await interaction.response.send_message(
            f"Impossible d'envoyer un message privé à {membre.display_name}, mais il sera quand même banni.",
            ephemeral=True
        )
    except Exception as e:
        # Gestion des autres erreurs
        await interaction.response.send_message(
            f"Une erreur inattendue s'est produite : {e}",
            ephemeral=True
        )
        return

    # Bannir l'utilisateur
    await interaction.guild.ban(membre, reason=raison)
    
    # Répondre dans le canal
    await interaction.response.send_message(f"{membre.display_name} a été banni pour la raison suivante : {raison}")

@bot.tree.command(name="kick", description="Expulse un utilisateur du serveur avec une raison.")
@app_commands.checks.has_permissions(administrator=True)
async def kick(interaction: discord.Interaction, membre: discord.Member, raison: str):
    try:
        # Envoi du message privé à l'utilisateur expulsé
        await membre.send(f"Vous avez été expulsé du serveur **{interaction.guild.name}** pour la raison suivante : {raison}")
    except discord.Forbidden:
        # Si l'utilisateur a les MP désactivés ou bloqués
        await interaction.response.send_message(
            f"Impossible d'envoyer un message privé à {membre.display_name}, mais il sera quand même expulsé.",
            ephemeral=True
        )
    except Exception as e:
        # Gestion des autres erreurs
        await interaction.response.send_message(
            f"Une erreur inattendue s'est produite : {e}",
            ephemeral=True
        )
        return

    # Expulser l'utilisateur
    await interaction.guild.kick(membre, reason=raison)
    
    # Répondre dans le canal
    await interaction.response.send_message(f"{membre.display_name} a été expulsé pour la raison suivante : {raison}")
@bot.tree.command(name="infoserveur", description="Affiche des informations détaillées sur le serveur.")
async def infoserveur(interaction: discord.Interaction):
    # Récupérer les informations sur le serveur
    guild = interaction.guild
    nom_serveur = guild.name
    proprietaire = guild.owner
    date_creation = guild.created_at.strftime("%d %B %Y à %H:%M:%S")
    nombre_membres = len(guild.members)
    nombre_bots = len([membre for membre in guild.members if membre.bot])
    nombre_humains = nombre_membres - nombre_bots
    roles = [role.mention for role in guild.roles if role.name != "@everyone"]  # Exclure @everyone
    emojis = [str(emoji) for emoji in guild.emojis]
    niveau_boost = guild.premium_tier
    boosts = guild.premium_subscription_count

    # Créer un embed pour afficher les informations
    embed = discord.Embed(
        title=f"Informations sur le serveur : {nom_serveur}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Propriétaire", value=proprietaire.mention, inline=False)
    embed.add_field(name="Date de création", value=date_creation, inline=False)
    embed.add_field(name="Membres", value=f"Total : {nombre_membres}\nHumains : {nombre_humains}\nBots : {nombre_bots}", inline=False)
    embed.add_field(name="Niveau de boost", value=f"Niveau {niveau_boost} ({boosts} boosts)", inline=False)
    embed.add_field(name="Rôles", value=", ".join(roles) if roles else "Aucun rôle", inline=False)
    embed.add_field(name="Emojis", value=", ".join(emojis) if emojis else "Aucun emoji", inline=False)

    # Envoyer l'embed
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="infomembre", description="Affiche des informations sur un membre du serveur.")
async def infomembre(interaction: discord.Interaction, membre: discord.Member):
    # Récupérer les informations du membre
    nom = membre.name
    pseudo = membre.nick if membre.nick else "Aucun"
    date_creation_discord = membre.created_at.strftime("%d %B %Y à %H:%M:%S")
    date_rejoignage_serveur = membre.joined_at.strftime("%d %B %Y à %H:%M:%S") if membre.joined_at else "Inconnu"
    roles = [role.mention for role in membre.roles if role.name != "@everyone"]

    # Créer un embed pour afficher les informations
    embed = discord.Embed(
        title=f"Informations sur {nom}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Nom", value=nom, inline=False)
    embed.add_field(name="Pseudo (dans le serveur)", value=pseudo, inline=False)
    embed.add_field(name="Date de création du compte Discord", value=date_creation_discord, inline=False)
    embed.add_field(name="Date de rejoignage du serveur", value=date_rejoignage_serveur, inline=False)
    embed.add_field(name="Rôles", value=", ".join(roles) if roles else "Aucun rôle", inline=False)

    # Envoyer l'embed
    await interaction.response.send_message(embed=embed)

import datetime

@bot.tree.command(name="mute", description="Rend un membre muet pour une durée spécifiée.")
@app_commands.checks.has_permissions(administrator=True)
async def mute(interaction: discord.Interaction, membre: discord.Member, duree: int):
    # Vérifie si le rôle "Muted" existe
    mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not mute_role:
        await interaction.response.send_message(
            "Le rôle 'Muted' n'existe pas. Veuillez le créer et configurer ses permissions.",
            ephemeral=True
        )
        return

    # Ajoute le rôle "Muted" au membre
    await membre.add_roles(mute_role, reason=f"Muted par {interaction.user} pour {duree} minutes")
    await interaction.response.send_message(
        f"{membre.mention} a été rendu muet pour {duree} minutes.",
        ephemeral=False
    )

    # Planifie la suppression du rôle après la durée spécifiée
    await asyncio.sleep(duree * 60)  # Convertit la durée de minutes en secondes
    if mute_role in membre.roles:
        await membre.remove_roles(mute_role, reason="Durée de mute expirée")
        try:
            await membre.send(f"Vous n'êtes plus muet sur le serveur **{interaction.guild.name}**.")
        except discord.Forbidden:
            pass  # Si l'utilisateur a désactivé les MP

@bot.tree.command(name="qr", description="Génère un code QR à partir d'un texte ou d'une URL.")
async def qr(interaction: discord.Interaction, texte: str):
    # URL de l'API pour générer le code QR
    qr_url = f"https://quickchart.io/qr?text={texte}"
    
    # Créer un embed avec le code QR
    embed = discord.Embed(
        title="Code QR généré",
        description=f"Voici votre code QR pour : `{texte}`",
        color=discord.Color.blue()
    )
    embed.set_image(url=qr_url)  # Ajoute l'image du QR code
    embed.set_footer(text="Généré avec QuickChart.io")
    
    # Envoie l'embed
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="bombe", description="Effectue un compte à rebours avant une explosion.")
async def bombe(interaction: discord.Interaction):
    await interaction.response.defer()  # Évite le timeout Discord pour les longues tâches
    
    # Liste du compte à rebours
    countdown = ["5", "4", "3", "2", "1"]
    
    # Message initial
    message = await interaction.followup.send("Ça va exploser : 5")
    await asyncio.sleep(1)
    
    # Modifier le message pour chaque étape du compte à rebours
    for i in range(1, len(countdown)):
        await message.edit(content=f"Ça va exploser : {countdown[i]}")
        await asyncio.sleep(1)
    
    # Remplace le message par le GIF de l'explosion
    await message.edit(content="💥 BOUM 💥\nhttps://c.tenor.com/uBrOl8WjH-EAAAAd/tenor.gif")
    await asyncio.sleep(3)
    
    # Supprime le message
    await message.delete()

# Commande Slash pour récupérer la température
@bot.tree.command(name="temperature", description="Affiche la température d'une ville.")
@app_commands.describe(ville="La ville pour laquelle afficher la température.")
async def temperature(interaction: discord.Interaction, ville: str):
    # Construire l'URL de l'API
    url = f"https://wttr.in/{ville}?format=%t"

    try:
        # Envoyer la requête à l'API
        response = requests.get(url)
        if response.status_code == 200:
            temperature = response.text.strip()  # Récupérer la température (nettoyer les espaces)
            
            # Créer un embed bleu
            embed = discord.Embed(
                title=f"Température de {ville.capitalize()}",
                description=f"**{temperature}**",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Via l'API wttr.in")

            # Envoyer l'embed
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                f"❌ Impossible de récupérer la température pour **{ville}**. Vérifiez l'orthographe ou réessayez plus tard.",
                ephemeral=True
            )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Une erreur est survenue en récupérant la température : {str(e)}",
            ephemeral=True
        )

# Commande Slash pour Rickroll
@bot.tree.command(name="rickroll", description="Envoie un Rickroll en message privé à un membre.")
@app_commands.describe(membre="Le membre à Rickroller.")
async def rickroll(interaction: discord.Interaction, membre: discord.Member):
    try:
        # Message Rickroll
        message = f"La personne {interaction.user.display_name} souhaite te partager cette vidéo : <https://youtu.be/dQw4w9WgXcQ?si=Hpc6awRKbIBqN3ws>"
        
        # Envoyer un message privé au membre
        await membre.send(message)
        
        # Répondre dans le salon pour confirmer l'envoi
        await interaction.response.send_message(f"Rickroll envoyé à {membre.display_name} !", ephemeral=True)
    except discord.Forbidden:
        # Si l'utilisateur a désactivé les MP
        await interaction.response.send_message(
            f"Impossible d'envoyer un message privé à {membre.display_name}.",
            ephemeral=True
        )
    except Exception as e:
        # Gestion des autres erreurs
        await interaction.response.send_message(
            f"Une erreur inattendue s'est produite : {str(e)}",
            ephemeral=True
        )

# Commande Slash pour un exercice de respiration
@bot.tree.command(name="respiration_exercice", description="Lance un exercice de respiration guidée (1 minute).")
async def respiration_exercice(interaction: discord.Interaction):
    try:
        # Informer l'utilisateur que l'exercice va commencer
        await interaction.response.send_message("Préparez-vous... L'exercice de respiration va commencer dans 5 secondes !")
        await asyncio.sleep(5)  # Pause initiale de 5 secondes

        # Variables pour contrôler le temps de l'exercice
        total_duration = 60  # Durée totale de l'exercice en secondes
        cycle_duration = 19  # Durée d'un cycle complet (inspirez 5s + expirez 5s + attendez 4s)
        cycles = total_duration // cycle_duration  # Nombre total de cycles (60 / 19)

        # Lancer l'exercice de respiration
        for cycle in range(cycles):
            for phase, phase_text, duration in [
                ("inspirez", "Inspirez...", 5),
                ("expirez", "Expirez...", 5),
                ("attendez", "Attendez...", 4),
            ]:
                # Créer un compte à rebours pour chaque étape
                for countdown in range(duration, 0, -1):
                    await interaction.channel.send(f"**{countdown}** {phase_text}")
                    await asyncio.sleep(1)

        # Fin de l'exercice
        await interaction.channel.send("🎉 Exercice de respiration terminé ! Bravo ! 🎉")

    except Exception as e:
        # Gestion des erreurs
        await interaction.followup.send(f"❌ Une erreur est survenue pendant l'exercice : {str(e)}", ephemeral=True)

# Commande Slash pour jouer une radio
@bot.tree.command(name="radio", description="Joue une station de radio dans votre salon vocal.")
@app_commands.describe(radio="Le nom de la station de radio.")
async def radio(interaction: discord.Interaction, radio: str):
    # Vérifiez si l'utilisateur est dans un salon vocal
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("❌ Vous devez être dans un salon vocal pour utiliser cette commande.", ephemeral=True)
        return

    # Rejoindre le salon vocal
    voice_channel = interaction.user.voice.channel
    voice_client = await voice_channel.connect()

    # Récupérer la liste des radios via l'API Radio-Browser
    url = "https://de1.api.radio-browser.info/json/stations/bycountry/France"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await interaction.response.send_message("❌ Impossible de récupérer les stations de radio. Réessayez plus tard.", ephemeral=True)
                return

            radios = await response.json()
            # Trouver la radio correspondante
            station = next((r for r in radios if radio.lower() in r["name"].lower()), None)
            if not station:
                await interaction.response.send_message(f"❌ La station de radio `{radio}` est introuvable.", ephemeral=True)
                await voice_client.disconnect()
                return

            stream_url = station["url"]
            await interaction.response.send_message(f"🎵 Lecture de `{station['name']}` dans {voice_channel.name}...")

            # Jouer le stream audio
            try:
                ydl_opts = {"format": "bestaudio/best", "quiet": True}
                ffmpeg_opts = {
                    "options": "-vn",
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(stream_url, download=False)
                    url2play = info["url"]

                voice_client.play(discord.FFmpegPCMAudio(url2play, **ffmpeg_opts))
            except Exception as e:
                await interaction.response.send_message(f"❌ Une erreur s'est produite en jouant la radio : {e}", ephemeral=True)
                await voice_client.disconnect()
                return

            # Déconnecter après la fin
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()

# Code déjà initialisé pour garder le bot actif via Flask
keep_alive()

# Lancer le bot Discord
bot.run(os.getenv('DISCORD_TOKEN'))

