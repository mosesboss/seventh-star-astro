# astrology_engine.py
# محرك الحسابات والقواعد التقليدية لتطبيق "النجم السابع"

class EssentialDignities:
    """
    محرك تقييم الكرامات الجوهرية للكواكب (Essential Dignities)
    وفق نظام الدرجات والكرامات الست التقليدية.
    """
    
    # جدول أوزان القوة للكرامات الست
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
        الاحتراق أو التراجع يعطل أو يضعف أثر الكرامات بشدة.
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
    
    # زوايا الاتصالات الكلاسيكية
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
        # نموذج مبسط لفحص اتجاه الحركة والاقتراب من الاتصال
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
        تقييم ما إذا كانت المسألة ستتم أم تتعثر بناءً على القواعد الكلاسيكية:
        - انصراف الدليلين قبل الاتصال = تعثر أو إلغاء.
        - حدوث المنع (Prohibition) أو الرد (Refraction) = فسخ أو تدخل مانع.
        """
        if refraction_detected:
            return "مرفوضة أو متعثرة (بسبب تراجع الكوكب الثقيل - الرد)"
        if prohibition_detected:
            return "ممنوعة (تدخل كوكب ثالث وقطع الاتصال - المنع)"
        if separation_status == "Separating":
            return "متعثرة أو ملغاة (الدليلان منصرفان عن الاتصال)"
        
        return "مبشرة وقابلة للإتمام (الاتصال سليم وقائم)"
