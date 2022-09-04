from typing import Optional
from dataclasses import dataclass
import pytest


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
    if (movie.age_limit == 15 and 11 <= guest.age < movie.age_limit) and (
            supervised_by is not None and supervised_by.age >= 18):
        return True
    # grant access if movie age limit is 11, guest age is between 7 and 11,
    # has a supervisor who is older than 18
    if (movie.age_limit == 11 and 7 <= guest.age < movie.age_limit) and (
            supervised_by is not None and supervised_by.age >= 18):
        return True
    # grant access if movie age limit is 7, guest age is between 0 and 7,
    # has a supervisor who is older than 18
    if (movie.age_limit == 7 and 0 <= guest.age < movie.age_limit) and (
            supervised_by is not None and supervised_by.age >= 18):
        return True
    # otherwise, deny access to the movie
    return False


# movies
movie_no_age_limit = Movie(title="Kung Fu Panda")
movie_15_age_limit = Movie(title="Crouching Tiger, Hidden Dragon", age_limit=15)
movie_11_age_limit = Movie(title="Hero", age_limit=11)
movie_7_age_limit = Movie(title="Peppa Pigs", age_limit=7)

# guests
guest_19_yo = Visitor(name="Lucy Chen", age=19)
guest_16_yo = Visitor(name="Sofia Chen", age=16)
guest_12_yo = Visitor(name="Mama Chen", age=12)
guest_8_yo = Visitor(name="Anna Chen", age=8)
guest_6_yo = Visitor(name="Emily Chen", age=6)


@pytest.mark.parametrize(
    ("movie", "guest", "expected"),
    (
            # grant access if the movie has no age limit and guest is 19 (older than 15)
            (movie_no_age_limit, guest_19_yo, True),
            # deny access if the movie has no age limit and guest is 12 (younger than 15)
            (movie_no_age_limit, guest_12_yo, False),
            # grant access if the movie age limit is 15 and guest is 16
            (movie_15_age_limit, guest_16_yo, True),
            # deny access if the movie age limit is 15 and guest is 12
            (movie_15_age_limit, guest_12_yo, False),
            # grant access if the movie age limit is 11 and guest is 12
            (movie_11_age_limit, guest_12_yo, True),
            # deny access if the movie age limit is 11 and guest is 8
            (movie_11_age_limit, guest_8_yo, False),
            # grant access if the movie age limit is 7 and guest is 8
            (movie_7_age_limit, guest_8_yo, True),
            # deny access if the movie age limit is 7 and guest is 6
            (movie_7_age_limit, guest_6_yo, False)
    )
)
def test_guest_access_no_supervisor(movie, guest, expected):
    # GIVEN
    movie = movie
    guest = guest
    # WHEN
    expected = grant_access(guest=guest, movie=movie)
    # THEN
    assert expected is expected


@pytest.mark.parametrize(
    ("movie", "guest", "supervisor", "expected"),
    (
            # grant access if the movie has no age limit, the guest is 12 with a supervisor who is 19
            (movie_no_age_limit, guest_12_yo, guest_19_yo, True),
            # deny access if the movie has no age limit, the guest is 12 with a supervisor who is 16
            (movie_no_age_limit, guest_12_yo, guest_16_yo, False),
            # deny access if the movie has no age limit, the guest is 6 with a supervisor who is 19
            (movie_no_age_limit, guest_6_yo, guest_19_yo, False),
            # deny access if the movie has no age limit, the guest is 6 with a supervisor who is 16
            (movie_no_age_limit, guest_6_yo, guest_16_yo, False),
            # grant access if the movie has age limit 15, the guest is 12 with a supervisor who is 19
            (movie_15_age_limit, guest_12_yo, guest_19_yo, True),
            # deny access if the movie has age limit 15, the guest is 12 with a supervisor who is 16
            (movie_15_age_limit, guest_12_yo, guest_16_yo, False),
            # deny access if the movie has age limit 15, the guest is 8 with a supervisor who is 19
            (movie_15_age_limit, guest_8_yo, guest_19_yo, False),
            # deny access if the movie has age limit 15, the guest is 8 with a supervisor who is 16
            (movie_15_age_limit, guest_8_yo, guest_16_yo, False),
            # grant access if the movie has age limit 11, the guest is 8 with a supervisor who is 19
            (movie_11_age_limit, guest_8_yo, guest_19_yo, True),
            # deny access if the movie has age limit 11, the guest is 8 with a supervisor who is 16
            (movie_11_age_limit, guest_8_yo, guest_16_yo, False),
            # deny access if the movie has age limit 11, the guest is 6 with a supervisor who is 19
            (movie_11_age_limit, guest_6_yo, guest_19_yo, False),
            # deny access if the movie has age limit 11, the guest is 6 with a supervisor who is 12
            (movie_11_age_limit, guest_6_yo, guest_12_yo, False),
            # grant access if the movie has age limit 7, the guest is 6 with a supervisor who is 19
            (movie_7_age_limit, guest_6_yo, guest_19_yo, True),
            # deny access if the movie has age limit 7, the guest is 6 with a supervisor who is 16
            (movie_7_age_limit, guest_6_yo, guest_16_yo, False)
    )
)
def test_guest_access_supervisor(movie, guest, supervisor, expected):
    # GIVEN
    movie = movie
    guest = guest
    supervisor = supervisor
    # WHEN
    expected = grant_access(movie=movie, guest=guest, supervised_by=supervisor)
    # THEN
    assert expected is expected
