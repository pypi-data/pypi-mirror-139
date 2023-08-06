from urllib.parse import urlencode
from .config import get_config, is_client_grant


def urljoin(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """
    return "/".join(map(lambda x: str(x).strip('/'), args))


def get_metadata_url(id):
    host_url = get_config("APP_API_URL")
    return urljoin(host_url,
                   f"api/app/slide/{id}/metadata")


def get_tile_url(id):
    host_url = get_config("APP_API_URL")
    return urljoin(host_url,
                   f"api/app/slide/{id}/tile")


def get_folders_url(path: str,
                    tenant_name: str = '',
                    skip_count: int = 0,
                    max_result_count: int = 100000) -> str:
    host_url = get_config("APP_API_URL")
    params = {
        'path': path,
        'skipCount': skip_count,
        'maxResultCount': max_result_count
    }
    if tenant_name:
        params.update({
            'tenantName': tenant_name,
        })

    return urljoin(host_url,
                   f"api/app/cloud-folder-entry-backend/folders?{urlencode(params)}")


def find_folders_url(path: str,
                     tenant_name: str = '') -> str:
    host_url = get_config("APP_API_URL")
    params = {
        'path': path,
    }
    if tenant_name:
        params.update({
            'tenantName': tenant_name,
        })

    return urljoin(host_url,
                   f"api/app/cloud-folder-entry-backend/find-folders?{urlencode(params)}")


def get_folder_url(path: str, tenant_name: str = '') -> str:
    host_url = get_config("APP_API_URL")
    params = {
        'path': path,
    }
    if tenant_name:
        params.update({
            'tenantName': tenant_name,
        })
    return urljoin(host_url,
                   f"/api/app/cloud-folder-entry-backend/folder?{urlencode(params)}")


def get_slides_url(path: str,
                   tenant_name: str = '',
                   skip_count: int = 0,
                   max_result_count: int = 100000) -> str:
    host_url = get_config('APP_API_URL')
    params = {
        'path': path,
        'skipCount': skip_count,
        'maxResultCount': max_result_count
    }
    if tenant_name:
        params.update({
            'tenantName': tenant_name,
        })
    return urljoin(host_url,
                   f"/api/app/cloud-slide-entry-backend/slides?{urlencode(params)}")


def find_slides_url(path: str,
                    tenant_name: str = '',) -> str:
    host_url = get_config('APP_API_URL')
    params = {
        'path': path,
    }
    if tenant_name:
        params.update({
            'tenantName': tenant_name,
        })
    return urljoin(host_url,
                   f"/api/app/cloud-slide-entry-backend/find-slides?{urlencode(params)}")


def get_slide_url(path: str, tenant_name: str = '') -> str:
    host_url = get_config('APP_API_URL')
    params = {
        'path': path,
    }
    if tenant_name:
        params.update({
            'tenantName': tenant_name,
        })

    return urljoin(host_url,
                   f"/api/app/cloud-slide-entry-backend/slide?{urlencode(params)}")
