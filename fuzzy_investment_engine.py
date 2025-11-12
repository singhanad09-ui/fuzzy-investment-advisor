# -----------------------------------------------------------------
# PROJECT: Fuzzy Investment Advisor
# FILE: fuzzy_investment_engine.py
# AUTHOR: (Your Name) / Gemini AI
# REQUIRES: pip install scikit-fuzzy
# -----------------------------------------------------------------

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyInvestmentEngine:
    """
    คลาสหลักสำหรับประมวลผล Fuzzy Logic
    เพื่อแนะนำสัดส่วนการลงทุน (Asset Allocation)
    """

    def __init__(self):
        # --- 1. กำหนดตัวแปร Input (Antecedents) ---

        # อายุ (Age): 18 - 80
        self.age = ctrl.Antecedent(np.arange(18, 81, 1), 'age')
        self.age['young'] = fuzz.trapmf(self.age.universe, [18, 18, 30, 35])
        self.age['middle_aged'] = fuzz.trimf(self.age.universe, [30, 45, 55])
        self.age['senior'] = fuzz.trapmf(self.age.universe, [50, 60, 80, 80])

        # รายได้ (Income): 15,000 - 500,000
        self.income = ctrl.Antecedent(np.arange(15000, 500001, 1000), 'income')
        self.income['low'] = fuzz.trapmf(self.income.universe, [15000, 15000, 40000, 60000])
        self.income['medium'] = fuzz.trimf(self.income.universe, [45000, 80000, 120000])
        self.income['high'] = fuzz.trapmf(self.income.universe, [100000, 150000, 500000, 500000])

        # ระยะเวลาลงทุน (Time Horizon): 1 - 30 ปี
        self.time_horizon = ctrl.Antecedent(np.arange(1, 31, 1), 'time_horizon')
        self.time_horizon['short'] = fuzz.trapmf(self.time_horizon.universe, [1, 1, 3, 5])
        self.time_horizon['medium'] = fuzz.trimf(self.time_horizon.universe, [3, 7, 12])
        self.time_horizon['long'] = fuzz.trapmf(self.time_horizon.universe, [10, 15, 30, 30])
        
        # ความเสี่ยง (Risk Tolerance): 1 - 10
        self.risk_tolerance = ctrl.Antecedent(np.arange(1, 11, 1), 'risk_tolerance')
        self.risk_tolerance['low'] = fuzz.trapmf(self.risk_tolerance.universe, [1, 1, 3, 5])
        self.risk_tolerance['medium'] = fuzz.trimf(self.risk_tolerance.universe, [3, 5, 7])
        self.risk_tolerance['high'] = fuzz.trapmf(self.risk_tolerance.universe, [5, 7, 10, 10])

        # --- 2. กำหนดตัวแปร Output (Consequents) ---
        # เราจะกำหนดสัดส่วนสำหรับแต่ละสินทรัพย์ (0% - 100%)
        
        universe = np.arange(0, 101, 1)
        self.equity = ctrl.Consequent(universe, 'equity') # หุ้น
        self.bonds = ctrl.Consequent(universe, 'bonds')   # พันธบัตร
        self.cash = ctrl.Consequent(universe, 'cash')     # เงินฝาก

        # กำหนด Membership functions สำหรับ Output
        names = ['low', 'medium', 'high']
        self.equity.automf(names=names)
        self.bonds.automf(names=names)
        self.cash.automf(names=names)

        # --- 3. กำหนดกฎ (Rules) ---
        
        # กฎที่ 1: Aggressive (เสี่ยงสูง)
        # IF Risk=High AND (Age=Young OR Time=Long) THEN Equity=High, Bonds=Low, Cash=Low
        rule1 = ctrl.Rule(
            self.risk_tolerance['high'] & (self.age['young'] | self.time_horizon['long']),
            (self.equity['high'], self.bonds['low'], self.cash['low'])
        )

        # กฎที่ 2: Conservative (ปลอดภัย)
        # IF Risk=Low OR Age=Senior THEN Equity=Low, Bonds=High, Cash=Medium
        rule2 = ctrl.Rule(
            self.risk_tolerance['low'] | self.age['senior'] | self.time_horizon['short'],
            (self.equity['low'], self.bonds['high'], self.cash['medium'])
        )

        # กฎที่ 3: Balanced (สมดุล)
        # IF Risk=Medium AND Time=Medium AND Income=Medium THEN Equity=Medium, Bonds=Medium, Cash=Low
        rule3 = ctrl.Rule(
            self.risk_tolerance['medium'] & self.time_horizon['medium'] & self.income['medium'],
            (self.equity['medium'], self.bonds['medium'], self.cash['low'])
        )
        
        # กฎที่ 4: Wealthy Conservative (มีรายได้สูง แต่รับความเสี่ยงได้น้อย)
        rule4 = ctrl.Rule(
            self.income['high'] & self.risk_tolerance['low'],
            (self.equity['low'], self.bonds['medium'], self.cash['high'])
        )

        # --- 4. สร้างระบบ Control System ---
        self.investment_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
        self.advisor = ctrl.ControlSystemSimulation(self.investment_ctrl)

    def calculate_portfolio(self, user_age, user_income, user_time, user_risk):
        """
        รับ Input จากผู้ใช้และคำนวณสัดส่วนพอร์ต
        """
        # 1. ป้อนค่า Input
        try:
            self.advisor.input['age'] = user_age
            self.advisor.input['income'] = user_income
            self.advisor.input['time_horizon'] = user_time
            self.advisor.input['risk_tolerance'] = user_risk
        except Exception as e:
            print(f"Error setting inputs: {e}")
            print("Please ensure inputs are within the defined ranges.")
            return None

        # 2. คำนวณ (Defuzzification)
        self.advisor.compute()

        # 3. ดึงผลลัพธ์
        raw_results = {
            'equity': self.advisor.output['equity'],
            'bonds': self.advisor.output['bonds'],
            'cash': self.advisor.output['cash']
        }

        # 4. Normalize ผลลัพธ์ให้รวมเป็น 100% (สำคัญมาก!)
        total = sum(raw_results.values())
        if total == 0:
            return {'equity': 0, 'bonds': 0, 'cash': 100} # Default case

        normalized_results = {
            'equity': (raw_results['equity'] / total) * 100,
            'bonds': (raw_results['bonds'] / total) * 100,
            'cash': (raw_results['cash'] / total) * 100
        }
        
        return normalized_results

