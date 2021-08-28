from utils.db import db
from utils.queries import save_dna_query, get_dna_query, update_dna_query, stats_query
import numpy as np

from utils.constants import ALLOWED_LETTERS, DNA_TYPE_MUTANT, DNA_TYPE_HUMAN


def create_mutant(raw_dna) -> bool:
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
