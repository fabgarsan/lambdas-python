import random
import unittest

from utils.constants import (DNA_HUMAN, DNA_MUTANT_HORIZONTALLY, DNA_MUTANT_VERTICALLY, DNA_TYPE_HUMAN)
from utils.functions import is_mutant, save_dna, get_dna, update_dna, create_mutant, get_stats
from utils.db import db


class TestLambdaFunction(unittest.TestCase):
    def test_is_not_mutant(self):
        result = is_mutant(DNA_HUMAN)
        self.assertFalse(result)

    def test_is_mutant_vertically(self):
        result = is_mutant(DNA_MUTANT_VERTICALLY)
        self.assertTrue(result)

    def test_is_mutant_horizontally(self):
        result = is_mutant(DNA_MUTANT_HORIZONTALLY)
        self.assertTrue(result)

    def test_update_existing_dna(self):
        db.open_connection()
        db.begin_transaction()
        save_dna(''.join(DNA_HUMAN), DNA_TYPE_HUMAN)
        result = update_dna(''.join(DNA_HUMAN))
        self.assertEqual(result, 1)
        result = get_dna(''.join(DNA_HUMAN))
        (key, type, count) = result[0]
        self.assertEqual(key, ''.join(DNA_HUMAN))
        self.assertEqual(type, DNA_TYPE_HUMAN)
        self.assertEqual(count, 2)

        result = update_dna(''.join(DNA_HUMAN))
        self.assertEqual(result, 1)
        result = get_dna(''.join(DNA_HUMAN))
        (key, type, count) = result[0]
        self.assertEqual(key, ''.join(DNA_HUMAN))
        self.assertEqual(type, DNA_TYPE_HUMAN)
        self.assertEqual(count, 3)

        db.rollback()
        db.close_connection()

    def test_save_dna(self):
        db.open_connection()
        db.begin_transaction()
        result = save_dna(''.join(DNA_HUMAN), DNA_TYPE_HUMAN)
        self.assertEqual(result, 1)
        result = get_dna(''.join(DNA_HUMAN))
        (key, type, count) = result[0]
        self.assertEqual(key, ''.join(DNA_HUMAN))
        self.assertEqual(type, DNA_TYPE_HUMAN)
        self.assertEqual(count, 1)
        db.rollback()
        db.close_connection()

    def test_save_dna_duplicated_not_allowed(self):
        db.open_connection()
        db.begin_transaction()
        result = save_dna(''.join(DNA_HUMAN), DNA_TYPE_HUMAN)
        self.assertEqual(result, 1)
        result = save_dna(''.join(DNA_HUMAN), DNA_TYPE_HUMAN)
        self.assertFalse(result)
        db.rollback()
        db.close_connection()

    def test_create_mutant_fails_when_human_dna(self):
        db.open_connection()
        db.begin_transaction()
        result = create_mutant(DNA_HUMAN)
        self.assertFalse(result)
        db.rollback()
        db.close_connection()

    def test_create_mutant_successfully(self):
        db.open_connection()
        db.begin_transaction()
        result = create_mutant(DNA_MUTANT_HORIZONTALLY)
        self.assertTrue(result)
        result = create_mutant(DNA_MUTANT_HORIZONTALLY)
        self.assertTrue(result)
        db.rollback()
        db.close_connection()

    def test_get_stats(self):
        numbers_mutants_horizontally = random.randint(25, 50)
        numbers_mutants_vertically = random.randint(25, 50)
        numbers_humans = random.randint(80, 150)
        ratio = (numbers_mutants_horizontally + numbers_mutants_vertically) / numbers_humans
        db.open_connection()
        db.begin_transaction()

        for x in range(numbers_mutants_horizontally):
            create_mutant(DNA_MUTANT_HORIZONTALLY)

        for x in range(numbers_mutants_vertically):
            create_mutant(DNA_MUTANT_VERTICALLY)

        for x in range(numbers_humans):
            create_mutant(DNA_HUMAN)

        (count_mutant_dna, count_human_dna) = get_stats()[0]
        self.assertEqual(numbers_humans, count_human_dna)
        self.assertEqual(numbers_mutants_vertically + numbers_mutants_horizontally, count_mutant_dna)
        self.assertEqual(ratio, count_mutant_dna / count_human_dna)
        db.rollback()
        db.close_connection()
