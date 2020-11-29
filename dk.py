import discord
from discord.ext import commands
import sys
import os
import json
import asyncio
import ast
import time
from datetime import datetime
from youtube_search import YoutubeSearch
from discord.utils import get
import youtube_dl
import os



volumes = 25
pf = []
INTENTS = discord.Intents.all()
bot = commands.Bot(command_prefix=['/','케이야 '],intents=INTENTS)
admin = ['724561925341446217','657773087571574784','712290125505363980']
item = {'6':10,'5':20,'4':30,'3':35,'2':50,'1':100}
item2 = {'6':"🥉ㅣ브론즈 『Bronzes』",'5':"🥈ㅣ실버 『Silver』",'4':"🥇ㅣ골드 『Gold 』",'3':"🏅ㅣ플래티넘 『Platinum』",'2':"💎ㅣ다이아 『Diamond』",'1':"🏆ㅣ마스터 『Master』"}
jstring = open("warn2.json", "r", encoding='utf-8-sig').read()
warn = json.loads(jstring)
jstring = open("warnlimit2.json", "r", encoding='utf-8-sig').read()
warnlimit = json.loads(jstring)
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
def ifadmin(ids):
    if str(ids) in admin:
        return True
    else:
        False
@bot.event
async def on_ready():
    print(bot.user.name)
    await bot.change_presence(activity=discord.Streaming(name="DK Country의 관리를 돕고 있어요!",url="https://www.twitch.tv/dkcountry"))
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.id = data.get('id')
        self.uploader = data.get('uploader')
        self.uploaderid = data.get('uploader_id')
        self.filename = ytdl.prepare_filename(data)
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.command(pass_context=True, aliases=['j', 'join'])
async def 들어와(msg,*,channel:discord.VoiceChannel = None):
    if channel == None:
        channel = msg.author.voice.channel
    if msg.voice_client is not None:
        await msg.voice_client.move_to(channel)
    else:
        await channel.connect()
@bot.command(pass_context=True, aliases=['v', 'vol'])
async def 볼륨(ctx, vol: int):
    try:
        global volumes
        if ctx.voice_client is None:
            return await ctx.send("봇이 음성채널에 있지 않습니다.")
        if vol < 0 and vol > 200:
            await ctx.send(f"{ctx.author.mention}에 의해 불륨이 변경되었습니다.")
        print(vol / 100)
        ctx.voice_client.source.volume = vol / 100
        await ctx.send(f"볼륨: {vol}%")
        volumes = vol
    except Exception as e:
        print(f'error\n{e}')
@bot.command(pass_context=True, aliases=['s', 'sto'])
async def 중지(ctx):
    global volumes
    voice = get(bot.voice_clients, guild=ctx.guild)
    volumes = 15

    if voice and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        os.remove(player.filename)
        await ctx.send("완료!")
    else:
        await ctx.send("음악이 재생돼고있지 않습니다.")
@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def 일시정지(ctx):
    try:
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("노래가 일시정지 되었습니다.")
        else:
            await ctx.send("일시정지할 노래가 없습니다.")
    except Exception as e:
        print('error')
@bot.command(pass_context=True, aliases=['r', 'res'])
async def 다시재생(ctx):
    try:
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("재생 시작!")
        else:
            print("ERROR")
            await ctx.send("ERROR")
    except Exception as e:
        print('error')
@bot.command(pass_context=True, aliases=['l', 'lea'])
async def 나가(msg):
    await msg.voice_client.disconnect()

