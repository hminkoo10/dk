import discord
from discord.ext import commands
import sys
import os
import json
import asyncio
import ast
import time
from datetime import datetime

bot = commands.Bot(command_prefix=['/','케이야 '])
admin = ['724561925341446217','657773087571574784']
item = {'6':10,'5':20,'4':30,'3':35,'2':50,'1':100}
item2 = {'6':"🥉ㅣ브론즈 『Bronzes』",'5':"🥈ㅣ실버 『Silver』",'4':"🥇ㅣ골드 『Gold 』",'3':"🏅ㅣ플래티넘 『Platinum』",'2':"💎ㅣ다이아 『Diamond』",'1':"🏆ㅣ마스터 『Master』"}

f = open("dkpoint.json", "r", encoding='utf-8-sig').read()
point = json.loads(f)

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
@bot.event
async def on_ready():
    print(bot.user.name)
    await bot.change_presence(activity=discord.Streaming(name="DK Country의 관리를 돕고 있어요!",url="https://www.twitch.tv/dkcountry"))
        
        

@bot.command()
async def 밴(ctx, user:discord.Member, *, text="밴"): 
    if ctx.author.guild_permissions.administrator: 
        await ctx.guild.ban(user, reason=text) 
        await user.send(embed=discord.Embed(title=f'이런.... {ctx.guild.name}서버에서 밴 됐어요...\n사유는 {text}예요',color=discord.Color.red()))
        await ctx.send(f"{user}님을 밴 했어요! \n 밴사유:{text}") 
    else: 
        await ctx.send("관리자 권한이 없어요!")
        
@bot.command()
async def 킥(ctx, user:discord.Member, *, text="킥"): 
    if ctx.author.guild_permissions.administrator: 
        await ctx.guild.kick(user, reason=text) 
        await user.send(embed=discord.Embed(title=f'이런.... {ctx.guild.name}서버에서 킥 됐어요...\n사유는 {text}예요',color=discord.Color.red()))
        await ctx.send(f"{user}님을 킥 했어요! \n 킥사유:{text}") 
    else: 
        await ctx.send("관리자 권한이 없어요!")
