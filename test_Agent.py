from unittest import TestCase

from Agent import *


class TestKnowledgeBase(TestCase):
    def setUp(self):
        self.KB = KnowledgeBase(5)
        self.at = Cell(1, 1)
        self.test = Cell(1, 2)

    def test_ask_with_no_percepts(self):
        self.KB = KnowledgeBase(5)
        self.KB.tell(Visited(self.at))
        self.assertEqual(self.KB.askSafe(self.test.x, self.test.y), True)

    def test_ask_with_smell(self):
        self.KB = KnowledgeBase(5)
        KB = KnowledgeBase(5)
        KB.tell(Smell(self.at))
        self.assertEqual(KB.askSafe(self.test.x, self.test.y), False)

    # +-+-+-+
    # | |W| |
    # +-+-+-+
    # | |S|?|
    # +-+-+-+
    # | |V|V|
    # +-+-+-+
    def test_ask_with_one_neighbor_safe(self):
        self.KB = KnowledgeBase(5)
        KB = KnowledgeBase(5)
        KB.tell(Smell(Cell(1, 1)))
        KB.tell(Visited(Cell(1, 2)))
        KB.tell(Visited(Cell(2, 2)))
        self.assertEqual(KB.askSafe(2, 1), True)

    # +-+-+-+
    # | |W| |
    # +-+-+-+
    # | |S|?|
    # +-+-+-+
    # | |V|S|
    # +-+-+-+
    def test_ask_with_no_known_neighbors_safe(self):
        self.KB = KnowledgeBase(5)
        KB = KnowledgeBase(5)
        KB.tell(Smell(Cell(1, 1)))
        KB.tell(Visited(Cell(1, 2)))
        KB.tell(Smell(Cell(2, 2)))
        self.assertEqual(KB.askSafe(2, 1), False)

    # +-+-+-+
    # | | | |
    # +-+-+-+
    # | |g|?|
    # +-+-+-+
    # | | | |
    # +-+-+-+
    def test_ask_gold_one_known(self):
        self.KB = KnowledgeBase(5)
        KB = KnowledgeBase(5)
        KB.tell(Glitter(Cell(1, 1)))
        self.assertEqual(KB.askGold(2, 1), True)

    # +-+-+-+
    # | | | |
    # +-+-+-+
    # | |g|?|
    # +-+-+-+
    # | | |V|
    # +-+-+-+
    def test_ask_gold_neighbor_no_glitter(self):
        self.KB = KnowledgeBase(5)
        KB = KnowledgeBase(5)
        KB.tell(Glitter(Cell(1, 1)))
        KB.tell(Visited(Cell(2, 2)))
        self.assertEqual(KB.askGold(2, 1), False)

    # +-+-+-+
    # | | | |
    # +-+-+-+
    # | |g|?|
    # +-+-+-+
    # | | |G|
    # +-+-+-+
    def test_ask_gold_neighbor_glitter(self):
        self.KB = KnowledgeBase(5)
        KB = KnowledgeBase(5)
        KB.tell(Glitter(Cell(1, 1)))
        KB.tell(Glitter(Cell(2, 2)))
        self.assertEqual(KB.askGold(2, 1), True)