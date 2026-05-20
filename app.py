import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="MM Team Incentives & Rules Bible", layout="wide")

# --- CORE FUNCTIONS & CONSTANTS ---
def get_individual_payout_percentage(vehicles):
    if vehicles >= 104: return 150
    elif vehicles >= 84: return 125
    elif vehicles >= 75: return 100
    elif vehicles >= 67: return 75
    elif vehicles >= 59: return 50
    else: return 0

def get_manager_payout_percentage(vehicles):
    if vehicles >= 208: return 150
    elif vehicles >= 168: return 125
    elif vehicles >= 150: return 100
    elif vehicles >= 134: return 75
    elif vehicles >= 118: return 50
    else: return 0

def get_garrett_hunter_multiplier(direct_volume):
    if direct_volume >= 882: return 1.50    # +150%
    elif direct_volume >= 756: return 1.25  # +125%
    elif direct_volume >= 630: return 1.00  # +100%
    elif direct_volume >= 504: return 0.75  # +75%
    elif direct_volume >= 378: return 0.50  # +50%
    elif direct_volume >= 252: return 0.25  # +25%
    else: return 0.0

BONUS_100_ANDRES = 2914
BONUS_100_CONOR = 3045
BONUS_100_GARRETT = 4921

# --- INITIALIZATION & REFRESH TO ZERO ---
if "init_done" not in st.session_state:
    st.session_state["init_done"] = True
    st.session_state["uploader_key"] = 0
    st.session_state["df_data"] = None

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📌 Navigation")
app_mode = st.sidebar.radio("Go to:", ["1. Rules Bible (Règles)", "2. Live Calculator (Calculateur)"])

# ==========================================
# TAB 1: RULES BIBLE
# ==========================================
if app_mode == "1. Rules Bible (Règles)":
    st.title("📖 Mobility Manager Incentive Bible")
    st.write("Official framework for Q3 2026 sales commissions and performance targets.")
    
    st.markdown("---")
    st.header("1. Core Historical Bonus (6-Tier Grid)")
    st.write("Calculated on **Total Vehicles** from all sources (IAM + DIA + Central + Direct MM).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Individual Grid (Andres / Conor)")
        grid_data = {
            "Total Vehicles": ["0 - 58", "59 - 66", "67 - 74", "75 - 83", "84 - 103", "104 - 125+"],
            "Payout %": ["0%", "50%", "75%", "100%", "125%", "150% (Cap)"]
        }
        st.table(pd.DataFrame(grid_data))
        
    with col2:
        st.subheader("Manager Grid (Garrett - Doubled Tiers)")
        mgr_grid_data = {
            "Team Combined Vehicles": ["0 - 116", "118 - 132", "134 - 148", "150 - 166", "168 - 206", "208+"],
            "Payout %": ["0%", "50%", "75%", "100%", "125%", "150% (Cap)"]
        }
        st.table(pd.DataFrame(mgr_grid_data))

    st.markdown("---")
    st.header("2. Hunter Accelerator & Growth Scale")
    
    st.subheader("🤠 For Mobility Managers (Andres & Conor)")
    st.write("• Triggers from **Vehicle #126** onwards, **ONLY** on **Direct MM** units.")
    st.write("• **Condition:** Must personally sign at least **5 POS** during the quarter.")
    
    st.markdown("---")
    st.subheader("🦅 For the Manager (Garrett) - Dual Hunter Track")
    
    col_track_a, col_track_b = st.columns(2)
    
    with col_track_a:
        st.markdown("#### **Track A: Team Growth Multiplier (Managership)**")
        st.write("• Multiplier applied to Garrett's Historical Bonus payout.")
        st.write("• Based **ONLY** on the Combined Direct MM Units of Andres + Conor.")
        st.write("• *Condition:* The 2 MMs combined must sign at least **10 POS**.")
        
        # Le tableau d'échelle du Booster de Garrett
        garrett_booster_grid = {
            "Combined MMs Direct Volume": ["0 - 251 units", "252 - 377 units", "378 - 503 units", "504 - 629 units", "630 - 755 units", "756 - 881 units", "882+ units"],
            "Bonus Multiplier Added": ["+0% (None)", "+25%", "+50%", "+75%", "+100%", "+125%", "+150% (Cap)"]
        }
        st.table(pd.DataFrame(garrett_booster_grid))
        
    with col_track_b:
        st.markdown("#### **Track B: Personal Cash Accelerator (Hunter)**")
        st.write("• Garrett earns **$100/car** from his **126th personal vehicle**.")
        st.write("• **STRICT GLOBAL CONDITION:** This bonus is only unlocked if Team USA (Andres + Conor + Garrett) signs a minimum of **15 POS total**.")

