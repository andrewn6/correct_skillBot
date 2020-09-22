"""
Cog that looks for new video of a channel if a new video comes then posts a notification
"""
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import aiofiles
import discord
from aiohttp import request
from discord.ext import tasks
from discord.ext.commands import Cog
from config import BOT_CHANNEL, YOUTUBE_NOTIFICATIONS  # pylint: disable=E0401


def to_pages_by_lines(content: str, max_size: int):
    """Shortens the youtube video description"""
    pages = ['']
    i = 0
    for line in content.splitlines(keepends=True):
        if len(pages[i] + line) > max_size:
            i += 1
            pages.append('')
        pages[i] += line
    return pages


class Youtube(Cog):
    """Youtube cog class that looks for new videos"""

    def __init__(self, bot):
        self.bot = bot

    async def save_to_json(self, video, filename):
        """saves video to json"""
        async with aiofiles.open(f"{filename}.json", 'w') as jsonfile:
            await jsonfile.write(json.dumps(video))

    async def _get_stored_video(self, filename):
        """gets last stored video"""
        try:
            async with aiofiles.open(f"{filename}.json", "r") as jsonfile:
                video = dict()
                resp = await jsonfile.read()
                video = json.loads(resp)
                return video
        except:  # pylint: disable=W0702
            return None

    @tasks.loop(seconds=120.0)
    async def _get_last_video(self):  # pylint: disable=R0914
        """looped function that looks for new video"""
        print("querying yt routine")
        url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UC4JX40jDee_tINbkjycV4Sg'
        try:
            async with request("GET", url) as resp:
                data = resp.content
                with open('channelFeed.xml', 'wb') as f:  # pylint: disable=C0103
                    f.write(await data.read())
        except:  # pylint: disable=W0702
            print("ERROR IN YT COG WHILE FETCHING")
            return
        tree = ET.parse('channelFeed.xml')
        videoitems = []
        ns = '{http://www.w3.org/2005/Atom}'  # pylint: disable=C0103
        md = '{http://search.yahoo.com/mrss/}'  # pylint: disable=C0103
        for entry in tree.findall(ns + "entry"):
            video = {}
            url = entry.find(ns + "link")
            video["video_url"] = url.attrib["href"]
            title = entry.find(ns + "title")
            video["title"] = f"{title.text}"
            date_str = str(entry.find((ns + "published")).text)
            video["time"] = date_str

            for mediagroup in entry.findall(md + 'group'):
                thumbnail = mediagroup.find(md + 'thumbnail')
                video['image'] = thumbnail.attrib['url']
                description = mediagroup.find(md + 'description')
                video['description'] = description.text

            videoitems.append(video)
            break
        new_video = videoitems[0]
        video = await self._get_stored_video("videos")

        if video == None:  # pylint: disable=C0121
            await self.save_to_json(new_video, "videos")
            return

        if video['video_url'] == new_video['video_url']:
            print("old")


        else:
            print("new")
            description = to_pages_by_lines(new_video["description"], max_size=500)[0].replace('*',
                                                                                               '').strip()  # pylint: disable=C0301
            embed = discord.Embed(title=new_video['title'],
                                  url=new_video['video_url'],
                                  description=description,
                                  color=discord.Colour.red(),
                                  timestamp=datetime.strptime(new_video["time"],
                                                              '%Y-%m-%dT%H:%M:%S%z'))
            url = new_video["image"]
            embed.set_image(url=url)
            embed.set_thumbnail(url=self.bot.guild.icon_url)
            embed.set_author(name="Tech With Tim",
                             url="https://www.youtube.com/c/TechWithTim/featured",
                             icon_url=self.bot.guild.icon_url)
            embed.set_footer(text='Uploaded:', icon_url=self.bot.guild.icon_url)
            channel = self.bot.guild.get_channel(BOT_CHANNEL)
            await channel.send(embed=embed)
            await self.save_to_json(new_video, "videos")
            return

    @Cog.listener()
    async def on_ready(self):
        """readies the cog"""
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("youtube")
            # print("youtube cog ready")
            if YOUTUBE_NOTIFICATIONS == "True":
                print("TRUE starting routine")
                self._get_last_video.start()  # pylint: disable=E1101


def setup(bot):
    """sets up the cog"""
    bot.add_cog(Youtube(bot))
