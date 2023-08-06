from nonebot import on_regex, require, on_keyword
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.params import State
from .genshin_handle import genshin_draw, update_genshin_info, reset_count, reload_genshin_pool
from .prts_handle import update_prts_info, prts_draw, reload_prts_pool
from .pretty_handle import update_pretty_info, pretty_draw, reload_pretty_pool
from .guardian_handle import update_guardian_info, guardian_draw, reload_guardian_pool
from .pcr_handle import update_pcr_info, pcr_draw
from .azur_handle import update_azur_info, azur_draw
from .fgo_handle import update_fgo_info, fgo_draw
from .onmyoji_handle import update_onmyoji_info, onmyoji_draw
from .update_game_info import update_info
from .util import is_number, check_num
from .rule import is_switch
from .config import draw_config
from .async_update_game_info import async_update_game
from nonebot.log import logger
import re
import asyncio

scheduler = require('nonebot_plugin_apscheduler').scheduler

prts = on_regex(r'.*?方舟[1-9|一][0-9]{0,2}[抽|井|连]', rule=is_switch('prts'), priority=5, block=True)
prts_update = on_keyword({'更新方舟信息', '更新明日方舟信息'}, permission=SUPERUSER, priority=1, block=True)
prts_up_reload = on_keyword({'重载方舟卡池'}, priority=1, block=True)

genshin = on_regex(r'.*?原神(武器|角色)?池?[1-9|一][0-9]{0,2}[抽|井|连]', rule=is_switch('genshin'), priority=5, block=True)
genshin_update = on_keyword({'更新原神信息'}, permission=SUPERUSER, priority=1, block=True)
genshin_reset = on_keyword({'重置原神抽卡'}, priority=1, block=True)
genshin_up_reload = on_keyword({'重载原神卡池'}, priority=1, block=True)

pretty = on_regex(r'.*?马娘卡?[1-9|一][0-9]{0,2}[抽|井|连]', rule=is_switch('pretty'), priority=5, block=True)
pretty_update = on_keyword({'更新马娘信息', '更新赛马娘信息'}, permission=SUPERUSER, priority=1, block=True)
pretty_up_reload = on_keyword({'重载赛马娘卡池'}, priority=1, block=True)

guardian = on_regex(r'.*?坎公骑冠剑武?器?[1-9|一][0-9]{0,2}[抽|井|连]', rule=is_switch('guardian'), priority=5, block=True)
guardian_update = on_keyword({'更新坎公骑冠剑信息'}, permission=SUPERUSER, priority=1, block=True)
guardian_up_reload = on_keyword({'重载坎公骑冠剑卡池'}, priority=1, block=True)

pcr = on_regex(r'.*?(pcr|公主连结|公主连接|公主链接|公主焊接)[1-9|一][0-9]{0,2}[抽|井|连]', rule=is_switch('pcr'), priority=5, block=True)
pcr_update = on_keyword({'更新pcr信息', '更新公主连结信息'}, permission=SUPERUSER, priority=1, block=True)

azur = on_regex(r'.*?碧蓝航?线?(轻型|重型|特型)池?[1-9|一][0-9]{0,2}[抽|连]', rule=is_switch('azur'), priority=5, block=True)
azur_update = on_keyword({'更新碧蓝信息', '更新碧蓝航线信息'}, permission=SUPERUSER, priority=1, block=True)

fgo = on_regex(r'.*?fgo[1-9|一][0-9]{0,2}[抽|连]', rule=is_switch('fgo'), priority=5, block=True)
fgo_update = on_keyword({'更新fgo信息'}, permission=SUPERUSER, priority=1, block=True)

onmyoji = on_regex(r'.*?阴阳师[1-9|一][0-9]{0,2}[抽|连]', rule=is_switch('onmyoji'), priority=5, block=True)
onmyoji_update = on_keyword({'更新阴阳师信息'}, permission=SUPERUSER, priority=1, block=True)


@prts.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    msg = str(event.get_message()).strip()
    if msg in ['方舟一井', '方舟1井']:
        num = 300
    else:
        rmsg = re.search(r'.*?方舟(.*)[抽|连]', msg)
        if rmsg:
            num, flag = check_num(rmsg.group(1), 300)
            if not flag:
                await prts.finish(num, at_sender=True)
        else:
            return
    await prts.send(await prts_draw(int(num)), at_sender=True)


@prts_up_reload.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    text = await reload_prts_pool()
    await prts_up_reload.finish(Message(f'重载完成！\n{text}'))


@genshin.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    msg = str(event.get_message()).strip()
    rmsg = re.search(r'.*?原神(武器|角色)?池?(.*)[抽|井|连]', msg)
    if rmsg:
        pool_name = rmsg.group(1)
        if pool_name == '武器':
            pool_name = 'arms'
        elif pool_name == '角色':
            pool_name = 'char'
        else:
            pool_name = ''
        num = rmsg.group(2)
        if msg.find('一井') != -1 or msg.find('1井') != -1:
            num = 180
        else:
            num, flag = check_num(num, 180)
            if not flag:
                await genshin.finish(num, at_sender=True)
    else:
        return
    await genshin.send(await genshin_draw(event.user_id, int(num), pool_name), at_sender=True)


@genshin_up_reload.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    text = await reload_genshin_pool()
    await genshin_reset.finish(Message(f'重载成功！\n{text}'))


@genshin_reset.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    reset_count(event.user_id)
    await genshin_reset.send('重置了原神抽卡次数', at_sender=True)


