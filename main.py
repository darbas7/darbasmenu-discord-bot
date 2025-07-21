import discord
from discord.ext import commands
import asyncio
import os
from datetime import datetime
import json

# Configurações do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Canal onde serão postadas as atualizações (você deve definir o ID do canal)
UPDATE_CHANNEL_ID = None  # Substitua pelo ID do seu canal

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')
    print(f'Bot ID: {bot.user.id}')
    print('------')

@bot.command(name='setar_canal')
@commands.has_permissions(administrator=True)
async def set_update_channel(ctx):
    """Define o canal atual como canal de atualizações"""
    global UPDATE_CHANNEL_ID
    UPDATE_CHANNEL_ID = ctx.channel.id
    
    embed = discord.Embed(
        title="✅ Canal Configurado", 
        description=f"Este canal será usado para atualizações do DarbasMenu!",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@bot.command(name='atualização', aliases=['update', 'att'])
@commands.has_permissions(administrator=True)
async def post_update(ctx, *, mensagem):
    """Posta uma atualização do DarbasMenu
    Uso: !atualização <mensagem>
    """
    if UPDATE_CHANNEL_ID is None:
        await ctx.send("❌ Canal de atualizações não configurado! Use `!setar_canal` primeiro.")
        return
    
    channel = bot.get_channel(UPDATE_CHANNEL_ID)
    if channel is None:
        await ctx.send("❌ Canal de atualizações não encontrado!")
        return
    
    # Cria um embed bonito para a atualização
    embed = discord.Embed(
        title="🍽️ DarbasMenu - Nova Atualização!",
        description=mensagem,
        color=0x3498db,
        timestamp=datetime.now()
    )
    
    embed.set_footer(text="DarbasMenu App", icon_url="https://cdn.discordapp.com/attachments/placeholder/logo.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/placeholder/app_icon.png")
    
    # Adiciona alguns campos úteis
    embed.add_field(name="📱 Versão", value="v1.0.0", inline=True)
    embed.add_field(name="📅 Data", value=datetime.now().strftime("%d/%m/%Y"), inline=True)
    
    await channel.send(embed=embed)
    
    # Confirma no canal onde foi usado o comando
    if ctx.channel.id != UPDATE_CHANNEL_ID:
        await ctx.send("✅ Atualização postada com sucesso!")

@bot.command(name='changelog')
@commands.has_permissions(administrator=True)
async def post_changelog(ctx, versao, *, mudancas):
    """Posta um changelog detalhado
    Uso: !changelog v1.2.0 - Correção de bugs\n- Nova funcionalidade\n- Melhorias
    """
    if UPDATE_CHANNEL_ID is None:
        await ctx.send("❌ Canal de atualizações não configurado! Use `!setar_canal` primeiro.")
        return
    
    channel = bot.get_channel(UPDATE_CHANNEL_ID)
    if channel is None:
        await ctx.send("❌ Canal de atualizações não encontrado!")
        return
    
    embed = discord.Embed(
        title=f"📋 DarbasMenu - Changelog {versao}",
        description="**O que há de novo:**",
        color=0xe74c3c,
        timestamp=datetime.now()
    )
    
    # Processa as mudanças em linhas
    mudancas_formatadas = ""
    for linha in mudancas.split('\n'):
        linha = linha.strip()
        if linha:
            if not linha.startswith('-'):
                linha = f"• {linha}"
            mudancas_formatadas += f"{linha}\n"
    
    embed.add_field(name="🔄 Mudanças:", value=mudancas_formatadas or "Nenhuma mudança especificada", inline=False)
    embed.add_field(name="📱 Versão", value=versao, inline=True)
    embed.add_field(name="📅 Lançamento", value=datetime.now().strftime("%d/%m/%Y às %H:%M"), inline=True)
    
    embed.set_footer(text="DarbasMenu App • Obrigado por usar nosso app!", 
                    icon_url="https://cdn.discordapp.com/attachments/placeholder/logo.png")
    
    await channel.send(embed=embed)
    
    if ctx.channel.id != UPDATE_CHANNEL_ID:
        await ctx.send("✅ Changelog postado com sucesso!")

@bot.command(name='anuncio')
@commands.has_permissions(administrator=True)
async def post_announcement(ctx, *, mensagem):
    """Posta um anúncio importante com destaque
    Uso: !anuncio <mensagem>
    """
    if UPDATE_CHANNEL_ID is None:
        await ctx.send("❌ Canal de atualizações não configurado! Use `!setar_canal` primeiro.")
        return
    
    channel = bot.get_channel(UPDATE_CHANNEL_ID)
    if channel is None:
        await ctx.send("❌ Canal de atualizações não encontrado!")
        return
    
    embed = discord.Embed(
        title="📢 ANÚNCIO IMPORTANTE - DarbasMenu",
        description=mensagem,
        color=0xf39c12,
        timestamp=datetime.now()
    )
    
    embed.set_footer(text="DarbasMenu Team")
    
    # Posta com @everyone (cuidado com spam!)
    await channel.send("@everyone", embed=embed)
    
    if ctx.channel.id != UPDATE_CHANNEL_ID:
        await ctx.send("✅ Anúncio postado com sucesso!")

@bot.command(name='status')
async def bot_status(ctx):
    """Mostra informações do bot"""
    embed = discord.Embed(
        title="🤖 Status do Bot",
        color=0x9b59b6
    )
    
    embed.add_field(name="📊 Servidores", value=len(bot.guilds), inline=True)
    embed.add_field(name="👥 Usuários", value=len(set(bot.get_all_members())), inline=True)
    embed.add_field(name="📡 Latência", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    if UPDATE_CHANNEL_ID:
        channel = bot.get_channel(UPDATE_CHANNEL_ID)
        embed.add_field(name="📺 Canal de Updates", 
                       value=f"#{channel.name}" if channel else "Canal não encontrado", 
                       inline=True)
    else:
        embed.add_field(name="📺 Canal de Updates", value="Não configurado", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='help_darbasmenu')
async def help_command(ctx):
    """Mostra todos os comandos disponíveis"""
    embed = discord.Embed(
        title="🛠️ Comandos do DarbasMenu Bot",
        description="Lista de comandos disponíveis:",
        color=0x3498db
    )
    
    commands_list = [
        ("!setar_canal", "Define o canal atual para postar atualizações (Admin)"),
        ("!atualização <mensagem>", "Posta uma atualização simples (Admin)"),
        ("!changelog <versão> <mudanças>", "Posta um changelog detalhado (Admin)"),
        ("!anuncio <mensagem>", "Posta um anúncio importante (Admin)"),
        ("!status", "Mostra informações do bot"),
        ("!help_darbasmenu", "Mostra esta mensagem de ajuda")
    ]
    
    for cmd, desc in commands_list:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    await ctx.send(embed=embed)

# Tratamento de erros
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Argumento obrigatório não fornecido! Use `!help_darbasmenu` para ver como usar.")
    elif isinstance(error, commands.CommandNotFound):
        return  # Ignora comandos que não existem
    else:
        print(f"Erro não tratado: {error}")

# Inicia o bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN') or 'MTM5NjkxODc0MTE4MjMyMDc3Mg.GmAjn1.CXT7rxOUPt01pF-YDhPSPBphLNxXNcLdRFrSf0'
    bot.run(token)