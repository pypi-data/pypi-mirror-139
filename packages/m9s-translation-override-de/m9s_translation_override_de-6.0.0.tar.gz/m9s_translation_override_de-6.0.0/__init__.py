# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool

__all__ = ['register']


def register():
    Pool.register(
        module='translation_override_de', type_='model')
    Pool.register(
        module='translation_override_de', type_='wizard')
    Pool.register(
        module='translation_override_de', type_='report')
