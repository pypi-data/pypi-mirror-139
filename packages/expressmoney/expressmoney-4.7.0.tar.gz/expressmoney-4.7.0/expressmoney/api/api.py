"""
API Client
"""
import os
from typing import OrderedDict

from django.contrib.auth.models import User
from django.core.cache import cache
from expressmoney.django.utils import DjangoRequest
from expressmoney.utils import HttpStatus
from rest_framework import serializers


__all__ = ('API', 'NotAuthenticated', 'CreateObjectClientError', 'CreateObjectServerError', 'FlushCacheAPI',
           'Contract', 'PaginationContract',
           )


class ApiError(Exception):
    pass


class NotAuthenticated(ApiError):
    pass


class SortByNotSet(ApiError):
    pass


class FilterAttrNotSet(ApiError):
    pass


class LookupFieldValueNone(ApiError):
    pass


class CreateObjectClientError(ApiError):
    pass


class CreateObjectServerError(ApiError):
    pass


class CacheMixin:

    _cache_period: int = None
    _service_name: str = None
    _app: str = None
    _point: str = None
    _action: str = None

    def __init__(self, user: User, lookup_field_value: str = None):
        self._user = user
        self._memory_cache = None
        super().__init__(user, lookup_field_value)

    @property
    def _cache_key(self):
        return self._user.id

    @property
    def _data_key(self):
        data_key = f'{self._service_name}_{self._app}_{self._point}'
        data_key = f'{data_key}_{self._action}' if self._action else data_key
        return data_key

    @property
    def _cache(self):
        if self._memory_cache is None:
            all_cache_data = cache.get(self._cache_key)
            self._memory_cache = all_cache_data.get(self._data_key) if all_cache_data else None
            if self._memory_cache and os.getenv('IS_ENABLE_CACHE_LOG', False):
                print(f"GET REDIS {self}")
        return self._memory_cache

    @_cache.setter
    def _cache(self, value: any):
        if value is not None:
            data = cache.get(self._cache_key)
            ext_data = self._memory_cache = {f'{self._data_key}': value}
            data = dict(**data, **ext_data) if data else ext_data
            cache.set(self._cache_key, data, self._cache_period)

    def flush_cache(self):
        cache.delete(self._cache_key)

    def create(self, payload: dict):
        super().create(payload)
        self.flush_cache()

    def update(self, payload: dict):
        super().update(payload)
        self.flush_cache()


