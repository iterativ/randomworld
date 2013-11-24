# -*- coding: utf-8 -*-
#
# ITerativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2012 ITerativ GmbH. All rights reserved.
#
# Created on Nov 24, 2013
# @author: maersu <me@maersu.ch>
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import factory
from randomworld.names import name_factory


class DefaultFactoryMixin(object):
    @classmethod
    def get_defaults(cls):
        return {}

    @classmethod
    def _prepare(cls, create, **kwargs):
        args = cls.get_defaults()
        for key, value in args.items():
            kwargs[key] = kwargs.get(key, value)

        return super(DefaultFactoryMixin, cls)._prepare(create, **kwargs)

UserKlass = get_user_model()
_user = UserKlass()
DUMMY_PASSWORD = 'test'
_user.set_password(DUMMY_PASSWORD)
DUMMY_PASSWORD_HASH = _user.password

class UserFactory(DefaultFactoryMixin, factory.Factory):
    FACTORY_FOR = UserKlass

    @classmethod
    def get_defaults(cls):
        first_name, last_name = name_factory.get_full_name(unique=True)
        username = slugify(u'{0}-{1}'.format(first_name, last_name).lower())
        email = '%s@%s.dy' % (username, slugify(last_name))

        return {
            'first_name': first_name,
            'last_name': last_name,
            'password': DUMMY_PASSWORD_HASH,
            'username': username,
            'email': email
        }
