# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
import os

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter

from favorites_crawler.constants.regexes import PIXIV_ORIGINAL_IMAGE_URL_PATTERN


class PixivFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        item_dict = ItemAdapter(item).asdict()
        return [
            Request(url, headers={'Referer': item_dict['referer']}, meta=item_dict)
            for url in item_dict['original_image_urls']
        ]

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Download Failed')
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        match = re.search(PIXIV_ORIGINAL_IMAGE_URL_PATTERN, request.url)
        file_id = match.group(1)
        file_ext = match.group(2)
        filename = item.get_filename(file_id, file_ext)
        return os.path.join('Pixiv', filename)


class YandreFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        item_dict = ItemAdapter(item).asdict()
        return [Request(item_dict['file_url'])]

    def file_path(self, request, response=None, info=None, *, item=None):
        return os.path.join('Yandere', item.get_filename())


class CollectionFilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        item_dict = ItemAdapter(item).asdict()
        referer = item_dict.get('referer')
        return (Request(url, headers={'referer': referer}) for url in item_dict.get('image_urls', ()))

    def file_path(self, request, response=None, info=None, *, item=None):
        return item.get_filepath(request.url)
