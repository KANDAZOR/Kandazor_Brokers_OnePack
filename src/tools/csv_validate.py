"""
Valida CSVs (schema e ordem temporal).
"""
import sys, csv, datetime

REQUIRED = ["timestamp","open","high","low","close","volume"]

def validate(path: str) -> bool:
    with open(path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for col in REQUIRED:
            if col not in rdr.fieldnames:
                print(f"[FAIL] {path}: falta coluna '{col}'")
                return False
        prev = None
        for row in rdr:
            try:
                ts = row["timestamp"]
                dt = datetime.datetime.fromisoformat(ts.replace("Z","").replace("z",""))
            except Exception:
                print(f"[FAIL] {path}: timestamp inválido '{row['timestamp']}'")
                return False
            if prev and dt <= prev:
                print(f"[FAIL] {path}: ordem temporal inválida {dt} <= {prev}")
                return False
            prev = dt
    print(f"[OK] {path}")
    return True

if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        ok &= validate(p)
    sys.exit(0 if ok else 1)