class BaseAPI:
    """For requests between microservices"""
    _contract = None
    _sort_by = 'id'
    _service_name = None
    _app = None
    _point = None
    _action = None

    def __init__(self, user: User, lookup_field_value: str = None):
        if os.getenv('IS_ENABLE_CACHE_LOG', False):
            print(f'NEW: {self}')
        if not user.is_authenticated:
            raise NotAuthenticated('User must be authonticated.')
        self._response = None
        self._cache = None
        self._lookup_field_value = lookup_field_value
        self._serivce = DjangoRequest(
            service=self._service_name,
            path=self._path,
            user=user
        )

    def all(self) -> tuple:
        return self._sorted_data

    def first(self) -> OrderedDict:
        result = self.all()
        return result[0] if len(result) > 0 else None

    def last(self) -> OrderedDict:
        result = self.all()
        return result[-1] if len(result) > 0 else None

    def filter(self, **kwargs) -> tuple:
        if not kwargs:
            raise FilterAttrNotSet('Set filter attr. Example: status="NEW"')
        key, value = next(iter(kwargs.items()))
        result = [item for item in self._sorted_data if item.get(key) == value]
        return tuple(result)

    def filter_first(self, **kwargs) -> OrderedDict:
        result = self.filter(**kwargs)
        return result[0] if len(result) > 0 else None

    def filter_last(self, **kwargs) -> OrderedDict:
        result = self.filter(**kwargs)
        return result[-1] if len(result) > 0 else None

    def get(self) -> OrderedDict:
        if self._lookup_field_value is None:
            raise LookupFieldValueNone('Fill lookup_field_value')
        result = self._sorted_data
        return result[0]

    def create(self, payload: dict):
        self._response = self._serivce.post(payload=payload)
        self._handle_create_error()

    def update(self, payload: dict):
        if self._lookup_field_value is None:
            raise LookupFieldValueNone('Fill lookup_field_value')
        self._response = self._serivce.put(payload=payload)
        self._handle_update_error()

    def get_response(self):
        """do not use @property"""
        return self._response

    @property
    def _sorted_data(self) -> tuple:
        if self._sort_by is None:
            raise SortByNotSet('Set key for sort or False')
        validated_data = self._validated_data
        sorted_data = sorted(validated_data, key=lambda obj: obj[self._sort_by]) if self._sort_by else validated_data
        return tuple(sorted_data)

    @property
    def _validated_data(self) -> list:
        validated_data = self._get_contract().validated_data
        validated_data = [validated_data] if isinstance(validated_data, OrderedDict) else validated_data
        return validated_data

    def _get_contract(self):
        data = self._handle_pagination(self._get_initial_data())
        many = True if self._lookup_field_value is None else False
        contract = self._contract(data=data, many=many)
        contract.is_valid(raise_exception=True)
        if self._cache is None:
            self._cache = contract.data
        return contract

    def _get_initial_data(self) -> dict:
        if self._cache is not None:
            data = self._cache
        else:
            if os.getenv('IS_ENABLE_CACHE_LOG', False):
                print(f'GET MICROSRVICE {self}')
            response = self._serivce.get()
            setattr(self, 'response', response)
            data = response.json()
        return data

    @property
    def _path(self):
        path = f'/{self._app}/{self._point}'
        path = path if self._lookup_field_value is None else f'{path}/{self._lookup_field_value}'
        path = path if self._action is None else f'{path}/{self._action}'
        return path

    def _handle_create_error(self):
        response = self._response
        if response.status_code != HttpStatus.HTTP_201_CREATED:
            self.__raise_exception(response)

    def _handle_update_error(self):
        response = self._response
        if response.status_code != HttpStatus.HTTP_200_OK:
            self.__raise_exception(response)

    def __raise_exception(self, response):
        if HttpStatus.is_client_error(response.status_code):
            raise CreateObjectClientError(f'{response.status_code}:{self._service_name}:{self._path}:{response.json()}')
        raise CreateObjectServerError(f'{response.status_code}:{self._service_name}:{self._path}:{response.text}')

    @staticmethod
    def _handle_pagination(data):
        """Get current page and link on next page"""
        if isinstance(data, list) or None in (data.get('count'), data.get('results')):
            return data
        pagination = {
            'previous': data.get('previous'),
            'next': data.get('next'),
            'count': data.get('count'),
        }
        data = data.get('results')
        data = [dict(**entity, pagination=pagination) for entity in data]
        return data


class API(CacheMixin, BaseAPI):
    pass


class FlushCacheAPI(API):
    pass


# from django.contrib.auth import get_user_model
# from api.loans import OrderAPI
# User = get_user_model()
# user = User.objects.get(id=1)
# from api.loans import OrderAPI
# api = OrderAPI(user)
# api.all()
# api.flush_cache()

# class OrderApi(API):
#     _contract = contracts.OrdersContract
#     _cache_prefix = 'orders'
#     _service_name = 'loans'
#     _app = 'orders'
#     _point = 'order'
#
#
# class LoanApi(API):
#     _contract = contracts.LoansContract
#     _cache_prefix = 'loans'
#     _service_name = 'loans'
#     _app = 'loans'
#     _point = 'loan'
#
#
# class LoanOpenApi(API):
#     _contract = contracts.LoansContract
#     _cache_prefix = 'open_loans'
#     _service_name = 'loans'
#     _app = 'loans'
#     _point = 'loan'
#     _action = 'open'
#
#
# class ProfileApi(API):
#     _contract = contracts.RussianProfileContract
#     _cache_prefix = 'profile'
#     _sort_by = False
#     _service_name = 'profiles'
#     _app = 'profiles'
#     _point = 'russian-profile'
#
#
# class BankCardApi(API):
#     _contract = contracts.BankCardsContract
#     _cache_prefix = 'bank_cards'
#     _service_name = 'payments'
#     _app = 'bank_cards'
#     _point = 'bank-card'
#
#
# class StorageUserApi(API):
#     _contract = contracts.UserStorageContract
#     _cache_prefix = 'user_storage'
#     _service_name = 'storage'
#     _app = 'storage'
#     _point = 'user'
#
#
# class PayLoansApi(API):
#     _contract = contracts.PayLoansContract
#     _cache_prefix = 'pay_loans'
#     _service_name = 'loans'
#     _app = 'loans'
#     _point = 'pay'


class Contract(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PaginationContract(Contract):
    previous = serializers.URLField(allow_null=True)
    next = serializers.URLField(allow_null=True)
    count = serializers.IntegerField()