@bot.command(pass_context=True, aliases=['p', 'pla']) #재생
async def 재생(ctx, *, url):
    try:
        await ctx.voice_client.disconnect()
    except:
        pass
    channel = ctx.author.voice.channel
    try:
        ss = await channel.connect()
    except:
        pass
    try:
        os.remove(pf[0])
        pf.remove(pf[0])
    except:
        pass
    async with ctx.typing():
        player = await YTDLSource.from_url(url)
        print(player.id)
        print(player.title)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
        ctx.voice_client.source.volume = volumes / 100
    pf.append(player.filename)
    embedt = discord.Embed(title=f'{player.title}재생중!!',color=0x00c8ff)
    embedt.set_image(url=f'https://i.ytimg.com/vi/{player.id}/hqdefault.jpg')
    embedt.set_footer(text='다른노래가 나올 경우엔 다시 재생 해 주세요')
    await ctx.send(embed=embedt)
   
        

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
async def eval__(ctx, *, cmd): 
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
@bot.command(name="코받기",aliases=['돈받기'])
async def 받기(ctx):
    import datetime
    f = open("dkpoint.json", "r", encoding='utf-8-sig').read()
    point = json.loads(f)
    f = open("dkcool.json", "r", encoding='utf-8-sig').read()
    cool = json.loads(f)
    #str(datetime.date.today())
    try:
        if cool[str(ctx.author.id)] != str(datetime.date.today()):
            test = True
        else:
            test = False
    except:
        point[str(ctx.author.id)] = 0
        test = True
    if test == False:
        await ctx.send(embed=discord.Embed(title=f'이미 오늘({str(datetime.date.today())})코인을 받으셨습니다',color=discord.Color.red()))
        return
    elif test == True:
        cool[str(ctx.author.id)] = str(datetime.date.today())
        point[str(ctx.author.id)] += 1
        print('테스트')
    nexttime = str(int(str(datetime.date.today()).split('-')[1])) + '월 ' + str(int(str(datetime.date.today()).split('-')[2]) + 1) + '일'
    if nexttime == 32:
        nexttime = str(int(str(datetime.date.today()).split('-')[1])) + '월 ' + '1일'
    with open(f"dkpoint.json", "w+", encoding='utf-8-sig') as f: 
        json_string = json.dump(point, f, indent=2, ensure_ascii=False)
    with open(f"dkcool.json", "w+", encoding='utf-8-sig') as f: 
        json_string = json.dump(cool, f, indent=2, ensure_ascii=False)
    await ctx.send(embed=discord.Embed(title=f'<a:tada_gif:772304409941508107> {ctx.author}님의 코에 1코인추가했어요! <a:tada_gif:772304409941508107>',description =f"{nexttime}에 명령어를 다시 사용하실 수 있어요!",color=discord.Color.green()))
@bot.command()
async def 삭제(ctx, *, amount=999999999999999999999): 
    if ctx.author.guild_permissions.manage_messages: 
        await ctx.channel.purge(limit=amount) 
    else: 
        await ctx.channel.send('메시지 관리권한이 없어요!')
@bot.command(name="코인확인")
async def 확인(ctx,user:discord.Member="none"):
    if user == "none":
        user = ctx.author
    f = open("dkpoint.json", "r", encoding='utf-8-sig').read()
    point = json.loads(f)
    await ctx.send(embed=discord.Embed(title=f'지금 {user}님 코인 {point[str(user.id)]}원이예요!',color=discord.Color.blue()))
@bot.command(name="코인지급")
async def 관리자_돈추가(ctx, user: discord.Member, money1):
    if str(ctx.author.id) in admin:
        with open('dkpoint.json', 'r') as f:
            jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
            point = json.loads(jstring)
        point[str(user.id)] += int(money1)
        with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(point, f, indent=2, ensure_ascii=False)
        await ctx.send(embed=discord.Embed(title=f"{user}님의 코에서 {money1}원을 추가했어요!",color=discord.Color.green()))
@bot.command(name="코빼기")
async def 관리자_돈뺴기(ctx, user: discord.Member, money1):
    if str(ctx.author.id) in admin:
        with open('dkpoint.json', 'r') as f:
            jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
            point = json.loads(jstring)
        point[str(user.id)] -= int(money1)
        with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(point, f, indent=2, ensure_ascii=False)
        await ctx.send(embed=discord.Embed(title=f"{user}님의 코에서 {money1}원을 뺏어요!",color=discord.Color.green()))
@bot.command(name="코설정")
async def 관리자_돈설정(ctx, user: discord.Member, money1):
    if str(ctx.author.id) in admin:
        with open('dkpoint.json', 'r') as f:
            jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
            point = json.loads(jstring)
        point[str(user.id)] = int(money1)
        with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(point, f, indent=2, ensure_ascii=False)
        await ctx.send(embed=discord.Embed(title=f"{user}님의 코에서 {money1}원으로 설정했어요!",color=discord.Color.green()))
