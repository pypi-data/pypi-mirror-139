import logging
import typing
from .auth import get
from .utils import capitalize
from .api_urls import get_folders_url,\
    get_folder_url, find_folders_url
logger = logging.getLogger(__name__)


class FolderDto:
    HasChildFolder = False
    DisplayName = ''
    Path = ''
    CreationTime = None
    LastModificationTime = None

    def __init__(self, folder_dict):
        self.__dict__ = capitalize(folder_dict)

    def __repr__(self) -> str:
        return "%s(%r)" % (self.__class__, self.__dict__)


def get_folders(path: str, tenant_name: str = '') -> typing.List[FolderDto]:
    """
    get folders from api
    :param path: the path looking for
    :param tenant_name: the tenant name of app, default is empty, you can think of it as organization name
    :return: return children folders under the path
    """
    url = get_folders_url(path, tenant_name)
    data = get(url)
    if('totalCount' not in data or int(data['totalCount']) == 0):
        return []
    if 'items' not in data:
        raise Exception(f"unsupported data {data}")

    return [FolderDto(d) for d in data['items']]


def get_folder(path: str, tenant_name: str = '') -> FolderDto:
    """
    get specified folder informations
    :param path: the path of folder
    :param tenant_name: refer to get_folders
    :return: return the folder informations
    """
    url = get_folder_url(path, tenant_name)
    data = get(url)
    return FolderDto(data)


def find_folders(path: str, tenant_name: str = '') -> typing.List[FolderDto]:
    """
    find folders where it's path contains the param path
    :param path: a part of whole path
    :param tenant_name: refer to get_folders
    :return: return found folders by the rule
    """
    url = find_folders_url(path, tenant_name)
    data = get(url)
    return [FolderDto(d) for d in data]
