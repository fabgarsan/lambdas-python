ALLOWED_LETTERS = {'A', 'T', 'C', 'G'}
DNA_WRONG_LETTERS = [
    "ATGCAT",
    "TGCATA",
    "GCATAT",
    "CATATG",
    "ATATNC",
    "TATGCB"
]
DNA_WRONG_ARRAY_SIZE = [
    "ATGCAT",
    "TGCATA",
    "GCATAT",
    "CATATG"
]
DNA_WRONG_ARRAY_GROUP_SIZE = [
    "ATGCAT",
    "TGCAT",
    "GCATAT",
    "CATATG",
    "ATATNC",
    "TATGCB"
]
DNA_HUMAN = [
    "ATGCAA",
    "TGCTGA",
    "CAAACT",
    "ATGCAG",
    "TGCTGA",
    "CATGCT"
]

DNA_MUTANT_VERTICALLY = [
    "ATGCAT",
    "TGCATT",
    "GCATAT",
    "CATATT",
    "ATATGC",
    "TATGCA"
]

DNA_MUTANT_HORIZONTALLY = [
    "TTTGTA",
    "ACGTAT",
    "CGTATA",
    "GTATAC",
    "TATACG",
    "ATACGT"
]

DNA_MUTANT_DIAGONAL = [
    "ATGCAA",
    "TACTGA",
    "CAAACT",
    "ATGCAG",
    "TGCTAA",
    "CATGCT"
]

DNA_MUTANT_DIAGONAL_FLIPPED = [
    "CATGCT",
    "TGCTAA",
    "ATGCAG",
    "CAAACT",
    "TACTGA",
    "ATGCAA"
]

DNA_TYPE_HUMAN = 'H'
DNA_TYPE_MUTANT = 'M'

RESPONSE_ERROR_DNA_SIZE_WRONG = "Your DNA size must have 6 elements!"
RESPONSE_ERROR_DNA_GROUPS_SIZE_WRONG = "Your DNA elements must have 6 letters!"
RESPONSE_ERROR_DNA_LETTERS_WRONG = "Your DNA has some wrong letters!"
RESPONSE_ERROR_FORBIDDEN = "Not authorized request"
