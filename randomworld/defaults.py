# -*- coding: utf-8 -*-
#
# ITerativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2012 ITerativ GmbH. All rights reserved.
#
# Created on Nov 24, 2013
# @author: maersu <me@maersu.ch>

import random
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.encoding import force_unicode
import factory
from randomworld.names import name_factory
from django.contrib.auth.models import Group
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.utils.text import slugify


class DefaultFactoryMixin(object):
    @classmethod
    def get_defaults(cls):
        return {}

    @classmethod
    def _prepare(cls, create, **kwargs):
        cls.kwargs = kwargs
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
        # do not overwrite kwargs
        first_name = force_unicode(cls.kwargs.get('first_name', first_name))
        last_name = force_unicode(cls.kwargs.get('last_name', last_name))

        username = slugify(u'{0}-{1}'.format(first_name, last_name).lower())
        email = '%s@%s.dy' % (username, slugify(last_name))

        return {
            'first_name': first_name,
            'last_name': last_name,
            'password': DUMMY_PASSWORD_HASH,
            'username': username,
            'email': email
        }


class StaffFactory(UserFactory):
    is_staff = True
    is_superuser = True


class FlatPageFactory(factory.Factory):
    FACTORY_FOR = FlatPage
    title = factory.LazyAttribute(lambda o: name_factory.get_noun(unique=True))
    content = factory.LazyAttribute(lambda o: name_factory.get_html(count=random.randint(10, 50)))
    url = factory.LazyAttribute(lambda o: '/%s/' % slugify(unicode(o.title)))
    registration_required = factory.LazyAttribute(lambda o: bool(random.getrandbits(1)))

    @classmethod
    def _prepare(cls, create, **kwargs):
        page = super(FlatPageFactory, cls)._prepare(create, **kwargs)
        page.save()
        page.sites.add(Site.objects.get_current())
        return page
