# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_slots', 'django_slots.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'django-slots',
    'version': '0.2.6',
    'description': 'django_slots = inclusion tag + blocks',
    'long_description': '# django_slots\n\nAllows multiline strings to be captured and passed to template tags.\n\n## Demo\n\n1. Register a component\n  \n```python\n# app/templatetags/component_tags.py\nfrom django_slots import Library, Component\n\nregister = Library()\n\n\n@register.block_component\nclass Details(Component):\n  pass\n```\n\n2. Create a template\n\n```html+django\n{# app/templates/components/details.html #}\n<details>\n<summary>{{ summary|default:slots.summary }}</summary>\n{{ slot }}\n</details>\n```\n\nUsage:\n\n```html+django\n{% load component_tags %}\n{% load slot_tags %}\n\n{% details summary="the summary" %}\n  the default slot\n{% /details %}\n\n{% details %}\n  {% slot summary %}the <b>summary</b>{% /slot %}\n  the default slot\n{% /details %}\n```\n\n## Installation\n\n```shell\npip install django-slots\n```\n\n```python\nINSTALLED_APPS = [\n    # ...\n    \n    \'django_slots\',\n]\n```\n\n## Slots\n\nUse `{% slot name %}{% /slot %}` to capture and name a slot. These slots will be available in the template in a dictionary called `slots`. eg `{{ slots.name }}`.\n\nAny lines not surrounded by a slot tag will be available in thh component template as `{{ slot }}`.\n\n## Custom name\n\nBy default, the template tag name will be the Component class name converted to snake case. Use the `name` attribute to override.\n\neg:\n\n```python\nfrom django_slots import Component, Library\n\nregister = Library()\n\n\n@register.inline_component\nclass Button(Component):\n    name = \'btn\'\n```\n\n```html+django\n{% btn %}\n```\n\n## Change tag name\n\nBy default, inline tags are named `"{name}/"` and block tags are named `"{name}", "/{name}"`. To change this format specify `inline_tag_name` and `block_tag_names` attributes.\n\neg:\n\n```python\nfrom django_slots import Component, Library\n\nregister = Library()\n\n\nclass AppComponent(Component):\n    inline_tag_name = "{name}end"\n    block_tag_names = "{name}", "end{name}"    \n\n    \n@register.component\nclass Button(AppComponent):\n    pass\n```\n\n```html+django\n{% buttonend %}\n\n{% button %}{% endbutton %}\n```\n\n## Inline only template tag\n\nUse `@register.inline_component` to only allow `{% inline/ %}` use.\n\n## Block only template tag\n\nUse `@register.block_component` to only allow `{% block %}{% /block %}` use.\n\n## Validate arguments\n\nImplement `def get_content_data(slots, **kwargs)` to validate arguments. \n\neg:\n\n```python\nfrom django_slots import Component, Library\n\nregister = Library()\n\n\n@register.component\nclass Button(Component):\n    STYLE = ["primary", "secondary"]\n    def get_context_data(self, slots, *, style: str):\n        if style not in self.STYLE:\n            raise self.validation_error(f"style {style!r} not in {self.STYLE!r}")\n        return super().get_context_data(slots, style=style)\n```\n\n## Namespace components\n\nComponents can be namespaced which is useful for creating a third party app.\n\n```python\nfrom django_slots import Library, Component\n\nregister = Library()\n\n\nclass NHSUKComponent(Component):\n    namespace = \'nhsuk\'\n\n\n@register.component\nclass Button(NHSUKComponent):\n    pass\n```\n\n```html+django\n{% nhsuk:button %}\n  Save and continue\n{% /nhsuk:button %}\n```\n\nSee https://github.com/nwjlyons/nhsuk-components\n',
    'author': 'Neil Lyons',
    'author_email': 'nwjlyons@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nwjlyons/django_slots',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
