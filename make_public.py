"""非公開の data.json から、投資家・事業責任者向けに出してよい数字だけを抜いて docs/data.json を作る。
出さないもの: 個人名・口座の動き・取引先名・初期投資の内訳・施策・検索順位。
使い方: python3 make_public.py <非公開data.json> <docs/data.json>"""
import json, sys
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src))
keep = ("month", "days", "nights", "bookings", "occupancy", "adr", "gross", "fee", "net",
        "rent", "linen", "cleaning", "other_cost", "cost", "profit")
done = [m for m in d["months"] if m["status"] == "実績"]
for m in done:
    x = d["detail"].get(m["month"], {})
    m["turn_stays"], m["net_per_turnover"], m["guests"] = x.get("stays"), x.get("net_per_turnover"), x.get("guests")
ahead = [{"month": m["month"], "status": m["status"], "nights": m["nights"], "bookings": m["bookings"],
          "gross": m["gross"], "net": m["net"]}
         for m in d["months"] if m["status"] != "実績"][:4]
json.dump({"generated": d["generated"], "opening": d["opening"], "ledger_until": d["ledger_until"],
           "initial_total": d["initial"]["total"], "initial_rent": d["initial"]["by_cat"].get("地代家賃", 0),
           "months": [{k: m[k] for k in keep + ("turn_stays", "net_per_turnover", "guests")} for m in done],
           "ahead": ahead},
          open(dst, "w"), ensure_ascii=False, indent=1)
