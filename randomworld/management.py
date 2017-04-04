# -*- coding: utf-8 -*-
#
# ITerativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2012 ITerativ GmbH. All rights reserved.
#
# Created on Nov 24, 2013
# @author: maersu <me@maersu.ch>

# -*- coding: utf-8 -*-
import sys
from django.contrib.auth import get_user_model
from django.core.management import load_command_class
from django.core.management.base import NoArgsCommand
from djangojames.db.utils import reset_schema
from optparse import make_option, NO_DEFAULT

from randomworld.defaults import UserFactory, DUMMY_PASSWORD
from randomworld.names import name_factory


class LoadRandomData(NoArgsCommand):
    ignore_reset_default = False
    dummy_factories = [(UserFactory, 30)]


    option_list = NoArgsCommand.option_list + (
        make_option('-i', '--ignore_reset', action='store_true', dest='ignore_reset',
                    help='Do not extecute the reset command (equivalent to syncdb)'),
    )
    help = "Drops and recreates database and loads dummydata."

    def log(self, message):
        sys.stdout.write("%s\n" % message)

    def create_objects(self):
        for klass, count in self.dummy_factories:
            #self.log("create %s %s ..." % (count, klass.FACTORY_FOR.__name__))
            for i in range(count):
                klass().save()

    def handle_noargs(self, **options):
        from django.conf import settings
        from django.db import models
        from django.core.management.sql import emit_post_sync_signal
        from django.db.utils import DEFAULT_DB_ALIAS
        from django.core.management import call_command

        ignore_reset = options.get('ignore_reset')
        if ignore_reset is None:
            ignore_reset = self.ignore_reset_default

        db = options.get('database', DEFAULT_DB_ALIAS)
        database_config = settings.DATABASES[db]

        if not ignore_reset:
            reset_schema(database_config)

            # hack to avoid using south
            klass = load_command_class('django.core', 'syncdb')
            args = {}
            defaults = {}
            options['interactive'] = False
            for opt in klass.option_list:
                if opt.default is NO_DEFAULT:
                    defaults[opt.dest] = None
                else:
                    defaults[opt.dest] = opt.default
            defaults.update(options)
            klass.execute(*args, **defaults)

            # Emit the post sync signal. This allows individual
            # applications to respond as if the database had been
            # sync'd from scratch.
            emit_post_sync_signal(models.get_models(), 0, 0, db)

            call_command('migrate', fake=True)

        self.log("load Random Dummy data ...")

        try:
            user = get_user_model().objects.create_superuser('admin', 'admin@admin.dummy', DUMMY_PASSWORD)
            user.first_name, user.last_name = name_factory.get_full_name()
            user.save()
            self.log("superuser: admin")
        except Exception, e:
            self.log("WARNING: could not create superuser: %s" % str(e))

        self.create_objects()

        self.log("dummy passwords: %s" % DUMMY_PASSWORD)