@bot.command(name="eval")
async def eval_(ctx, *, cmd): 
    if str(ctx.author.id) in admin:
        try:
            fn_name = "_eval_expr"

            cmd = cmd.strip("` ")

    # add a layer of indentation
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
            body = f"async def {fn_name}():\n{cmd}"

            parsed = ast.parse(body)
            body = parsed.body[0].body

            insert_returns(body)

            env = {
                'bot': ctx.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = (await eval(f"{fn_name}()", env))
            await ctx.send(result)
        except Exception as ex:
            await ctx.send(f'오류발생!\n에러내용:{str(ex)}')
@bot.command()
async def eval_(ctx,*,cmd):
    if str(ctx.author.di) in admin:
        await ctx.send(eval(cmd))
@bot.command(name="dc받기")
async def 받기(ctx):
    f = open("dkpoint.json", "r", encoding='utf-8-sig').read()
    point = json.loads(f)
    f = open("dkcool.json", "r", encoding='utf-8-sig').read()
    cool = json.loads(f)
    try:
        abcd = int(time.time()) - int(cool[str(ctx.author.id)])
    except:
        abcd = 10000000000000
    if not int(abcd) >= int('86400'):
        await ctx.send(embed=discord.Embed(title='쿨타임이 안지났어요!',description=f'쿨타임이 {(int(time.time()) - cool[str(ctx.author.id)]) // 60}분 남았어요!',color=discord.Color.red()))
        return
    cool[str(ctx.author.id)] = int(time.time())
    try:
        point[str(ctx.author.id)] += 1
    except:
        point[str(ctx.author.id)] = 1
    with open(f"dkpoint.json", "w+", encoding='utf-8-sig') as f: 
        json_string = json.dump(point, f, indent=2, ensure_ascii=False)
    with open(f"dkcool.json", "w+", encoding='utf-8-sig') as f: 
        json_string = json.dump(cool, f, indent=2, ensure_ascii=False)
    await ctx.send(embed=discord.Embed(title=f'<:cheer1:753782753173962877> {ctx.author}님의 DC에 1DC를 추가했어요! <:cheer2:753782752045826140>',description ="1일 후에 명령어를 다시 사용하실 수 있어요!",color=discord.Color.gold()))
@bot.command()
async def 삭제(ctx, *, amount=999999999999999999999): 
    if ctx.author.guild_permissions.manage_messages: 
        await ctx.channel.purge(limit=amount) 
    else: 
        await ctx.channel.send('메시지 관리권한이 없어요!')
@bot.command(name="dc확인")
async def 확인(ctx,user:discord.Member="none"):
    if user == "none":
        user = ctx.author
    f = open("dkpoint.json", "r", encoding='utf-8-sig').read()
    point = json.loads(f)
    await ctx.send(embed=discord.Embed(title=f'지금 {user}님 DC는 {point[str(user.id)]}원이예요!',color=discord.Color.blue()))
@bot.command(name="dc지급")
async def 관리자_돈추가(ctx, user: discord.Member, money1):
    if str(ctx.author.id) in admin:
        with open('dkpoint.json', 'r') as f:
            jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
            point = json.loads(jstring)
        point[str(user.id)] += int(money1)
        with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(point, f, indent=2, ensure_ascii=False)
        await ctx.send(embed=discord.Embed(title=f"{user}님의 DC에서 {money1}원을 추가했어요!",color=discord.Color.green()))
@bot.command(name="dc빼기")
async def 관리자_돈뺴기(ctx, user: discord.Member, money1):
    if str(ctx.author.id) in admin:
        with open('dkpoint.json', 'r') as f:
            jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
            point = json.loads(jstring)
        point[str(user.id)] -= int(money1)
        with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(point, f, indent=2, ensure_ascii=False)
        await ctx.send(embed=discord.Embed(title=f"{user}님의 DC에서 {money1}원을 뺏어요!",color=discord.Color.green()))
@bot.command(name="dc설정")
async def 관리자_돈설정(ctx, user: discord.Member, money1):
    if str(ctx.author.id) in admin:
        with open('dkpoint.json', 'r') as f:
            jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
            point = json.loads(jstring)
        point[str(user.id)] = int(money1)
        with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(point, f, indent=2, ensure_ascii=False)
        await ctx.send(embed=discord.Embed(title=f"{user}님의 DC에서 {money1}원으로 설정했어요!",color=discord.Color.green()))
@bot.command()
async def 상점(ctx):
    embed = discord.Embed(title='상점',color=0x00ffae)
    embed = embed.add_field(name=":one: 마스터", value="<@&753036029249978400>:100DC", inline=True)
    embed = embed.add_field(name=":two: 다이아", value="<@&753030296236195860>:50DC", inline=False)
    embed = embed.add_field(name=":three: 플래티넘", value="<@&753036226138865714>:35DC", inline=True)
    embed = embed.add_field(name=":four: 골드", value="<@&753034992053125170>:30DC", inline=False)
    embed = embed.add_field(name=":five: 실버", value="<@&753035683198795778>:20DC", inline=True)
    embed = embed.add_field(name=":six: 브론즈", value="<@&753035721928867840>:10DC", inline=False)
    embed = embed.add_field(name=":seven: 니트로", value="니트로:500DC", inline=False)
    embed.set_footer(text="/구매 (아이템 번호) 로 아이템을 사보세요!", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def 구매(ctx,an):
    with open('dkpoint.json', 'r') as f:
        jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
        point = json.loads(jstring)
    if an == "7":
        if point[str(ctx.author.id)] <= 500:
            await ctx.send(embed=discord.Embed(title=f'{an}아이템을 사려면 DC가 더 필요해요!',color=discord.Color.red()))
            return
        else:
            point[str(ctx.author.id)] -= 500
            with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(point, f, indent=2, ensure_ascii=False)
            await bot.get_user(724561925341446217).send(f'{ctx.author}님이 니트로를 구매하셨어요!')
            await ctx.send(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',description="토리님한테 얘기해 구매를 이여가세요",color=discord.Color.green()))
            return
    if point[str(ctx.author.id)] >= item[str(an)]:
        role = discord.utils.get(ctx.guild.roles, name=f"{item2[str(an)]}")
        await ctx.author.add_roles(role)
        point[str(ctx.author.id)] -= int(item[str(an)])
        await ctx.send(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',color=discord.Color.green()))
    else:
        await ctx.send(embed=discord.Embed(title=f'{an}아이템을 사려면 DC가 더 필요해요!',color=discord.Color.red()))
    with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
        json_string = json.dump(point, f, indent=2, ensure_ascii=False)
@bot.listen()
async def on_message(message):
    if message.content.startswith("/공지"):

        await message.delete()

        if str(message.author.id) in admin:

            now = datetime.now()
            time = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 " + str(now.hour) + "시 " + str(now.minute) + "분 " + str(now.second) + "초"

            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name="DK Country 공지", value="""
            {}
            """.format(message.content[3: ]), inline=False)
            embed.set_footer(text=message.author.name + " - 인증됨 {}".format(time), icon_url=message.author.avatar_url)
            message = await bot.get_channel(752778923989008455).send(embed=embed)
            await asyncio.sleep(0.1)
            await message.add_reaction("✅")

        else:
            now = datetime.now()
            time = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 " + str(now.hour) + "시 " + str(now.minute) + "분 " + str(now.second) + "초"

            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="오류", value="""
            명령어를 실행할 수 없습니다.
            사유: 명령어를 실행할 수 있는 권한이 없습니다.
            """, inline=False)
            embed.set_footer(text=message.author.name + " - 인증되지 않음 {}".format(time), icon_url=message.author.avatar_url)

            message = await message.channel.send(embed=embed)
            await asyncio.sleep(0.1)
            await message.add_reaction("✅")
    if message.content.startswith("/봇공지"):

        await message.delete()

        if str(message.author.id) in admin:

            now = datetime.now()
            time = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 " + str(now.hour) + "시 " + str(now.minute) + "분 " + str(now.second) + "초"

            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name="DK Bot 봇공지", value="""
            {}
            """.format(message.content[3: ]), inline=False)
            embed.set_footer(text=message.author.name + " - 인증됨 {}".format(time), icon_url=message.author.avatar_url)
            message = await bot.get_channel(752780296109162566).send(embed=embed)
            await asyncio.sleep(0.1)
            await message.add_reaction("✅")
        else:
            now = datetime.now()
            time = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 " + str(now.hour) + "시 " + str(now.minute) + "분 " + str(now.second) + "초"

            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="오류", value="""
            명령어를 실행할 수 없습니다.
            사유: 명령어를 실행할 수 있는 권한이 없습니다.
            """, inline=False)
            embed.set_footer(text=message.author.name + " - 인증되지 않음 {}".format(time), icon_url=message.author.avatar_url)

            message = await message.channel.send(embed=embed)
            await asyncio.sleep(0.1)
            await message.add_reaction("✅")
