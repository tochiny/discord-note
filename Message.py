from turtle import title
import discord
from discord.ext import commands
from Storage import Storage

import time

class Message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = Storage().database
        self.checking = Storage().checking

    @commands.command()
    async def say(self,ctx, *, text):
        await ctx.send(text)
    
    @commands.command()
    async def speed(self, ctx):
        start = time.time()
        message = await ctx.send("กำลังทำสอบสปีด")
        end = time.time() - start
        await message.edit(content="ความเร็วที่ได้ %s วินาที" %(end))

    @commands.command()
    async def login_user(self, ctx):
        if self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณเคยลงชื่อ 'ผู้ใช้' ไปแล้ว")
        else:
            self.database["user"][str(ctx.author.id)] = {}
            await ctx.send("ลงทะเบียนสำหรับ 'ผู้ใช้' งานเรียบร้อยแล้ว")

    @commands.command()
    async def logout_user(self, ctx):
        if not self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณไม่เคยลงชื่อ 'ผู้ใช้' อยู่แล้ว")
        else:
            del self.database["user"][str(ctx.author.id)]
            await ctx.send("ลบทะเบียน 'ผู้ใช้' งานเรียบร้อยแล้ว")

    @commands.command()
    async def keyword_list(self, ctx):
        if not self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
        else:
            if self.database["user"][str(ctx.author.id)] == {}:
                await ctx.send("ไม่พบข้อมูลของ 'keyword' โปรดใส่ข้อมูลก่อน")
            else:
                await ctx.send(self.return_list_keyword(ctx.author.id))
    
    def return_list_keyword(self, id):
        text = "ข้อมูลของ 'keyword' ทั้งหมด:"
        for keyword in self.database["user"][str(id)]:
            text += f"\n- {str(keyword)}"
        return text

    @commands.command()
    async def keyword_add(self, ctx, *, text):
        if not self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
        else:
            if self.checking.checking_user_keyword(ctx.author.id, text):
                await ctx.send(f"คุณเคยลงคำว่า '{str(text)}' ใน keyword แล้ว")
            else:
                self.database["user"][str(ctx.author.id)][str(text)] = {}
                await ctx.send(f"ทำการบันทึก '{str(text)}' ไว้ใน keyword เรียบร้อยแล้ว")
    
    @commands.command()
    async def keyword_del(self, ctx, *, text):
        if not self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
        else:
            if not self.checking.checking_user_keyword(ctx.author.id, text):
                await ctx.send(f"คุณไม่ได้ลงคำว่า '{str(text)}' ใน keyword อยู่แล้ว")
            else:
                del self.database["user"][str(ctx.author.id)][str(text)]
                await ctx.send(f"ทำการลบบันทึก '{str(text)}' ใน keyword เรียบร้อยแล้ว")

    @commands.command()
    async def title_list(self, ctx, word):
        if not self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
        else:
            if not self.checking.checking_user_keyword(ctx.author.id, word):
                await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
            else:
                if self.database["user"][str(ctx.author.id)][str(word)] == {}:
                    await ctx.send("ไม่พบข้อมูลของ 'keyword' โปรดใส่ข้อมูลก่อน")
                else:
                    await ctx.send(self.return_list_title(ctx.author.id, word))
    
    def return_list_title(self, id, word):
        text = "ข้อมูลของ 'title' ทั้งหมด:"
        for keyword in self.database["user"][str(id)][str(word)]:
            text += f"\n- {str(keyword)}"
        return text

    @commands.command()
    async def title_add(self, ctx, *, text):
        if not self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
        else:
            if ";;" not in text:
                await ctx.send("คำสั่งใช้งานผิด ไม่พบเงื่อนไข")
            else:
                word = text.split(";;")[0]
                title = text.split(";;")[1]
                if not self.checking.checking_user_keyword(ctx.author.id, word):
                    await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
                else:
                    if self.checking.checking_user_title(ctx.author.id, word, title):
                        await ctx.send(f"คุณเคยลงคำว่า '{str(title)}' ใน title แล้ว")
                    else:
                        self.database["user"][str(ctx.author.id)][str(word)][str(title)] = ""
                        await ctx.send(f"ทำการบันทึก '{str(title)}' ไว้ใน {str(word)} เรียบร้อยแล้ว")

    @commands.command()
    async def title_del(self, ctx, *, text):
        if not self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
        else:
            if ";;" not in text:
                await ctx.send("คำสั่งใช้งานผิด ไม่พบเงื่อนไข")
            else:
                word = text.split(";;")[0]
                title = text.split(";;")[1]
                if not self.checking.checking_user_keyword(ctx.author.id, word):
                    await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
                else:
                    if not self.checking.checking_user_title(ctx.author.id, word, title):
                        await ctx.send(f"คุณไม่เคยลงคำว่า '{str(title)}' ใน title อยู่แล้ว")
                    else:
                        del self.database["user"][str(ctx.author.id)][str(word)][str(title)]
                        await ctx.send(f"ทำการลบบันทึก '{str(title)}' ใน {str(word)} เรียบร้อยแล้ว")

    @commands.command()
    async def data_list(self, ctx, text):
        if not self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
        else:
            if ";;" not in text:
                await ctx.send("คำสั่งใช้งานผิด ไม่พบเงื่อนไข")
            else:
                word = text.split(";;")[0]
                title = text.split(";;")[1]
                if not self.checking.checking_user_keyword(ctx.author.id, word):
                    await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
                else:
                    if not self.checking.checking_user_title(ctx.author.id, word, title):
                        await ctx.send(f"คุณไม่เคยลงคำว่า '{str(title)}' ใน title เลย")
                    else:
                        if self.database["user"][str(ctx.author.id)][str(word)][str(title)] == "":
                            await ctx.send("ไม่พบข้อมูลของ 'data' โปรดใส่ข้อมูลก่อน")
                        else:
                            await ctx.send(self.return_list_data(ctx.author.id, word, title))

    def return_list_data(self, id, word, title):
        return self.database["user"][str(id)][str(word)][str(title)]

    @commands.command()
    async def data_add(self, ctx, *, text):
        if not self.checking.checking_user_info(ctx.author.id):
            await ctx.send("คุณยังไม่เคยลงชื่อ 'ผู้ใช้' โปรดลงชื่อผู้ใช้ก่อน")
        else:
            if ";;" not in text:
                await ctx.send("คำสั่งใช้งานผิด ไม่พบเงื่อนไข")
            else:
                word = text.split(";;")[0]
                title = text.split(";;")[1]
                data = text.split(";;")[2]
                if not self.checking.checking_user_keyword(ctx.author.id, word):
                    await ctx.send(f"คุณไม่เคยลงคำว่า '{str(word)}' ใน keyword เลย")
                else:
                    if not self.checking.checking_user_title(ctx.author.id, word, title):
                        await ctx.send(f"คุณไม่เคยลงคำว่า '{str(title)}' ใน title เลย")
                    else:
                        if self.checking.checking_user_data(ctx.author.id, word, title, data):
                            await ctx.send(f"คุณเคยลงคำว่า '{str(data)}' ใน data แล้ว")
                        else:
                            self.database["user"][str(ctx.author.id)][str(word)][str(title)] = str(data)
                            await ctx.send(f"ทำการบันทึก '{str(data)}' ไว้ใน {str(title)} เรียบร้อยแล้ว")

def setup(bot):
    bot.add_cog(Message(bot))