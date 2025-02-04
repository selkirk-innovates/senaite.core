# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2023 by it's authors.
# Some rights reserved, see README and LICENSE.

from AccessControl import getSecurityManager
from plone.app.contentmenu.menu import \
    DisplaySubMenuItem as BaseDisplaySubMenuItem
from plone.app.contentmenu.menu import \
    FactoriesSubMenuItem as BaseFactoriesSubMenuItem
from plone.app.contentmenu.menu import \
    PortletManagerSubMenuItem as BasePortletManagerSubMenuItem
from plone.app.contentmenu.menu import \
    WorkflowSubMenuItem as BaseWorkflowSubMenuItem
from plone.memoize.instance import memoize
from plone.portlets.interfaces import ILocalPortletAssignable
from senaite.core.interfaces import IShowDisplayMenu
from senaite.core.interfaces import IShowFactoriesMenu


class DisplaySubMenuItem(BaseDisplaySubMenuItem):
    """The "Display" Menu
    """
    @memoize
    def available(self):
        return IShowDisplayMenu.providedBy(self.context)


class FactoriesSubMenuItem(BaseFactoriesSubMenuItem):
    """The "Add" Menu
    """

    @memoize
    def available(self):
        return IShowFactoriesMenu.providedBy(self.context)


class PortletManagerSubMenuItem(BasePortletManagerSubMenuItem):
    """The "Manage Portlets" Menu
    """
    @memoize
    def available(self):
        secman = getSecurityManager()
        has_manage_portlets_permission = secman.checkPermission(
            "Manage portal",
            self.context
        )
        if not has_manage_portlets_permission:
            return False
        else:
            return ILocalPortletAssignable.providedBy(self.context)


class WorkflowSubMenuItem(BaseWorkflowSubMenuItem):
    """The Workflow Menu
    """

    def available(self):
        return super(WorkflowSubMenuItem, self).available()
