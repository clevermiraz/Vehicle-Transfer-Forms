from app.services.money import amount_in_words, format_taka
from app.services.normalize import normalize_phone, normalize_registration


def test_taka_format_uses_lakh_grouping():
    assert format_taka(500000) == "5,00,000/-"
    assert format_taka(12500000) == "1,25,00,000/-"
    assert format_taka(999) == "999/-"


def test_amount_in_words():
    assert amount_in_words(500000) == "Five Lac"
    assert amount_in_words(1250000) == "Twelve Lac Fifty Thousand"
    assert amount_in_words(10000000) == "One Crore"
    assert amount_in_words(85550) == "Eighty Five Thousand Five Hundred Fifty"


def test_phone_normalization():
    assert normalize_phone("+880 1900-000001") == "01900000001"
    assert normalize_phone("৮৮০১৯০০০০০০০১") == "01900000001"


def test_registration_normalization_keeps_bangla_vowel_signs():
    assert normalize_registration("Dhaka Metro-GA 12-3456") == "DHAKAMETROGA123456"
    assert normalize_registration("ঢাকা মেট্রো-গ-১২") == "ঢাকামেট্রোগ12"
