import os
import json
from app.config import Config
from app.database import init_db, db_session

ETHIOPIAN_TEXTBOOKS = [
    # ==========================================
    # GRADE 9 (General Secondary Education)
    # ==========================================
    {
        "title": "Ethiopian Grade 9 Mathematics Student Textbook",
        "subject_code": "MATH-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 14.8,
        "cover_badge_color": "primary",
        "description": "Ministry of Education curriculum covering Unit 1: The Real Number System; Unit 2: Linear Equations & Inequalities; Unit 3: Linear Functions & Graphs; Unit 4: Geometry (Congruence, Triangles, Polygons); Unit 5: Statistics & Probability with Ethiopian demographic data.",
        "units": [
            {
                "title": "Unit 1: The Real Number System",
                "summary": "Rational and irrational numbers, radical expressions, and real-life measurement applications in Ethiopian commerce and agriculture.",
                "content": "# Unit 1: The Real Number System\n\n## 1.1 Rational and Irrational Numbers\nA number that can be expressed in the form $\\frac{a}{b}$, where $a, b \\in \\mathbb{Z}$ and $b \\neq 0$, is called a **rational number**.\n\nNumbers such as $\\sqrt{2}$, $\\sqrt{3}$, and $\\pi$ cannot be written as fractions of integers and are called **irrational numbers**.\n\n### Practical Ethiopian Application:\nWhen calculating agricultural plot boundaries in rural Ethiopian farming (Timad or Gasha conversions), square root approximations $\\sqrt{A}$ are essential to compute perimeter fencing requirements."
            },
            {
                "title": "Unit 2: Linear Equations & Applications",
                "summary": "Solving linear equations in one variable, system of equations, and cost-benefit analysis for Ethiopian rural farming cooperatives.",
                "content": "# Unit 2: Linear Equations and Inequalities\n\n## 2.1 Solving First-Degree Equations\nAn equation of the form $ax + b = 0$ ($a \\neq 0$) has a unique solution $x = -\\frac{b}{a}$.\n\n### Example Problem:\nA rural grain cooperative in Gojjam sells quintals of white Teff at 6,500 ETB each. If transport costs 3,000 ETB, find the number of quintals $q$ needed to make 100,000 ETB revenue.\n$$6500q - 3000 = 100000 \\implies 6500q = 103000 \\implies q \\approx 15.85 \\text{ quintals}$$\n"
            }
        ]
    },
    {
        "title": "Ethiopian Grade 9 Physics Student Textbook",
        "subject_code": "PHYS-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 18.2,
        "cover_badge_color": "warning",
        "description": "Covers Unit 1: Physics and Human Society; Unit 2: Physical Quantities & Measurement; Unit 3: Motion in a Straight Line; Unit 4: Force, Newton's Laws, Work, Energy & Power; Unit 5: Simple Machines (traditional Ethiopian plows / Maresha, levers, pulleys).",
        "units": [
            {
                "title": "Unit 1: Physics and Ethiopian Society",
                "summary": "Role of physics in national development: energy production (GERD, geothermal at Aluto Langano), telecommunications, and medical diagnostics.",
                "content": "# Unit 1: Physics and Human Society in Ethiopia\n\nPhysics is central to modernizing infrastructure in Ethiopia:\n1. **Hydroelectric Power Generation:** Converting gravitational potential energy of water in river basins (e.g., Grand Ethiopian Renaissance Dam on the Abay River, Gilgel Gibe) into electrical energy: $P = \\eta \\rho g Q H$.\n2. **Geothermal Energy:** Tapping magma heat in the Ethiopian Great Rift Valley (Aluto Langano and Tendaho fields).\n3. **Solar Energy:** Utilizing abundant equatorial sunlight (5.5 kWh/m²/day) for off-grid rural electrification."
            },
            {
                "title": "Unit 5: Simple Machines & The Traditional Maresha",
                "summary": "Mechanical advantage, velocity ratio, and efficiency of traditional Ethiopian ox-drawn ard plows (Maresha).",
                "content": "# Unit 5: Simple Machines: The Ethiopian Maresha\n\n## The Maresha as an Inclined Wedge\nThe traditional Ethiopian plow, the **Maresha**, has been used for millennia across the Ethiopian highlands.\n\nFrom a physics standpoint, the iron tip (**Wegel**) acts as a double inclined plane (wedge):\n- **Force Applied:** Forward traction from oxen $\\vec{F}_{oxen}$.\n- **Normal Reaction & Soil Cleavage:** The wedge converts horizontal force into lateral splitting forces to break tough clay and Vertisol soils.\n- **Mechanical Advantage:** $\\text{MA} = \\frac{\\text{Load}}{\\text{Effort}} = \\frac{L}{t}$ (length of wedge divided by thickness)."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 9 Chemistry Student Textbook",
        "subject_code": "CHEM-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 16.5,
        "cover_badge_color": "success",
        "description": "Covers Unit 1: Chemistry and Society; Unit 2: Measurements & Units; Unit 3: Atomic Structure & the Periodic Table; Unit 4: Chemical Bonding; Unit 5: Physical and Chemical Changes with applications in Ethiopian cement (Muger, Dangote), pottery, and food processing.",
        "units": [
            {
                "title": "Unit 1: Chemistry in Ethiopian Industry & Agriculture",
                "summary": "Applications in local manufacturing: cement production in Mugher, sugar refining at Wonji and Metehara, and traditional brewing.",
                "content": "# Unit 1: Chemistry and Its Importance in Ethiopia\n\nChemical processes underpin Ethiopia's growing industrial base:\n- **Cement Manufacturing (Limestone Calcination):** $\\text{CaCO}_3(s) \\xrightarrow{\\Delta} \\text{CaO}(s) + \\text{CO}_2(g)$ at factories in Derba, Mugher, and Dire Dawa.\n- **Teff Fermentation Chemistry:** Lactic acid bacteria and yeast fermentation during injera batter preparation converts starches to carbon dioxide and organic acids, giving injera its distinctive eyes (*Ayn*) and tangy flavor."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 9 Biology Student Textbook",
        "subject_code": "BIOL-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 21.0,
        "cover_badge_color": "success",
        "description": "Covers Unit 1: Biology and Technology; Unit 2: Cell Biology; Unit 3: Human Biology & Nutrition; Unit 4: Microorganisms & Disease; Unit 5: Ecology and Conservation of Ethiopian Endemic Biodiversity (Walia Ibex, Gelada Baboon, Ethiopian Wolf).",
        "units": [
            {
                "title": "Unit 5: Conservation of Ethiopian Endemic Biodiversity",
                "summary": "Study of Ethiopia's unique afro-alpine ecosystems, protected national parks (Simien, Bale Mountains), and endemic species conservation.",
                "content": "# Unit 5: Ecology and Conservation of Ethiopian Biodiversity\n\nEthiopia is one of the world's 36 global biodiversity hotspots, home to diverse ecosystems ranging from the Danakil Depression (126m below sea level) to Ras Dashen (4,550m above sea level).\n\n## Endemic Wildlife Species:\n1. **Walia Ibex (*Capra walie*):** Found exclusively in Simien Mountains National Park on precipitous cliff faces.\n2. **Ethiopian Wolf (*Canis simensis*):** Africa's most endangered carnivore, specialized in hunting giant mole-rats in the Afro-alpine meadows of Bale Mountains and Guassa.\n3. **Gelada Baboon (*Theropithecus gelada*):** Grass-eating primate endemic to the Ethiopian highlands.\n\n## Endemic Flora and Crops:\n- **Teff (*Eragrostis tef*):** Indigenous gluten-free cereal grain domesticated in Ethiopia.\n- **Enset (*Ensete ventricosum*):** Known as the 'false banana', providing staple nutrition (Kocho, Bulla) for over 20 million people in southern Ethiopia."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 9 Geography Student Textbook",
        "subject_code": "GEOG-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 17.4,
        "cover_badge_color": "primary",
        "description": "Covers Unit 1: Geological History & Topography of Ethiopia; Unit 2: Drainage Systems and Water Resources (Abay, Awash, Tekeze, Baro, Rift Valley Lakes); Unit 3: Climate of Ethiopia (Dega, Weyna Dega, Kolla, Bereha, Wurch agro-ecological zones).",
        "units": [
            {
                "title": "Unit 1: The Great Rift Valley & Topography of Ethiopia",
                "summary": "Tectonic rifting, Ethiopian highlands, high plateaus, and deep gorges formed by volcanic activity and water erosion.",
                "content": "# Unit 1: Geological History and Topography of Ethiopia\n\nEthiopia's physical landscape is divided into three major physiographic regions:\n1. **Western Highlands and Lowlands:** Includes the North-Central massifs, Shewan plateau, and fertile valleys drained by the Blue Nile (Abay).\n2. **The Great East African Rift Valley:** Bisects the country diagonally from northeast (Afar depression) to southwest (Lake Turkana), housing numerous alkaline and freshwater lakes (Ziway, Langano, Abijatta, Shala, Hawassa, Chamo, Abaya).\n3. **Southeastern Highlands and Lowlands:** Includes the Arsi-Bale massifs, Hararghe plateau, and the Ogaden lowlands drained by the Wabe Shebelle and Genale rivers."
            },
            {
                "title": "Unit 3: Traditional Agro-Climatic Zones of Ethiopia",
                "summary": "Elevation-based climate zones: Wurch, Dega, Weyna Dega, Kolla, and Bereha with their characteristic crops and human activities.",
                "content": "# Unit 3: Climate and Agro-Ecological Zones of Ethiopia\n\nAltitude is the single most dominant factor determining climate in Ethiopia:\n- **Wurch (Alpine):** Above 3,200 meters. Cold temperatures (< 10°C). Barley, sheep farming, frost common.\n- **Dega (Cool temperate):** 2,300 to 3,200 meters. 10°C - 16°C. High rainfall. Ideal for wheat, barley, pulses, potatoes.\n- **Weyna Dega (Warm temperate):** 1,500 to 2,300 meters. 16°C - 20°C. 'Wine of the highlands'. Most densely populated zone; supports teff, maize, coffee, wheat.\n- **Kolla (Warm semiarid):** 500 to 1,500 meters. 20°C - 30°C. Sorghum, millet, sesame, pastoral livestock.\n- **Bereha (Hot desert/arid):** Below 500 meters. > 30°C. Nomadic pastoralism (camels, goats); Afar and Somali lowlands."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 9 History Student Textbook",
        "subject_code": "HIST-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 15.6,
        "cover_badge_color": "warning",
        "description": "Covers Unit 1: Human Evolution & Paleontology in the Awash Valley (Lucy/Dinknesh, Ardi); Unit 2: Ancient Civilizations (Punt, Da'amat, Kingdom of Axum); Unit 3: The Zagwe Dynasty and Lalibela Rock-Hewn Churches; Unit 4: The Gondarine Period and Medieval Ethiopia.",
        "units": [
            {
                "title": "Unit 1: Ethiopia as the Cradle of Humankind",
                "summary": "Hadar, Middle Awash, and Omo Valley fossil discoveries that revolutionized human evolutionary science.",
                "content": "# Unit 1: Early Humans and Prehistoric Discoveries in Ethiopia\n\nEthiopia's Afar Depression and Awash Valley are internationally recognized as the **Cradle of Humankind**:\n- **Lucy ('Dinknesh' - You are marvelous):** Discovered in 1974 at Hadar by Donald Johanson. *Australopithecus afarensis*, dated to 3.2 million years ago, proved that bipedal walking preceded large brain expansion.\n- **Ardi (*Ardipithecus ramidus*):** Discovered at Aramis, dated to 4.4 million years ago.\n- **Omo Kibish Human Remains:** *Homo sapiens* fossils dated to over 233,000 years ago, representing the earliest anatomically modern humans."
            },
            {
                "title": "Unit 2: The Kingdom of Axum",
                "summary": "Axumite civilization, maritime trade across Adulis, coinage, Ge'ez script, and architectural monoliths (Stelae).",
                "content": "# Unit 2: The Kingdom of Axum\n\nFrom the 1st millennium BCE to the 10th century CE, the **Kingdom of Axum** was one of the four great world powers alongside Rome, Persia, and China:\n- **Monolithic Obelisks:** Single blocks of solid granite carved and erected without mortar; the largest standing stele rises over 24 meters.\n- **Coinage:** King Endubis in the late 3rd century was the first sub-Saharan African ruler to mint gold, silver, and bronze coins for international trade.\n- **Maritime Port of Adulis:** Linked Ethiopian ivory, frankincense, gold, and agricultural produce to the Red Sea, Mediterranean, India, and Arabia.\n- **Script and Literacy:** Development of the vocalized **Ge'ez alphabet** (Abugida), which remains the basis for modern Ethiopian scripts (Amharic, Tigrinya)."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 9 Information Technology (IT)",
        "subject_code": "IT-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 12.5,
        "cover_badge_color": "primary",
        "description": "Covers Unit 1: Introduction to Information and Communication Technology; Unit 2: Computer Hardware & Architecture; Unit 3: Operating Systems; Unit 4: Word Processing; Unit 5: Safe and Responsible Use of Digital Technology.",
        "units": [
            {
                "title": "Unit 1: Foundations of ICT in Ethiopia",
                "summary": "How digital technology transforms education, health delivery, agriculture, and government e-services in Ethiopia.",
                "content": "# Unit 1: Introduction to ICT\n\nInformation and Communication Technology (ICT) refers to digital tools used to create, store, transmit, and share information.\n\nIn Ethiopia's Digital Transformation Strategy, ICT powers:\n- **Fayda National Digital ID:** Secure citizen identification and social inclusion.\n- **Agricultural Extension Services:** SMS weather forecasts and crop market prices delivered to rural smallholders.\n- **Telemedicine & Digital Health:** Tele-consultations bridging remote district hospitals with central referral centers in Addis Ababa."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 9 English Student Textbook",
        "subject_code": "ENG-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 14.1,
        "cover_badge_color": "secondary",
        "description": "Curriculum covering Unit 1: Living in Rural and Urban Communities; Unit 2: Indigenous Technologies; Unit 3: Environmental Protection & Green Legacy; Unit 4: Reading and Writing for Academic Success.",
        "units": [
            {
                "title": "Unit 3: Environmental Protection & The Green Legacy",
                "summary": "Reading comprehension, essay writing, and vocabulary on afforestation, climate resilience, and indigenous agroforestry.",
                "content": "# Unit 3: Environmental Protection and The Green Legacy\n\nEthiopia's **Green Legacy Initiative** represents one of the largest mass afforestation campaigns in world history, planting billions of tree seedlings annually.\n\n### Vocabulary and Grammar in Context:\n- *Biodiversity, afforestation, drought resilience, watershed rehabilitation, carbon sequestration.*\n- **Grammar Focus:** Using passive voice in scientific descriptions (e.g., *'Millions of indigenous seedlings were planted across the degraded hillsides to prevent soil erosion.'*)"
            }
        ]
    },
    {
        "title": "Ethiopian Grade 9 Citizenship Education",
        "subject_code": "CITZ-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 11.8,
        "cover_badge_color": "primary",
        "description": "Covers Unit 1: Building a Democratic Community; Unit 2: Rule of Law & Constitutional Governance; Unit 3: Equality in Diversity; Unit 4: Patriotism, Civic Responsibility & Peaceful Coexistence.",
        "units": [
            {
                "title": "Unit 2: Rule of Law and The Federal Constitution",
                "summary": "Fundamental human rights, separation of powers, and civic responsibilities under the Ethiopian constitutional framework.",
                "content": "# Unit 2: Rule of Law and Constitutional Governance\n\nThe rule of law means that no citizen, official, or institution is above the law. Every person is entitled to equal protection and due process.\n\n### Core Principles:\n1. **Constitutional Supremacy:** The constitution is the supreme law of the land.\n2. **Separation of Powers:** Division between the Legislature (law-making), Executive (administration), and Judiciary (independent courts).\n3. **Civic Duties:** Respecting community rights, paying lawful taxes, protecting public infrastructure, and participating in local Kebele councils."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 9 Economics Student Textbook",
        "subject_code": "ECON-09",
        "grade_level": "Grade 9",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 13.0,
        "cover_badge_color": "warning",
        "description": "Covers Unit 1: The Nature and Scope of Economics; Unit 2: Scarcity, Choice and Opportunity Cost; Unit 3: Markets, Demand and Supply; Unit 4: Structure of the Ethiopian Economy (Agriculture, Industry, and Services).",
        "units": [
            {
                "title": "Unit 4: Structure of the Ethiopian Economy",
                "summary": "Overview of Ethiopian agricultural productivity, emerging manufacturing industrial parks, and the service sector expansion.",
                "content": "# Unit 4: Overview of the Ethiopian Economy\n\nEthiopia has one of the fastest-growing economies in sub-Saharan Africa:\n- **Agriculture Sector:** Employs over 65% of the labor force; major export earner through Arabica coffee, oilseeds (sesame), pulses, flowers, and live animals.\n- **Industrial Sector:** Rapidly expanding through textile, garment, leather, and agro-processing in Industrial Parks (Hawassa, Bole Lemi, Kombolcha, Kilinto).\n- **Services Sector:** Aviation (Ethiopian Airlines), telecommunications, financial banking, and logistics."
            }
        ]
    },

    # ==========================================
    # GRADE 10 (General Secondary Education)
    # ==========================================
    {
        "title": "Ethiopian Grade 10 Mathematics Student Textbook",
        "subject_code": "MATH-10",
        "grade_level": "Grade 10",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 15.4,
        "cover_badge_color": "primary",
        "description": "Covers Unit 1: Relations and Functions; Unit 2: Polynomial Functions; Unit 3: Exponential and Logarithmic Functions; Unit 4: Coordinate Geometry; Unit 5: Plane Trigonometry.",
        "units": [
            {
                "title": "Unit 3: Exponential and Logarithmic Functions",
                "summary": "Exponential growth models, compound interest in Ethiopian Microfinance Institutions (MFI), and logarithmic scales.",
                "content": "# Unit 3: Exponential Functions and Growth Models\n\nAn exponential function is given by $f(x) = a \\cdot b^x$, where $b > 0, b \\neq 1$.\n\n### Application to Population Growth in Ethiopia:\nIf a woreda population $P_0 = 120,000$ grows at an annual rate of $r = 2.6\\%$, the population after $t$ years is:\n$$P(t) = P_0 (1 + r)^t = 120000(1.026)^t$$\nUsing logarithms, we can calculate the exact year when the population will double: $t = \\frac{\\ln(2)}{\\ln(1.026)} \\approx 27 \\text{ years}$."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 10 Physics Student Textbook",
        "subject_code": "PHYS-10",
        "grade_level": "Grade 10",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 19.1,
        "cover_badge_color": "warning",
        "description": "Covers Unit 1: Vectors and 2D Motion; Unit 2: Newton's Laws and Universal Gravitation; Unit 3: Heat Energy and Thermal Expansion; Unit 4: Waves, Acoustics, and Light Optics; Unit 5: Electromagnetism.",
        "units": [
            {
                "title": "Unit 3: Heat Energy, Specific Heat & Solar Heating",
                "summary": "Thermal physics, heat capacity, phase changes, and design of solar thermal water collectors for rural clinics.",
                "content": "# Unit 3: Heat and Thermal Energy\n\nHeat energy transferred to an object is directly proportional to its mass $m$, specific heat capacity $c$, and temperature change $\\Delta T$:\n$$Q = m c \\Delta T$$\n\n### Solar Thermal Water Disinfection (SODIS) Context:\nWater has a very high specific heat capacity ($c_{water} = 4,184\\text{ J/kg}\\cdot\\text{K}$). Raising 10 liters (10 kg) of water from ambient 20°C to the pasteurization threshold of 65°C requires:\n$$Q = (10)(4184)(65 - 20) = 1,882,800\\text{ J} \\approx 1.88\\text{ MJ}$$\nIn sunny regions of Ethiopia receiving $800\\text{ W/m}^2$, a $1\\text{ m}^2$ simple solar collector delivers this energy in under 45 minutes!"
            }
        ]
    },
    {
        "title": "Ethiopian Grade 10 Chemistry Student Textbook",
        "subject_code": "CHEM-10",
        "grade_level": "Grade 10",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 17.0,
        "cover_badge_color": "success",
        "description": "Covers Unit 1: Chemical Reactions and Stoichiometry; Unit 2: Solutions; Unit 3: Important Inorganic Compounds (Acids, Bases, Salts); Unit 4: Energy Changes in Chemical Reactions; Unit 5: Chemistry in Agriculture and Industry.",
        "units": [
            {
                "title": "Unit 3: Acids, Bases, and Soil pH Management in Ethiopia",
                "summary": "Acidic soils in Western Ethiopia (Nedjo, Wollega) and alkaline sodic soils in the Rift Valley, and neutralization through agricultural liming (CaCO3).",
                "content": "# Unit 3: Inorganic Compounds and Agricultural Soil Chemistry\n\nSoil pH dictates nutrient availability for crop uptake:\n- **Acidic Soils (pH < 5.5):** Common in high-rainfall highland areas of Western Oromia and Benishangul-Gumuz. Aluminum and iron toxicity stunt root growth of crops like maize and barley.\n- **Treatment (Agricultural Liming):** Applying pulverized limestone (calcium carbonate) neutralizes excess hydrogen ions:\n$$\\text{CaCO}_3(s) + 2\\text{H}^+(aq) \\rightarrow \\text{Ca}^{2+}(aq) + \\text{CO}_2(g) + \\text{H}_2\\text{O}(l)$$\nThis raises soil pH back to optimal levels (6.0 - 7.0), unlocking phosphorus and nitrogen for plant roots."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 10 Biology Student Textbook",
        "subject_code": "BIOL-10",
        "grade_level": "Grade 10",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 20.3,
        "cover_badge_color": "success",
        "description": "Covers Unit 1: Sub-disciplines of Biology; Unit 2: Plant Anatomy & Physiology; Unit 3: Animal Physiology; Unit 4: Genetics and Heredity; Unit 5: Conservation of Natural Resources in Ethiopia.",
        "units": [
            {
                "title": "Unit 2: Plant Physiology & Coffee Arabica Diversity",
                "summary": "Photosynthesis, water transport, transpiration, and genetic preservation of wild forest Coffea arabica in the Kaffa biosphere reserve.",
                "content": "# Unit 2: Plant Physiology & Ethiopian Forest Coffee\n\nEthiopia is the primary evolutionary center of origin and genetic diversity for **Arabica Coffee (*Coffea arabica*)**.\n\n## Ecological Importance of Shade Coffee:\n- Traditional Ethiopian coffee grows under the canopy of native forest trees (such as *Millettia ferruginea*, *Albizia gummifera*).\n- Canopy shade reduces leaf transpiration, mitigates temperature extremes, and fixes atmospheric nitrogen via leguminous tree roots.\n- The moist montane cloud forests of Kaffa, Yayu, and Sheka serve as global UNESCO Biosphere Reserves harboring irreplaceable wild coffee genetic varieties."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 10 Geography Student Textbook",
        "subject_code": "GEOG-10",
        "grade_level": "Grade 10",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 16.8,
        "cover_badge_color": "primary",
        "description": "Covers Unit 1: Population of Ethiopia and the Horn; Unit 2: Economic Activities (Sedentary Agriculture, Pastoralism, Mining, Energy); Unit 3: Urbanization, Transport Networks and Foreign Trade.",
        "units": [
            {
                "title": "Unit 2: Water Resources & The Blue Nile (Abay) Basin",
                "summary": "Hydrology of the Abay basin, seasonal monsoon rains (Kiremt), sediment load, and international riparian cooperation.",
                "content": "# Unit 2: Ethiopia's Water Towers and Transboundary River Basins\n\nEthiopia is frequently called the **'Water Tower of Eastern Africa'** because of its high topography and copious seasonal rainfall.\n\n## Major River Basins:\n1. **Abay (Blue Nile):** Originates at Gish Abay, flows through Lake Tana, and plunges over Tis Issat falls. Contributes over 60% of the main Nile River's annual flow.\n2. **Awash Basin:** Entirely endorheic (inland drainage); irrigates sugar plantations at Wonji, Metehara, and Kessem.\n3. **Omo-Gibe Basin:** Drains into Lake Turkana; powers the Gibe III hydroelectric complex.\n4. **Wabe Shebelle and Genale-Dawa:** Flow across the southeastern lowlands into Somalia and the Indian Ocean."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 10 History Student Textbook",
        "subject_code": "HIST-10",
        "grade_level": "Grade 10",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 17.2,
        "cover_badge_color": "warning",
        "description": "Covers Unit 1: Modern State Formation in Ethiopia; Unit 2: The Victory of Adwa (1896) and its Pan-African Legacy; Unit 3: The Fascist Italian Aggression and Patriotic Resistance (1935–1941); Unit 4: Post-WWII Ethiopia.",
        "units": [
            {
                "title": "Unit 2: The Battle of Adwa (1896) & Its Pan-African Significance",
                "summary": "Strategic leadership of Emperor Menelik II and Empress Taytu Betul, military mobilization, and the decisive victory over colonial Italy.",
                "content": "# Unit 2: The Battle of Adwa (March 1, 1896)\n\nThe **Battle of Adwa** was a defining milestone in global modern history, where an African sovereign nation decisively defeated an invading European colonial army.\n\n## Strategic Factors Leading to Victory:\n1. **National Unity:** Warriors, patriots, and leaders mobilized from across Ethiopia—including Oromo, Amhara, Tigrayan, Gurage, Sidama, Afar, and southern peoples.\n2. **Empress Taytu Betul's Military Strategy:** Commanded troops and strategically seized the Mekelle water springs, cutting off the Italian fortress supplies.\n3. **Tactical Superiority:** Emperor Menelik II assembled over 100,000 disciplined, well-armed troops that outflanked General Baratieri's three Italian brigades.\n\n## Global Legacy:\n- Preserved Ethiopian independence during the 'Scramble for Africa'.\n- Inspired Pan-Africanism, civil rights movements worldwide, and the adoption of Ethiopia's tricolor (Green, Yellow, Red) by over 20 independent African nations."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 10 Information Technology (IT)",
        "subject_code": "IT-10",
        "grade_level": "Grade 10",
        "stream": "Common",
        "file_path": None,
        "file_size_mb": 13.9,
        "cover_badge_color": "primary",
        "description": "Covers Unit 1: Electronic Spreadsheets and Mathematical Modeling; Unit 2: Database Management Systems; Unit 3: Telecommunications and Computer Networks; Unit 4: Computer Security and Cyber Ethics.",
        "units": [
            {
                "title": "Unit 1: Spreadsheet Analysis for School and Farm Budgets",
                "summary": "Formulas, conditional formatting, data sorting, and chart visualization for practical record-keeping.",
                "content": "# Unit 1: Electronic Spreadsheets\n\nSpreadsheets allow users to organize numeric data into tables and compute automated calculations.\n\n### Essential Functions:\n- `=SUM(A1:A20)`: Calculates total revenue or yield.\n- `=AVERAGE(B1:B20)`: Computes mean student exam score or harvest per hectare.\n- `=IF(C2 >= 50, \"Pass\", \"Fail\")`: Evaluates student pass/fail status."
            }
        ]
    },

    # ==========================================
    # GRADE 11 (Secondary Specialization)
    # ==========================================
    {
        "title": "Ethiopian Grade 11 Information Technology Student Textbook",
        "subject_code": "IT-11",
        "grade_level": "Grade 11",
        "stream": "Natural Science",
        "file_path": "Grade-11_ICT_Textbook.pdf",  # <-- Real PDF on disk!
        "file_size_mb": 4.37,
        "cover_badge_color": "primary",
        "description": "Official Ministry of Education (MoE) Grade 11 ICT Student Textbook. Covers Unit 1: Information Systems and Society; Unit 2: Emerging Technologies (Artificial Intelligence, IoT, Cloud Computing); Unit 3: Computer Networking and Telecommunications; Unit 4: Computer Programming and Algorithm Development (Python). Includes complete official PDF download (4.37 MB).",
        "units": [
            {
                "title": "Unit 1: Information Systems & Its Impact on Society",
                "summary": "Components of an information system, data processing cycle, enterprise systems, and technological advancement in developing nations.",
                "content": "# Unit 1: Information Systems and Society\n\n*Direct reference from the official Ethiopian Grade 11 ICT Textbook:*\n\nAn Information System (IS) is a formal, socio-technical, organizational system designed to collect, process, store, and distribute information.\n\n## Core Components:\n1. **Hardware:** Physical computers, servers, storage media, and networking devices.\n2. **Software:** Operating systems, application software, and database engines.\n3. **Data:** Raw unorganized facts that are processed into meaningful information.\n4. **Procedures:** Operational rules, policies, and workflows guiding system use.\n5. **People:** End users, system administrators, software engineers, and database managers."
            },
            {
                "title": "Unit 2: Emerging Technologies in Ethiopia",
                "summary": "Artificial Intelligence (AI), Internet of Things (IoT), Cloud Computing, and Big Data in Ethiopian economic transformation.",
                "content": "# Unit 2: Emerging Technologies\n\nEthiopia's Artificial Intelligence Institute (EAII) and Ministry of Innovation and Technology (MInT) are driving adoption of:\n- **Machine Learning & NLP for Local Languages:** Developing speech-to-text and translation models for Amharic, Afaan Oromoo, Tigrinya, and Somali.\n- **Precision Agriculture (IoT Sensors):** Soil moisture sensors providing automated drip irrigation alerts via local SMS networks.\n- **Fintech & Mobile Money:** Platforms like Telebirr handling billions of ETB in cashless peer-to-peer and merchant payments."
            },
            {
                "title": "Unit 4: Algorithm Development and Python Programming",
                "summary": "Flowcharts, pseudocode, variables, control flow, loops, functions, and structured problem solving in Python.",
                "content": "# Unit 4: Python Programming Basics\n\nPython is an interpreted, high-level, dynamically typed language known for clean readability.\n\n```python\n# Example: Calculating Ethiopian student average grade\ndef compute_student_result(scores):\n    total = sum(scores)\n    average = total / len(scores)\n    passed = average >= 50.0\n    return average, \"PASSED\" if passed else \"NEEDS IMPROVEMENT\"\n\nmarks = [78, 85, 62, 90, 71]\navg, status = compute_student_result(marks)\nprint(f\"Average: {avg:.1f}% | Academic Status: {status}\")\n```"
            }
        ]
    },
    {
        "title": "Ethiopian Grade 11 Physics Student Textbook",
        "subject_code": "PHYS-11",
        "grade_level": "Grade 11",
        "stream": "Natural Science",
        "file_path": None,
        "file_size_mb": 22.4,
        "cover_badge_color": "warning",
        "description": "Preparatory Natural Science textbook covering Unit 1: Measurement and Practical Work; Unit 2: Two-Dimensional Kinematics; Unit 3: Rotational Dynamics and Equilibrium; Unit 4: Work, Energy, and Power; Unit 5: Fluid Mechanics with applications to the Grand Ethiopian Renaissance Dam (GERD).",
        "units": [
            {
                "title": "Unit 5: Fluid Dynamics & The Grand Ethiopian Renaissance Dam (GERD)",
                "summary": "Hydrostatic pressure, Bernoulli's equation, Torricelli's law, and hydro-turbine power calculations for the GERD power plant.",
                "content": "# Unit 5: Fluid Dynamics: The Physics of GERD\n\nThe Grand Ethiopian Renaissance Dam (GERD) on the Blue Nile is Africa's largest hydroelectric power plant (installed capacity 5,150 MW).\n\n## Bernoulli's Principle & Power Output:\nAt the dam penstocks, fluid flow follows Bernoulli's conservation equation:\n$$P_1 + \\frac{1}{2}\\rho v_1^2 + \\rho g h_1 = P_2 + \\frac{1}{2}\\rho v_2^2 + \\rho g h_2$$\n\n### Hydroelectric Power Equation:\n$$P = \\eta \\cdot \\rho \\cdot g \\cdot Q \\cdot H$$\nWhere:\n- $\\eta \\approx 0.90$ (Francis turbine efficiency)\n- $\\rho = 1000\\text{ kg/m}^3$ (density of water)\n- $g = 9.81\\text{ m/s}^2$ (acceleration due to gravity)\n- $Q$ is volume discharge flow rate in $\\text{m}^3\\text{/s}$\n- $H \\approx 140\\text{ m}$ is the net hydraulic head height."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 11 Chemistry Student Textbook",
        "subject_code": "CHEM-11",
        "grade_level": "Grade 11",
        "stream": "Natural Science",
        "file_path": None,
        "file_size_mb": 21.6,
        "cover_badge_color": "success",
        "description": "Preparatory Natural Science curriculum covering Unit 1: Fundamental Concepts of Chemistry; Unit 2: Atomic Theory and Quantum Structure; Unit 3: Chemical Bonding & Molecular Geometry; Unit 4: Chemical Kinetics and Equilibrium.",
        "units": [
            {
                "title": "Unit 4: Chemical Equilibrium & Industrial Ammonia Synthesis",
                "summary": "Le Chatelier's principle, equilibrium constants (Kc, Kp), and Haber-Bosch synthesis of nitrogenous fertilizers for Ethiopian agriculture.",
                "content": "# Unit 4: Chemical Equilibrium & The Haber Process\n\nNitrogen fertilizers (Urea and DAP) are critical inputs for boosting cereal crop yields across Ethiopia.\n\n## The Haber-Bosch Reaction:\n$$\\text{N}_2(g) + 3\\text{H}_2(g) \\rightleftharpoons 2\\text{NH}_3(g) \\quad \\Delta H = -92.4\\text{ kJ/mol}$$\n\nApplying **Le Chatelier's Principle** to optimize industrial ammonia yield:\n- **Pressure:** Increasing pressure shifts equilibrium toward products (fewer gas moles: $4 \\rightarrow 2$).\n- **Temperature:** Exothermic reaction favors lower temperature for equilibrium yield, but higher temperature for reaction rate ($450^\\circ\\text{C}$ is the economic optimum with iron catalyst)."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 11 Biology Student Textbook",
        "subject_code": "BIOL-11",
        "grade_level": "Grade 11",
        "stream": "Natural Science",
        "file_path": None,
        "file_size_mb": 24.0,
        "cover_badge_color": "success",
        "description": "Covers Unit 1: The Chemical Basis of Life; Unit 2: Cell Biology and Cellular Energetics; Unit 3: Enzymes and Metabolism; Unit 4: Molecular Genetics; Unit 5: Endocrine and Nervous Systems.",
        "units": [
            {
                "title": "Unit 2: Cellular Respiration and Energy Transformation",
                "summary": "Glycolysis, the Krebs cycle, electron transport chain, and ATP synthesis in aerobic and anaerobic conditions.",
                "content": "# Unit 2: Cellular Respiration and ATP Production\n\nCellular respiration converts glucose into usable biological energy (ATP):\n$$\\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2 \\rightarrow 6\\text{CO}_2 + 6\\text{H}_2\\text{O} + 36-38\\text{ ATP}$$\n\n### Fermentation in Traditional Ethiopian Culinary Science:\n- Anaerobic yeast fermentation of *Eragrostis tef* starch produces $\\text{CO}_2$ gas pockets that create injera's porous, spongy texture."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 11 History Student Textbook",
        "subject_code": "HIST-11",
        "grade_level": "Grade 11",
        "stream": "Social Science",
        "file_path": None,
        "file_size_mb": 19.5,
        "cover_badge_color": "warning",
        "description": "Preparatory Social Science textbook covering Unit 1: State, Society, and Economy in Medieval Ethiopia; Unit 2: The Gondarine Period and Zemene Mesafint (Era of the Princes); Unit 3: European Imperialism in Africa; Unit 4: Ethiopian Diplomatic History.",
        "units": [
            {
                "title": "Unit 2: The Zemene Mesafint (Era of the Princes, 1769–1855)",
                "summary": "Decline of central imperial power, regional autonomous warlords (Ras Mikael Sehul, Ras Gugsa), and the reunification under Emperor Tewodros II.",
                "content": "# Unit 2: The Zemene Mesafint and National Reunification\n\nThe **Zemene Mesafint** ('Era of the Princes') was a period of regional political fragmentation where provincial warlords held de facto power while puppet emperors remained in Gondar.\n\n## The Rise of Kassa Hailu (Emperor Tewodros II):\n- Began as a patriotic shifta in Qwara with deep convictions to restore national central authority.\n- Defeated regional lords at battles of Gur Amba, Takusa, Ayshal, and Deresge.\n- Crowned **Emperor Tewodros II** in 1855, initiating modern state modernization, legal reforms, and indigenous arms manufacturing at Gafat."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 11 Geography Student Textbook",
        "subject_code": "GEOG-11",
        "grade_level": "Grade 11",
        "stream": "Social Science",
        "file_path": None,
        "file_size_mb": 18.0,
        "cover_badge_color": "primary",
        "description": "Covers Unit 1: Advanced Geomorphology and Plate Tectonics; Unit 2: Soil Types of Ethiopia (Vertisols, Nitisols, Fluvisols); Unit 3: Geographic Information Systems (GIS) & Remote Sensing.",
        "units": [
            {
                "title": "Unit 2: Major Soil Types and Soil Conservation in Ethiopia",
                "summary": "Agricultural characteristics of Ethiopian soils: Vertisols (black cotton soil), Nitisols (red highland soils), and soil erosion control.",
                "content": "# Unit 2: Ethiopian Soils and Land Rehabilitation\n\nSoil is Ethiopia's most foundational natural resource:\n1. **Nitisols (Red Tropical Soils):** Deep, well-drained, acidic to neutral. Widespread in Western and Central highlands (Gojjam, Wollega, Kaffa); highly fertile for coffee, teff, and maize.\n2. **Vertisols (Heavy Black Clay):** High clay content (> 30%). Expand when wet and crack deeply when dry. Highly fertile but require Broad Bed Makers (BBM) for drainage during heavy Kiremt rains."
            }
        ]
    },

    # ==========================================
    # GRADE 12 (University Preparatory)
    # ==========================================
    {
        "title": "Ethiopian Grade 12 Mathematics Student Textbook",
        "subject_code": "MATH-12-NS",
        "grade_level": "Grade 12",
        "stream": "Natural Science",
        "file_path": None,
        "file_size_mb": 17.5,
        "cover_badge_color": "primary",
        "description": "University preparatory mathematics covering Unit 1: Sequences and Series (Arithmetic, Geometric); Unit 2: Introduction to Differential Calculus; Unit 3: Applications of Derivatives; Unit 4: Integral Calculus.",
        "units": [
            {
                "title": "Unit 2: Differential Calculus and Rate of Change",
                "summary": "Limits, derivatives from first principles, differentiation rules, and optimization of engineering problems.",
                "content": "# Unit 2: Introduction to Limits and Derivatives\n\nThe derivative of a function $f(x)$ at $x$ represents the instantaneous rate of change:\n$$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$$\n\n### Optimization Application:\nA cooperative building a rectangular grain storehouse along a riverbank requires maximum floor area with fixed perimeter fencing $2x + y = 200\\text{ m}$.\n$$A(x) = x(200 - 2x) = 200x - 2x^2$$\nSetting $A'(x) = 200 - 4x = 0 \\implies x = 50\\text{ m}, y = 100\\text{ m}$. Maximum floor area is $5,000\\text{ m}^2$."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 12 Physics Student Textbook",
        "subject_code": "PHYS-12",
        "grade_level": "Grade 12",
        "stream": "Natural Science",
        "file_path": None,
        "file_size_mb": 23.0,
        "cover_badge_color": "warning",
        "description": "Preparatory Natural Science textbook covering Unit 1: Thermodynamics and Heat Engines; Unit 2: Oscillations and Waves; Unit 3: Electromagnetic Induction and AC Circuits; Unit 4: Modern Physics, Photoelectric Effect, and Nuclear Energy.",
        "units": [
            {
                "title": "Unit 3: Electromagnetic Induction & Power Grid Transmission in Ethiopia",
                "summary": "Faraday's law, Lenz's law, step-up transformers, and high-voltage transmission from Ethiopian power stations to national and regional East African grids.",
                "content": "# Unit 3: Electromagnetic Induction & Electrical Power Transmission\n\nFaraday's Law of Electromagnetic Induction states that the induced electromotive force (EMF) is proportional to the time rate of change of magnetic flux:\n$$\\mathcal{E} = -N \\frac{d\\Phi_B}{dt}$$\n\n## High-Voltage Power Transmission in Ethiopia:\nElectricity generated at GERD (15 kV) is stepped up using massive transformers to **500 kV** for long-distance transmission to Addis Ababa and neighboring East African Power Pool nations (Kenya, Sudan, Djibouti).\n\nStepping up voltage reduces transmission line resistive heat dissipation ($P_{loss} = I^2 R$) by a factor of thousands, ensuring power arrives in cities and rural towns with minimal loss."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 12 Chemistry Student Textbook",
        "subject_code": "CHEM-12",
        "grade_level": "Grade 12",
        "stream": "Natural Science",
        "file_path": None,
        "file_size_mb": 22.1,
        "cover_badge_color": "success",
        "description": "Preparatory Natural Science chemistry covering Unit 1: Acid-Base Equilibria and Buffer Systems; Unit 2: Electrochemistry, Galvanic Cells, and Battery Storage; Unit 3: Organic Chemistry (Hydrocarbons, Alcohols, Polymers); Unit 4: Industrial Chemical Processes in Ethiopia.",
        "units": [
            {
                "title": "Unit 2: Electrochemistry and Solar Battery Storage",
                "summary": "Galvanic cells, standard electrode potentials ($E^\\circ$), the Nernst equation, and lead-acid/lithium battery chemistries for off-grid rural solar installations.",
                "content": "# Unit 2: Electrochemistry & Battery Energy Storage\n\nElectrochemical cells convert chemical potential energy into electrical energy through spontaneous redox reactions.\n\n## Nernst Equation:\n$$E = E^\\circ - \\frac{RT}{nF} \\ln Q = E^\\circ - \\frac{0.0592}{n} \\log_{10} Q \\quad (\\text{at } 25^\\circ\\text{C})$$\n\nIn solar-powered rural schools, deep-cycle batteries store chemical energy during daytime insolation and discharge during evening study hours."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 12 Biology Student Textbook",
        "subject_code": "BIOL-12",
        "grade_level": "Grade 12",
        "stream": "Natural Science",
        "file_path": None,
        "file_size_mb": 25.5,
        "cover_badge_color": "success",
        "description": "Covers Unit 1: Evolution, Natural Selection, and Speciation; Unit 2: Human Biology and Immunology (Vaccines, Immune Response); Unit 3: Biotechnology and Genetic Modification in Agriculture.",
        "units": [
            {
                "title": "Unit 3: Agricultural Biotechnology & Crop Improvement in Ethiopia",
                "summary": "Tissue culture, marker-assisted breeding, disease-free seed multiplication for Enset, potato, and drought-tolerant maize varieties.",
                "content": "# Unit 3: Biotechnology in Agriculture\n\nEthiopia's Institute of Agricultural Research (EIAR) uses modern biological tools:\n- **Tissue Culture Micropropagation:** Multiplying disease-free plantlets of enset, banana, and potato in sterile nutrient agar.\n- **Breeding for Drought Tolerance:** Selecting teff varieties with high harvest index and resistance to lodging (*Kora*, *Quncho*)."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 12 History Student Textbook",
        "subject_code": "HIST-12",
        "grade_level": "Grade 12",
        "stream": "Social Science",
        "file_path": None,
        "file_size_mb": 20.2,
        "cover_badge_color": "warning",
        "description": "Preparatory Social Science textbook covering Unit 1: Ethiopia and the Horn from 1941 to 1974; Unit 2: The Ethiopian Revolution and the Derg Period (1974–1991); Unit 3: Pan-Africanism and the Founding of the OAU/African Union in Addis Ababa.",
        "units": [
            {
                "title": "Unit 3: Ethiopia and the Birth of the African Union (AU)",
                "summary": "Ethiopia's diplomatic leadership in African decolonization, Emperor Haile Selassie I, and the establishment of the Organization of African Unity (OAU) headquarters in Addis Ababa.",
                "content": "# Unit 3: Pan-Africanism and Ethiopia's Diplomatic Role\n\nEthiopia played a central role in unifying the African continent:\n- In May 1963, leaders of 32 independent African states convened in Addis Ababa to sign the charter of the **Organization of African Unity (OAU)**.\n- Addis Ababa was chosen as the permanent diplomatic capital of Africa.\n- In 2002, the OAU evolved into the **African Union (AU)**, cementing Ethiopia's standing as the diplomatic hub of the continent."
            }
        ]
    },
    {
        "title": "Ethiopian Grade 12 Economics Student Textbook",
        "subject_code": "ECON-12",
        "grade_level": "Grade 12",
        "stream": "Social Science",
        "file_path": None,
        "file_size_mb": 17.8,
        "cover_badge_color": "warning",
        "description": "Covers Unit 1: Macroeconomic Policy Frameworks; Unit 2: Monetary Policy and Inflation Dynamics in Developing Economies; Unit 3: International Trade and Foreign Direct Investment (FDI); Unit 4: Economic Planning and Sustainable Development Goals in Africa.",
        "units": [
            {
                "title": "Unit 3: International Trade and Export Diversification in Ethiopia",
                "summary": "Comparative advantage, balance of payments, exchange rate policy, and the African Continental Free Trade Area (AfCFTA).",
                "content": "# Unit 3: International Trade & The AfCFTA\n\nEthiopia's trade strategy focuses on shifting from raw agricultural commodity exports to value-added manufactured goods:\n- **Export Products:** Coffee Arabica, cut flowers, textiles, processed leather, gold, sesame seeds.\n- **The AfCFTA Opportunity:** Eliminating tariffs on 90% of goods across 54 African countries to expand regional manufacturing and intra-African commerce."
            }
        ]
    }
]


GRADE_11_12_SUBJECT_CATALOG = [
    ("Grade 11", "MATH-11-NS", "Mathematics", "Natural Science", "grid"),
    ("Grade 11", "PHYS-11", "Physics", "Natural Science", "zap"),
    ("Grade 11", "CHEM-11", "Chemistry", "Natural Science", "droplet"),
    ("Grade 11", "BIOL-11", "Biology", "Natural Science", "feather"),
    ("Grade 11", "IT-11", "Information Technology", "Natural Science", "cpu"),
    ("Grade 11", "MATH-11-SS", "Mathematics", "Social Science", "grid"),
    ("Grade 11", "GEOG-11", "Geography", "Social Science", "compass"),
    ("Grade 11", "HIST-11", "History", "Social Science", "shield"),
    ("Grade 11", "ECON-11", "Economics", "Social Science", "book"),
    ("Grade 11", "CITZ-11", "Civics & Ethical Education", "Social Science", "book"),
    ("Grade 11", "ENG-11", "English", "Common", "book"),
    ("Grade 12", "MATH-12-NS", "Mathematics", "Natural Science", "grid"),
    ("Grade 12", "PHYS-12", "Physics", "Natural Science", "zap"),
    ("Grade 12", "CHEM-12", "Chemistry", "Natural Science", "droplet"),
    ("Grade 12", "BIOL-12", "Biology", "Natural Science", "feather"),
    ("Grade 12", "MATH-12-SS", "Mathematics", "Social Science", "grid"),
    ("Grade 12", "GEOG-12", "Geography", "Social Science", "compass"),
    ("Grade 12", "HIST-12", "History", "Social Science", "shield"),
    ("Grade 12", "ECON-12", "Economics", "Social Science", "book"),
    ("Grade 12", "CITZ-12", "Civics & Ethical Education", "Social Science", "book"),
    ("Grade 12", "ENG-12", "English", "Common", "book"),
]


def seed_grade_11_12_subject_catalog():
    init_db()
    added = 0

    with db_session() as conn:
        cursor = conn.cursor()

        for grade, code, subject, stream, icon in GRADE_11_12_SUBJECT_CATALOG:
            stream_label = "" if stream == "Common" else f" ({stream})"
            title = f"Ethiopian {grade} {subject}{stream_label} - Subject Listing"
            description = (
                f"Catalog listing for {grade} {subject} in the {stream} stream. "
                "A textbook PDF or lesson content has not been added yet."
            )

            cursor.execute(
                "SELECT id FROM textbooks WHERE subject_code = ? AND grade_level = ?",
                (code, grade),
            )
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO textbooks (
                        title, subject_code, grade_level, stream, description,
                        file_path, file_size_mb, cover_badge_color
                    ) VALUES (?, ?, ?, ?, ?, NULL, 0, 'secondary')
                """, (title, code, grade, stream, description))
                added += 1

            cursor.execute("SELECT id FROM subjects WHERE code = ?", (code,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO subjects (title, code, grade_level, description, icon, created_by)
                    VALUES (?, ?, ?, ?, ?, NULL)
                """, (title, code, grade, description, icon))

    print(f"Added {added} Grade 11-12 subject catalog entries.")


def seed_ethiopian_textbooks():
    init_db()

    with db_session() as conn:
        cursor = conn.cursor()

        # Get teacher or admin id for attribution
        cursor.execute("SELECT id FROM users WHERE role IN ('teacher', 'admin') LIMIT 1")
        user_row = cursor.fetchone()
        author_id = user_row["id"] if user_row else None

        print("Populating Ethiopian Grade 9-12 Digital Textbooks & Curriculum...")

        for book in ETHIOPIAN_TEXTBOOKS:
            # 1. Check or Insert Textbook Record
            cursor.execute("SELECT id FROM textbooks WHERE subject_code = ? AND grade_level = ?", 
                           (book["subject_code"], book["grade_level"]))
            existing_book = cursor.fetchone()

            if existing_book:
                cursor.execute("""
                    UPDATE textbooks SET 
                        title = ?, stream = ?, description = ?, file_path = ?, file_size_mb = ?
                    WHERE id = ?
                """, (book["title"], book["stream"], book["description"], book["file_path"], book["file_size_mb"], existing_book["id"]))
                book_id = existing_book["id"]
            else:
                cursor.execute("""
                    INSERT INTO textbooks (
                        title, subject_code, grade_level, stream, publisher, 
                        curriculum_type, edition_year, description, file_path, file_size_mb, cover_badge_color
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    book["title"], book["subject_code"], book["grade_level"], book["stream"],
                    "Ministry of Education (MoE) Ethiopia", "New Ethiopian Curriculum", "2023/2024 Revised Edition",
                    book["description"], book["file_path"], book["file_size_mb"], book["cover_badge_color"]
                ))
                book_id = cursor.lastrowid

            # 2. Also register matching interactive Subject in the LMS for student access
            cursor.execute("SELECT id FROM subjects WHERE code = ?", (book["subject_code"],))
            existing_subj = cursor.fetchone()

            icon_name = "book"
            if "MATH" in book["subject_code"]: icon_name = "grid"
            elif "PHYS" in book["subject_code"]: icon_name = "zap"
            elif "CHEM" in book["subject_code"]: icon_name = "droplet"
            elif "BIOL" in book["subject_code"]: icon_name = "feather"
            elif "GEOG" in book["subject_code"]: icon_name = "compass"
            elif "HIST" in book["subject_code"]: icon_name = "shield"
            elif "IT" in book["subject_code"]: icon_name = "cpu"

            if existing_subj:
                subject_id = existing_subj["id"]
                cursor.execute("""
                    UPDATE subjects SET title = ?, grade_level = ?, description = ?, icon = ?
                    WHERE id = ?
                """, (book["title"], book["grade_level"], book["description"], icon_name, subject_id))
            else:
                cursor.execute("""
                    INSERT INTO subjects (title, code, grade_level, description, icon, created_by)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (book["title"], book["subject_code"], book["grade_level"], book["description"], icon_name, author_id))
                subject_id = cursor.lastrowid

            # 3. Add Lessons from the textbook units
            for order, unit in enumerate(book.get("units", []), start=1):
                cursor.execute("SELECT id FROM lessons WHERE subject_id = ? AND title = ?", (subject_id, unit["title"]))
                existing_lesson = cursor.fetchone()

                if existing_lesson:
                    cursor.execute("""
                        UPDATE lessons SET content_markdown = ?, summary = ? WHERE id = ?
                    """, (unit["content"], unit["summary"], existing_lesson["id"]))
                else:
                    cursor.execute("""
                        INSERT INTO lessons (subject_id, title, order_num, content_markdown, summary, estimated_minutes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (subject_id, unit["title"], order, unit["content"], unit["summary"], 20))

    print(f"Successfully seeded {len(ETHIOPIAN_TEXTBOOKS)} Ethiopian Grade 9-12 textbooks and curriculum modules!")

if __name__ == "__main__":
    seed_ethiopian_textbooks()
    seed_grade_11_12_subject_catalog()