# -----------------------------------------------------------------
# PART 2: POST-PROCESSING WRAPPER (Simple Rule-Based)
# -----------------------------------------------------------------

def get_example_recommendations(equity_pct, bonds_pct, cash_pct):
    """
    ฟังก์ชัน "Wrapper" นี้จะให้ "ตัวอย่าง" สินทรัพย์
    โดยใช้ตรรกะ IF-THEN ธรรมดา (ไม่ใช่ Fuzzy)
    """
    
    recommendations = {
        'portfolio_type': '',
        'equity_examples': [],
        'bonds_examples': [],
        'cash_examples': []
    }

    # ตีความประเภทของพอร์ต
    if equity_pct > 70:
        recommendations['portfolio_type'] = 'Aggressive (เน้นเติบโตสูง)'
    elif equity_pct > 40:
        recommendations['portfolio_type'] = 'Balanced (สมดุล)'
    else:
        recommendations['portfolio_type'] = 'Conservative (เน้นปลอดภัย)'

    # 1. ตีความสัดส่วนหุ้น (Equity)
    if equity_pct > 60:
        recommendations['equity_examples'].append("กองทุนดัชนี S&P 500 (ตปท.)")
        recommendations['equity_examples'].append("กองทุนหุ้นเทคโนโลยี (ราย Sector)")
    elif equity_pct > 20:
        recommendations['equity_examples'].append("กองทุนดัชนี SET50 (ในประเทศ)")
    else:
        recommendations['equity_examples'].append("กองทุนหุ้นปันผล (เน้นกระแสเงินสด)")

    # 2. ตีความสัดส่วนพันธบัตร (Bonds)
    if bonds_pct > 50:
        recommendations['bonds_examples'].append("พันธบัตรรัฐบาล (ปลอดภัยสูง)")
    elif bonds_pct > 20:
        recommendations['bonds_examples'].append("กองทุนตราสารหนี้ผสม (ภาครัฐและเอกชน)")
    else:
        recommendations['bonds_examples'].append("กองทุนตราสารหนี้ระยะสั้น")

    # 3. ตีความสัดส่วนเงินฝาก (Cash)
    if cash_pct > 20:
        recommendations['cash_examples'].append("เงินฝากออมทรัพย์ดอกเบี้ยสูง (E-Saving)")
        recommendations['cash_examples'].append("กองทุนรวมตลาดเงิน (Money Market)")
    else:
        recommendations['cash_examples'].append("เงินฝากออมทรัพย์ (สำหรับสภาพคล่อง)")

    return recommendations

# -----------------------------------------------------------------
# MAIN: ส่วนสำหรับทดสอบการทำงาน (Demo Usage)
# -----------------------------------------------------------------
if __name__ == "__main__":
    
    print("--- [Fuzzy Investment Advisor Demo] ---")
    
    # --- ⬇️ (ทดลองเปลี่ยนค่าตรงนี้) ---
    user_inputs = {
        "age": 25,          # (18-80)
        "income": 60000,    # (15000-500000)
        "time": 10,         # (1-30)
        "risk": 8           # (1-10)
    }
    print(f"Inputs: {user_inputs}\n")

    # 1. สร้าง Engine
    engine = FuzzyInvestmentEngine()
    
    # 2. คำนวณผลลัพธ์จาก AI (Core AI)
    portfolio = engine.calculate_portfolio(
        user_inputs['age'],
        user_inputs['income'],
        user_inputs['time'],
        user_inputs['risk']
    )
    
    if portfolio:
        print("--- 1. ผลลัพธ์จาก AI (Fuzzy Logic) ---")
        print(f"   หุ้น (Equity): {portfolio['equity']:.1f}%")
        print(f"   พันธบัตร (Bonds): {portfolio['bonds']:.1f}%")
        print(f"   เงินฝาก (Cash): {portfolio['cash']:.1f}%")
        
        # 3. ส่งผลลัพธ์ไปให้ Wrapper ตีความ
        examples = get_example_recommendations(
            portfolio['equity'],
            portfolio['bonds'],
            portfolio['cash']
        )
        
        print("\n--- 2. คำแนะนำเพิ่มเติม (Rule-Based Wrapper) ---")
        print(f"   ประเภทพอร์ต: {examples['portfolio_type']}")
        print(f"   ตัวอย่างหุ้น: {examples['equity_examples']}")
        print(f"   ตัวอย่างพันธบัตร: {examples['bonds_examples']}")
        print(f"   ตัวอย่างเงินฝาก: {examples['cash_examples']}")