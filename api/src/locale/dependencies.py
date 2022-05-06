import re

import i18n

from typing import Any, Protocol

from fastapi import Request

from src.config import LocalizationConfiguration


class Translator(Protocol):
    def __call__(self, expression: str, **kwargs: Any) -> str:
        ...


# Extracts (language, quality) pairs from Accept-Language header.
# For example, following header:
# "fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5,"
# will produce pairs:
# ('fr', ''), ('fr', '0.9'), ('en', '0.8'), ('de', '0.7'), ('*', '0.5'),
# Note that all blocks have to end with comma for this to work
_ACCEPT_LANGUAGE_REGEXP = re.compile(
    r'((?:[a-zA-Z\*\-]{2}|\*))[a-zA-Z\*\-]*(?:;q=((?:0\.?\d{0,3}|1)))?\,'
)


def _parse_header(header: str) -> list[str]:
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language

    # Required for regexp to work, all blocks have to end with a comma
    if not header.endswith(','):
        header += ','

    pairs = _ACCEPT_LANGUAGE_REGEXP.findall(header)
    for i, (lang, q) in enumerate(pairs):
        pairs[i] = lang, (float(q) if q else 1)

    sorted_pairs = sorted(pairs, key=lambda p: p[1], reverse=True)
    return [lang for lang, _ in sorted_pairs]


def _get_translator_from_locale(locale: str) -> Translator:
    return lambda expression, **kwargs: i18n.t(expression, locale=locale, **kwargs)


def get_translator(request: Request) -> Translator:
    config: LocalizationConfiguration = request.app.app_state.config.localization

    header: str = request.headers.get('accept-language') or ''
    accepted_langs = _parse_header(header)
    for lang in accepted_langs:
        if lang in config.available_locales:
            return _get_translator_from_locale(lang)
        if lang == '*':
            return _get_translator_from_locale(config.fallback_locale)

    return _get_translator_from_locale(config.fallback_locale)
