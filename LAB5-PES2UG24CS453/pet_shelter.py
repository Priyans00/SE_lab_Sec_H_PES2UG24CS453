"""Manage a small in-memory animal shelter adoption register."""

import secrets
import sqlite3


conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE pets (id INTEGER PRIMARY KEY, name TEXT, species TEXT, "
    "age INTEGER, adopted INTEGER)"
)


def register_pet(name, species, age, tags=None):
    """Register a pet and return the supplied tags with its species added."""
    if tags is None:
        tags = []
    conn.execute(
        "INSERT INTO pets (name, species, age, adopted) VALUES (?, ?, ?, 0)",
        (name, species, age),
    )
    tags.append(species)
    return tags


def adopt(pet_id):
    """Mark a pet as adopted by its database ID."""
    conn.execute("UPDATE pets SET adopted = 1 WHERE id = ?", (pet_id,))


def adoption_code():
    """Return a difficult-to-guess adoption code."""
    return f"PET-{secrets.randbelow(9000) + 1000}"


def oldest_available():
    """Return the name of the oldest available pet, if one exists."""
    row = conn.execute(
        "SELECT name FROM pets WHERE adopted = 0 ORDER BY age DESC"
    ).fetchone()
    return row[0] if row else None


def clear_unadopted():
    """Remove all pets that have not been adopted."""
    conn.execute("DELETE FROM pets WHERE adopted = 0")


def shelter_status():
    """Return whether the shelter has recorded any adoptions."""
    adopted = conn.execute(
        "SELECT COUNT(*) FROM pets WHERE adopted = 1"
    ).fetchone()[0]
    return "active" if adopted else "quiet"


def main():
    """Run the shelter demonstration."""
    register_pet("Bruno", "dog", 7)
    register_pet("Mitzi", "cat", 3)
    register_pet("Kiwi", "parrot", 12)
    adopt(1)
    print(oldest_available(), adoption_code(), shelter_status())
    clear_unadopted()


if __name__ == "__main__":
    main()
