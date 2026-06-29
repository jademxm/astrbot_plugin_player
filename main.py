from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Video
import os
import random

VIDEO_DIR = "/Users/mixuanmin/data/attachments"

def search_video(keyword: str) -> str | None:
        """
        模糊匹配文件名（包含后缀）
        """
        keyword = keyword.lower()
        matched = []

        for fname in os.listdir(VIDEO_DIR):
            if keyword in fname.lower():
                matched.append(os.path.join(VIDEO_DIR, fname))

        if not matched:
            return None

        # 多条 → 随机一条
        return random.choice(matched)
@register("player", "player", "一个简单的 插件玩吧", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 player。注册成功后，发送 `/player` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("player")
    async def player(self, event: AstrMessageEvent):
        """这是一个 player 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
    
    @filter.command("video")
    async def video(self, event: AstrMessageEvent,keyword: str):
        """用法：/video 哈哈"""
        if keyword == "":
            yield event.plain_result("请输入关键字，例如：/video 哈哈")
            return

        path = search_video(keyword)

        if path == None:
            yield event.plain_result(f"没找到和「{keyword}」相关的视频 😢")
            return

        video = Video.fromFileSystem(path=path)
        yield event.chain_result([video])