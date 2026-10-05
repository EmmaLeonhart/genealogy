"""Print the frozen creation description and label inputs for Geni ids, using the functions
in build-garborg-day.py unchanged (pulled out with ast so the module's main is not run)."""
import ast, csv, gzip, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
src = (ROOT / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
keep = {"DATE_WORDS", "DESC_MAX", "_PLACE_QIDS", "_PLACE_LABELS", "normalise_date_case",
        "life_description", "place_qid", "place_label"}
mod = ast.parse(src); body = []
for n in mod.body:
    names = ({t.id for t in n.targets if isinstance(t, ast.Name)} if isinstance(n, ast.Assign)
             else {n.target.id} if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)
             else {n.name} if isinstance(n, ast.FunctionDef) else set())
    if names & keep or (isinstance(n, ast.Expr) is False and isinstance(n, (ast.Assign, ast.AugAssign))
                        and isinstance(n, ast.Assign) is False and False):
        body.append(n)
    if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and getattr(n.value.func, "attr", "") == "update" \
            and getattr(n.value.func.value, "id", "") == "DATE_WORDS":
        body.append(n)
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Subscript) and getattr(n.targets[0].value, "id", "") == "DATE_WORDS":
        body.append(n)
ns = {"ROOT": ROOT, "csv": csv}
exec(compile(ast.Module(body=body, type_ignores=[]), "bgd", "exec"), ns)
ids = set(sys.argv[1:])
def rows(name):
    p = ROOT / "reports" / name
    fh = gzip.open(str(p) + ".gz", "rt", encoding="utf-8") if not p.exists() else open(p, encoding="utf-8")
    for r in csv.DictReader(fh):
        g = r.get("geni_id") or r.get("id") or ""
        if g in ids: yield g, r
facts = dict(rows("derived-facts.csv")); places = dict(rows("derived-places.csv"))
for g in sys.argv[1:]:
    f = facts.get(g, {})
    print(g, "|", f.get("sex", ""), "|", ns["life_description"](f, places.get(g)), "|",
          {k: v for k, v in f.items() if k in ("name", "given", "surname", "birth_date_raw", "death_date_raw")})
