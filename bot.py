# Créé par la Team CF Games avec l'aide de GPT.
# Sous license CC-BY, voir le fichier LICENSE
# (c) Team CF Games 2025
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import asyncio
from discord import ui
from discord import app_commands
import wikipediaapi
from discord.app_commands import MissingPermissions
from discord.ui import View, Button
from server import keep_alive

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

    salutations = ["salut", "bonjour", "coucou", "hi", "hola", "hello", "yo", "bonsoir", "cc", "slt", "bjr"]
    depart = ["au revoir", "bye", "a+", "ciao", "see ya", "à bientôt", "adieu", "bonne nuit", "bn", "tchao"]
    faim = ["j'ai faim", "faim", "j’ai la dalle", "je crève de faim", "trop faim", "je crève la dalle"]
    quoifeur = ["quoi"]
    cava = ["ca va?", "cv?", "ça va ?", "bien ou bien"]


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
@bot.command(name="dire")
@commands.has_permissions(administrator=True)  
async def dire(ctx, *, message: str):
    await ctx.send(message)  

# Gestion des erreurs pour la commande /dire si l'utilisateur n'est pas admin
@dire.error
async def dire_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Désolé, vous devez être un administrateur pour utiliser cette commande.")

# Fonction pour obtenir une blague de l'API (format JSON)
def get_joke():
    url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous?lang=fr&blacklistFlags=nsfw,religious,racist,sexist,explicit"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            joke_data = response.json()  # Essaie d'analyser la réponse JSON
            print("Réponse JSON : ", joke_data)  # Affiche la réponse brute pour vérifier son contenu

            # Vérifie si la blague est de type "single" ou "twopart"
            if joke_data.get('type') == 'single':
                return joke_data.get('joke', 'Désolé, je n\'ai pas trouvé de blague.')
            elif joke_data.get('type') == 'twopart':
                setup = joke_data.get('setup')
                delivery = joke_data.get('delivery')
                return f"{setup}\n{delivery}"  # Formatte la blague à deux parties
            else:
                return "Désolé, je n'ai pas trouvé de blague pour le moment."
        except Exception as e:
            print("Erreur lors de l'analyse JSON:", e)  # Affiche l'erreur en cas de problème d'analyse
            return "Désolé, je n'ai pas pu traiter la réponse de l'API."
    else:
        print(f"Erreur API: {response.status_code}")  # Affiche un message d'erreur si la réponse n'est pas correcte
        return "Désolé, je n'ai pas trouvé de blague pour le moment."

# Commande slash !blague
@bot.tree.command(name="blague", description="Obtiens une blague !")
async def blague(interaction: discord.Interaction):
    joke = get_joke()  # Récupère la blague
    embed = discord.Embed(
        title="Blague du jour",
        description=joke,
        color=discord.Color.blue()
    )
    embed.set_footer(text="Via JokeAPI | Commande : /blague")
    
    # Envoie la blague sous forme d'embed
    await interaction.response.send_message(embed=embed)

# Code déjà initialisé pour garder le bot actif via Flask
keep_alive()

# Lancer le bot Discord
bot.run(os.getenv('DISCORD_TOKEN'))

