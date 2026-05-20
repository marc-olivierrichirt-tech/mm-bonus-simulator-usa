import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="MM Team Incentives & Rules Bible", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📌 Navigation")
app_mode = st.sidebar.radio("Go to:", ["1. Rules Bible (Règles)", "2. Live Calculator (Calculateur)"])

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
    st.write("• Triggers from **Vehicle #126** onwards, **ONLY** on **Direct MM** units (100% autonomous).")
    st.write("• **Hard Condition:** Must sign at least **5 POS** during the quarter. Otherwise, Hunter Bonus = $0.")
    
    st.subheader("🦅 For the Manager (Garrett) - Dual Hunter Track (No Double-Dipping)")
    st.write("**Track A: Team Direct Growth Scale (Multiplier)**")
    st.write("Garrett receives an extra % on his Historical Bonus based **ONLY** on the **Combined Direct MM Units sold by his MMs (Andres + Conor)**:")
    st.write("• **252 to 377 MM Direct Cars:** +25% | **378 to 503 MM Direct Cars:** +50% | **504 to 629 MM Direct Cars:** +75%")
    st.write("• **630 to 755 MM Direct Cars:** +100% | **756 to 881 MM Direct Cars:** +125% | **882+ MM Direct Cars:** +150%")
    st.write("• *Condition:* Team must sign at least **10 POS combined** (Andres + Conor) to activate this scale.")
    st.write("")
    st.write("**Track B: Personal Direct Sales (Cash Accelerator)**")
    st.write("• If Garrett does personal direct sales, he earns **$100/car** starting from his **126th personal vehicle**.")
    st.write("• *Hard Condition:* Must personally sign at least **5 personal POS** during the quarter to unlock this track. If < 5 POS, Hunter Bonus = $0.")

