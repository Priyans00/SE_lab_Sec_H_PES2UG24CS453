# Reflection

## 1. Which tool found the most useful issues, and why?

Pylint found the broadest set of issues because it checked documentation, naming,
exception handling, mutable defaults, global state, and formatting. Bandit was
especially useful for identifying the SQL injection risk, which is more important
than a purely stylistic warning.

## 2. Which issue was the highest priority?

The interpolated SQL was the highest priority because untrusted pet data could
change the meaning of a database statement. Parameterized queries remove that
injection risk while keeping the same database behavior.

## 3. Were any findings difficult to fix or potentially false positives?

The warning about `random.randint` was not a false positive: an adoption code can
be guessed because the standard generator is not designed for security-sensitive
values. Replacing it with `secrets.randbelow` is a small change. The global-state
warning required a behavior decision, so the shelter status now derives from the
database instead of maintaining a separate adoption counter.

## 4. What would you do next in a production project?

I would add automated tests for registration, adoption, empty shelters, quoted
input, repeated calls with default tags, and cleanup. I would also use a persistent
database with transactions, validate input values such as age, and run Pylint,
Flake8, and Bandit in continuous integration so regressions are caught before
deployment.