# ==========================================
# TAB 2: LIVE CALCULATOR
# ==========================================
else:
    st.title("📊 Live Performance & Commission Calculator")
    st.write("Upload a file (Excel/CSV) or adjust variables manually to compute quarterly sales rewards.")
    
    st.markdown("### 📂 Data Import (Optionnel)")
    
    uploaded_file = st.file_uploader(
        "Glisse ton fichier Excel (.xlsx) ou CSV (.csv) ici :", 
        type=["csv", "xlsx"], 
        key=f"csv_uploader_{st.session_state['uploader_key']}"
    )
    
    data_source = "Saisie Manuelle"
    default_vals = {
        "Andres": {"iam": 0, "dia": 0, "central": 0, "direct": 0, "pos": 0},
        "Conor": {"iam": 0, "dia": 0, "central": 0, "direct": 0, "pos": 0},
        "Garrett": {"iam": 0, "dia": 0, "central": 0, "direct": 0, "pos": 0}
    }

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, sep=None, engine='python')
            else:
                df = pd.read_excel(uploaded_file)
            
            df = df.dropna(how='all')
            df.columns = [str(c).strip().replace('_', '').replace(' ', '').lower() for c in df.columns]
            
            required_cleaned = ["collaborateur", "iam", "dia", "centralassisted", "directsales", "possigned"]
            
            if all(rc in df.columns for rc in required_cleaned):
                data_source = f"Fichier Importé ({uploaded_file.name})"
                df["collaborateur"] = df["collaborateur"].astype(str).str.strip().str.lower()
                
                st.info("🔍 **Aperçu technique du tableau lu par la machine :**")
                st.dataframe(df[required_cleaned])
                
                for name in ["Andres", "Conor", "Garrett"]:
                    row = df[df["collaborateur"] == name.lower()]
                    if not row.empty:
                        default_vals[name] = {
                            "iam": int(pd.to_numeric(row["iam"].values[0], errors='coerce') or 0),
                            "dia": int(pd.to_numeric(row["dia"].values[0], errors='coerce') or 0),
                            "central": int(pd.to_numeric(row["centralassisted"].values[0], errors='coerce') or 0),
                            "direct": int(pd.to_numeric(row["directsales"].values[0], errors='coerce') or 0),
                            "pos": int(pd.to_numeric(row["possigned"].values[0], errors='coerce') or 0)
                        }
                st.success(f"✅ Données synchronisées avec succès depuis : {data_source}")
            else:
                st.error("❌ Erreur de format de colonnes.")
        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture : {str(e)}")

    st.markdown("---")
    st.subheader(f"🚗 Performance Inputs ({data_source})")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 👤 Andres Metrics")
        a_iam = st.number_input("Andres - IAM Deals", min_value=0, value=default_vals["Andres"]["iam"])
        a_dia = st.number_input("Andres - DIA Deals", min_value=0, value=default_vals["Andres"]["dia"])
        a_central = st.number_input("Andres - Central Assisted", min_value=0, value=default_vals["Andres"]["central"])
        a_direct = st.number_input("Andres - DIRECT MM Units", min_value=0, value=default_vals["Andres"]["direct"])
        a_pos = st.number_input("Andres - POS Signed", min_value=0, value=default_vals["Andres"]["pos"])
        
    with c2:
        st.markdown("#### 👤 Conor Metrics")
        c_iam = st.number_input("Conor - IAM Deals", min_value=0, value=default_vals["Conor"]["iam"])
        c_dia = st.number_input("Conor - DIA Deals", min_value=0, value=default_vals["Conor"]["dia"])
        c_central = st.number_input("Conor - Central Assisted", min_value=0, value=default_vals["Conor"]["central"])
        c_direct = st.number_input("Conor - DIRECT MM Units", min_value=0, value=default_vals["Conor"]["direct"])
        c_pos = st.number_input("Conor - POS Signed", min_value=0, value=default_vals["Conor"]["pos"])

    # Somme automatique pour l'équipe VaaS
    team_vaas_sum = a_pos + c_pos

    with c3:
        st.markdown("#### 🦅 Garrett (Manager & Personal Sales)")
        g_direct = st.number_input("Garrett - Personal DIRECT MM Units", min_value=0, value=default_vals["Garrett"]["direct"])
        g_pos_personal = st.number_input("POS VAAS TEAM SIGNED", min_value=0, value=team_vaas_sum)

    # --- PROCESS CALCULATIONS ---
    global_team_usa_pos = g_pos_personal
    
    # Andres Calculations
    a_total_cars = a_iam + a_dia + a_central + a_direct
    a_payout_pct = get_individual_payout_percentage(a_total_cars)
    a_hist_money = (a_payout_pct / 100.0) * BONUS_100_ANDRES
    a_hunter_eligible = a_direct > 125 and a_pos >= 5
    a_super_bonus = max(0, a_direct - 125) * 100 if a_hunter_eligible else 0
    a_total_bonus = a_hist_money + a_super_bonus
    a_bonus_per_car = a_total_bonus / a_total_cars if a_total_cars > 0 else 0
    
    # Conor Calculations
    c_total_cars = c_iam + c_dia + c_central + c_direct
    c_payout_pct = get_individual_payout_percentage(c_total_cars)
    c_hist_money = (c_payout_pct / 100.0) * BONUS_100_CONOR
    c_hunter_eligible = c_direct > 125 and c_pos >= 5
    c_super_bonus = max(0, c_direct - 125) * 100 if c_hunter_eligible else 0
    c_total_bonus = c_hist_money + c_super_bonus
    c_bonus_per_car = c_total_bonus / c_total_cars if c_total_cars > 0 else 0
    
    # Garrett Calculations
    g_team_cars = a_total_cars + c_total_cars
    g_mms_pos = a_pos + c_pos
    g_payout_pct = get_manager_payout_percentage(g_team_cars)
    g_hist_money = (g_payout_pct / 100.0) * BONUS_100_GARRETT
    
    mms_only_direct = a_direct + c_direct
    g_multiplier = get_garrett_hunter_multiplier(mms_only_direct) if g_mms_pos >= 10 else 0.0
    g_team_growth_bonus = g_hist_money * g_multiplier
    
    g_hunter_personal_eligible = g_direct > 125 and global_team_usa_pos >= 15
    g_personal_hunter_bonus = max(0, g_direct - 125) * 100 if g_hunter_personal_eligible else 0
    
    g_total_bonus = g_hist_money + g_team_growth_bonus + g_personal_hunter_bonus
    g_bonus_per_car = g_total_bonus / g_team_cars if g_team_cars > 0 else 0

    # Company Stats
    total_bonuses_paid = a_total_bonus + c_total_bonus + g_total_bonus
    total_unique_cars = g_team_cars + g_direct
    global_bonus_per_car = total_bonuses_paid / total_unique_cars if total_unique_cars > 0 else 0

    # --- OUTPUT TABLE ---
    st.markdown("---")
    st.subheader("🏆 Summary Commission Breakdown")
    
    a_over = max(0, a_direct - 125)
    c_over = max(0, c_direct - 125)
    g_over = max(0, g_direct - 125)

    calc_data = {
        "Commissions & Metrics": [
            "Total Volume Counted",
            "Historical Bonus Payout %",
            "Historical Bonus Payout ($)",
            "Direct MM Units (Counted)",
            "POS Count (Total / Individual)",
            "Hunter Accelerator Status",
            "Hunter Accelerator Payout ($)",
            "TOTAL QUARTER COMMISSION ($)",
            "📊 BONUS PAYOUT PER CAR"
        ],
        "Andres": [
            f"{a_total_cars} cars",
            f"{a_payout_pct}%",
            f"${a_hist_money:,.2f}",
            f"{a_direct} cars",
            f"{a_pos} / 5 personal POS",
            f"{a_over} car(s) over 125",
            f"${a_super_bonus:,.2f}",
            f"${a_total_bonus:,.2f}",
            f"${a_bonus_per_car:,.2f} / car"
        ],
        "Conor": [
            f"{c_total_cars} cars",
            f"{c_payout_pct}%",
            f"${c_hist_money:,.2f}",
            f"{c_direct} cars",
            f"{c_pos} / 5 personal POS",
            f"{c_over} car(s) over 125",
            f"${c_super_bonus:,.2f}",
            f"${c_total_bonus:,.2f}",
            f"${c_bonus_per_car:,.2f} / car"
        ],
        "Garrett (Boss)": [
            f"{g_team_cars} cars (Team Sum)",
            f"{g_payout_pct}%",
            f"${g_hist_money:,.2f}",
            f"{g_direct} personal / {mms_only_direct} MMs",
            f"{global_team_usa_pos} / 15 Team POS",
            f"+{g_multiplier*100:.0f}% Team Growth",
            f"${g_team_growth_bonus + g_personal_hunter_bonus:,.2f}",
            f"${g_total_bonus:,.2f}",
            f"${g_bonus_per_car:,.2f} / car"
        ]
    }
    st.table(pd.DataFrame(calc_data))
    
    # --- GLOBAL METRICS ---
    st.markdown("---")
    st.subheader("📊 Global Company Investment Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Bonuses Distributed", value=f"${total_bonuses_paid:,.2f}")
    col2.metric(label="Total Team Volume", value=f"{total_unique_cars} cars")
    col3.metric(label="📉 GLOBAL BONUS COST PER CAR", value=f"${global_bonus_per_car:,.2f} / car")
