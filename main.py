from tkinter.tix import IMAGE

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp
from astrbot.api.message_components import Video
import os
import random

VIDEO_DIR = "/Users/mixuanmin/data/attachments"
IMAGE_DIR = "/Users/mixuanmin/Desktop"

def search_video(path:str,keyword: str) -> str | None:
        """
        模糊匹配文件名（包含后缀）
        """
        keyword = keyword.lower()
        matched = []

        for fname in os.listdir(path):
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
    async def player(self, event: AstrMessageEvent,keyword: str):
        """用法：/player 图片名""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        if keyword == "":
            yield event.plain_result("请输入关键字，例如：/video 哈哈")
            return
        chain = [
            Comp.At(qq=event.get_sender_id()), # At 消息发送者
            # Comp.Plain("来看这个图："),
            Comp.Image.fromFileSystem(search_video(IMAGE_DIR,keyword)), # 从本地文件目录发送图片
            # Comp.Plain("这是一个图片。")
        ]
        yield event.chain_result(chain)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
    
    @filter.command("video")
    async def video(self, event: AstrMessageEvent,keyword: str):
        """用法：/video 哈哈"""
        if keyword == "":
            yield event.plain_result("请输入关键字，例如：/video 哈哈")
            return

        path = search_video(VIDEO_DIR,keyword)

        if path == None:
            yield event.plain_result(f"没找到和「{keyword}」相关的视频 😢")
            return

        video = Video.fromFileSystem(path=path)
        yield event.chain_result([video])