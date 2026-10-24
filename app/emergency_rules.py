"""
SuFix — Acil Durum Kural Motoru (TODO.md Bölüm 3.2 ve Bölüm 6.3)

NOT: Can güvenliği riski içeren durumlar YZ'ye bırakılmaz.
Deterministik kural motoruyla yakalanır ve doğrudan KRİTİK olarak işaretlenir.
"""
import re
from typing import Tuple, Optional

ACIL_DURUM_KALIPLARI = [
    r"\bduman\b",
    r"\bgaz\s*kokusu\b",
    r"\bkıvılcım\b",
    r"\byangın\b",
    r"\belektrik\s*çarp(tı|ması)\b",
    r"\bsu\s*baskını\b",
    r"\basansörde\s*mahsur\b",
    r"\bpatlama\b"
]

ACIL_UYARI_MESAJI = (
    "⚠️ Bildirdiğin durum acil olabilir. Bildirimin en yüksek öncelikle (KRİTİK) iletildi. "
    "Can güvenliği riski varsa lütfen hemen 112'yi ve kampüs güvenliğini (0332 223 00 00) ara."
)

def acil_durum_kontrolu(metin: str) -> Tuple[bool, Optional[str]]:
    """
    Kullanıcı mesajında acil can güvenliği tehdidi olup olmadığını kontrol eder.
    Dönen değer: (acil_mi, eslesen_kural)
    """
    metin_kucuk = metin.lower()
    for kalip in ACIL_DURUM_KALIPLARI:
        if re.search(kalip, metin_kucuk, re.IGNORECASE):
            return True, kalip
    return False, None