@bot.command()
async def 상점(ctx):
    jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
    point = json.loads(jstring)
    embed = discord.Embed(title='상점',color=0x00ffae)
    embed = embed.add_field(name=":one: 마스터", value="<@&765706176725385226>:100코", inline=True)
    embed = embed.add_field(name=":two: 다이아", value="<@&765706625158742016>:50코인", inline=False)
    embed = embed.add_field(name=":three: 플래티넘", value="<@&765706819049488474>:35코인", inline=True)
    embed = embed.add_field(name=":four: 골드", value="<@&765706973962043392>:30코인", inline=False)
    embed = embed.add_field(name=":five: 실버", value="<@&765707199967133696>:20코인", inline=True)
    embed = embed.add_field(name=":six: 브론즈", value="<@&765707200299532309>:10코", inline=False)
    embed = embed.add_field(name=":seven: 니트로", value="니트로:500코", inline=False)
    embed.set_footer(text="아래 이모지 반응으로 구매해보세요!", icon_url=ctx.author.avatar_url)
    t = await ctx.send(embed=embed)
    await t.add_reaction(u'\U00000031\U0000FE0F\U000020E3')
    await t.add_reaction(u'\U00000032\U0000FE0F\U000020E3')
    await t.add_reaction(u'\U00000033\U0000FE0F\U000020E3')
    await t.add_reaction(u'\U00000034\U0000FE0F\U000020E3')
    await t.add_reaction(u'\U00000035\U0000FE0F\U000020E3')
    await t.add_reaction(u'\U00000036\U0000FE0F\U000020E3')
    await t.add_reaction(u'\U00000037\U0000FE0F\U000020E3')
    await asyncio.sleep(1)
    def check(reaction,user):
        return user.id == ctx.author.id
    await asyncio.sleep(1)
    try:
        reaction = await bot.wait_for('reaction_add',timeout=25,check=check)
    except asyncio.TimeoutError:
        return
    else:
        pass
    a = f'{reaction[0]}'
    if str(a) == '1️⃣':
        role = discord.utils.get(ctx.guild.roles, name=item2['1'])
        if role in ctx.author.roles:
            await ctx.send('이미 마스터를 구매하셨습니다')
        else:
            role = discord.utils.get(ctx.guild.roles, name=item2['2'])
            if not role in ctx.author.roles:
                await ctx.send(embed=discord.Embed(title='그 전 엠블럼을 구매해야 이 엠블럼 구매가 가능합니다',color=discord.Color.red()))
                return
            if point[str(ctx.author.id)] >= item[str('1')]:
                role = discord.utils.get(ctx.guild.roles, name=f"{item2[str('1')]}")
                await ctx.author.add_roles(role)
                point[str(ctx.author.id)] -= int(item[str('1')])
                await t.edit(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(title=f"{item2[str('1')]}아이템을 사려면 코인이 더 필요해요!",color=discord.Color.red()))
            with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(point, f, indent=2, ensure_ascii=False)
            return
    elif str(a) == '2️⃣':
        role = discord.utils.get(ctx.guild.roles, name=item2['2'])
        if role in ctx.author.roles:
            await ctx.send('이미 다이아를 구매하셨습니다')
        else:
            role = discord.utils.get(ctx.guild.roles, name=item2['3'])
            if not role in ctx.author.roles:
                await ctx.send(embed=discord.Embed(title='그 전 엠블럼을 구매해야 이 엠블럼 구매가 가능합니다',color=discord.Color.red()))
                return
            if point[str(ctx.author.id)] >= item[str('2')]:
                role = discord.utils.get(ctx.guild.roles, name=f"{item2[str('2')]}")
                await ctx.author.add_roles(role)
                point[str(ctx.author.id)] -= int(item[str('2')])
                await t.edit(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(title=f"{item2[str('2')]}아이템을 사려면 코인 더 필요해요!",color=discord.Color.red()))
            with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(point, f, indent=2, ensure_ascii=False)
            return
    elif str(a) == '3️⃣':
        role = discord.utils.get(ctx.guild.roles, name=item2['3'])
        if role in ctx.author.roles:
            await ctx.send('이미 플래티넘를 구매하셨습니다')
        else:
            role = discord.utils.get(ctx.guild.roles, name=item2['4'])
            if not role in ctx.author.roles:
                await ctx.send(embed=discord.Embed(title='그 전 엠블럼을 구매해야 이 엠블럼 구매가 가능합니다',color=discord.Color.red()))
                return
            if point[str(ctx.author.id)] >= item[str('3')]:
                role = discord.utils.get(ctx.guild.roles, name=f"{item2[str('3')]}")
                await ctx.author.add_roles(role)
                point[str(ctx.author.id)] -= int(item[str('3')])
                await t.edit(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(title=f"{item2[str('3')]}아이템을 사려면 코인이 더 필요해요!",color=discord.Color.red()))
            with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(point, f, indent=2, ensure_ascii=False)
            return
    elif str(a) == '4️⃣':
        role = discord.utils.get(ctx.guild.roles, name=item2['4'])
        if role in ctx.author.roles:
            await ctx.send('이미 골드를 구매하셨습니다')
        else:
            role = discord.utils.get(ctx.guild.roles, name=item2['5'])
            if not role in ctx.author.roles:
                await ctx.send(embed=discord.Embed(title='그 전 엠블럼을 구매해야 이 엠블럼 구매가 가능합니다',color=discord.Color.red()))
                return
            if point[str(ctx.author.id)] >= item[str('4')]:
                role = discord.utils.get(ctx.guild.roles, name=f"{item2[str('4')]}")
                await ctx.author.add_roles(role)
                point[str(ctx.author.id)] -= int(item[str('4')])
                await t.edit(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(title=f"{item2[str('4')]}아이템을 사려면 코인 더 필요해요!",color=discord.Color.red()))
            with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(point, f, indent=2, ensure_ascii=False)
            return
    elif str(a) == '5️⃣':
        role = discord.utils.get(ctx.guild.roles, name=item2['5'])
        if role in ctx.author.roles:
            await ctx.send('이미 실버를 구매하셨습니다')
        else:
            role = discord.utils.get(ctx.guild.roles, name=item2['6'])
            if not role in ctx.author.roles:
                await ctx.send(embed=discord.Embed(title='그 전 엠블럼을 구매해야 이 엠블럼 구매가 가능합니다',color=discord.Color.red()))
                return
            if point[str(ctx.author.id)] >= item[str('5')]:
                role = discord.utils.get(ctx.guild.roles, name=f"{item2[str('5')]}")
                await ctx.author.add_roles(role)
                point[str(ctx.author.id)] -= int(item[str('5')])
                await t.edit(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(title=f"{item2[str('5')]}아이템을 사려면 코인이 더 필요해요!",color=discord.Color.red()))
            with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(point, f, indent=2, ensure_ascii=False)
            return
    elif str(a) == '6️⃣':
        role = discord.utils.get(ctx.guild.roles, name=item2['6'])
        if role in ctx.author.roles:
            await ctx.send('이미 브론즈를 구매하셨습니다')
        else:
            if point[str(ctx.author.id)] >= item[str('6')]:
                role = discord.utils.get(ctx.guild.roles, name=f"{item2[str('6')]}")
                await ctx.author.add_roles(role)
                point[str(ctx.author.id)] -= int(item[str('6')])
                await t.edit(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(title=f"{item2[str('6')]}아이템을 사려면 코인이 더 필요해요!",color=discord.Color.red()))
            with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(point, f, indent=2, ensure_ascii=False)
            return
    elif str(a) == "7️⃣":
        if point[str(ctx.author.id)] <= 500:
            await ctx.send(embed=discord.Embed(title=f"니트로 아이템을 사려면 코인이 더 필요해요!",color=discord.Color.red()))
            return
        else:
            point[str(ctx.author.id)] -= 500
            with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(point, f, indent=2, ensure_ascii=False)
            await bot.get_user(724561925341446217).send(f'{ctx.author}님이 니트로를 구매하셨어요!')
            await ctx.send(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',description="토리님한테 얘기해 구매를 이어가세요",color=discord.Color.green()))
            return
#@bot.command()
async def 구매(ctx,an):
    with open('dkpoint.json', 'r') as f:
        jstring = open("dkpoint.json", "r", encoding='utf-8-sig').read()
        point = json.loads(jstring)
    if an == "7":
        if point[str(ctx.author.id)] <= 500:
            await ctx.send(embed=discord.Embed(title=f'{an}아이템을 사려면 코인이 더 필요해요!',color=discord.Color.red()))
            return
        else:
            point[str(ctx.author.id)] -= 500
            with open("dkpoint.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(point, f, indent=2, ensure_ascii=False)
            await bot.get_user(724561925341446217).send(f'{ctx.author}님이 니트로를 구매하셨어요!')
            await ctx.send(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',description="토리님한테 얘기해 구매를 이어가세요",color=discord.Color.green()))
            return
    if point[str(ctx.author.id)] >= item[str(an)]:
        role = discord.utils.get(ctx.guild.roles, name=f"{item2[str(an)]}")
        await ctx.author.add_roles(role)
        point[str(ctx.author.id)] -= int(item[str(an)])
        await ctx.send(embed=discord.Embed(title=f'와우! 구매가 완료돼었어요!',color=discord.Color.green()))
    else:
        await ctx.send(embed=discord.Embed(title=f'{an}아이템을 사려면 코인이 더 필요해요!',color=discord.Color.red()))
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
            message = await bot.get_channel(765460712192475146).send(embed=embed)
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
@bot.command()
async def 경고(ctx,user:discord.Member,limit:int,*,reason='None'):
    global warnlimit
    global warn
    if not str(ctx.author.id) in admin:
        return
    jstring = open("warn2.json", "r", encoding='utf-8-sig').read()
    warn = json.loads(jstring)
    jstring = open("warnlimit2.json", "r", encoding='utf-8-sig').read()
    warnlimit = json.loads(jstring)
    try:
        warn[str(user.id)] += int(limit)
        with open(f"warn2.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
    except:
        warn[str(user.id)] = int(limit)
        with open(f"warn2.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
    if warn[str(user.id)] >= int(warnlimit):
        try:
            await user.send(embed=discord.Embed(title="경고,밴 안내",description=f'당신은 경고 갯수가 {warnlimit}이상이 되어 이 봇에 의해 밴당했어요 :angry:!\n경고 사유 : {reason}',color=discord.Color.red()))
        except:
            pass
        await ctx.guild.ban(user,reason=f'경고 한도 초과. 마지막 경고 {reason}')
        del warn[str(user.id)]
        c = await ctx.send(f'{str(user)}님이 경고한도 {warnlimit}({warn[str(user.id)]}/{warnlimit})를 초과하여 밴됬습니다')
        await c.add_reaction('<a:complete:760472208774135868>')
    else:
        try:
            await user.send(embed=discord.Embed(title="경고 안내",description=f'당신은 경고 {limit}개를 받아 경고 갯수가 {warn[str(user.id)]}/{warnlimit}가 되었어요 :angry:!\n경고 사유 : {reason}',color=discord.Color.red()))
        except:
            pass
        await ctx.message.add_reaction('<a:complete:760472208774135868>')
    with open(f"warn2.json", "w+", encoding='utf-8-sig') as f:
        json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
@bot.command()
async def 경고한도(ctx,limit:int):
    global warnlimit
    if not str(ctx.author.id) in admin:
        return
    with open(f"warnlimit2.json", "w+", encoding='utf-8-sig') as f:
        json_string = json.dump(limit, f, indent=2, ensure_ascii=False)
    await ctx.message.add_reaction('<a:complete:760472208774135868>')
@bot.command()
async def 경고확인(ctx,user:discord.Member='None'):
    if user == 'None':
        user = ctx.author
    jstring = open("warn2.json", "r", encoding='utf-8-sig').read()
    warn = json.loads(jstring)
    jstring = open("warnlimit2.json", "r", encoding='utf-8-sig').read()
    warnlimit = json.loads(jstring)
    try:
        await ctx.send(embed=discord.Embed(title=f'{str(user)}님의 경고는 {warn[str(user.id)]}/{warnlimit}개입니다!',color=discord.Color.blue()))
    except:
        await ctx.send(f'{str(user)}님은 경고를 받지 않았어요!')
@bot.command()
async def 경고초기화(ctx,user:discord.Member):
    if not str(ctx.author.id) in admin:
        return
    jstring = open("warn2.json", "r", encoding='utf-8-sig').read()
    warn = json.loads(jstring)
    del warn[str(user.id)]
    with open(f"warn2.json", "w+", encoding='utf-8-sig') as f:
        json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
    await ctx.message.add_reaction('<a:complete:760472208774135868>')
@bot.command()
async def 경고삭제(ctx,user:discord.Member,limit:int):
    if not str(ctx.author.id) in admin:
        return
    jstring = open("warn2.json", "r", encoding='utf-8-sig').read()
    warn = json.loads(jstring)
    try:
        warn[str(user.id)] -= limit
        if warn[str(user.id)] < 0:
            await ctx.send(f'{str(user)}님 경고가 {limit}개 이하여서 경고를 삭제하지 못했어요!')
            warn[str(user.id)] += limit
            with open(f"warn2.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
            return
    except:
        await ctx.send(f'{str(user)}님은 경고를 받지 않았어요!')
        return
    with open(f"warn2.json", "w+", encoding='utf-8-sig') as f:
        json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
    await ctx.message.add_reaction('<a:complete:760472208774135868>')
@bot.command()
async def 뮤트(ctx,user:discord.Member):
    if not str(ctx.author.id) in admin:
        return
    mutemessage = await ctx.send(embed=discord.Embed(title='뮤트안내',description=f'정말로 {str(user)}님을 뮤트하겠습니까?',color=discord.Color.red()))
    await mutemessage.add_reaction('<a:complete:760472208774135868>')
    await mutemessage.add_reaction('<a:pass:760474783606505503>')
    def check(reaction,users):
        return ctx.author.id == users.id and ctx.channel.id == reaction.message.channel.id
    try:
        reaction = await bot.wait_for('reaction_add',timeout=20,check=check)
        a = reaction[0]
    except asyncio.TimeoutError:
        await mutemessage.edit(embed=discord.Embed(title='만료됨',color=discord.Color.blue()))
        return
    else:
        if str(a) == '<a:complete:760472208774135868>':
            role = discord.utils.get(ctx.guild.roles, id=765840144745889832)
            await user.add_roles(role)
            role = discord.utils.get(ctx.guild.roles, id=765675273127198730)
            await user.remove_roles(role)
            await mutemessage.edit(embed=discord.Embed(title='뮤트안내',description=f'{ctx.author.mention}님이 {user.mention}님을 뮤트했습니다',color=discord.Color.green()))
            return
        elif str(a) == '<a:pass:760474783606505503>':
            await mutemessage.edit(embed=discord.Embed(title='취소됨',color=discord.Color.red()))
@bot.command()
async def 언뮤트(ctx,user:discord.Member):
    if not str(ctx.author.id) in admin:
        return
    mutemessage = await ctx.send(embed=discord.Embed(title='뮤트안내',description=f'정말로 {str(user)}님을 언뮤트하겠습니까?',color=discord.Color.red()))
    await mutemessage.add_reaction('<a:complete:760472208774135868>')
    await mutemessage.add_reaction('<a:pass:760474783606505503>')
    muteinfo = 'yes'
    def check(reaction,users):
        return ctx.author.id == users.id and ctx.channel.id == reaction.message.channel.id
    try:
        reaction = await bot.wait_for('reaction_add',timeout=20,check=check)
        a = reaction[0]
    except asyncio.TimeoutError:
        await mutemessage.edit(embed=discord.Embed(title='만료됨',color=discord.Color.blue()))
        return
    else:
        if str(a) == '<a:complete:760472208774135868>':
            role = discord.utils.get(ctx.guild.roles, id=765840144745889832)
            await user.add_roles(role)
            role = discord.utils.get(ctx.guild.roles, id=765840144745889832)
            await user.remove_roles(role)
            await mutemessage.edit(embed=discord.Embed(title='뮤트안내',description=f'{ctx.author.mention}님이 {user.mention}님을 언뮤트했습니다',color=discord.Color.green()))
            return
        elif str(a) == '<a:pass:760474783606505503>':
            await mutemessage.edit(embed=discord.Embed(title='취소됨',color=discord.Color.red()))
@bot.listen()
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    with open('msg.json', 'r') as f:
        jstring = open("msg.json", "r", encoding='utf-8-sig').read()
        msg = json.loads(jstring)
    try:
        msg[str(message.author.id)] += 1
    except:
        msg[str(message.author.id)] = 1
    if msg[str(message.author.id)] == 80:
        role = discord.utils.get(message.guild.roles, name="채팅 100회 이상")
    elif msg[str(message.author.id)] == 200:
        role = discord.utils.get(message.guild.roles, name="채팅 200회 이상")
    elif msg[str(message.author.id)] == 300:
        role = discord.utils.get(message.guild.roles, name="채팅 300회 이상")
    elif msg[str(message.author.id)] == 1000:
        role = discord.utils.get(message.guild.roles, name="채팅 1000회 이상")
    elif msg[str(message.author.id)] == 5000:
        role = discord.utils.get(message.guild.roles, name="채팅 5000회 이상")
    else:
        with open("msg.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(msg, f, indent=2, ensure_ascii=False)
        return
    await message.author.add_roles(role)
    await message.channel.send(f'축하합니다! 특별 역할이 지급돼셨습니다!')
    #except:
    #    msg[str(message.author.id)] = 1
    with open("msg.json", "w+", encoding='utf-8-sig') as f:
        json_string = json.dump(msg, f, indent=2, ensure_ascii=False)

bot.run('NzU1OTk2MTUwMzc2NTYyNzI5.X2LaRw.Lgbz6en8cr1bq5zemTd6URNrCmM')
