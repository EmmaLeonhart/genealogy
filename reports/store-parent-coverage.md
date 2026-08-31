# Are the parents on Wikidata actually in our store?

**Emma, 2026-08-15:** *"I was under the assumption that… we would have
effectively covered the entirety of the wikidata network that would ever run
into this issue… My impression was it was pretty much entirely 20th-century
people who are not like this."*

Every missing parent is a row in `reports/store-parent-coverage.csv`.

## The answer

- **2,248,462** items in the store
- **1,529,832** parent statements (`P22` + `P25`) across them
- **34,151** point at an item the store does not hold (**2.2%**)
- **32,670** distinct people are named as a parent and not held
- **25,319** of **911,453** items with any recorded parent are missing at least one (**2.8%**)

## By the CHILD's century

**The child's date, not the parent's** — we do not hold the parent, so the
parent has no date to read. This is a *lower bound* on the parent's era, not
an estimate of it: a missing parent of somebody born 1950 is a 20th-century
case, a missing parent of somebody born 1200 is not. No date is inferred.

| child's century | parent statements | missing | missing rate |
| --- | ---: | ---: | ---: |
| BCE | 3,457 | 56 | 1.6% |
| 1s | 521 | 4 | 0.8% |
| 101s | 426 | 4 | 0.9% |
| 201s | 544 | 8 | 1.5% |
| 301s | 617 | 7 | 1.1% |
| 401s | 1,128 | 7 | 0.6% |
| 501s | 1,421 | 9 | 0.6% |
| 601s | 1,539 | 20 | 1.3% |
| 701s | 1,906 | 26 | 1.4% |
| 801s | 2,123 | 28 | 1.3% |
| 901s | 3,360 | 27 | 0.8% |
| 1001s | 6,081 | 71 | 1.2% |
| 1101s | 9,225 | 172 | 1.9% |
| 1201s | 12,174 | 312 | 2.6% |
| 1301s | 14,236 | 578 | 4.1% |
| 1401s | 21,009 | 659 | 3.1% |
| 1501s | 38,587 | 721 | 1.9% |
| 1601s | 81,854 | 1,470 | 1.8% |
| 1701s | 158,460 | 1,552 | 1.0% |
| 1801s | 346,473 | 2,146 | 0.6% |
| 1901s | 334,319 | 1,880 | 0.6% |
| 2001s | 17,824 | 93 | 0.5% |
| no birth date | 472,548 | 24,301 | 5.1% |

Undated children are their own row and are never distributed across the
dated ones — they are a large share, and folding them in would manufacture
whatever the dated part already suggested.
