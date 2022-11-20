# coding=utf8
"""sopel-senpainotice

Silly Sopel plugin to see if senpai will notice you.
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import random

import requests

from sopel import plugin
from sopel.config import types


class SenpaiNoticeSection(types.StaticSection):
    alternate_source = types.ValidatedAttribute('alternate_source')


def setup(bot):
    bot.config.define_section('senpainotice', SenpaiNoticeSection)

    url = bot.config.senpainotice.alternate_source
    if url is None:
        url = 'https://raw.githubusercontent.com/kmanion/senpai/master/senpai.txt'

    r = requests.get(url)
    bot.memory['senpai_notice_lines'] = [l.strip() for l in r.text.splitlines() if l]


def shutdown(bot):
    try:
        del bot.memory['senpai_notice_lines']
    except KeyError:
        pass


@plugin.commands('senpai', 'noticeme')
@plugin.output_prefix('[NOTICE ME] ')
def senpai_notice(bot, trigger):
    bot.say(random.choice(bot.memory['senpai_notice_lines']))
