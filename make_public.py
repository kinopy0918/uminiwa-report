"""非公開の data.json から、公開ページに出してよい数字だけを抜いて docs/data.json を作る。
出さないもの: 個人名・取引先名・口座の個別の動き・注文番号（unconfirmed は件数と金額だけ）。
使い方: python3 make_public.py <非公開data.json> <docs/data.json>"""
import json, sys
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src))
keep = ("month", "status", "days", "nights", "bookings", "occupancy", "adr", "gross", "fee", "net",
        "rent", "linen", "cleaning", "other_cost", "cost", "profit")
months = []
for m in d["months"]:
    x = d["detail"].get(m["month"], {})
    row = {k: m[k] for k in keep}
    row.update({k: x.get(k) for k in ("stays", "net_per_turnover", "guests", "bands", "views", "view_days", "bookings_made", "cvr", "rank_avg")})
    months.append(row)
out = {
    "generated": d["generated"], "opening": d["opening"], "ledger_until": d["ledger_until"],
    "initial": d["initial"],                     # 科目別の合計のみ（取引先名なし）
    "months": months,
    "bands": d["bands"],
    "views": d["views"],
    "rank": d["rank"],
    "experiments": [{k: e.get(k) for k in ("id", "title", "status", "started", "planned", "days", "verdict", "detail")} for e in d["experiments"]],
    "tatekae": d["tatekae"],
    "unconfirmed_total": sum(u["amount"] for u in d.get("unconfirmed", [])),
}
json.dump(out, open(dst, "w"), ensure_ascii=False, indent=1)
