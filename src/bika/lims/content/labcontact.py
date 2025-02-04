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
# Copyright 2018-2021 by it's authors.
# Some rights reserved, see README and LICENSE.

from AccessControl import ClassSecurityInfo
from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.fields import UIDReferenceField
from senaite.core.browser.widgets.referencewidget import ReferenceWidget
from bika.lims.catalog.bikasetup_catalog import SETUP_CATALOG
from bika.lims.config import PROJECTNAME
from bika.lims.content.contact import Contact
from bika.lims.content.person import Person
from bika.lims.interfaces import IDeactivable
from bika.lims.interfaces import IHaveDepartment
from bika.lims.interfaces import ILabContact
from Products.Archetypes import atapi
from Products.Archetypes.Field import ImageField
from Products.Archetypes.Field import ImageWidget
from Products.Archetypes.public import registerType
from Products.CMFPlone.utils import safe_unicode
from zope.interface import implements

schema = Person.schema.copy() + atapi.Schema((

    ImageField(
        "Signature",
        widget=ImageWidget(
            label=_("Signature"),
            description=_(
                "Upload a scanned signature to be used on printed "
                "analysis results reports. Ideal size is 250 pixels "
                "wide by 150 high"),
        ),
    ),

    UIDReferenceField(
        "Departments",
        required=0,
        allowed_types=("Department",),
        vocabulary="_departmentsVoc",
        multiValued=1,
        widget=ReferenceWidget(
            label=_("Departments"),
            description=_("The laboratory departments"),
        ),
    ),

    UIDReferenceField(
        "DefaultDepartment",
        required=0,
        allowed_types=("Department",),
        widget=ReferenceWidget(
            label=_("Default Department"),
            description=_("Default Department"),
            showOn=True,
            catalog_name=SETUP_CATALOG,
            base_query={
                "is_active": True,
                "sort_on": "sortable_title",
                "sort_order": "ascending"
            },
        ),
    ),
))

schema["JobTitle"].schemata = "default"
# Don't make title required - it will be computed from the Person's Fullname
schema["title"].required = 0
schema["title"].widget.visible = False
schema["Department"].required = 0
schema["Department"].widget.visible = False


class LabContact(Contact):
    """A Lab Contact, which can be linked to a System User
    """
    implements(ILabContact, IHaveDepartment, IDeactivable)

    schema = schema
    displayContentsTab = False
    security = ClassSecurityInfo()
    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def Title(self):
        """Return the contact's Fullname as title
        """
        return safe_unicode(self.getFullname()).encode("utf-8")

    @security.public
    def getDepartment(self):
        """Required by IHaveDepartment. Returns the list of departments this
        laboratory contact is assigned to plus the default department
        """
        departments = self.getDepartments() + [self.getDefaultDepartment()]
        return filter(None, list(set(departments)))

    @security.public
    def getDefaultDepartment(self):
        """Returns the assigned default department

        :returns: Department object
        """
        return self.getField("DefaultDepartment").get(self)

    def hasUser(self):
        """Check if contact has user
        """
        username = self.getUsername()
        if not username:
            return False
        user = api.get_user(username)
        return user is not None

    def _departmentsVoc(self):
        """Vocabulary of available departments
        """
        query = {
            "portal_type": "Department",
            "is_active": True
        }
        results = api.search(query, "senaite_catalog_setup")
        items = map(lambda dept: (api.get_uid(dept), api.get_title(dept)),
                    results)
        dept_uids = map(api.get_uid, results)
        # Currently assigned departments
        depts = self.getDepartments()
        # If one department assigned to the Lab Contact is disabled, it will
        # be shown in the list until the department has been unassigned.
        for dept in depts:
            uid = api.get_uid(dept)
            if uid in dept_uids:
                continue
            items.append((uid, api.get_title(dept)))

        return api.to_display_list(items, sort_by="value", allow_empty=False)


    def addDepartment(self, dep):
        """Adds a department

        :param dep: UID or department object
        :returns: True when the department was added
        """
        if api.is_uid(dep):
            dep = api.get_object_by_uid(dep)
        deps = self.getDepartments()
        if dep not in deps:
            return False
        deps.append(dep)
        self.setDepartments(deps)
        return True

    def removeDepartment(self, dep):
        """Removes a department

        :param dep: UID or department object
        :returns: True when the department was removed
        """
        if api.is_uid(dep):
            dep = api.get_object_by_uid(dep)
        deps = self.getDepartments()
        if dep not in deps:
            return False
        deps.remove(dep)
        self.setDepartments(deps)
        return True


registerType(LabContact, PROJECTNAME)
