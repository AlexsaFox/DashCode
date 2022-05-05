import i18n

from src.config import LocalizationConfiguration


def set_up_locale(config: LocalizationConfiguration):
    i18n.set('filename_format', '{locale}.{format}')
    i18n.set('file_format', 'yaml')
    i18n.set('fallback', config.fallback_locale)
    i18n.set('available_locales', config.available_locales)

    i18n.load_path.append('src/locale/translations')
