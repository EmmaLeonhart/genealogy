# Are the parents on Wikidata actually in our store?

**Emma, 2026-08-15:** *"I was under the assumption that… we would have
effectively covered the entirety of the wikidata network that would ever run
into this issue… My impression was it was pretty much entirely 20th-century
people who are not like this."*

Every missing parent is a row in `reports/store-parent-coverage.csv`.

## The answer

- **1,423,032** items in the store
- **1,528,454** parent statements (`P22` + `P25`) across them
- **34,104** point at an item the store does not hold (**2.2%**)
- **32,628** distinct people are named as a parent and not held
- **25,280** of **910,543** items with any recorded parent are missing at least one (**2.8%**)

## By the CHILD's century

**The child's date, not the parent's** — we do not hold the parent, so the
parent has no date to read. This is a *lower bound* on the parent's era, not
an estimate of it: a missing parent of somebody born 1950 is a 20th-century
case, a missing parent of somebody born 1200 is not. No date is inferred.

| child's century | parent statements | missing | missing rate |
| --- | ---: | ---: | ---: |
| BCE | 3,457 | 57 | 1.6% |
| 1s | 521 | 4 | 0.8% |
| 101s | 426 | 4 | 0.9% |
| 201s | 544 | 8 | 1.5% |
| 301s | 617 | 7 | 1.1% |
| 401s | 1,128 | 7 | 0.6% |
| 501s | 1,421 | 9 | 0.6% |
| 601s | 1,538 | 20 | 1.3% |
| 701s | 1,906 | 26 | 1.4% |
| 801s | 2,123 | 28 | 1.3% |
| 901s | 3,360 | 27 | 0.8% |
| 1001s | 6,081 | 71 | 1.2% |
| 1101s | 9,222 | 172 | 1.9% |
| 1201s | 12,170 | 312 | 2.6% |
| 1301s | 14,232 | 578 | 4.1% |
| 1401s | 21,000 | 659 | 3.1% |
| 1501s | 38,516 | 715 | 1.9% |
| 1601s | 81,775 | 1,469 | 1.8% |
| 1701s | 158,272 | 1,543 | 1.0% |
| 1801s | 345,923 | 2,133 | 0.6% |
| 1901s | 334,162 | 1,875 | 0.6% |
| 2001s | 17,824 | 93 | 0.5% |
| no birth date | 472,236 | 24,287 | 5.1% |

Undated children are their own row and are never distributed across the
dated ones — they are a large share, and folding them in would manufacture
whatever the dated part already suggested.
