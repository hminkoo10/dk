import discord
from discord.ext import commands
import sys
import os
import json
import asyncio
import ast
import time

bot = commands.Bot(command_prefix=['/'])
admin = ['724561925341446217','657773087571574784']

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
        await user.send(f'이런.... {ctx.guild.name}서버에서 밴 됐어요...￦n사유는 {text}예요')
        await ctx.send(f"{user}님을 밴 했어요! \n 밴사유:{text}") 
    else: 
        await ctx.send("관리자 권한이 없어요!")
        
@bot.command()
async def 킥(ctx, user:discord.Member, *, text="킥"): 
    if ctx.author.guild_permissions.administrator: 
        await ctx.guild.ban(user, reason=text) 
        await user.send(f'이런.... {ctx.guild.name}서버에서 킥 됐어요...￦n사유는 {text}예요')
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
        await ctx.send(embed=discord.Embed(title='쿨타임이 안지났어요!',color=discord.Color.red()))
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
    await ctx.send(embed=discord.Embed(title=f'<:cheer1:756028272231579688> {ctx.author}님의 DC에 1DC를 추가했어요! <:cheer2:756028062424105010>',description ="1일 후에 명령어를 다시 사용하실 수 있어요!",color=discord.Color.gold()))
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
        await ctx.send(embed=discord.Embed(title=f"{user}님의 돈에서 {money1}원을 추가했어요!",color=discord.Color.green()))
@bot.command(name="dc빼기")
async def 관리자_돈뺴기(ctx, user: discord.Member, money1):
    if str(ctx.author.id) in admin:
        with open('dkpoint.json', 'r') as f:
            jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
            point = json.loads(jstring)
        point[str(user.id)] -= int(money1)
        with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(point, f, indent=2, ensure_ascii=False)
        await ctx.send(embed=discord.Embed(title=f"{user}님의 돈에서 {money1}원을 뺏어요!",color=discord.Color.green()))
@bot.command(name="dc설정")
async def 관리자_돈설정(ctx, user: discord.Member, money1):
    if str(ctx.author.id) in admin:
        with open('dkpoint.json', 'r') as f:
            jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
            point = json.loads(jstring)
        point[str(user.id)] = int(money1)
        with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(point, f, indent=2, ensure_ascii=False)
        await ctx.send(embed=discord.Embed(title=f"{user}님의 돈에서 {money1}원으로 설정했어요!",color=discord.Color.green()))
bot.run('NzU1OTk2MTUwMzc2NTYyNzI5.X2LaRw.Lgbz6en8cr1bq5zemTd6URNrCmM')
