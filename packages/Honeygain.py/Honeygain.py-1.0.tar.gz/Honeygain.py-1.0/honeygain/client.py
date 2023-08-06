from pydantic import parse_obj_as

from .exceptions import ClientException
from .http import HoneygainHTTP
from .schemas import UserProfile, Device, TermsOfService, \
    ReferralEarnings, TodayStats, DailyStats, \
    Balance, HoneygainBalance, WalletStats


def _requires_login(func):
    def wrapper(*args, **kwargs):
        # self is accessible because it's called from a Client instance
        if not args[0].http.is_logged_in:
            raise ClientException('You must log in first.')

        return func(*args, **kwargs)

    return wrapper


class Client:
    def __init__(self):
        """
        A Client that communicates with the HoneyGain API.
        """
        self.http = HoneygainHTTP()

    @property
    def token(self):
        return self.http.token

    @token.setter
    def token(self, account_token):
        if self.http.is_logged_in:
            raise ClientException('You must logout first')

        self.http.prepare()
        self.http.token = account_token

    def login(self, email, password):
        if self.http.is_logged_in:
            raise ClientException('You must logout first')

        # Clean up session and fetch our token
        self.http.prepare()
        token = self.http.get_token(email, password)
        self.token = token

    @_requires_login
    def get_profile(self) -> UserProfile:
        data = self.http.get_me().get('data')
        return UserProfile(**data)

    @_requires_login
    def get_devices(self):
        data = self.http.get_devices().get('data')
        return parse_obj_as(list[Device], data)

    @_requires_login
    def get_tos(self) -> TermsOfService:
        data = self.http.get_tos().get('data')
        return TermsOfService(**data)

    @_requires_login
    def get_monthly_stats(self) -> list[DailyStats]:
        data = self.http.get_stats()
        parsed: list[dict] = [{'date': k, **v} for k, v in data.items()]

        return parse_obj_as(list[DailyStats], parsed)

    @_requires_login
    def get_jt_monthly_stats(self) -> list[DailyStats]:
        data = self.http.get_jt_stats()
        parsed: list[dict] = [{'date': k, **v} for k, v in data.items()]

        return parse_obj_as(list[DailyStats], parsed)

    @_requires_login
    def get_today_earnings(self) -> TodayStats:
        data = self.http.get_earnings_today()
        return TodayStats(**data)

    @_requires_login
    def get_jt_today_earnings(self) -> TodayStats:
        data = self.http.get_jt_earnings_today()
        return TodayStats(**data)

    @_requires_login
    def get_referral_earnings(self) -> ReferralEarnings:
        data = self.http.get_referral_earnings()
        return ReferralEarnings(**data)

    @_requires_login
    def get_balance(self) -> HoneygainBalance:
        data = self.http.get_balance().get('data')
        return HoneygainBalance(**data)

    @_requires_login
    def get_jt_balance(self) -> Balance:
        data = self.http.get_jt_balance().get('data')
        return Balance(**data)

    @_requires_login
    def get_wallet_stats(self) -> list[WalletStats]:
        data = self.http.get_wallet_stats().get('data')
        parsed: list[dict] = [{'date': k, **v} for k, v in data.items()]

        return parse_obj_as(list[WalletStats], parsed)