@pretty.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    msg = str(event.get_message()).strip()
    if msg.find('1井') != -1 or msg.find('一井') != -1:
        num = 200
        if msg.find("卡") == -1:
            pool_name = 'char'
        else:
            pool_name = 'card'
    else:
        rmsg = re.search(r'.*?马娘(.*)[抽|连]', msg)
        if rmsg:
            num = rmsg.group(1)
            if num[0] == '卡':
                num = num[1:]
                pool_name = 'card'
            else:
                pool_name = 'char'
            num, flag = check_num(num, 200)
            if not flag:
                await pretty.finish(num, at_sender=True)
        else:
            return
    await pretty.send(await pretty_draw(int(num), pool_name), at_sender=True)


@pretty_up_reload.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    text = await reload_pretty_pool()
    await genshin_reset.finish(Message(f'重载成功！\n{text}'))


@guardian.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    msg = str(event.get_message()).strip()
    pool_name = 'char'
    if msg.find('1井') != -1 or msg.find('一井') != -1:
        num = 300
        if msg.find('武器') != -1:
            pool_name = 'arms'
    else:
        rmsg = re.search(r'.*?坎公骑冠剑(.*)[抽|连]', msg)
        if rmsg:
            num = rmsg.group(1)
            if num.find('武器') != -1:
                pool_name = 'arms'
                num = num.replace('武器', '')
            num, flag = check_num(num, 300)
            if not flag:
                await guardian.finish(num, at_sender=True)
        else:
            return
    await guardian.send(await guardian_draw(int(num), pool_name), at_sender=True)


@guardian_up_reload.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    text = await reload_guardian_pool()
    await genshin_reset.finish(Message(f'重载成功！\n{text}'))


@pcr.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    msg = str(event.get_message()).strip()
    if msg.find('1井') != -1 or msg.find('一井') != -1:
        num = 300
    else:
        rmsg = re.search(r'.*?(pcr|公主连结)(.*)[抽|井|连]', msg)
        if rmsg:
            num, flag = check_num(rmsg.group(2), 300)
            if not flag:
                await pcr.finish(num, at_sender=True)
        else:
            return
    await pcr.send(await pcr_draw(int(num)), at_sender=True)


@azur.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    msg = str(event.get_message()).strip()
    rmsg = re.search(r'.*?碧蓝航?线?(轻型|重型|特型)池?(.*)[抽|连]', msg)
    if rmsg:
        pool_name = rmsg.group(1)
        num, flag = check_num(rmsg.group(2), 300)
        if not flag:
            await azur.finish(num, at_sender=True)
    else:
        return
    await azur.send(await azur_draw(int(num), pool_name), at_sender=True)


@fgo.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    msg = str(event.get_message()).strip()
    rmsg = re.search(r'.*?fgo(.*)[抽|连]', msg)
    if rmsg:
        num, flag = check_num(rmsg.group(1), 300)
        if not flag:
            await fgo.finish(num, at_sender=True)
    else:
        return
    await fgo.send(await fgo_draw(int(num)), at_sender=True)


@onmyoji.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    msg = str(event.get_message()).strip()
    rmsg = re.search(r'.*?阴阳师(.*)[抽|连]', msg)
    if rmsg:
        num, flag = check_num(rmsg.group(1), 300)
        if not flag:
            await onmyoji.finish(num, at_sender=True)
    else:
        return
    await onmyoji.send(await onmyoji_draw(int(num)), at_sender=True)


@prts_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    await update_prts_info()
    await prts_update.finish('更新完成！')


@genshin_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    await update_genshin_info()
    await genshin_update.finish('更新完成！')


@pretty_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    await update_pretty_info()
    await genshin_update.finish('更新完成！')


@guardian_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    await update_guardian_info()
    await genshin_update.finish('更新完成！')


@pcr_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    await update_pcr_info()
    await genshin_update.finish('更新完成！')


@azur_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    await update_azur_info()
    await genshin_update.finish('更新完成！')


@fgo_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    await update_fgo_info()
    await genshin_update.finish('更新完成！')


@onmyoji_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State=State()):
    await update_onmyoji_info()
    await genshin_update.finish('更新完成！')


# 更新资源
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    tasks = []
    if draw_config.PRTS_FLAG:
        tasks.append(asyncio.ensure_future(update_prts_info()))
    if draw_config.GENSHIN_FLAG:
        tasks.append(asyncio.ensure_future(update_genshin_info()))
    if draw_config.PRETTY_FLAG:
        tasks.append(asyncio.ensure_future(update_pretty_info()))
    if draw_config.GUARDIAN_FLAG:
        tasks.append(asyncio.ensure_future(update_guardian_info()))
    if draw_config.PCR_FLAG:
        tasks.append(asyncio.ensure_future(update_pcr_info()))
    if draw_config.AZUR_FLAG:
        tasks.append(asyncio.ensure_future(update_azur_info()))
    if draw_config.FGO_FLAG:
        tasks.append(asyncio.ensure_future(update_fgo_info()))
    if draw_config.ONMYOJI_FLAG:
        tasks.append(asyncio.ensure_future(update_onmyoji_info()))
    await asyncio.gather(*tasks)


# 每天四点重载方舟up卡池
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    if draw_config.PRTS_FLAG:
        await reload_prts_pool()


# 每天四点重载赛马娘up卡池
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    if draw_config.PRETTY_FLAG:
        await reload_pretty_pool()


# 每天下午六点点重载原神up卡池
@scheduler.scheduled_job(
    'cron',
    hour=18,
    minute=1,
)
async def _():
    if draw_config.PRTS_FLAG:
        await reload_genshin_pool()


# 重载坎公骑冠剑卡池
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    if draw_config.GUARDIAN_FLAG:
        await reload_guardian_pool()
