from django.test import TestCase
from django.dispatch.dispatcher import _make_id
from django.db.models.signals import m2m_changed, pre_delete, post_delete, pre_save, post_save


class NoSignalTestCase(TestCase):
    def _receiver_in_lookup_keys(self, receiver, lookup_keys):
        """
        Evaluate if the receiver is in the provided lookup_keys; instantly terminates when found.
        """
        for key in lookup_keys:
            #           print('%s - %s - %s' % (key[0], receiver[0][1], key[1]))
            if (receiver[0][0] == key[0] or key[0] is None) and receiver[0][1] == key[1]:
                return True
        return False

    def _find_allowed_receivers(self, receivers, lookup_keys):
        """
        Searches the receivers, keeping any that have a lookup_key in the lookup_keys list
        """
        kept_receivers = []
        for receiver in receivers:
            if self._receiver_in_lookup_keys(receiver, lookup_keys):
                kept_receivers.append(receiver)
        return kept_receivers

    def _create_lookup_keys(self, sender_receivers_tuple_list):
        """
        Creates a signal lookup keys from the provided array of tuples.
        """
        lookup_keys = []

        for keep in sender_receivers_tuple_list:
            receiver = keep[0]
            sender = keep[1]
            lookup_key = (_make_id(receiver) if receiver else receiver, _make_id(sender))
            lookup_keys.append(lookup_key)
        return lookup_keys

    def _remove_disallowed_receivers(self, receivers, lookup_keys):
        """
        Searches the receivers, discarding any that have a lookup_key in the lookup_keys list
        """
        kept_receivers = []
        for receiver in receivers:
            if not self._receiver_in_lookup_keys(receiver, lookup_keys):
                kept_receivers.append(receiver)
        return kept_receivers

    def setUp(self, sender_receivers_to_keep=None, sender_receivers_to_discard=None):
        """
        Turns off signals from other apps

        The `sender_receivers_to_keep` can be set to an array of tuples (reciever, sender,), preserving matching signals.
        The `sender_receivers_to_discard` can be set to an array of tuples (reciever, sender,), discarding matching signals.
            with both, you can set the `receiver` to None if you want to target all signals for a model
        """
        super(NoSignalTestCase, self).setUp()
        self.m2m_changed_receivers = m2m_changed.receivers
        self.pre_delete_receivers = pre_delete.receivers
        self.pre_save_receivers = pre_save.receivers
        self.post_delete_receivers = post_delete.receivers
        self.post_save_receivers = post_save.receivers

        new_m2m_changed_receivers = []
        new_pre_delete_receivers = []
        new_pre_save_receivers = []
        new_post_delete_receivers = []
        new_post_save_receivers = []

        if sender_receivers_to_keep:
            lookup_keys = self._create_lookup_keys(sender_receivers_to_keep)
            new_m2m_changed_receivers = self._find_allowed_receivers(self.m2m_changed_receivers, lookup_keys)
            new_pre_delete_receivers = self._find_allowed_receivers(self.pre_delete_receivers, lookup_keys)
            new_pre_save_receivers = self._find_allowed_receivers(self.pre_save_receivers, lookup_keys)
            new_post_delete_receivers = self._find_allowed_receivers(self.post_delete_receivers, lookup_keys)
            new_post_save_receivers = self._find_allowed_receivers(self.post_save_receivers, lookup_keys)

        if sender_receivers_to_discard:
            lookup_keys = self._create_lookup_keys(sender_receivers_to_discard)

            new_m2m_changed_receivers = self._remove_disallowed_receivers(
                new_m2m_changed_receivers or self.m2m_changed_receivers, lookup_keys)
            new_pre_delete_receivers = self._remove_disallowed_receivers(
                new_pre_delete_receivers or self.pre_delete_receivers, lookup_keys)
            new_pre_save_receivers = self._remove_disallowed_receivers(
                new_pre_save_receivers or self.pre_save_receivers, lookup_keys)
            new_post_delete_receivers = self._remove_disallowed_receivers(
                new_post_delete_receivers or self.post_delete_receivers, lookup_keys)
            new_post_save_receivers = self._remove_disallowed_receivers(
                new_post_save_receivers or self.post_save_receivers, lookup_keys)

        m2m_changed.receivers = new_m2m_changed_receivers
        pre_delete.receivers = new_pre_delete_receivers
        pre_save.receivers = new_pre_save_receivers
        post_delete.receivers = new_post_delete_receivers
        post_save.receivers = new_post_save_receivers

    def tearDown(self):
        """
        Restores the signals that were turned off.
        """
        super(NoSignalTestCase, self).tearDown()
        m2m_changed.receivers = self.m2m_changed_receivers
        pre_delete.receivers = self.pre_delete_receivers
        pre_save.receivers = self.pre_save_receivers
        post_delete.receivers = self.post_delete_receivers
        post_save.receivers = self.post_save_receivers
