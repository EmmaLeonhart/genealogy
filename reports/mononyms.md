# People recorded with one name and no surname

**53,827 mononyms** out of 870,356 people in the corpus.

Emma, 2026-08-18: *"if it repeats, it's a name. If it repeats over 10 times, I think that was our actual criterion. […] People with mononyms get a first name if it's a repeated name."*

| | people | |
| --- | ---: | --- |
| qualify for a `P735` given name | 1,339 | the token repeats 10+ times and is not a marker |
| a redaction or unknown marker | 40,711 | `Private`, `NN` — a person, but not a name |
| the token appears exactly once | 8,652 | too thin to call a name |

The qualifying people share just **65 distinct names**, which is the whole reason the rule is worth having: a handful of name items covers thousands of people.

Nothing in the repo handled mononyms before this. `genimerge.namelinks` splits a name into given and family parts and a mononym has no family part, so these people were never singled out either way.

## The most common mononyms that qualify

| name | people |
| --- | ---: |
| Anna | 75 |
| Anders | 70 |
| Lars | 46 |
| Maria | 45 |
| Olof | 44 |
| Nils | 42 |
| Erik | 40 |
| Johan | 32 |
| Per | 32 |
| Ukjent | 31 |
| Johannes | 30 |
| 未知 | 29 |
| Ingeborg | 28 |
| Ola | 28 |
| Hans | 27 |
| Isteri | 27 |
| Daughter | 23 |
| Jon | 23 |
| Karin | 22 |
| Peder | 22 |
| Ole | 21 |
| Brita | 20 |
| Knut | 19 |
| Marta | 19 |
| Abdullah | 18 |
| Ali | 17 |
| Okänd | 17 |
| .... | 16 |
| CHANDRA | 16 |
| Kerstin | 16 |
| Margareta | 16 |
| Son | 16 |
| Sven | 16 |
| Anne | 15 |
| Catarina | 15 |
| David | 15 |
| Jakob | 15 |
| Malin | 15 |
| Kari | 14 |
| N.N | 14 |
