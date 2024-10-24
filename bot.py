import discord
from discord import app_commands
from transformers import pipeline
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class LLMBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
        print("モデルを読み込んでいます...")
        self.generator = pipeline(
            "text-generation",
            model="rinna/japanese-gpt-neox-small",
            device=-1
        )
        print("モデルの読み込みが完了しました")

    async def setup_hook(self):
        await self.tree.sync()

client = LLMBot()

@client.tree.command(name="chat", description="AIとチャットする")
async def chat(interaction: discord.Interaction, メッセージ: str):
    await interaction.response.defer()
    
    try:
        response = client.generator(
            メッセージ,
            max_length=100,
            num_return_sequences=1,
            temperature=0.7
        )[0]['generated_text']
        
        embed = discord.Embed(
            title="AIの回答",
            description=response,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"エラーが発生しました: {str(e)}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)