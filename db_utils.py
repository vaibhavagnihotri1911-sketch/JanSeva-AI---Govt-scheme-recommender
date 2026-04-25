import psycopg2


# DB Connection
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="india_schemes_db",
        user="postgres",
        password="Sneha@123",
        port="5433"
    )


# Category Classification Function
def classify_scheme(name):
    name = name.lower()

    if "women" in name:
        return "Women"
    elif "student" in name or "scholarship" in name:
        return "Student"
    elif "kisan" in name or "farmer" in name or "agriculture" in name:
        return "Farmer"
    elif "startup" in name or "entrepreneur" in name:
        return "Startup"
    elif "msme" in name or "small business" in name:
        return "MSME"
    elif "senior" in name or "old age" in name:
        return "Senior Citizen"
    elif "sc" in name or "st" in name:
        return "SC/ST"
    elif "minority" in name:
        return "Minority"
    elif "disability" in name or "disabled" in name:
        return "Disability"
    elif "health" in name or "medical" in name:
        return "Health"
    elif "housing" in name or "awas" in name:
        return "Housing"
    elif "employment" in name or "job" in name:
        return "Unemployed"
    else:
        return "General"


# Main Insert Function
def insert_full_scheme(s):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Insert into schemes (with duplicate protection)
        cur.execute("""
            INSERT INTO schemes (
                scheme_name,
                description_short,
                ministry,
                central_or_state,
                state_name,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (scheme_name) DO NOTHING
            RETURNING scheme_id;
        """, (
            s.get("scheme_name"),
            s.get("description_short"),
            s.get("ministry"),
            "Central",
            "All India",
            "active"
        ))

        result = cur.fetchone()

        # If already exists -> fetch existing id
        if result:
            scheme_id = result[0]
        else:
            cur.execute(
                "SELECT scheme_id FROM schemes WHERE scheme_name = %s;",
                (s.get("scheme_name"),)
            )
            scheme_id = cur.fetchone()[0]

        # 2. Category Classification
        category_name = classify_scheme(s.get("scheme_name", ""))

        cur.execute("""
            SELECT category_id FROM categories
            WHERE category_name = %s;
        """, (category_name,))
        cat = cur.fetchone()

        if cat:
            category_id = cat[0]

            cur.execute("""
                INSERT INTO scheme_categories (scheme_id, category_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (scheme_id, category_id))

        # 3. Eligibility
        cur.execute("""
            INSERT INTO eligibility (
                scheme_id,
                income_max,
                occupation
            )
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            scheme_id,
            None,
            s.get("target_group", "General")
        ))

        # 4. Benefits
        cur.execute("""
            INSERT INTO benefits (
                scheme_id,
                benefit_type
            )
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            scheme_id,
            s.get("benefit_type", "General")
        ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error inserting scheme:", e)

    finally:
        cur.close()
        conn.close()


# Fetch Function (for recommender)
def fetch_all_schemes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT scheme_name, description_short
        FROM schemes;
    """)

    rows = cur.fetchall()

    data = []
    for r in rows:
        data.append({
            "scheme_name": r[0],
            "description_short": r[1]
        })

    cur.close()
    conn.close()

    return data