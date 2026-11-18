import json
from app.database import init_db, db_session

def seed_data():
    init_db()
    
    with db_session() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM subjects WHERE code = ?", ("SCI-501",))
        if cursor.fetchone():
            print("Database already contains the seeded curriculum. Skipping seed.")
            return

        print("Seeding rural curriculum subjects...")
        
        # 2. Subjects
        # Subject 1: Science & Water
        cursor.execute("""
            INSERT INTO subjects (title, code, grade_level, description, icon, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("Environmental Science & Clean Water", "SCI-501", "Grade 5", 
              "Understanding rural water sources, filtration methods, sanitation, and disease prevention.", "droplet", None))
        sci_id = cursor.lastrowid

        # Subject 2: Practical Agriculture
        cursor.execute("""
            INSERT INTO subjects (title, code, grade_level, description, icon, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("Sustainable Agriculture & Soil Health", "AGR-503", "Grade 5", 
              "Practical lessons on organic composting, moisture conservation, and local crop rotation.", "feather", None))
        agr_id = cursor.lastrowid

        # Subject 3: Practical Math
        cursor.execute("""
            INSERT INTO subjects (title, code, grade_level, description, icon, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("Practical Mathematics for Farming & Trade", "MTH-502", "Grade 5", 
              "Applied arithmetic for weighing harvest, estimating farm land area, and local market trade.", "grid", None))
        mth_id = cursor.lastrowid

        # Subject 4: Literacy
        cursor.execute("""
            INSERT INTO subjects (title, code, grade_level, description, icon, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("Language, Reading & Storytelling", "LIT-504", "Grade 5", 
              "Reading comprehension, preserving oral traditions, and communicating community notices.", "book", None))
        lit_id = cursor.lastrowid

        print("Seeding lessons & question banks...")
        
        # --- Science Lessons ---
        sci_l1_content = """# Sources of Water in Rural Communities

Water is essential for life, farming, and community health. In rural and remote areas, communities rely on several natural sources for their daily water needs.

## Common Water Sources
1. **Rainwater Harvesting:** Collecting rainwater from roofs into clean storage tanks or barrels. This is often the cleanest raw water available.
2. **Springs and Protected Wells:** Ground water that surfaces naturally or through dug wells. When protected with a concrete apron, it is relatively safe from surface runoff contamination.
3. **Rivers and Streams:** Flowing surface water used for household chores and livestock. It frequently carries sediment and pathogens from upstream activities.

> **Key Rule of Hygiene:** Surface water from rivers and open ponds should never be consumed directly without filtration or boiling.

## Protection of Water Points
- Keep livestock at least 30 meters away from wells and intake points.
- Ensure drainage ditches divert muddy surface rainwater away from wellheads.
- Clean roof catchments before the first rains of the wet season.
"""
        cursor.execute("""
            INSERT INTO lessons (subject_id, title, order_num, content_markdown, summary, estimated_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sci_id, "Sources of Water in Rural Communities", 1, sci_l1_content, 
              "Learn the three primary rural water sources and methods to protect local water points from contamination.", 12))

        sci_l2_content = """# Household Water Purification Methods

Even clear-looking water can harbor microscopic bacteria, parasites, and viruses that cause waterborne illnesses like cholera and dysentery.

## Three Accessible Purification Methods

### 1. Rolling Boil
- Bring clear water to a vigorous, rolling boil for at least **1 full minute** (or 3 minutes at high altitude).
- Allow water to cool naturally in a covered, clean container with a lid.
- Highly effective against all types of biological germs.

### 2. Bio-Sand and Charcoal Multi-Layer Filter
Constructing a low-cost bio-sand filter uses locally available materials layered in a clean container:
- **Bottom layer:** Clean coarse gravel (prevents sand from escaping into the spout).
- **Middle layer:** Fine, washed river sand (mechanically traps sediment and parasites).
- **Top active layer:** Fine wood charcoal (adsorbs organic compounds and improves odor/taste).

### 3. Solar Water Disinfection (SODIS)
- Fill transparent, clean plastic PET bottles (like soda bottles) with clear water.
- Place the bottles flat on a metal corrugated roof under direct sunlight for at least **6 hours** (or 2 consecutive days if cloudy).
- The sun's ultraviolet (UV-A) rays and thermal heating destroy harmful pathogens.
"""
        cursor.execute("""
            INSERT INTO lessons (subject_id, title, order_num, content_markdown, summary, estimated_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sci_id, "Household Water Purification Methods", 2, sci_l2_content, 
              "Discover simple, low-cost water treatment techniques: boiling, bio-sand filtration, and solar SODIS disinfection.", 15))
        sci_l2_id = cursor.lastrowid

        # Quiz for Science Lesson 2
        cursor.execute("""
            INSERT INTO quizzes (lesson_id, subject_id, title, description, passing_score)
            VALUES (?, ?, ?, ?, ?)
        """, (sci_l2_id, sci_id, "Water Purification Comprehension Check", 
              "Check your understanding of household water filtration and disinfection techniques.", 70))
        quiz_sci_id = cursor.lastrowid

        questions_sci = [
            ("How long must water boil vigorously at rolling boil to destroy pathogens?", 
             ["30 seconds", "1 full minute", "10 seconds", "It does not need to boil"], 
             1, "A rolling boil of 1 full minute destroys almost all biological pathogens, viruses, and parasites.", 10),
            ("Which material in a three-stage bio-sand filter traps fine sediments?", 
             ["Fine, clean sand", "Large boulders", "Plastic shavings", "Tree leaves"], 
             0, "Clean fine sand mechanically filters out turbidity and eggs of parasites.", 10),
            ("In Solar Disinfection (SODIS), how many hours under direct sunlight are recommended?", 
             ["1 hour", "30 minutes", "At least 6 hours", "12 continuous hours"], 
             2, "At least 6 hours of full tropical sun provides sufficient UV-A radiation and heat to disinfect water.", 10),
            ("Why should livestock be kept at least 30 meters away from village wells?", 
             ["To keep animals calm", "To prevent animal waste from contaminating groundwater runoff", "Because animals dislike water", "To save grass"], 
             1, "Animal waste is a major vector for bacterial contamination of shallow wellheads and aquifers.", 10)
        ]

        for q_text, opts, c_idx, expl, pts in questions_sci:
            cursor.execute("""
                INSERT INTO questions (quiz_id, question_text, options_json, correct_option_index, explanation, points)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (quiz_sci_id, q_text, json.dumps(opts), c_idx, expl, pts))

        # --- Agriculture Lessons ---
        agr_l1_content = """# Building a Low-Cost Compost Heap

Healthy soil is the foundation of food security in our community. Composting turns organic crop residues and animal manure into dark, rich humus without chemical fertilizers.

## The Recipe: Brown & Green Layers
1. **Green Materials (Nitrogen-rich):** Fresh weeds, vegetable scraps, green grass cuttings, and livestock manure.
2. **Brown Materials (Carbon-rich):** Dry maize stalks, straw, dry leaves, and wood ash (in small amounts).
3. **Moisture:** The pile should be damp like a squeezed sponge, not waterlogged.
4. **Air:** Turning the heap every 2 weeks introduces oxygen, speeding up decomposition through aerobic bacteria.

In 6 to 8 weeks, the heap transforms into dark, sweet-smelling compost that boosts soil water retention during dry seasons.
"""
        cursor.execute("""
            INSERT INTO lessons (subject_id, title, order_num, content_markdown, summary, estimated_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (agr_id, "Building a Low-Cost Compost Heap", 1, agr_l1_content, 
              "Learn how to combine nitrogen-rich greens and carbon-rich browns into natural soil fertilizer.", 15))
        agr_l1_id = cursor.lastrowid

        # Agriculture Quiz
        cursor.execute("""
            INSERT INTO quizzes (lesson_id, subject_id, title, description, passing_score)
            VALUES (?, ?, ?, ?, ?)
        """, (agr_l1_id, agr_id, "Composting & Soil Enrichment Quiz", 
              "Test your knowledge of organic farming inputs and moisture management.", 70))
        quiz_agr_id = cursor.lastrowid

        questions_agr = [
            ("Which of the following is considered a 'Green' (Nitrogen-rich) composting material?", 
             ["Dry maize stalks", "Livestock manure and fresh weeds", "Cardboard and dry leaves", "Crushed stones"], 
             1, "Fresh manure and green foliage supply nitrogen to fuel microbial activity in the pile.", 10),
            ("How moist should an active compost pile be kept?", 
             ["Bone dry with zero water", "Like a wrung-out damp sponge", "Completely flooded in water", "It does not matter"], 
             1, "Damp like a squeezed sponge allows microorganisms to thrive without suffocating from lack of oxygen.", 10),
            ("What is the primary benefit of turning the compost heap every two weeks?", 
             ["To change its color", "To add oxygen for beneficial aerobic decomposition", "To scare insects away", "To reduce the volume to zero"], 
             1, "Aeration supplies oxygen to heat up the heap and destroy weed seeds and plant diseases.", 10)
        ]

        for q_text, opts, c_idx, expl, pts in questions_agr:
            cursor.execute("""
                INSERT INTO questions (quiz_id, question_text, options_json, correct_option_index, explanation, points)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (quiz_agr_id, q_text, json.dumps(opts), c_idx, expl, pts))

        # --- Math Lessons ---
        mth_l1_content = """# Measuring Farm Land Area & Pacing

When measuring agricultural plots or school garden beds without long tape measures, farmers use standardized body pacing.

## Step Pacing Method
- One average adult pace (stride) covers approximately **0.75 meters** (or 2.5 feet).
- **Two steps** (a double-pace) is roughly **1.5 meters**.

### Calculating Rectangular Plot Area
$$\\text{Area} = \\text{Length} \\times \\text{Width}$$

**Example:**
If a vegetable garden bed is 10 paces long and 4 paces wide:
- Length $\\approx 10 \\times 0.75 = 7.5\\text{ meters}$
- Width $\\approx 4 \\times 0.75 = 3.0\\text{ meters}$
- $\\text{Area} = 7.5 \\times 3.0 = 22.5\\text{ square meters}$

This calculation helps you determine how much seed or compost is needed for optimal crop spacing.
"""
        cursor.execute("""
            INSERT INTO lessons (subject_id, title, order_num, content_markdown, summary, estimated_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (mth_id, "Measuring Farm Land Area & Pacing", 1, mth_l1_content, 
              "Calculate plot dimensions and garden area using stride pacing and multiplication.", 14))
        
        print("Database successfully populated with rural school curriculum!")

if __name__ == "__main__":
    seed_data()