# ==========================================
# TAB 2: LIVE CALCULATOR
# ==========================================
else:
    st.title("📊 Live Performance & Commission Calculator")
    st.write("Enter quarterly volumes to calculate team historical payouts, hunter bonuses, and vehicle bonus metrics.")
    
    st.markdown("---")
    st.subheader("🚗 Performance Inputs")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 👤 Andres Metrics")
        a_iam = st.number_input("Andres - IAM Deals", min_value=0, value=40, key="n_a_iam")
        a_dia = st.number_input("Andres - DIA Deals", min_value=0, value=30, key="n_a_dia")
        a_central = st.number_input("Andres - Central Assisted", min_value=0, value=0, key="n_a_cent")
        a_direct = st.number_input("Andres - DIRECT MM Units", min_value=0, value=126, key="n_a_dir")
        a_pos = st.number_input("Andres - POS Signed", min_value=0, value=5, key="n_a_pos")
        
    with c2:
        st.markdown("#### 👤 Conor Metrics")
        c_iam = st.number_input("Conor - IAM Deals", min_value=0, value=35, key="n_c_iam")
        c_dia = st.number_input("Conor - DIA Deals", min_value=0, value=25, key="n_c_cent")
        c_central = st.number_input("Conor - Central Assisted", min_value=0, value=0, key="n_c_cent_as")
        c_direct = st.number_input("Conor - DIRECT MM Units", min_value=0, value=126, key="n_c_dir")
        c_pos = st.number_input("Conor - POS Signed", min_value=0, value=5, key="n_c_pos")

    with c3:
        st.markdown("#### 🦅 Garrett (Manager & Personal Sales)")
        g_direct = st.number_input("Garrett - Personal DIRECT MM Units", min_value=0, value=0, key="n_g_dir")
        g_pos_personal = st.number_input("Garrett - Personal POS Signed", min_value=0, value=0, key="n_g_pos_pers")

    # --- PROCESS CALCULATIONS ---
    # Andres
    a_total_cars = a_iam + a_dia + a_central + a_direct
    a_payout_pct = get_individual_payout_percentage(a_total_cars)
    a_hist_money = (a_payout_pct / 100.0) * BONUS_100_ANDRES
    a_hunter_eligible = a_direct > 125 and a_pos >= 5
    a_super_bonus = max(0, a_direct - 125) * 100 if a_hunter_eligible else 0
    a_total_bonus = a_hist_money + a_super_bonus
    a_bonus_per_car = a_total_bonus / a_total_cars if a_total_cars > 0 else 0
    
    # Conor
    c_total_cars = c_iam + c_dia + c_central + c_direct
    c_payout_pct = get_individual_payout_percentage(c_total_cars)
    c_hist_money = (c_payout_pct / 100.0) * BONUS_100_CONOR
    c_hunter_eligible = c_direct > 125 and c_pos >= 5
    c_super_bonus = max(0, c_direct - 125) * 100 if c_hunter_eligible else 0
    c_total_bonus = c_hist_money + c_super_bonus
    c_bonus_per_car = c_total_bonus / c_total_cars if c_total_cars > 0 else 0
    
    # Garrett (Manager & Team)
    g_team_cars = a_total_cars + c_total_cars
    g_team_pos = a_pos + c_pos
    g_payout_pct = get_manager_payout_percentage(g_team_cars)
    g_hist_money = (g_payout_pct / 100.0) * BONUS_100_GARRETT
    
    # Garrett Track A: MM-Only Growth Multiplier (Excludes g_direct)
    mms_only_direct_sales = a_direct + c_direct
    g_multiplier = get_garrett_hunter_multiplier(mms_only_direct_sales) if g_team_pos >= 10 else 0.0
    g_team_growth_bonus = g_hist_money * g_multiplier
    
    # Garrett Track B: Personal Hunter Accelerator ($100/car > 125, strict condition)
    g_hunter_personal_eligible = g_direct > 125 and g_pos_personal >= 5
    g_personal_hunter_bonus = max(0, g_direct - 125) * 100 if g_hunter_personal_eligible else 0
    
    # Garrett Total Combined
    g_total_bonus = g_hist_money + g_team_growth_bonus + g_personal_hunter_bonus
    g_bonus_per_car = g_total_bonus / g_team_cars if g_team_cars > 0 else 0

    # Total Company Investment Statistics
    total_bonuses_paid = a_total_bonus + c_total_bonus + g_total_bonus
    total_unique_cars = g_team_cars + g_direct
    global_bonus_per_car = total_bonuses_paid / total_unique_cars if total_unique_cars > 0 else 0

    # --- OUTPUT TABLE ---
    st.markdown("---")
    st.subheader("🏆 Summary Commission Breakdown (Payout Only)")
    
    a_over = max(0, a_direct - 125)
    c_over = max(0, c_direct - 125)
    g_over = max(0, g_direct - 125)

    calc_data = {
        "Commissions & Metrics": [
            "Total Volume Counted",
            "Historical Bonus Payout %",
            "Historical Bonus Payout ($)",
            "Direct MM Units (Counted)",
            "POS Status (Team / Indiv)",
            "Hunter Accelerator Reward Info",
            "Hunter Accelerator Payout ($)",
            "TOTAL QUARTER COMMISSION ($)",
            "📊 BONUS PAYOUT PER CAR"
        ],
        "Andres": [
            f"{a_total_cars} cars",
            f"{a_payout_pct}%",
            f"${a_hist_money:,.2f}",
            f"{a_direct} cars",
            f"{a_pos} / 5 POS",
            f"{a_over} {'car' if a_over <= 1 else 'cars'} over 125",
            f"${a_super_bonus:,.2f}",
            f"${a_total_bonus:,.2f}",
            f"${a_bonus_per_car:,.2f} / car"
        ],
        "Conor": [
            f"{c_total_cars} cars",
            f"{c_payout_pct}%",
            f"${c_hist_money:,.2f}",
            f"{c_direct} cars",
            f"{c_pos} / 5 POS",
            f"{c_over} {'car' if c_over <= 1 else 'cars'} over 125",
            f"${c_super_bonus:,.2f}",
            f"${c_total_bonus:,.2f}",
            f"${c_bonus_per_car:,.2f} / car"
        ],
        "Garrett (Boss)": [
            f"{g_team_cars} cars (Team Sum)",
            f"{g_payout_pct}%",
            f"${g_hist_money:,.2f}",
            f"{g_direct} personal / {mms_only_direct_sales} MMs",
            f"{g_team_pos} team / {g_pos_personal} personal POS",
            f"+{g_multiplier*100:.0f}% MM Growth | {g_over} personal cars",
            f"${g_team_growth_bonus + g_personal_hunter_bonus:,.2f}",
            f"${g_total_bonus:,.2f}",
            f"${g_bonus_per_car:,.2f} / car"
        ]
    }
    
    st.table(pd.DataFrame(calc_data))
    
    # --- GLOBAL METRICS CARD ---
    st.markdown("---")
    st.subheader("📊 Global Company Investment Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Bonuses Distributed", value=f"${total_bonuses_paid:,.2f}")
    col2.metric(label="Total Team Volume (Unique Sales)", value=f"{total_unique_cars} cars")
    col3.metric(label="📉 TOTAL BONUS COST PER CAR (GLOBAL)", value=f"${global_bonus_per_car:,.2f} / car")

    # --- LIVE FEEDS ---
    st.markdown("### 🔔 Management Alerts")
    if g_team_pos < 10 and mms_only_direct_sales >= 252:
        st.error(f"🚨 **Garrett Manager Warning:** MMs achieved {mms_only_direct_sales} Direct sales but signed only {g_team_pos}/10 POS. Garrett's Growth Multiplier is LOCKED.")
    
    if g_direct > 125 and g_pos_personal < 5:
        st.warning(f"⚠️ **Garrett Personal Sales Warning:** Garrett sold {g_direct} personal cars (>125) but signed only {g_pos_personal}/5 personal POS. His individual $100/car bonus is LOCKED.")
    elif g_personal_hunter_bonus > 0:
        st.success(f"🎯 **Garrett Individual Success:** Garrett unlocked his personal Hunter Accelerator! Adding ${g_personal_hunter_bonus:,.2f} ($100/car over 125).")
