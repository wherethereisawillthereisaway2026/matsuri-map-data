# 酒アプリ(sake-app/web-trial/data.json)の蔵 → 祭りマップ用 sake_breweries.json
# 日本酒(クラフトサケ含む)の銘柄がある蔵=35 酒蔵、焼酎・泡盛の銘柄がある蔵=36 焼酎。両方あれば両方に出す
import json, pathlib
here = pathlib.Path(__file__).parent
d = json.load(open(here.parent / "sake-app/web-trial/data.json", encoding="utf-8"))
brands = {}
for s in d["s"]:
    kind = s[3] if len(s) > 3 else ""
    cat = 36 if kind in ("焼酎", "泡盛") else 35
    brands.setdefault((s[2], cat), []).append(s[0])
out = []
for (bi, cat), names in sorted(brands.items()):
    name, kana, pref, lat, lon = d["b"][bi]
    if lat is None or lon is None: continue
    out.append({"name": name, "kana": kana, "pref": pref, "lat": lat, "lng": lon, "category": cat,
                "overview": "銘柄: " + "、".join(names[:8]) + (" ほか" if len(names) > 8 else "")})
json.dump(out, open(here / "sake_breweries.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(out), {c: sum(1 for o in out if o["category"] == c) for c in (35, 36)})
