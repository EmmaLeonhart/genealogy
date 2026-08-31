# Are the parents on Wikidata actually in our store?

**Emma, 2026-08-15:** *"I was under the assumption that… we would have
effectively covered the entirety of the wikidata network that would ever run
into this issue… My impression was it was pretty much entirely 20th-century
people who are not like this."*

Every missing parent is a row in `reports/store-parent-coverage.csv`.

## The answer

- **2,255,560** items in the store
- **1,536,797** parent statements (`P22` + `P25`) across them
- **32,957** point at an item the store does not hold (**2.1%**)
- **31,538** distinct people are named as a parent and not held
- **24,388** of **916,017** items with any recorded parent are missing at least one (**2.7%**)

## By the CHILD's century

**The child's date, not the parent's** — we do not hold the parent, so the
parent has no date to read. This is a *lower bound* on the parent's era, not
an estimate of it: a missing parent of somebody born 1950 is a 20th-century
case, a missing parent of somebody born 1200 is not. No date is inferred.

| child's century | parent statements | missing | missing rate |
| --- | ---: | ---: | ---: |
| BCE | 3,461 | 57 | 1.6% |
| 1s | 521 | 4 | 0.8% |
| 101s | 430 | 5 | 1.2% |
| 201s | 546 | 3 | 0.5% |
| 301s | 619 | 7 | 1.1% |
| 401s | 1,130 | 6 | 0.5% |
| 501s | 1,425 | 9 | 0.6% |
| 601s | 1,550 | 20 | 1.3% |
| 701s | 1,936 | 32 | 1.7% |
| 801s | 2,154 | 32 | 1.5% |
| 901s | 3,385 | 24 | 0.7% |
| 1001s | 6,110 | 59 | 1.0% |
| 1101s | 9,313 | 128 | 1.4% |
| 1201s | 12,339 | 293 | 2.4% |
| 1301s | 14,355 | 568 | 4.0% |
| 1401s | 21,115 | 641 | 3.0% |
| 1501s | 38,727 | 681 | 1.8% |
| 1601s | 82,019 | 1,400 | 1.7% |
| 1701s | 158,725 | 1,447 | 0.9% |
| 1801s | 347,055 | 2,032 | 0.6% |
| 1901s | 335,472 | 1,760 | 0.5% |
| 2001s | 18,002 | 86 | 0.5% |
| no birth date | 476,408 | 23,663 | 5.0% |

Undated children are their own row and are never distributed across the
dated ones — they are a large share, and folding them in would manufacture
whatever the dated part already suggested.
