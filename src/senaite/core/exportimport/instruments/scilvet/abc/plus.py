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

""" ScilVet abc Plus
"""
from senaite.core.exportimport.instruments.abaxis.vetscan.vs2 import \
    AbaxisVetScanCSVVS2Parser, AbaxisVetScanVS2Importer, Import as VS2Import

title = "ScilVet abc - Plus"


def Import(context, request):
    """
    We will use the same import logic as Abaxis VetScan VS2
    """
    return VS2Import(context, request)


class ScilVetabcPlusCSVParser(AbaxisVetScanCSVVS2Parser):
    """
    This instrument will use the same parser as Abaxis VetScan VS2
    """


class ScilVetabcPlusImporter(AbaxisVetScanVS2Importer):
    """
    This instrument will use the same importer as Abaxis VetScan VS2
    """
