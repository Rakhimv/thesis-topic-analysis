import pandas as pd
from categories import apply_categories, get_category, categories,teacher_eng_mapping

STOP_WORDS = {
    "для", "на", "по", "в", "с", "и", "к", "о", "из",
    "при", "за", "от", "не", "до", "об",
}

df = pd.read_excel("thesis_data.xlsx")
df = apply_categories(df)

faculty_filter = df['Faculty'] == 'Процессы управления' 
df = df[faculty_filter]                                 

df["Advisor"] = df["Advisor"].astype(str).str.strip()
df["Advisor"] = df["Advisor"].map(teacher_eng_mapping).fillna(df["Advisor"])
df = df[~df["Advisor"].isin(["nan", "None", ""])]

CROSSTAB = pd.crosstab(df["Advisor"], df["category"])
ADVISOR_NAMES = sorted(CROSSTAB.index)


def advisor_main_topic(advisor: str) -> str:
    row = CROSSTAB.loc[advisor]
    without_other = row.drop("Прочее", errors="ignore")
    if without_other.sum() > 0:
        return without_other.idxmax()
    return row.idxmax()


def get_advisor(name: str) -> dict | None:
    name = name.strip()
    if name not in CROSSTAB.index:
        return None
    g = df[df["Advisor"] == name].copy()
    g = g[g["Title_ru"].notna()]
    if "Graduation" in g.columns:
        g = g.sort_values("Graduation", ascending=False, na_position="last")
    works = []
    for _, row in g.iterrows():
        year = row["Graduation"] if "Graduation" in g.columns else None
        if pd.notna(year):
            year = int(year)
        else:
            year = None
        works.append({
            "title": row["Title_ru"],
            "category": row["category"],
            "year": year,
        })
    return {
        "name": name,
        "total": len(works),
        "main_topic": advisor_main_topic(name),
        "works": works,
    }


def query_keywords(query: str) -> list[str]:
    q = query.lower()
    return [kw for kws in categories.values() for kw in kws if kw in q]


def tokenize(query: str) -> list[str]:
    return [
        w for w in query.lower().split()
        if len(w) > 3 and w not in STOP_WORDS
    ]


def title_hits(title: str, kws: list[str], tokens: list[str]) -> bool:
    t = title.lower()
    return any(kw in t for kw in kws) or any(tok in t for tok in tokens)


def find_advisors(query: str, limit: int = 8) -> list[dict]:
    q = query.strip()
    if not q:
        return []

    query_cat = get_category(q)
    kws = query_keywords(q)
    tokens = tokenize(q)

    if query_cat == "Прочее" and not kws and not tokens:
        return []

    results = []
    for advisor in CROSSTAB.index:
        total = int(CROSSTAB.loc[advisor].sum())
        if total < 3:
            continue

        in_cat = int(CROSSTAB.loc[advisor].get(query_cat, 0))
        advisor_df = df[df["Advisor"] == advisor]
        matched = [
            row["Title_ru"]
            for _, row in advisor_df.iterrows()
            if pd.notna(row["Title_ru"]) and title_hits(str(row["Title_ru"]), kws, tokens)
        ]

        if query_cat != "Прочее":
            if in_cat == 0 and not matched:
                continue
        elif not matched:
            continue

        score = in_cat * 15 + len(matched) * 10
        pct = round(100 * in_cat / total) if total else 0

        results.append({
            "name": advisor,
            "total": total,
            "main_topic": advisor_main_topic(advisor),
            "in_topic": in_cat,
            "pct": pct,
            "score": score,
            "matches": matched[:3],
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:limit]
    if not results:
        return []

    top = results[0]["score"]
    for r in results:
        r["rating"] = max(1, round(100 * r["score"] / top)) if top > 0 else 1
        r["score"] = round(r["score"], 1)

    return results
