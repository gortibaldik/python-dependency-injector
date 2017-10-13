"""Dependency injector base providers unit tests."""

import unittest2 as unittest

from dependency_injector import (
    providers,
    errors,
)


class ProviderTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.Provider()

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.provider))

    def test_call(self):
        self.assertRaises(NotImplementedError, self.provider.__call__)

    def test_delegate(self):
        delegate1 = self.provider.delegate()

        self.assertIsInstance(delegate1, providers.Delegate)
        self.assertIs(delegate1(), self.provider)

        delegate2 = self.provider.delegate()

        self.assertIsInstance(delegate2, providers.Delegate)
        self.assertIs(delegate2(), self.provider)

        self.assertIsNot(delegate1, delegate2)

    def test_provider(self):
        delegate1 = self.provider.provider

        self.assertIsInstance(delegate1, providers.Delegate)
        self.assertIs(delegate1(), self.provider)

        delegate2 = self.provider.provider

        self.assertIsInstance(delegate2, providers.Delegate)
        self.assertIs(delegate2(), self.provider)

        self.assertIsNot(delegate1, delegate2)

    def test_override(self):
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)
        self.assertTrue(self.provider.overridden)
        self.assertIs(self.provider.last_overriding, overriding_provider)

    def test_overriding_context(self):
        overriding_provider = providers.Provider()
        with self.provider.override(overriding_provider):
            self.assertTrue(self.provider.overridden)
        self.assertFalse(self.provider.overridden)

    def test_override_with_itself(self):
        self.assertRaises(errors.Error, self.provider.override, self.provider)

    def test_override_with_not_provider(self):
        obj = object()
        self.provider.override(obj)
        self.assertIs(self.provider(), obj)

    def test_reset_last_overriding(self):
        overriding_provider1 = providers.Provider()
        overriding_provider2 = providers.Provider()

        self.provider.override(overriding_provider1)
        self.provider.override(overriding_provider2)

        self.assertIs(self.provider.overridden[-1], overriding_provider2)
        self.assertIs(self.provider.last_overriding, overriding_provider2)

        self.provider.reset_last_overriding()
        self.assertIs(self.provider.overridden[-1], overriding_provider1)
        self.assertIs(self.provider.last_overriding, overriding_provider1)

        self.provider.reset_last_overriding()
        self.assertFalse(self.provider.overridden)
        self.assertIsNone(self.provider.last_overriding)

    def test_reset_last_overriding_of_not_overridden_provider(self):
        self.assertRaises(errors.Error, self.provider.reset_last_overriding)

    def test_reset_override(self):
        overriding_provider = providers.Provider()
        self.provider.override(overriding_provider)

        self.assertTrue(self.provider.overridden)
        self.assertEqual(self.provider.overridden, (overriding_provider,))

        self.provider.reset_override()

        self.assertEqual(self.provider.overridden, tuple())

    def test_deepcopy(self):
        provider = providers.Provider()

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Provider)

    def test_deepcopy_from_memo(self):
        provider = providers.Provider()
        provider_copy_memo = providers.Provider()

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_overridden(self):
        provider = providers.Provider()
        overriding_provider = providers.Provider()

        provider.override(overriding_provider)

        provider_copy = providers.deepcopy(provider)
        overriding_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Provider)

        self.assertIsNot(overriding_provider, overriding_provider_copy)
        self.assertIsInstance(overriding_provider_copy, providers.Provider)

    def test_repr(self):
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.'
                         'Provider() at {0}>'.format(hex(id(self.provider))))


class ObjectProviderTests(unittest.TestCase):

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(providers.Object(object())))

    def test_call_object_provider(self):
        obj = object()
        self.assertIs(providers.Object(obj)(), obj)

    def test_call_overridden_object_provider(self):
        obj1 = object()
        obj2 = object()
        provider = providers.Object(obj1)
        provider.override(providers.Object(obj2))
        self.assertIs(provider(), obj2)

    def test_deepcopy(self):
        provider = providers.Object(1)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Object)

    def test_deepcopy_from_memo(self):
        provider = providers.Object(1)
        provider_copy_memo = providers.Provider()

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_overridden(self):
        provider = providers.Object(1)
        overriding_provider = providers.Provider()

        provider.override(overriding_provider)

        provider_copy = providers.deepcopy(provider)
        overriding_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Object)

        self.assertIsNot(overriding_provider, overriding_provider_copy)
        self.assertIsInstance(overriding_provider_copy, providers.Provider)

    def test_repr(self):
        some_object = object()
        provider = providers.Object(some_object)
        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'Object({0}) at {1}>'.format(
                             repr(some_object),
                             hex(id(provider))))


class DelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Provider()
        self.delegate = providers.Delegate(self.delegated)

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.delegate))

    def test_init_with_not_provider(self):
        self.assertRaises(errors.Error, providers.Delegate, object())

    def test_call(self):
        delegated1 = self.delegate()
        delegated2 = self.delegate()

        self.assertIs(delegated1, self.delegated)
        self.assertIs(delegated2, self.delegated)

    def test_repr(self):
        self.assertEqual(repr(self.delegate),
                         '<dependency_injector.providers.'
                         'Delegate({0}) at {1}>'.format(
                             repr(self.delegated),
                             hex(id(self.delegate))))


class ExternalDependencyTests(unittest.TestCase):

    def setUp(self):
        self.provider = providers.ExternalDependency(instance_of=list)

    def test_init_with_not_class(self):
        self.assertRaises(TypeError, providers.ExternalDependency, object())

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.provider))

    def test_call_overridden(self):
        self.provider.provided_by(providers.Factory(list))
        self.assertIsInstance(self.provider(), list)

    def test_call_overridden_but_not_instance_of(self):
        self.provider.provided_by(providers.Factory(dict))
        self.assertRaises(errors.Error, self.provider)

    def test_call_not_overridden(self):
        self.assertRaises(errors.Error, self.provider)

    def test_deepcopy(self):
        provider = providers.ExternalDependency(int)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.ExternalDependency)

    def test_deepcopy_from_memo(self):
        provider = providers.ExternalDependency(int)
        provider_copy_memo = providers.Provider()

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_overridden(self):
        provider = providers.ExternalDependency(int)
        overriding_provider = providers.Provider()

        provider.override(overriding_provider)

        provider_copy = providers.deepcopy(provider)
        overriding_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.ExternalDependency)

        self.assertIsNot(overriding_provider, overriding_provider_copy)
        self.assertIsInstance(overriding_provider_copy, providers.Provider)

    def test_repr(self):
        self.assertEqual(repr(self.provider),
                         '<dependency_injector.providers.'
                         'ExternalDependency({0}) at {1}>'.format(
                             repr(list),
                             hex(id(self.provider))))
