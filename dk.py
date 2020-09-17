import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=['/'])
admin = ['724561925341446217','657773087571574784']

with open("dkpoint.json", "r", encoding='utf-8-sig').read() as f:
    point = json.loads(f)
@bot.event
async def on_ready():
    print(bot.user.name)


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
        import ast
        try: 
            fn_name = "_eval_expr" 
            cmd = cmd.strip("` ") 
            # add a layer of indentation 
            cmd = "\n".join(f" {i}" for i in cmd.splitlines()) 
            # wrap in async def body 
            body = f"async def {fn_name}():\n{cmd}" 
            parsed = ast.parse(body) 
            body = parsed.body[0].body 
            insert_returns(body) 
            env = { 'bot': ctx.bot, 'discord': discord, 'commands': commands, 'ctx': ctx, '__import__': __import__ } 
            exec(compile(parsed, filename="<ast>", mode="exec"), env) 
            result = (await eval(f"{fn_name}()", env)) 
            await ctx.send(result)
        except Exception as ex: 
            await ctx.send(f'오류발생!\n에러내용:{str(ex)}')

 
@bot.command()
