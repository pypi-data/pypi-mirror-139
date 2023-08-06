# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.translation_override_de.tests.test_translation_override_de import suite
except ImportError:
    from .test_translation_override_de import suite

__all__ = ['suite']
