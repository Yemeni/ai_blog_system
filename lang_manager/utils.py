def get_active_languages():
    from .models import Language
    return [
        {'code': lang.code, 'name': lang.name}
        for lang in Language.objects.filter(is_active=True)
    ]
