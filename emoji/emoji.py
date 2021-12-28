

import discord
import os
from discord.ext import commands
from discord.ext import commands
import aiohttp
from io import BytesIO
import requests



class EmojiPlugin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(aliases=["addemo","emoadd","emojiadd"], help="Adds an emoji to the server.Emoji url can be .jpg/.png/.gif")
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(self, ctx, url: str, *, name,emoji:discord.Emoji):
            guild = ctx.guild
            if ctx.author.guild_permissions.manage_emojis:
                async with aiohttp.ClientSession() as ses:
                    async with ses.get(url) as r:

                        try:
                            img_or_gif = BytesIO(await r.read())
                            b_value = img_or_gif.getvalue()
                            if r.status in range(200, 299):
                                emoji = await guild.create_custom_emoji(
                                    image=b_value, name=name
                                )
                                if bool(emoji.animated)==True:
                                    em = discord.Embed(colour=discord.Color.green(),
                                        description=f"<a:{name}:{emoji.id}> Emoji was added with name {name }"
                                    )
                                else:    
                                    em = discord.Embed(colour=discord.Color.green(),
                                        description=f"<:{name}:{emoji.id}> Emoji was added with name {name }"
                                    )
                                await ctx.send(embed=em)
                                await ses.close()
                            else:
                                em = discord.Embed(
                                    description=f"Error when making request | {r.status} response.",color=discord.Color.red()
                                )
                                await ctx.send(embed=em)
                                await ses.close()

                        except discord.HTTPException:
                            em = discord.Embed(
                                title="Emoji Error", description="File size is too big!",colour=discord.Color.red()
                            )
                            await ctx.send(embed=em)

    @commands.command(
        alisas=["remove","delemoji"], help="Removes the specified emoji from the server."
    )
    @commands.has_permissions(manage_emojis=True)    
    async def emojiremove(self, ctx, emoji: discord.Emoji):
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            em = discord.Embed(color=discord.Color.green(),
                description=f"Successfully deleted {emoji}",
                colour=discord.Color.greyple()
            )
            await ctx.send(embed=em)
            await emoji.delete()


    @commands.command(name="steal", help="Steals an emoji form a server")
    @commands.has_permissions(manage_emojis=True)    
    async def steal(self, ctx, emoji: discord.PartialEmoji, *, emojiname=None):

        if ctx.author.guild_permissions.manage_emojis:

            if emojiname == None:
                emojiname = emoji.name
            else:
                text = emojiname.replace(" ", "_")

            r = requests.get(emoji.url, allow_redirects=True)

            if emoji.animated == True:
                open("emoji.gif", "wb").write(r.content)
                with open("emoji.gif", "rb") as f:
                    z = await ctx.guild.create_custom_emoji(name=emojiname, image=f.read())
                os.remove("emoji.gif")

            else:
                open("emoji.png", "wb").write(r.content)
                with open("emoji.png", "rb") as f:
                    z = await ctx.guild.create_custom_emoji(name=emojiname, image=f.read())
                os.remove("emoji.png")

            embed = discord.Embed(
                description=f"""Succesfully Stolen {z} as "{emojiname}" """,
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(EmojiPlugin(bot))
