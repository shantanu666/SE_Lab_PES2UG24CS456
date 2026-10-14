# Issues found in `music_catalog.py`

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection risk in song insert | Bandit B608 / CWE-89 | 9-10 | The SQL insert used a formatted string with `%s` placeholders inside a literal SQL statement, allowing untrusted input to alter query structure. | Use parameterized SQLite queries such as `INSERT INTO songs (title, artist, plays) VALUES (?, ?, ?)` and pass values as arguments. |
| Unsafe pickle use | Bandit B403 / B301, CWE-502 | 1, 33 | The module imported `pickle` and deserialized untrusted data with `pickle.loads()`, which is unsafe for untrusted input. | Replace pickling with a safer serialization format such as JSON and use `json.dumps()` / `json.loads()`. |
| Insecure random selection | Bandit B311 / CWE-330 | 16-17 | `random.choice()` was used for selecting a song, which is not suitable for security-sensitive randomness. | Use `secrets.choice()` for non-deterministic selection where stronger randomness is required. |
| Dangerous mutable default argument | Pylint W0102 | 9 | `playlist=[]` created a shared mutable object across calls and could produce unexpected state. | Use `playlist=None` and initialize inside the function. |
| Bare except block | Flake8 E722 / Pylint W0702 | 38-41 | `except:` without an exception type hides errors and makes debugging harder. | Catch a specific exception type or remove the try/except and return a safe default directly. |
| Style and maintainability problems | Flake8 E501 / E741 / E701, Pylint C0116, C0103 | Various | The code had long lines, ambiguous variable names, multiple statements on one line, and function names not matching Python conventions. | Rename functions to snake_case, add docstrings, split long lines, and simplify code formatting. |