@bot.command()
async def 핑(ctx):
    time1 = time.time()
    if (round(bot.latency*1000)) > 230:
            embed = discord.Embed(color=0x00ff00)
            embed = discord.Embed(title=":ping_pong:퐁!", description="""
            현재 디스코드 api핑: {0}ms
            상태: 매우 나쁨:no_entry:""".format(round(bot.latency*1000)), color=0xff0000)
    if (round(bot.latency*1000)) < 230:
            embed = discord.Embed(color=0x00ff00)
            embed = discord.Embed(title=":ping_pong:퐁!", description="""
            현재 디스코드 api핑: {0}ms
            상태: 양호:white_check_mark:""".format(round(bot.latency*1000)), color=0x00ff00)
    if (round(bot.latency*1000)) < 185:
            embed = discord.Embed(color=0x00ff00)
            embed = discord.Embed(title=":ping_pong:퐁!", description="""
            현재 디스코드 api핑: {0}ms
            상태: 매우 좋음:green_heart:""".format(round(bot.latency*1000)), color=0x0000ff)
    edit = await ctx.send(embed=discord.Embed(title='핑!', color=0x0ff00))
    time2 = time.time()
    time4 = float(time2) - float(time1)
    time5 = str(time4)
    time6 = time5[2:5]
    time7 = f'{time6}ms'
    embed.add_field(name="디스코드 메시지 핑", value=f'{time7}')
    await edit.edit(embed=embed)
bot.run('NzU1OTk2MTUwMzc2NTYyNzI5.X2LaRw.Lgbz6en8cr1bq5zemTd6URNrCmM')
