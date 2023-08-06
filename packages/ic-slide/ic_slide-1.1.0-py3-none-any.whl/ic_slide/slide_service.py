import logging
import typing
from .auth import get
from .utils import capitalize
from .api_urls import get_slides_url,\
    get_slide_url, find_slides_url
from .slide_source import open_slide
logger = logging.getLogger(__name__)


class SlideDto:
    SlideId: str = ''
    Format: str = ''
    Bytes: int = 0
    DisplayName: str = ''
    Path: str = ''
    CreationTime: str = ''
    LastModificationTime: str = ''

    def __init__(self, slide_dict):
        self.__dict__ = capitalize(slide_dict)

    def __repr__(self) -> str:
        return "%s(%r)" % (self.__class__, self.__dict__)


def get_slides(path: str, tenant_name: str = '') -> typing.List[SlideDto]:
    """
    get slides from api
    :param path: the path looking for
    :param tenant_name:  the tenant name of app, default is empty, you can think of it as organization name
    :return: return children slides under the path
    """
    url = get_slides_url(path, tenant_name)
    data = get(url)
    if('totalCount' not in data or int(data['totalCount']) == 0):
        return []
    if 'items' not in data:
        raise Exception(f"unsupported data {data}")

    return [SlideDto(d) for d in data['items']]


def get_slide(path: str, tenant_name: str = '') -> SlideDto:
    """
    get specified slide informations
    :param path: the path of slide
    :param tenant_name: refer to get_slides
    :return: return the slide informations
    """
    url = get_slide_url(path, tenant_name)
    data = get(url)
    return SlideDto(data)


def find_slides(path: str, tenant_name: str = '') -> typing.List[SlideDto]:
    """
    find slides where it's path contains the param path
    :param path: a part of whole path, contains slide name.
    :param tenant_name: refer to get_slides
    :return: return found slides by the rule
    """
    url = find_slides_url(path, tenant_name)
    data = get(url)
    return [SlideDto(d) for d in data]


def open_slides(path: str, tenant_name: str = ''):
    """
    open slides where it's path contains the param path
    :param path: a part of whole path, contains slide name.
    :param tenant_name: refer to get_slides
    :return: return opened slide by the rule
    """
    slideDtos = find_slides(path, tenant_name)

    def open(dto: SlideDto):
        slide = open_slide(dto.SlideId)
        slide.Path = dto.Path
        return slide

    return [open(slideDto) for slideDto in slideDtos]
