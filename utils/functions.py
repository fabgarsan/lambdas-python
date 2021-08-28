from utils.custom_exceptions import BadRequestException
from utils.db import db
from utils.queries import save_dna_query, get_dna_query, update_dna_query, stats_query
import numpy as np

from utils.constants import (
    ALLOWED_LETTERS,
    DNA_TYPE_MUTANT,
    DNA_TYPE_HUMAN,
    RESPONSE_ERROR_DNA_LETTERS_WRONG,
    RESPONSE_ERROR_DNA_GROUPS_SIZE_WRONG,
    RESPONSE_ERROR_DNA_SIZE_WRONG
)


def validate_is_valid_dna_letters(raw_dna):
    letter_in_sequence = set(''.join(raw_dna))
    if not all(letter in ALLOWED_LETTERS for letter in letter_in_sequence):
        raise BadRequestException(message=RESPONSE_ERROR_DNA_LETTERS_WRONG)


def validate_is_valid_dna_proper_array(raw_dna):
    if len(raw_dna) != 6:
        raise BadRequestException(message=RESPONSE_ERROR_DNA_SIZE_WRONG)


def validate_is_valid_dna_proper_array_groups(raw_dna):
    if any(len(group) != 6 for group in raw_dna):
        raise BadRequestException(message=RESPONSE_ERROR_DNA_GROUPS_SIZE_WRONG)


def validate_is_valid_dna(raw_dna):
    validate_is_valid_dna_letters(raw_dna)
    validate_is_valid_dna_proper_array(raw_dna)
    validate_is_valid_dna_proper_array_groups(raw_dna)


def create_mutant(raw_dna) -> bool:
    validate_is_valid_dna(raw_dna)
    dna_plain_string = ''.join(raw_dna)
    result = update_dna(dna_plain_string)
    if result > 0:
        result = get_dna(dna_plain_string)
        (key, creation_type, count) = result[0]
        return DNA_TYPE_MUTANT == creation_type
    else:
        if is_mutant(raw_dna):
            save_dna(dna_plain_string, DNA_TYPE_MUTANT)
            return True
        else:
            save_dna(dna_plain_string, DNA_TYPE_HUMAN)
            return False


def save_dna(dna, type):
    return db.run_query(save_dna_query, (dna, type, 1))


def get_stats():
    return db.run_query(stats_query)


def calculate_ratio(count_mutant_dna, count_human_dna):
    try:
        return count_mutant_dna / count_human_dna
    except TypeError:
        if count_human_dna is None and count_mutant_dna is None:
            return 0
        elif count_human_dna is None:
            return 100
        else:
            return 0
    except ZeroDivisionError:
        return 100


def get_dna(dna):
    return db.run_query(get_dna_query, (dna,))


def update_dna(dna):
    return db.run_query(update_dna_query, (dna,))


def is_mutant_horizontally(sequence: str) -> bool:
    return any(np.sum(sequence == char) > 3 for char in ALLOWED_LETTERS)


def is_mutant(dna) -> bool:
    dna = np.array([list(sequence) for sequence in dna], dtype=np.str_)
    for element in dna:
        if is_mutant_horizontally(element):
            return True
    dna_transposed = dna.transpose()
    for element in dna_transposed:
        if is_mutant_horizontally(element):
            return True
    return False
