# -*- coding: utf-8 -*-
{
    'name': "Website Language Selector",

    'summary': """Move the language select to the menu""",

    'description': """Move the language select to the menu""",

    'author': "Safyric Co., Ltd.",
    'website': "https://www.safyric.com",

    'category': 'Website',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['website'],

    # always loaded
    'data': [
        'views/website_template.xml',
    ],
    'installable': True,
}
