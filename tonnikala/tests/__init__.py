import unittest

from . import test_expressions, test_xml_templates


test_modules = [
    test_expressions,
    test_xml_templates
]

def create_test_suite(modules):
    suites = []
    for module in modules:
        suites.append(unittest.TestLoader().loadTestsFromModule(module))

    suite = unittest.TestSuite()
    suite.addTests(suites)
    return suite

test_all = create_test_suite(test_modules)
