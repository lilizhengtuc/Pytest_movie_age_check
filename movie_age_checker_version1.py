"""
Uppgift 3.

På biografkedjan "Videobyn" har man utvecklat ett system för att släppa in
besökare automatiskt med BankID och biljett.
Man vill i detta system försäkra sig om att man utför lagstadgade ålderskontroller
i enlighet med Statens Medieråds åldersgränser. (Lag 2010:1882, §11, §6)

Enligt dessa så gäller följande regler:
- Åldersgränser finns för 15, 11 och 7 år.
- En film med 15 års åldersgräns kan ses av ett barn fyllt 11 år i vuxens sällskap.
- En film med 11 års åldersgräns kan ses av ett barn fyllt 7 år i vuxens sällskap.
- En film med 7 års åldersgräns kan ses av alla bran i vuxens sällskap.
- En vuxen måste vara 18 år fyllda och myndig, för uppgiftens skulle antar vi att
  man är myndig vid 18.
- Om filmen ej är granskad (`age_limit = None`) så antas 15 års-gräns. **(VG)**

I denna uppgiften ska vi driva fram utvecklingen av en funktion med hjälp av
TDD-principerna. Det vill säga, vi låter testerna driva utvecklingen.

A.  Översätt kraven ovan till mer formella specifikationer i formaten
    `GIVEN-WHEN-THEN`. Lägg dessa i tomma test-funktioner.
B.  Implementera `grant_access(...)`-funktionen utifrån de tester som finns från
    början.
C.  Utvidga dina test-fall genom att implementera testerna från uppgift A enligt
    specifikationerna du tagit fram.
D.  Implementera resten av `grant_access(...)`-funktionen, så att alla dina
    tester från C går igenom, koden bör nu uppfylla alla krav från uppgiften
    och ha tester som verifierar detta.
E.  Refaktorisera din kod (förbättra), dokumentera med doc-strings och kommenterar.
    Detta ska inte påverka funktion såvida du inte tidigare haft en bugg i din kod.

**(G, VG)**
----------------------------------------------------------------------
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class Visitor:
    # Besökarens namn
    name: str
    # Besökarens ålder
    age: int


@dataclass
class Movie:
    # Filmtitel
    title: str
    # Åldersgräns på filmen, None för unrated annars 7, 11 eller 15.
    age_limit: Optional[int] = None


def grant_access(movie: Movie, guest: Visitor, supervised_by: Optional[Visitor] = None) -> bool:
    """
    Returns true if guest is allowed to see the movie at hand.

    Optionally the guest can enter with a supervising adult (supervised_by),
    we have to ensure that this person is actually an adult.
    """
    # if the movie has no age limit, 15 is the default age limit
    if movie.age_limit is None:
        movie.age_limit = 15
    # grant access to the movie if the guest age is above age limit
    if guest.age >= movie.age_limit:
        return True
    # grant access if movie age limit is 15, guest age is between 11 and 15,
    # has a supervisor who is older than 18
    if (movie.age_limit == 15 and 11 <= guest.age < movie.age_limit) and (supervised_by is not None and supervised_by.age >= 18):
        return True
    # grant access if movie age limit is 11, guest age is between 7 and 11,
    # has a supervisor who is older than 18
    if (movie.age_limit == 11 and 7 <= guest.age < movie.age_limit) and (supervised_by is not None and supervised_by.age >= 18):
        return True
    # grant access if movie age limit is 7, guest age is between 0 and 7,
    # has a supervisor who is older than 18
    if (movie.age_limit == 7 and 0 <= guest.age < movie.age_limit) and (supervised_by is not None and supervised_by.age >= 18):
        return True
    # otherwise, deny access to the movie
    return False


# 8 happy path test cases
def test_grant_access_age_limit_15():
    # GIVEN a movie with age limit 15 and a guest who is 17
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=15)
    guest_1 = Visitor(name="Sylvester Wileborne", age=17)
    # WHEN the guest tries to access the movie
    access = grant_access(guest=guest_1, movie=the_leather_patch_movie)
    # THEN the access it granted
    assert access is True


def test_grant_access_age_limit_11():
    # GIVEN a movie with age limit 11 and a guest who is 12
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=11)
    guest_1 = Visitor(name="Sylvester Wileborne", age=12)
    # WHEN the guest tries to access the movie
    access = grant_access(guest=guest_1, movie=the_leather_patch_movie)
    # THEN the access it granted
    assert access is True


def test_grant_access_age_limit_7():
    # GIVEN a movie with age limit 7 and a guest who is 7
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=7)
    guest_1 = Visitor(name="Sylvester Wileborne", age=7)
    # WHEN the guest tries to access the movie
    access = grant_access(guest=guest_1, movie=the_leather_patch_movie)
    # THEN the access it granted
    assert access is True


def test_grant_access_age_limit_15_with_right_supervisor():
    # GIVEN a movie with age limit 15, a guest who is 14, and a supervisor who is 18
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=15)
    guest_0 = Visitor(name="Alfred Willeborne", age=14)
    guest_1 = Visitor(name="Sylvester Willeborne", age=18)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it granted
    assert access is True


def test_grant_access_age_limit_11_with_right_supervisor():
    # GIVEN a movie with age limit 11, a guest who is 8, and a supervisor who is 20
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=11)
    guest_0 = Visitor(name="Alfred Willeborne", age=8)
    guest_1 = Visitor(name="Sylvester Willeborne", age=20)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it granted
    assert access is True


def test_grant_access_age_limit_7_with_right_supervisor():
    # GIVEN a movie with age limit 7, a guest who is 6, and a supervisor who is 18
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=7)
    guest_0 = Visitor(name="Alfred Willeborne", age=6)
    guest_1 = Visitor(name="Sylvester Willeborne", age=18)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it granted
    assert access is True


def test_grant_access_no_age_limit_with_no_supervisor():
    # GIVEN a movie with no age limit, a guest who is 16
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=None)
    guest_0 = Visitor(name="Alfred Willeborne", age=16)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0)
    # THEN the access it granted
    assert access is True


def test_grant_access_no_age_limit_with_right_supervisor():
    # GIVEN a movie with no age limit, a guest who is 12, and a supervisor who is 19
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=None)
    guest_0 = Visitor(name="Alfred Willeborne", age=12)
    guest_1 = Visitor(name="Sylvester Willeborne", age=19)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it granted
    assert access is True


# 11 sad path test cases
def test_deny_access_age_limit_15_with_no_supervisor():
    # GIVEN a movie with age limit 15, a guest who is 10
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=15)
    guest_0 = Visitor(name="Alfred Willeborne", age=10)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0)
    # THEN the access it denied
    assert access is False


def test_deny_access_age_limit_15_with_wrong_supervisor():
    # GIVEN a movie with age limit 15, a guest who is 14, and a supervisor who is 17
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=15)
    guest_0 = Visitor(name="Alfred Willeborne", age=14)
    guest_1 = Visitor(name="Sylvester Willeborne", age=17)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it denied
    assert access is False


def test_deny_access_age_limit_15_with_wrong_guest_right_supervisor():
    # GIVEN a movie with age limit 15, a guest who is 10, and a supervisor who is 20
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=15)
    guest_0 = Visitor(name="Alfred Willeborne", age=10)
    guest_1 = Visitor(name="Sylvester Willeborne", age=20)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it denied
    assert access is False


def test_deny_access_age_limit_11_with_no_supervisor():
    # GIVEN a movie with age limit 11, a guest who is 8
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=11)
    guest_0 = Visitor(name="Alfred Willeborne", age=8)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0)
    # THEN the access it denied
    assert access is False


def test_deny_access_age_limit_11_with_wrong_supervisor():
    # GIVEN a movie with age limit 11, a guest who is 9, and a supervisor who is 16
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=11)
    guest_0 = Visitor(name="Alfred Willeborne", age=9)
    guest_1 = Visitor(name="Sylvester Willeborne", age=16)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it denied
    assert access is False


def test_deny_access_age_limit_11_with_wrong_guest_right_supervisor():
    # GIVEN a movie with age limit 11, a guest who is 6, and a supervisor who is 20
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=11)
    guest_0 = Visitor(name="Alfred Willeborne", age=6)
    guest_1 = Visitor(name="Sylvester Willeborne", age=20)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it denied
    assert access is False


def test_deny_access_age_limit_7_with_no_supervisor():
    # GIVEN a movie with age limit 7, a guest who is 6
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=7)
    guest_0 = Visitor(name="Alfred Willeborne", age=6)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0)
    # THEN the access it denied
    assert access is False


def test_deny_access_age_limit_7_with_wrong_supervisor():
    # GIVEN a movie with age limit 7, a guest who is 6, and a supervisor who is 15
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=7)
    guest_0 = Visitor(name="Alfred Willeborne", age=6)
    guest_1 = Visitor(name="Sylvester Willeborne", age=15)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it denied
    assert access is False


def test_deny_access_no_age_limit_with_no_supervisor():
    # GIVEN a movie with no age limit, a guest who is 14
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=None)
    guest_0 = Visitor(name="Alfred Willeborne", age=14)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0)
    # THEN the access it denied
    assert access is False


def test_deny_access_no_age_limit_with_wrong_supervisor():
    # GIVEN a movie with no age limit, a guest who is 14, and a supervisor who is 17
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=None)
    guest_0 = Visitor(name="Alfred Willeborne", age=14)
    guest_1 = Visitor(name="Sylvester Willeborne", age=17)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0)
    # THEN the access it denied
    assert access is False


def test_deny_access_no_age_limit_with_wrong_guest_right_supervisor():
    # GIVEN a movie with no age limit, a guest who is 10, and a supervisor who is 18
    the_leather_patch_movie = Movie(title="Läderlappen", age_limit=None)
    guest_0 = Visitor(name="Alfred Willeborne", age=10)
    guest_1 = Visitor(name="Sylvester Willeborne", age=18)
    # WHEN the guest tries to access the movie
    access = grant_access(movie=the_leather_patch_movie, guest=guest_0, supervised_by=guest_1)
    # THEN the access it denied
    assert access is False