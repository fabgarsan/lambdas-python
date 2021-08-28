import random
import unittest

from utils.constants import (
    DNA_HUMAN,
    DNA_MUTANT_HORIZONTALLY,
    DNA_MUTANT_VERTICALLY,
    DNA_TYPE_HUMAN,
    DNA_WRONG_LETTERS,
    DNA_WRONG_ARRAY_GROUP_SIZE,
    RESPONSE_ERROR_DNA_LETTERS_WRONG,
    RESPONSE_ERROR_DNA_SIZE_WRONG,
    RESPONSE_ERROR_DNA_GROUPS_SIZE_WRONG
)

from utils.constants import DNA_WRONG_ARRAY_SIZE
from utils.custom_exceptions import BadRequestException
from utils.functions import (
    is_mutant,
    save_dna,
    get_dna,
    update_dna,
    create_mutant,
    get_stats,
    calculate_ratio,
    validate_is_valid_dna_letters,
    validate_is_valid_dna_proper_array,
    validate_is_valid_dna_proper_array_groups,
)
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

    def test_calculate_ratio(self):
        count_human_dna = random.randint(100, 150)
        count_mutant_dna = random.randint(25, 50)
        result = calculate_ratio(count_mutant_dna=count_mutant_dna, count_human_dna=count_human_dna)
        self.assertEqual(result, count_mutant_dna / count_human_dna)

    def test_calculate_ratio_human_none(self):
        count_mutant_dna = random.randint(25, 50)
        result = calculate_ratio(count_mutant_dna=count_mutant_dna, count_human_dna=None)
        self.assertEqual(result, 100)

    def test_calculate_ratio_mutant_none(self):
        count_human_dna = random.randint(25, 50)
        result = calculate_ratio(count_mutant_dna=None, count_human_dna=count_human_dna)
        self.assertEqual(result, 0)

    def test_calculate_ratio_mutant_none_human_none(self):
        result = calculate_ratio(count_mutant_dna=None, count_human_dna=None)
        self.assertEqual(result, 0)

    def test_calculate_ratio_human_zero(self):
        count_mutant_dna = random.randint(25, 50)
        result = calculate_ratio(count_mutant_dna=count_mutant_dna, count_human_dna=0)
        self.assertEqual(result, 100)

    def test_calculate_ratio_mutant_zero(self):
        count_human_dna = random.randint(25, 50)
        result = calculate_ratio(count_mutant_dna=0, count_human_dna=count_human_dna)
        self.assertEqual(result, 0)

    def test_validate_is_valid_dna_letters(self):
        validate_is_valid_dna_letters(DNA_HUMAN)
        validate_is_valid_dna_letters(DNA_MUTANT_HORIZONTALLY)
        validate_is_valid_dna_letters(DNA_MUTANT_VERTICALLY)

    def test_validate_is_valid_dna_letters_wrong_letters(self):
        try:
            validate_is_valid_dna_letters(DNA_WRONG_LETTERS)
        except BadRequestException as error:
            self.assertEqual(400, error.status_code)
            self.assertEqual(RESPONSE_ERROR_DNA_LETTERS_WRONG, error.message)

    def test_validate_is_valid_dna_proper_array(self):
        validate_is_valid_dna_proper_array(DNA_MUTANT_VERTICALLY)

    def test_validate_is_valid_dna_proper_array_wrong_size(self):
        try:
            validate_is_valid_dna_proper_array(DNA_WRONG_ARRAY_SIZE)
        except BadRequestException as error:
            self.assertEqual(400, error.status_code)
            self.assertEqual(RESPONSE_ERROR_DNA_SIZE_WRONG, error.message)

    def test_validate_is_valid_dna_proper_array_groups(self):
        validate_is_valid_dna_proper_array_groups(DNA_MUTANT_VERTICALLY)

    def test_validate_is_valid_dna_proper_array_groups_size(self):
        try:
            validate_is_valid_dna_proper_array_groups(DNA_WRONG_ARRAY_GROUP_SIZE)
        except BadRequestException as error:
            self.assertEqual(400, error.status_code)
            self.assertEqual(RESPONSE_ERROR_DNA_GROUPS_SIZE_WRONG, error.message)
