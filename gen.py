#!/usr/bin/env python3
import json
import os
from dataclasses import dataclass
from pprint import pprint  # DEBUG
from typing import Any, Union, Sequence
import sys

from bs4 import BeautifulSoup
from requests import request

_T_JSON = dict[str, Any]
_KWARGS = _T_JSON


class PerchanceApi:

    __GLITCH_DOMAIN_ENVAR = 'GLITCH_DOMAIN'
    __GLITCH_DOMAIN = os.environ.get(__GLITCH_DOMAIN_ENVAR)
    __GLITCH_BASE_URL = f'https://{__GLITCH_DOMAIN}.glitch.me/api'

    __GENERATOR_ENVAR = 'KANKAGEN_PERCHANCE_GENERATOR_ID'
    __PERCHANCE_GENERATOR = os.environ.get(__GENERATOR_ENVAR) or ''

    @classmethod
    def _request(cls, generator: str) -> str:
        resp = request(
            'GET', f'{cls.__GLITCH_BASE_URL}?generator={generator}&list=output')
        body = resp.content.decode('latin1')
        return body

    @classmethod
    def get_character_background(cls) -> dict[str, str]:
        KEYS = ('Motivation', 'Personality',
                'Quirks', 'Convictions', 'Occupation')

        resp = cls._request(cls.__PERCHANCE_GENERATOR)
        cup = BeautifulSoup(resp, 'html5lib')

        result: dict[str, str] = dict()
        for idx, element in enumerate(cup.find_all('div')):
            # out of bounds exceptions should throw here.
            result[KEYS[idx]] = element.decode_contents().strip()

        return result


class KankaApi:

    __API_TOKEN_ENVAR = 'KANKA_API_TOKEN'
    __API_TOKEN = os.environ.get(__API_TOKEN_ENVAR)

    __CAMPAIGN_ID_ENVAR = 'KANKA_CAMPAIGN_ID'
    __CAMPAIGN_ID = CAMPAIGN_ID = os.environ.get(__CAMPAIGN_ID_ENVAR)

    KANKA_BASE_URL = 'https://kanka.io/api/1.0/'
    HEADERS = {
        'Authorization': f'Bearer {__API_TOKEN}',
        'Content-Type': 'application/json'
    }

    @classmethod
    def _request(cls, method: str, path: str, **kwargs: _KWARGS) -> _T_JSON:
        resp = request(
            method, f'{cls.KANKA_BASE_URL}{path}',
            headers=cls.HEADERS,
            **kwargs
        )
        body = resp.content.decode('latin1')
        data: _T_JSON = json.loads(body)
        return data

    @classmethod
    def get_profile(cls) -> _T_JSON:
        return cls._request('GET', 'profile')

    @classmethod
    def get_campaigns(cls) -> _T_JSON:
        return cls._request('GET', 'campaigns')

    @classmethod
    def create_character(cls, data: _T_JSON) -> _T_JSON:
        data = cls._request(
            'POST', f'campaigns/{cls.__CAMPAIGN_ID}/characters',
            json=data
        )
        return {
            'url': f"https://kanka.io/en/campaign/{cls.__CAMPAIGN_ID}/characters/{data['data'].get('id')}"
        }


@dataclass
class Personality:

    traits: dict[str, str]

    def to_json(self) -> dict[str, list[str]]:

        names: list[str] = list()
        entries: list[str] = list()

        for k, v in self.traits.items():
            names.append(k)
            entries.append(v)

        return {
            'personality_name': names,
            'personality_entry': entries
        }


@dataclass
class Character:

    name: str
    gender: str

    personality: Personality

    def to_json(self) -> dict[str, Union[str, list[str]]]:
        return {
            'name': self.name,
            'sex': self.gender,
            **self.personality.to_json()
        }


def main(argv: Sequence[Any]) -> None:

    name: str
    gender: str
    if len(argv) < 2:
        print('usage: gen NAME GENDER')
        sys.exit(1)
    else:
        name = argv[0]
        gender = argv[1]

    background = PerchanceApi.get_character_background()
    personality = Personality(background)
    character = Character(name, gender, personality)
    resp = KankaApi.create_character(character.to_json())
    pprint(resp)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
