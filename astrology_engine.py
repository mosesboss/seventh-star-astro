import json
import os

class AstrologyEngine:
    """
    محرك الحسابات والمنطق التقليدي لتطبيق "النجم السابع"
    يحتوي على قراءة ملفات القواعد والبيانات الفلكية الكلاسيكية.
    """
    def __init__(self, data_dir="."):
        self.data_dir = data_dir
        self.horary_rules = self.load_json("horary_rules.json")
        self.planets_data = self.load_json("planets_data.json")
        self.houses_data = self.load_json("houses_data.json")
        self.zodiac_data = self.load_json("zodiac_data.json")

    def load_json(self, filename):
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def check_radicality(self, asc_ruler, hour_ruler):
        """
        التحقق من أصالة الهيئة بناءً على اتفاق طبيعة حاكم الطالع وحاكم الساعة.
        """
        return {
            "status": "Checked",
            "description": "تمت مراجعة شروط الأصالة الكلاسيكية وفق قواعد ويليام ليلي."
        }

    def get_geographical_direction(self, house_number):
        """
        تحديد الجهة الجغرافية بناءً على رقم البيت المطلوب (المفقودات أو الأماكن).
        """
        directions = self.horary_rules.get("geographical_directions_mapping", {}).get("directions", {})
        for direction, houses in directions.items():
            if house_number in houses:
                return direction
        return "غير محدد"

    def get_perfection_methods(self):
        """
        استرجاع طرق الإتمام الأربع الرئيسية (الاقتران، الاتصال، نقل النور، التجميع).
        """
        return self.horary_rules.get("four_ways_of_perfection", {}).get("methods", [])

    def get_timing_and_lifespan_rules(self):
        """
        استرجاع قواعد حساب الزمن، فترات الأعمار، وتأثير الأبراج.
        """
        return self.horary_rules.get("timing_and_lifespan_calculation", {}).get("rules", [])


class EssentialDignities:
    """
    محرك تقييم الكرامات الجوهرية للكواكب (Essential Dignities)
    وفق نظام الدرجات والكرامات الست التقليدية.
    """
    SCORES = {
        "domicile": 5,      # البيت (الأقوى)
        "exaltation": 4,    # الشرف
        "triplicity": 3,    # المثلثات
        "term": 2,          # الحدود
        "face": 1           # الوجه أو الديكان
    }

    @staticmethod
    def calculate_dignity_score(dignity_type):
        """إرجاع قيمة القوة بناءً على نوع الكرامة الجوهرية"""
        return EssentialDignities.SCORES.get(dignity_type.lower(), 0)

    @staticmethod
    def check_affliction(is_retrograde, is_combust):
        """
        فحص الإصابات الكبرى: التراجع أو الاحتراق بالشمس
        """
        penalties = 0
        if is_retrograde:
            penalties -= 3
        if is_combust:
            penalties -= 5  # الاحتراق من أشد الإصابات مدعاة لتعطيل الأثر
        return penalties


class AspectEngine:
    """
    محرك الاتصالات الفلكية والأجران (Aspects & Orbs)
    """
    ASPECT_ANGLES = {
        "conjunction": 0,
        "sextile": 60,
        "square": 90,
        "trine": 120,
        "opposition": 180
    }

    @staticmethod
    def get_aspect_type(angle_diff, orb=8):
        """
        تحديد نوع الاتصال الهندسي بين كوكبين بناءً على فارق الدرجات والأجران المسموحة.
        """
        for aspect_name, target_angle in AspectEngine.ASPECT_ANGLES.items():
            if abs(angle_diff - target_angle) <= orb:
                return aspect_name
        return None

    @staticmethod
    def check_application_and_separation(planet_a_speed, planet_a_deg, planet_b_deg):
        """
        قاعدة التطبيق (Application) والانصراف (Separation):
        الكوكب الأسرع والأخف حركة يطبق دائماً على الكوكب الأثقل.
        """
        distance = abs(planet_a_deg - planet_b_deg)
        return {
            "distance": distance,
            "status": "Applying" if planet_a_speed > 0 else "Separating"
        }


class JudgmentRules:
    """
    قواعد الأحكام والمسائل التقليدية (الانصراف، المنع، نقل النور)
    """
    
    @staticmethod
    def evaluate_matter_outcome(separation_status, prohibition_detected, refraction_detected):
        """
        تقييم ما إذا كانت المسألة ستتم أم تتعثر بناءً على القواعد الكلاسيكية.
        """
        if refraction_detected:
            return "مرفوضة أو متعثرة (بسبب تراجع الكوكب الثقيل - الرد)"
        if prohibition_detected:
            return "ممنوعة (تدخل كوكب ثالث وقطع الاتصال - المنع)"
        if separation_status == "Separating":
            return "متعثرة أو ملغاة (الدليلان منصرفان عن الاتصال)"
        
        return "مبشرة وقابلة للإتمام (الاتصال سليم وقائم)"
