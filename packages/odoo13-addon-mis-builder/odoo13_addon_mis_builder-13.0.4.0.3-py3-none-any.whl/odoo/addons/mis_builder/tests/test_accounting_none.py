# Copyright 2014 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from ..models import accounting_none
from .common import load_doctests

load_tests = load_doctests(accounting_none)
