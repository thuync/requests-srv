from urlparse import urlparse, urlunparse

from dns.resolver import Resolver
from dns.exception import DNSException
from requests import Session, ConnectionError
from requests.adapters import HTTPAdapter


class SRVResolverHTTPAdapter(HTTPAdapter):
    def __init__(self, dns_hosts=None, dns_port=None, **kwargs):
        self.dns_hosts = dns_hosts
        self.dns_port = dns_port
        self.resolver = Resolver()
        if dns_hosts is not None:
            self.resolver.nameservers = dns_hosts
        if dns_port is not None:
            self.resolver.port = dns_port
        super(SRVResolverHTTPAdapter, self).__init__(**kwargs)

    def get_connection(self, url, proxies=None):
        parsed = urlparse(url)
        host, port = self._resolve_srv(parsed.netloc)
        redirected_url = urlunparse((
            resolve_scheme(parsed.scheme),
            '%s:%d' % (host, port),
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
        return super(SRVResolverHTTPAdapter, self).get_connection(redirected_url, proxies=proxies)

    def _resolve_srv(self, service):
        try:
            answers = self.resolver.query(service, 'SRV')
        except DNSException as e:
            raise ConnectionError('DNS error: ' + e.__class__.__name__)
        return answers[0].target, answers[0].port


def request(method, url, **kwargs):
    with Session() as session:
        resolve_srv(session)
        return session.request(method=method, url=url, **kwargs)


def get(url, params=None, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return request('get', url, params=params, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return request('post', url, data=data, json=json, **kwargs)


def patch(url, data=None, **kwargs):
    return request('patch', url, data=data, **kwargs)


def head(url, **kwargs):
    kwargs.setdefault('allow_redirects', False)
    return request('head', url, **kwargs)


def delete(url, **kwargs):
    return request('delete', url, **kwargs)


def put(url, data=None, **kwargs):
    return request('put', url, data=data, **kwargs)


def options(url, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return request('options', url, **kwargs)


def resolve_scheme(origin_scheme):
    if 'https' in origin_scheme:
        return 'https'
    elif 'http' in origin_scheme:
        return 'http'

    return origin_scheme


def resolve_srv(session, prefix='srv+', **kwargs):
    """

    :param prefix:
    :type prefix: str
    :param session:
    :type session: Session
    :return:
    """
    session.mount(prefix, SRVResolverHTTPAdapter(**kwargs))
