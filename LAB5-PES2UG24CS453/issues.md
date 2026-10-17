# Static Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection risk | Security - medium | `register_pet` | Pet data was inserted into SQL with string formatting, so a name or species containing quotes could alter the query. | Use SQLite parameter placeholders and pass values separately. |
| Mutable default argument | Correctness - medium | `register_pet` | The default `tags=[]` list was shared between calls, allowing one registration to affect another. | Use `None` as the default and create a new list inside the function. |
| Broad and bare exception handling | Reliability - medium | `oldest_available`, `clear_unadopted` | The code hid unexpected database errors and made failures difficult to diagnose. | Handle the empty query result explicitly and remove unnecessary exception handling. |
| Import-time demonstration | Maintainability - medium | module bottom | Importing the module inserted records and printed output as a side effect. | Call `main()` only inside an `if __name__ == "__main__"` guard. |
| Predictable adoption code | Security - low | `adoption_code` | The standard pseudo-random generator is not intended for codes that may need to be difficult to guess. | Use `secrets.randbelow` to generate the numeric code. |
| Missing documentation | Maintainability - low | module and functions | The module and public functions had no docstrings, making their purpose and behavior unclear. | Add concise docstrings to the module and each function. |
| Non-standard names | Style - low | function definitions | CamelCase function names did not follow Python's snake_case convention. | Rename functions to `register_pet`, `adoption_code`, `oldest_available`, `clear_unadopted`, and `shelter_status`. |
| Long and compound lines | Style - low | table creation, SQL, status | Several lines exceeded the configured length and the status function used multiple statements on one line. | Wrap SQL and conditionals across readable lines. |