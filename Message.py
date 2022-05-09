import imp
from turtle import color, title
import discord
from discord.ext import commands
from Storage import Storage

import time
import asyncio

async def channel_only(ctx):
    if Storage().checking.checking_server_channel(ctx.guild.id, ctx.channel.id):
        return True
    else:
        raise commands.CommandError("sender not in main server.")

class Message(commands.Cog):

    def __init__(self, bot, prefix):
        self.bot = bot
        self.prefix = prefix
        self.database = Storage().database
        self.checking = Storage().checking
        self.time_delay_delete = 3

    @commands.command()
    async def help(self, ctx):
        embed_data = discord.Embed(title="เมนูคำสั่ง:", description="คำสั่งใช้งานบอททั้งหมด", color=0xa13bcc)
        embed_data.add_field(name=self.prefix+"help", value="คำสั่ง เมนูบอท", inline=False)
        embed_data.add_field(name=self.prefix+"install", value="คำสั่ง ติดตั้งบอท", inline=False)
        embed_data.add_field(name=self.prefix+"uninstall", value="คำสั่ง ยกเลิกติดตั้งบอท", inline=False)
        embed_data.add_field(name=self.prefix+"condition", value="คำสั่ง เงื่อนไขบอท", inline=False)
        embed_data.add_field(name=self.prefix+"say (value)", value="คำสั่ง ให้บอทพิมตาม", inline=False)
        embed_data.add_field(name=self.prefix+"speed", value="คำสั่ง เช็คความเร็วบอท", inline=False)
        embed_data.add_field(name=self.prefix+"login_user", value="คำสั่ง ลงทะเบียนผู้ใช้", inline=False)
        embed_data.add_field(name=self.prefix+"logout_user", value="คำสั่ง ยกเลิกลงทะเบียนผู้ใช้", inline=False)
        embed_data.add_field(name=self.prefix+"info_list", value="คำสั่ง ข้อมูลที่บันทึกทั้งหมดของผู้ใช้", inline=False)
        embed_data.add_field(name=self.prefix+"keyword_list", value="คำสั่ง ข้อมูลของ 'keyword' ของผู้ใช้ทั้งหมด", inline=False)
        embed_data.add_field(name=self.prefix+"keyword_add (value_word)", value="คำสั่ง บันทึก 'keyword' ของผู้ใช้", inline=False)
        embed_data.add_field(name=self.prefix+"keyword_del (value_word)", value="คำสั่ง ลบบันทึก 'keyword' ของผู้ใช้", inline=False)
        embed_data.add_field(name=self.prefix+"title_list", value="คำสั่ง ข้อมูลของ 'title' ของผู้ใช้ทั้งหมด", inline=False)
        embed_data.add_field(name=self.prefix+"title_add (value_word);;(value_title)", value="คำสั่ง บันทึก 'title' ของผู้ใช้", inline=False)
        embed_data.add_field(name=self.prefix+"title_del (value_word);;(value_title)", value="คำสั่ง ลบบันทึก 'title' ของผู้ใช้", inline=False)
        embed_data.add_field(name=self.prefix+"data_list", value="คำสั่ง ข้อมูลของ 'data' ของผู้ใช้ทั้งหมด", inline=False)
        embed_data.add_field(name=self.prefix+"data_add (value_word);;(value_title);;(value_data)", value="คำสั่ง บันทึก 'data' ของผู้ใช้", inline=False)
        embed_data.add_field(name=self.prefix+"data_del (value_word);;(value_title);;(value_data)", value="คำสั่ง ลบบันทึก 'data' ของผู้ใช้", inline=False)
        reply = await ctx.send(embed=embed_data)
        await asyncio.sleep(self.time_delay_delete)
        await ctx.message.delete()

    @commands.command()
    async def install(self, ctx):
        if str(ctx.guild.id) in self.database["server"]:
            reply = await ctx.send(f"เคยลงทะเบียนกับเซิฟเวอร์ '{ctx.guild.name}' อยู่แล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            channel = await ctx.guild.create_text_channel(self.bot.user.name)
            self.database["server"][str(ctx.guild.id)] = {"channel": str(channel.id)}
            reply = await ctx.send(f"ลงทะเบียนสำหรับเซิฟเวอร์ {ctx.guild.name} ที่ห้อง '{channel}' เสร็จเรียบร้อยแล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()

    @commands.command()
    async def uninstall(self, ctx):
        if str(ctx.guild.id) not in self.database["server"]:
            reply = await ctx.send(f"ไม่เคยลงทะเบียนกับเซิฟเวอร์ '{ctx.guild.name}' อยู่แล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            del self.database["server"][str(ctx.guild.id)]
            reply = await ctx.send(f"ยกเลิกลงทะเบียนสำหรับเซิฟเวอร์ {ctx.guild.name} เรียบร้อยแล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def condition(self, ctx):
        reply = await ctx.send("เงื่อนไขการใช้งานคือการใช้งานโดยมี ';;' เป็นตัวเชื่อม")
        await asyncio.sleep(self.time_delay_delete)
        await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def test(self, ctx):
        reply = await ctx.send("!!")
        await asyncio.sleep(self.time_delay_delete)
        await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def say(self,ctx, *, text):
        reply = await ctx.send(text)
        await asyncio.sleep(self.time_delay_delete)
        await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def speed(self, ctx):
        start = time.time()
        reply = await ctx.send("กำลังทำสอบสปีด")
        end = time.time() - start
        await reply.edit(content="ความเร็วที่ได้ %s วินาที" %(end))
        await asyncio.sleep(self.time_delay_delete)
        await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def login_user(self, ctx):
        if self.checking.checking_user_id(ctx.author.id):
            reply = await ctx.send("คุณเคยลงชื่อ 'ผู้ใช้' ไปแล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            self.database["user"][str(ctx.author.id)] = {}
            reply = await ctx.send("ลงทะเบียนสำหรับ 'ผู้ใช้' งานเรียบร้อยแล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def logout_user(self, ctx):
        if not self.checking.checking_user_id(ctx.author.id):
            reply = await ctx.send("คุณไม่เคยลงชื่อ 'ผู้ใช้' อยู่แล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            del self.database["user"][str(ctx.author.id)]
            reply = await ctx.send("ลบทะเบียน 'ผู้ใช้' งานเรียบร้อยแล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def info_list(self, ctx):
        if not self.checking.checking_user_id(ctx.author.id):
            reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            if self.database["user"][str(ctx.author.id)] == {}:
                reply = await ctx.send("ไม่พบข้อมูลของ 'keyword' โปรดใส่ข้อมูลก่อน")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            else:
                statsu_keyword = False
                for word in self.database["user"][str(ctx.author.id)]:
                    if word == {}:
                        statsu_keyword = True
                if statsu_keyword:
                    reply = await ctx.send("ไม่พบข้อมูลของ 'keyword' โปรดใส่ข้อมูลก่อน")
                    await asyncio.sleep(self.time_delay_delete)
                    await ctx.message.delete()
                else:
                    statsu_title = False
                    for word in self.database["user"][str(ctx.author.id)]:
                        for title in self.database["user"][str(ctx.author.id)][str(word)]:
                            if title == {}:
                                statsu_title = True
                    if statsu_title:
                        reply = await ctx.send("ไม่พบข้อมูลของ 'title' โปรดใส่ข้อมูลก่อน")
                        await asyncio.sleep(self.time_delay_delete)
                        await ctx.message.delete()
                    else:
                        statsu_data = False
                        for word in self.database["user"][str(ctx.author.id)]:
                            for title in self.database["user"][str(ctx.author.id)][str(word)]:
                                for data in self.database["user"][str(ctx.author.id)][str(word)][str(title)]:
                                    if data == "":
                                        self.database["user"][str(ctx.author.id)][str(word)][str(title)][str(data)] = None
                        if statsu_data:
                            reply = await ctx.send("ไม่พบข้อมูลของ 'data' โปรดใส่ข้อมูลก่อน")
                            await asyncio.sleep(self.time_delay_delete)
                            await ctx.message.delete()
                        else:
                            for keyword in self.database["user"][str(ctx.author.id)]:
                                list_ = self.set_info_list(self.database["user"][str(ctx.author.id)][str(keyword)])
                                embed_dict = self.return_info_list(ctx.author.id, ctx.author.name, str(keyword), list_)
                                for len_dict in embed_dict:
                                    for embed_value in embed_dict[len_dict]:
                                        await ctx.send(embed=embed_value)
                            await asyncio.sleep(self.time_delay_delete)
                            await ctx.message.delete()

    def set_info_list(self, list, limit=24):
        _list = {}
        number = 1
        _list[str(number)] = {}
        for (index, title) in enumerate(list, start=1):
            if len(_list[str(number)]) >= limit:
                number += 1
                _list[str(number)] = {}
            _list[str(number)][str(title)] = list[str(title)]
        return _list

    def return_info_list(self, id, name, keyword, list_):
        embed_dict = {}
        number_list = len(list(list_))
        number_embed = 0
        if int(number_list) > 1:
            number_value = 0
            for path in list(list_):
                number_embed += 1
                embed_dict[str(number_embed)] = {}
                embed_data = discord.Embed(title=f"ข้อมูลของ '{name}' ทั้งหมด:", description="\u200B", color=0x57f542)
                embed_data.add_field(name=f"[ {str(keyword)} ]", value=f"หน้าที่ {str(path)}/{str(len(list_))}", inline=False)
                for title in list_[path]:
                    number_value += 1
                    embed_data.add_field(name=f"{number_value}. {str(title)}", value=f"{list_[path][str(title)]}")
                embed_dict[str(number_embed)][embed_data] = True
        else:
            number_embed += 1
            embed_dict[str(number_embed)] = {}
            embed_data = discord.Embed(title=f"ข้อมูลของ '{name}' ทั้งหมด:", description="\u200B", color=0x57f542)
            embed_data.add_field(name=f"[ {str(keyword)} ]", value="\u200B", inline=False)
            number_value = 0
            for title in list_[str(str(number_list))]:
                number_value += 1
                embed_data.add_field(name=f"{number_value}. {str(title)}", value=f"{list_[path][str(title)]}")
            embed_dict[str(number_embed)][embed_data] = True
        return embed_dict

    @commands.command()
    @commands.check(channel_only)
    async def keyword_list(self, ctx):
        if not self.checking.checking_user_id(ctx.author.id):
            reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            if self.database["user"][str(ctx.author.id)] == {}:
                reply = await ctx.send("ไม่พบข้อมูลของ 'keyword' โปรดใส่ข้อมูลก่อน")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
        
            else:
                list_ = self.set_list_keyword(self.database["user"][str(ctx.author.id)])
                embed_dict = self.return_list_keyword(ctx.author.id, list_)
                for len_dict in embed_dict:
                    for embed_value in embed_dict[len_dict]:
                        await ctx.send(embed=embed_value)
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()

    def set_list_keyword(self, list, limit=24):
        _list = {}
        number = 1
        _list[str(number)] = []
        for (index, keyword) in enumerate(list, start=1):
            if len(_list[str(number)]) >= limit:
                number += 1
                _list[str(number)] = []
            _list[str(number)].append(str(keyword))
        return _list

    def return_list_keyword(self, id, list_):
        embed_dict = {}
        number_list = len(list(list_))
        number_embed = 0
        if int(number_list) > 1:
            number_value = 0
            for path in list(list_):
                number_embed += 1
                embed_dict[str(number_embed)] = {}
                embed_data = discord.Embed(title="ข้อมูลของ 'keyword' ทั้งหมด:", description=f"หน้าที่ {str(path)}/{str(len(list_))}", color=0x57f542)
                for title in list_[path]:
                    number_value += 1
                    embed_data.add_field(name=f"{number_value}. {str(title)}", value="\u200B")
                embed_dict[str(number_embed)][embed_data] = True
        else:
            number_embed += 1
            embed_dict[str(number_embed)] = {}
            embed_data = discord.Embed(title="ข้อมูลของ 'keyword' ทั้งหมด:", description="\u200B", color=0x57f542)
            number_value = 0
            for title in list_[str(str(number_list))]:
                number_value += 1
                embed_data.add_field(name=f"{number_value}. {str(title)}", value="\u200B")
            embed_dict[str(number_embed)][embed_data] = True
        return embed_dict

    @commands.command()
    @commands.check(channel_only)
    async def keyword_add(self, ctx, *, text):
        value_userid, value_word = self.checking.checking_user_id_keyword(ctx.author.id, text)
        if value_userid == "user:False":
            reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        elif value_word == "word:True":
            reply = await ctx.send(f"คุณเคยลงคำว่า '{str(text)}' ใน keyword แล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            self.database["user"][str(ctx.author.id)][str(text)] = {}
            reply = await ctx.send(f"ทำการบันทึก '{str(text)}' ไว้ใน keyword เรียบร้อยแล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
    
    @commands.command()
    @commands.check(channel_only)
    async def keyword_del(self, ctx, *, text):
        value_userid, value_word = self.checking.checking_user_id_keyword(ctx.author.id, text)
        if value_userid == "user:False":
            reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        elif value_word == "word:False":
            reply = await ctx.send(f"คุณไม่ได้ลงคำว่า '{str(text)}' ใน keyword อยู่แล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            del self.database["user"][str(ctx.author.id)][str(text)]
            reply = await ctx.send(f"ทำการลบบันทึก '{str(text)}' ใน keyword เรียบร้อยแล้ว")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def title_list(self, ctx, text):
        value_userid, value_word = self.checking.checking_user_id_keyword(ctx.author.id, text)
        if value_userid == "user:False":
            reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        elif value_word == "word:False":
            reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(text)}' ใน keyword เลย")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            if self.database["user"][str(ctx.author.id)][str(text)] == {}:
                reply = await ctx.send("ไม่พบข้อมูลของ 'title' โปรดใส่ข้อมูลก่อน")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            else:
                list_ = self.set_list_title(self.database["user"][str(ctx.author.id)][str(text)])
                embed_dict = self.return_list_title(ctx.author.id, text , list_)
                for len_dict in embed_dict:
                    for embed_value in embed_dict[len_dict]:
                        await ctx.send(embed=embed_value)
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
    
    def set_list_title(self, list, limit=24):
        _list = {}
        number = 1
        _list[str(number)] = []
        for (index, title) in enumerate(list, start=1):
            if len(_list[str(number)]) >= limit:
                number += 1
                _list[str(number)] = []
            _list[str(number)].append(str(title))   
        return _list

    def return_list_title(self, id, keyword, list_):
        embed_dict = {}
        number_list = len(list(list_))
        number_embed = 0
        if int(number_list) > 1:
            number_value = 0
            for path in list(list_):
                number_embed += 1
                embed_dict[str(number_embed)] = {}
                embed_data = discord.Embed(title="ข้อมูลของ 'title' ทั้งหมด:", description="\u200B", color=0x57f542)
                embed_data.add_field(name=f"[ {str(keyword)} ]", value=f"หน้าที่ {str(path)}/{str(len(list_))}", inline=False)
                for title in list_[path]:
                    number_value += 1
                    embed_data.add_field(name=f"{number_value}. {str(title)}", value="\u200B")
                embed_dict[str(number_embed)][embed_data] = True
        else:
            number_embed += 1
            embed_dict[str(number_embed)] = {}
            embed_data = discord.Embed(title="ข้อมูลของ 'title' ทั้งหมด:", description="\u200B", color=0x57f542)
            number_value = 0
            embed_data.add_field(name=f"[ {str(keyword)} ]", value=f"หน้าที่ {str(path)}/{str(len(list_))}", inline=False)
            for title in list_[str(str(number_list))]:
                number_value += 1
                embed_data.add_field(name=f"{number_value}. {str(title)}", value="\u200B")
            embed_dict[str(number_embed)][embed_data] = True
        return embed_dict

    @commands.command()
    @commands.check(channel_only)
    async def title_add(self, ctx, *, text):
        if ";;" not in text:
            reply = await ctx.send("คำสั่งใช้งานผิด โปรดสั่งให้ครบเงื่อนไขด้วย")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
            reply = await ctx.send("ใช้คำสั่ง 'condition' เพื่อทำการตรวจสอบ")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            word = text.split(";;")[0]
            title = text.split(";;")[1]
            value_userid, value_word, value_titel = self.checking.checking_user_id_keyword_title(ctx.author.id, word, title)
            if value_userid == "user:False":
                reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_word == "word:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_titel == "title:True":
                reply = await ctx.send(f"คุณเคยลงคำว่า '{str(title)}' ใน title แล้ว")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            else:
                self.database["user"][str(ctx.author.id)][str(word)][str(title)] = ""
                reply = await ctx.send(f"ทำการบันทึก '{str(title)}' ไว้ใน {str(word)} เรียบร้อยแล้ว")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def title_del(self, ctx, *, text):
        if ";;" not in text:
            reply = await ctx.send("คำสั่งใช้งานผิด โปรดสั่งให้ครบเงื่อนไขด้วย")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
            reply = await ctx.send("ใช้คำสั่ง 'condition' เพื่อทำการตรวจสอบ")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            word = text.split(";;")[0]
            title = text.split(";;")[1]
            value_userid, value_word, value_titel = self.checking.checking_user_id_keyword_title(ctx.author.id, word, title)
            if value_userid == "user:False":
                reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_word == "word:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_titel == "title:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(title)}' ใน title อยู่แล้ว")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            else:
                del self.database["user"][str(ctx.author.id)][str(word)][str(title)]
                reply = await ctx.send(f"ทำการลบบันทึก '{str(title)}' ใน {str(word)} เรียบร้อยแล้ว")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def data_list(self, ctx, text):
        if ";;" not in text:
            reply = await ctx.send("คำสั่งใช้งานผิด โปรดสั่งให้ครบเงื่อนไขด้วย")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
            reply = await ctx.send("ใช้คำสั่ง 'condition' เพื่อทำการตรวจสอบ")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            word = text.split(";;")[0]
            title = text.split(";;")[1]
            value_userid, value_word, value_titel = self.checking.checking_user_id_keyword_title(ctx.author.id, word, title)
            if value_userid == "user:False":
                reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_word == "word:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_titel == "title:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(title)}' ใน title เลย")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            else:
                if self.database["user"][str(ctx.author.id)][str(word)][str(title)] == "":
                    reply = await ctx.send("ไม่พบข้อมูลของ 'data' โปรดใส่ข้อมูลก่อน")
                    await asyncio.sleep(self.time_delay_delete)
                    await ctx.message.delete()
                else:
                    data = self.return_list_data(ctx.author.id, word, title)
                    embed_data = discord.Embed(title="ข้อมูลของ 'data' ทั้งหมด:", description="\u200B", color=0x57f542)
                    embed_data.add_field(name=f"[ {str(word)};;{str(title)} ]", value="\u200B", inline=False)
                    embed_data.add_field(name=f"{str(data)}", value="\u200B")
                    reply = await ctx.send(embed=embed_data)
                    await asyncio.sleep(self.time_delay_delete)
                    await ctx.message.delete()

    def return_list_data(self, id, word, title):
        return self.database["user"][str(id)][str(word)][str(title)]

    @commands.command()
    @commands.check(channel_only)
    async def data_add(self, ctx, *, text):
        if ";;" not in text:
            reply = await ctx.send("คำสั่งใช้งานผิด โปรดสั่งให้ครบเงื่อนไขด้วย")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
            reply = await ctx.send("ใช้คำสั่ง 'condition' เพื่อทำการตรวจสอบ")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            word = text.split(";;")[0]
            title = text.split(";;")[1]
            data = text.split(";;")[2]
            value_userid, value_word, value_titel, value_data = self.checking.checking_user_id_keyword_title_data(ctx.author.id, word, title, data)
            if value_userid == "user:False":
                reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_word == "word:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_titel == "title:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(title)}' ใน title เลย")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_data == "data:True":
                reply = await ctx.send(f"คุณเคยลงคำว่า '{str(data)}' ใน data แล้ว")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            else:
                self.database["user"][str(ctx.author.id)][str(word)][str(title)] = str(data)
                reply = await ctx.send(f"ทำการบันทึก '{str(data)}' ไว้ใน {str(title)} เรียบร้อยแล้ว")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()

    @commands.command()
    @commands.check(channel_only)
    async def data_del(self, ctx, *, text):
        if ";;" not in text:
            reply = await ctx.send("คำสั่งใช้งานผิด โปรดสั่งให้ครบเงื่อนไขด้วย")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
            reply = await ctx.send("ใช้คำสั่ง 'condition' เพื่อทำการตรวจสอบ")
            await asyncio.sleep(self.time_delay_delete)
            await ctx.message.delete()
        else:
            word = text.split(";;")[0]
            title = text.split(";;")[1]
            data = text.split(";;")[2]
            value_userid, value_word, value_titel, value_data = self.checking.checking_user_id_keyword_title_data(ctx.author.id, word, title, data)
            if value_userid == "user:False":
                reply = await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_word == "word:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_titel == "title:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(title)}' ใน title เลย")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            elif value_data == "data:False":
                reply = await ctx.send(f"คุณไม่เคยลงคำว่า '{str(title)}' ใน data อยู่แล้ว")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()
            else:
                self.database["user"][str(ctx.author.id)][str(word)][str(title)] = "None"
                reply = await ctx.send(f"ทำการลบบันทึก '{str(title)}' ใน {str(word)} เรียบร้อยแล้ว")
                await asyncio.sleep(self.time_delay_delete)
                await ctx.message.delete()

def setup(bot, prefix):
    bot.add_cog(Message(bot, prefix))