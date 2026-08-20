# The fathers the patronymics imply

Built by `scripts/build-patronymic-fathers.py` on top of `reports/patronymic-classification.csv`, which decides what is a patronymic from the father, per Emma 2026-08-15. **It emits no edit.**

- bearers classified `patronymic (inferred, no father recorded)`: **18518**
- of those, a name is available from confirmed fathers: **12145**
- token has no confirmed father anywhere, so no name: **6373**
- **fathers to create: 9158**
  (4023 people merged into 1036 shared fathers under her same-mother rule)

## The name comes from real fathers, never from the string

`Olsen` implies **Ole** because that is what 1,809 confirmed `Olsen` fathers are called. An earlier version stripped the suffix and produced a father called **`Ols`**, which is what Emma meant by *"we already addressed this"*.

| implied father | bearers |
| --- | ---: |
| Ole | 900 |
| Peder | 593 |
| Lars | 499 |
| Anders | 463 |
| Jon | 410 |
| Erik | 348 |
| Nils | 339 |
| Rasmus | 279 |
| Hans | 271 |
| Ola | 258 |
| Johannes | 237 |
| Johan | 212 |
| Sven | 195 |
| Per | 181 |
| Jakob | 163 |
| Tore | 153 |
| Knut | 146 |
| Olof | 144 |
| Jens | 121 |
| Elling | 101 |
| Karl | 97 |
| Jørgen | 91 |
| Henrik | 90 |
| Kristen | 84 |
| Ivar | 83 |

## One per person, with the exception she named

*"If you don't know the people are siblings you create one per individual."* The exception is a shared mother plus the same implied name, and it fires for **4023 people forming 1036 shared fathers**. Where the names differ under one mother they are not merged.

## Sourcing

Each created father is sourced to **the Geni profile of the child whose patronymic attests him** (Emma, 2026-08-19).
