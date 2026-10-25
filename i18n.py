"""
NazarSetu Internationalization (i18n) Engine.

Provides high-performance, dictionary-based localized strings for:
- English (en)
- Hindi (hi)
- Gujarati (gu)

Ensures 100% zero-dependency offline multilingual accessibility.
"""

from typing import Dict, Any

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Navigation
    "nav_overview": {
        "en": "🌐 Overview",
        "hi": "🌐 अवलोकन (Overview)",
        "gu": "🌐 ઝાંખી (Overview)",
    },
    "nav_report": {
        "en": "📸 Report Issue",
        "hi": "📸 शिकायत दर्ज करें (Report)",
        "gu": "📸 ફરિયાદ નોંધાવો (Report)",
    },
    "nav_mission_control": {
        "en": "🚀 AI Mission Control",
        "hi": "🚀 एआई मिशन कंट्रोल",
        "gu": "🚀 એઆઈ મિશન કંટ્રોલ",
    },
    "nav_track": {
        "en": "🔍 Track Complaint",
        "hi": "🔍 शिकायत ट्रैक करें (Track)",
        "gu": "🔍 ફરિયાદ ટ્રેક કરો (Track)",
    },
    "nav_civictwin": {
        "en": "♊ CivicTwin Verification",
        "hi": "♊ सिविकट्विन सत्यापन",
        "gu": "♊ સિવિકટ્વિન ચકાસણી",
    },
    "nav_neighborhood_pulse": {
        "en": "📊 Neighborhood Pulse",
        "hi": "📊 इलाका पल्स (Analytics)",
        "gu": "📊 વિસ્તાર પલ્સ (Analytics)",
    },
    "nav_admin": {
        "en": "🛡️ Demo Admin",
        "hi": "🛡️ नगर निगम प्रशासन",
        "gu": "🛡️ નગરપાલિકા સંચાલન",
    },

    # Branding
    "platform_tagline": {
        "en": "From Civic Problems to Intelligent Action",
        "hi": "नागरिक समस्याओं से त्वरित समाधान तक",
        "gu": "નાગરિક સમસ્યાઓથી ત્વરિત ઉકેલ સુધી",
    },
    "platform_subtitle": {
        "en": "An autonomous AI platform that sees civic problems, understands their impact, coordinates action, and verifies progress.",
        "hi": "एक स्वायत्त एआई प्लेटफ़ॉर्म जो नागरिक समस्याओं को समझता है, उनके प्रभाव का विश्लेषण करता है और समाधान सत्यापित करता है।",
        "gu": "એક સ્વાયત્ત AI પ્લેટફોર્મ જે નાગરિક સમસ્યાઓને સમજે છે, અસરનું વિશ્લેષણ કરે છે અને સમાધાનની ચકાસણી કરે છે.",
    },

    # Actions & Buttons
    "btn_analyze": {
        "en": "🔬 Analyze Visual Evidence & Generate Intelligence",
        "hi": "🔬 दृश्य साक्ष्य का विश्लेषण करें और रिपोर्ट बनाएं",
        "gu": "🔬 દ્રશ્ય પુરાવાનું વિશ્લેષણ કરો અને અહેવાલ બનાવો",
    },
    "btn_confirm_register": {
        "en": "🛡️ Confirm & Register Civic Complaint",
        "hi": "🛡️ पुष्टि करें और शिकायत दर्ज करें",
        "gu": "🛡️ પુષ્ટિ કરો અને ફરિયાદ નોંધાવો",
    },
    "btn_verify_repair": {
        "en": "♊ Run CivicTwin Comparison & Inspection",
        "hi": "♊ सिविकट्विन तुलना और निरीक्षण चलाएं",
        "gu": "♊ સિવિકટ્વિન સરખામણી અને તપાસ ચલાવો",
    },
    "btn_admin_resolve": {
        "en": "✅ Confirm Official Municipal Resolution",
        "hi": "✅ आधिकारिक नगर निगम समाधान की पुष्टि करें",
        "gu": "✅ સત્તાવાર નગરપાલિકા ઉકેલની પુષ્ટિ કરો",
    },

    # Statuses
    "status_reported": {
        "en": "Reported",
        "hi": "दर्ज की गई",
        "gu": "નોંધાયેલ",
    },
    "status_assigned": {
        "en": "Assigned",
        "hi": "विभाग को आवंटित",
        "gu": "વિભાગને સોંપાયેલ",
    },
    "status_in_progress": {
        "en": "In Progress",
        "hi": "प्रगति पर है",
        "gu": "પ્રગતિમાં છે",
    },
    "status_awaiting_verification": {
        "en": "Awaiting Verification",
        "hi": "सत्यापन की प्रतीक्षा में",
        "gu": "ચકાસણીની રાહમાં",
    },
    "status_resolved": {
        "en": "Resolved",
        "hi": "सुलझा लिया गया",
        "gu": "ઉકેલાઈ ગયેલ",
    },

    # Priorities
    "priority_low": {
        "en": "Low Priority",
        "hi": "सामान्य प्राथमिकता (Low)",
        "gu": "સામાન્ય અગ્રતા (Low)",
    },
    "priority_medium": {
        "en": "Medium Priority",
        "hi": "मध्यम प्राथमिकता (Medium)",
        "gu": "મધ્યમ અગ્રતા (Medium)",
    },
    "priority_high": {
        "en": "High Priority",
        "hi": "उच्च प्राथमिकता (High)",
        "gu": "ઉચ્ચ અગ્રતા (High)",
    },
    "priority_critical": {
        "en": "🚨 Critical Emergency",
        "hi": "🚨 आपातकालीन / गंभीर (Critical)",
        "gu": "🚨 કટોકટી / ગંભીર (Critical)",
    },

    # Reports
    "civic_intelligence_report": {
        "en": "Civic Intelligence Report",
        "hi": "नागरिक बुद्धिमत्ता रिपोर्ट (Intelligence Report)",
        "gu": "નાગરિક બુદ્ધિમત્તા અહેવાલ (Intelligence Report)",
    },
    "citizen_impact_label": {
        "en": "Projected Citizen Impact",
        "hi": "नागरिकों पर अनुमानित प्रभाव",
        "gu": "નાગરિકો પર અંદાજિત અસર",
    },
    "priority_rationale_label": {
        "en": "Priority Decision Rationale",
        "hi": "प्राथमिकता चयन का कारण",
        "gu": "અગ્રતા પસંદગીનું કારણ",
    },
    "action_plan_label": {
        "en": "Recommended Department Action",
        "hi": "विभाग हेतु अनुशंसित कार्ययोजना",
        "gu": "વિભાગ માટે ભલામણ કરેલ કાર્ય યોજના",
    },
}


def t(key: str, lang: str = "en") -> str:
    """Retrieve translated text by key with automatic English fallback."""
    item = TRANSLATIONS.get(key)
    if not item:
        return key
    return item.get(lang, item.get("en", key))
