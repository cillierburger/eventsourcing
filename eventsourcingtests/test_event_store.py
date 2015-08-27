import unittest
from eventsourcing.infrastructure.stored_events import InMemoryStoredEventRepository
from eventsourcing.infrastructure.event_store import EventStore
from eventsourcingtests.test_domain_events import Example


class TestEventStore(unittest.TestCase):

    def test(self):
        repo = InMemoryStoredEventRepository()
        event_store = EventStore(stored_event_repo=repo)

        # Check there are zero stored events in the repo.
        entity_events = repo.get_entity_events('entity1')
        self.assertEqual(0, len(entity_events))

        # Store a domain event.
        event1 = Example.Event(entity_id='entity1', a=1, b=2)
        event_store.append(event1)

        # Check there is one stored event in the repo.
        entity_events = repo.get_entity_events('entity1')
        self.assertEqual(1, len(entity_events))

        # Store another domain event.
        event1 = Example.Event(entity_id='entity1', a=1, b=2)
        event_store.append(event1)

        # Check there are two stored events in the repo.
        entity_events = repo.get_entity_events('entity1')
        self.assertEqual(2, len(entity_events))