# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

# class BooksToScrapePipeline(object): #Since we'll override ImagesPipeline, change to the pertinent superclass.
class BooksToScrapePipeline(ImagesPipeline):
    # The source module for the following two method overrides is: C:\Users\Paul\PycharmProjects\Udemy\venv\Lib\site-packages\scrapy\pipelines\images.py
    def get_media_requests(self, item, info):
        return [Request(x, meta={'bookname': item.get('book_name')}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block

        # image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        # return 'full/%s.jpg' % (image_guid)
        filename = request.meta['bookname'].replace(':', '')
        # request.meta['bookname'] will return a string because of book_name=scrapy.Field(output_processor=TakeFirst() in items.py
        # return 'full/%s.jpg' % (request.meta['bookname'])
        return 'full/%s.jpg' % (filename)

class FilesToScrapePipeline(FilesPipeline):
    # The source module for the following two method overrides is: C:\Users\Paul\PycharmProjects\Udemy\venv\Lib\site-packages\scrapy\pipelines\files.py
    def get_media_requests(self, item, info):
        return [Request(x, meta={'filename': item.get('file_name')}) for x in item.get(self.files_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('FilesPipeline.file_key(url) method is deprecated, please use '
                          'file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() method has been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        ## end of deprecation warning block

        # media_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        # media_ext = os.path.splitext(url)[1]  # change to request.url after deprecation
        # return 'full/%s%s' % (media_guid, media_ext)
        return 'full/%s' % (request.meta['filename'].replace('.log', '_log.txt'))


