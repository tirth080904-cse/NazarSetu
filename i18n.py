"""
NazarSetu Internationalization (i18n) Engine.

Provides comprehensive, high-performance, dictionary-based localized strings for:
- English (en)
- Hindi (hi)
- Gujarati (gu)

Ensures 100% zero-dependency offline multilingual accessibility across all views:
Streetverse Canvas, AI Investigation Studio, AI Mission Control, The Repair Story,
CivicTwin Transformation Studio, Neighborhood Pulse, and Civic Operations Studio.
"""

from typing import Dict, Any, Optional

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Navigation & Branding
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
    "streetverse_tagline": {
        "en": "Every Street Has a Story. Let's Change the Ending.",
        "hi": "हर गली की एक कहानी है। आइए इसका अंत बदलें।",
        "gu": "દરેક શેરીની એક વાર્તા છે. ચાલો તેનો અંત બદલીએ.",
    },

    # Command Capsule Navigation
    "capsule_explore": {
        "en": "🗺️ Explore",
        "hi": "🗺️ अन्वेषण",
        "gu": "🗺️ અન્વેષણ",
    },
    "capsule_report": {
        "en": "📸 Report",
        "hi": "📸 रिपोर्ट करें",
        "gu": "📸 ફરિયાદ કરો",
    },
    "capsule_mission": {
        "en": "🚀 AI Mission",
        "hi": "🚀 एआई मिशन",
        "gu": "🚀 એઆઈ મિશન",
    },
    "capsule_track": {
        "en": "🔍 Track Story",
        "hi": "🔍 कहानी ट्रैक",
        "gu": "🔍 વાર્તા ટ્રેક",
    },
    "capsule_civictwin": {
        "en": "♊ CivicTwin",
        "hi": "♊ सिविकट्विन",
        "gu": "♊ સિવિકટ્વિન",
    },
    "capsule_pulse": {
        "en": "📊 Neighborhood",
        "hi": "📊 इलाका पल्स",
        "gu": "📊 વિસ્તાર પલ્સ",
    },
    "capsule_admin": {
        "en": "🛡️ Operations",
        "hi": "🛡️ प्रशासन",
        "gu": "🛡️ સંચાલન",
    },
    "capsule_ask_ai": {
        "en": "🤖 Ask AI",
        "hi": "🤖 एआई साथी",
        "gu": "🤖 AI સાથી",
    },
    "capsule_stories": {
        "en": "📖 Stories",
        "hi": "📖 इलाका गाथा",
        "gu": "📖 વિસ્તાર વાર્તાઓ",
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
        "gu": "✅ સત્તાવાર મહાનગરપાલિકા ઉકેલની પુષ્ટિ કરો",
    },
    "btn_ask_ai": {
        "en": "🤖 Ask AI",
        "hi": "🤖 एआई से पूछें",
        "gu": "🤖 AI ને પૂછો",
    },
    "btn_return_street": {
        "en": "↩️ Return to Street",
        "hi": "↩️ मुख्य गली पर लौटें",
        "gu": "↩️ મુખ્ય શેરી પર પાછા ફરો",
    },
    "btn_inspect_dossier": {
        "en": "Inspect Dossier",
        "hi": "केस फाइल देखें",
        "gu": "કેસ ફાઇલ જુઓ",
    },
    "btn_follow_repair_story": {
        "en": "🔍 Follow in Repair Story",
        "hi": "🔍 मरम्मत यात्रा ट्रैक करें",
        "gu": "🔍 સમારકામ વાર્તા ટ્રેક કરો",
    },
    "btn_run_investigation": {
        "en": "🚀 Run AI Multimodal Diagnosis & Investigation",
        "hi": "🚀 एआई मल्टीमॉडल निदान एवं अनुसंधान शुरू करें",
        "gu": "🚀 AI મલ્ટીમોડલ નિદાન અને તપાસ શરૂ કરો",
    },
    "btn_confirm_file": {
        "en": "✍️ Confirm & Officially File Complaint",
        "hi": "✍️ पुष्टि करें और आधिकारिक शिकायत दर्ज करें",
        "gu": "✍️ પુષ્ટિ કરો અને સત્તાવાર ફરિયાદ નોંધાવો",
    },
    "btn_trigger_pipeline": {
        "en": "🚀 Trigger Real 10-Stage Agent Execution",
        "hi": "🚀 वास्तविक 10-चरणीय एजेंट निष्पादन शुरू करें",
        "gu": "🚀 વાસ્તવિક 10-તબક્કાનું એજન્ટ અમલીકરણ શરૂ કરો",
    },
    "btn_find_story": {
        "en": "🔍 Find Story",
        "hi": "🔍 कहानी खोजें",
        "gu": "🔍 વાર્તા શોધો",
    },
    "btn_ask_assistant": {
        "en": "Ask Assistant",
        "hi": "सहायक से पूछें",
        "gu": "સહાયકને પૂછો",
    },
    "btn_run_twin_studio": {
        "en": "🚀 Run Multimodal CivicTwin Verification Inspection",
        "hi": "🚀 मल्टीमॉडल सिविकट्विन सत्यापन निरीक्षण चलाएं",
        "gu": "🚀 મલ્ટીમોડલ સિવિકટ્વિન ચકાસણી નિરીક્ષણ શરૂ કરો",
    },
    "btn_confirm_resolution": {
        "en": "✅ Confirm Official Municipal Resolution",
        "hi": "✅ आधिकारिक नगर निगम समाधान की पुष्टि करें",
        "gu": "✅ સત્તાવાર મહાનગરપાલિકા ઉકેલની પુષ્ટિ કરો",
    },
    "btn_commit_status": {
        "en": "💾 Commit Status Transition to SQLite",
        "hi": "💾 डेटाबेस में स्थिति परिवर्तन सुरक्षित करें",
        "gu": "💾 ડેટાબેઝમાં સ્થિતિ સંક્રમણ સાચવો",
    },
    "btn_open_twin_studio": {
        "en": "♊ Open in CivicTwin Studio",
        "hi": "♊ सिविकट्विन स्टूडियो में खोलें",
        "gu": "♊ સિવિકટ્વિન સ્ટુડિયોમાં ખોલો",
    },
    "btn_send_query": {
        "en": "Send Query",
        "hi": "प्रश्न भेजें",
        "gu": "પ્રશ્ન મોકલો",
    },

    # Common Telemetry & Statuses
    "live_telemetry": {
        "en": "Live City Telemetry",
        "hi": "सक्रिय नगर टेलीमेट्री",
        "gu": "લાઇવ નગર ટેલિમેટ્રી",
    },
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
    "status_pending": {
        "en": "Pending",
        "hi": "लंबित",
        "gu": "બાકી",
    },

    # Priority Levels
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
    "Low": {
        "en": "Low",
        "hi": "सामान्य (Low)",
        "gu": "સામાન્ય (Low)",
    },
    "Medium": {
        "en": "Medium",
        "hi": "मध्यम (Medium)",
        "gu": "મધ્યમ (Medium)",
    },
    "High": {
        "en": "High",
        "hi": "उच्च (High)",
        "gu": "ઉચ્ચ (High)",
    },
    "Critical": {
        "en": "Critical",
        "hi": "गंभीर (Critical)",
        "gu": "ગંભીર (Critical)",
    },
    "Reported": {
        "en": "Reported",
        "hi": "दर्ज (Reported)",
        "gu": "નોંધાયેલ (Reported)",
    },
    "Assigned": {
        "en": "Assigned",
        "hi": "आवंटित (Assigned)",
        "gu": "સોંપાયેલ (Assigned)",
    },
    "In Progress": {
        "en": "In Progress",
        "hi": "प्रगति पर (In Progress)",
        "gu": "પ્રગતિમાં (In Progress)",
    },
    "Awaiting Verification": {
        "en": "Awaiting Verification",
        "hi": "सत्यापन प्रतीक्षित (Awaiting Verification)",
        "gu": "ચકાસણી બાકી (Awaiting Verification)",
    },
    "Resolved": {
        "en": "Resolved",
        "hi": "समाधान पूर्ण (Resolved)",
        "gu": "ઉકેલાઈ ગયેલ (Resolved)",
    },

    # Supported Issue Categories
    "cat_potholes": {
        "en": "Potholes and damaged roads",
        "hi": "सड़क के गड्ढे एवं क्षतिग्रस्त मार्ग",
        "gu": "રસ્તાના ખાડા અને તૂટેલા રસ્તા",
    },
    "cat_garbage": {
        "en": "Overflowing garbage",
        "hi": "सड़कों पर फैला कचरा",
        "gu": "ઉભરાતો કચરો",
    },
    "cat_streetlights": {
        "en": "Broken streetlights",
        "hi": "खराब स्ट्रीटलाइट्स",
        "gu": "બંધ સ્ટ્રીટલાઇટ",
    },
    "cat_drainage": {
        "en": "Waterlogging and drainage issues",
        "hi": "जलभराव एवं ड्रेनेज समस्याएं",
        "gu": "પાણી ભરાવ અને ડ્રેનેજ સમસ્યાઓ",
    },

    # Nodal Municipal Departments
    "dept_roads": {
        "en": "Roads & Infrastructure Department",
        "hi": "सड़क एवं बुनियादी ढांचा विभाग",
        "gu": "માર્ગ અને ઇન્ફ્રાસ્ટ્રક્ચર વિભાગ",
    },
    "dept_waste": {
        "en": "Solid Waste Management Department",
        "hi": "ठोस अपशिष्ट प्रबंधन विभाग",
        "gu": "ઘન કચરો વ્યવસ્થાપન વિભાગ",
    },
    "dept_electrical": {
        "en": "Electrical & Public Lighting Department",
        "hi": "विद्युत एवं सार्वजनिक प्रकाश विभाग",
        "gu": "વીજળી અને જાહેર લાઇટિંગ વિભાગ",
    },
    "dept_drainage": {
        "en": "Stormwater & Drainage Department",
        "hi": "तूफानी जल एवं जल निकासी विभाग",
        "gu": "વરસાદી પાણી અને ડ્રેનેજ વિભાગ",
    },
    # Cities
    "Bengaluru": {"en": "Bengaluru", "hi": "बेंगलुरु", "gu": "બેંગલુરુ"},
    "Mumbai": {"en": "Mumbai", "hi": "मुंबई", "gu": "મુંબઈ"},
    "Delhi": {"en": "Delhi", "hi": "दिल्ली", "gu": "દિલ્હી"},
    "Ahmedabad": {"en": "Ahmedabad", "hi": "अहमदाबाद", "gu": "અમદાવાદ"},
    "Pune": {"en": "Pune", "hi": "पुणे", "gu": "પુણે"},

    # Scenarios & Quick Stories
    "scenario_bengaluru_pothole": {"en": "Bengaluru Pothole", "hi": "बेंगलुरु गड्ढा", "gu": "બેંગલુરુ ખાડો"},
    "scenario_mumbai_garbage": {"en": "Mumbai Garbage", "hi": "मुंबई कचरा", "gu": "મુંબઈ કચરો"},
    "scenario_delhi_light": {"en": "Delhi Streetlight", "hi": "दिल्ली स्ट्रीटलाइट", "gu": "દિલ્હી સ્ટ્રીટલાઇટ"},
    "scenario_ahmedabad_drain": {"en": "Ahmedabad Drainage", "hi": "अहमदाबाद ड्रेनेज", "gu": "અમદાવાદ ડ્રેનેજ"},
    "pothole_short": {"en": "Pothole", "hi": "गड्ढा", "gu": "ખાડો"},
    "garbage_short": {"en": "Garbage", "hi": "कचरा", "gu": "કચરો"},
    "light_short": {"en": "Light", "hi": "लाइट", "gu": "લાઇટ"},
    "drain_short": {"en": "Drain", "hi": "ड्रेन", "gu": "ડ્રેનેજ"},
    "demo_road_story": {"en": "NS-DEMO-A101B202 (Road)", "hi": "NS-DEMO-A101B202 (सड़क)", "gu": "NS-DEMO-A101B202 (રસ્તો)"},
    "demo_waste_story": {"en": "NS-DEMO-C303D404 (Waste)", "hi": "NS-DEMO-C303D404 (कचरा)", "gu": "NS-DEMO-C303D404 (કચરો)"},
    "demo_light_story": {"en": "NS-DEMO-E505F606 (Lighting)", "hi": "NS-DEMO-E505F606 (लाइट)", "gu": "NS-DEMO-E505F606 (લાઇટ)"},
    "active_reports_sub": {"en": "active reports", "hi": "सक्रिय मामले", "gu": "સક્રિય ફરિયાદો"},
    "lighting_incidents_sub": {"en": "lighting incidents", "hi": "प्रकाश मामले", "gu": "લાઇટિંગ કેસ"},
    "waste_points_sub": {"en": "waste points", "hi": "कचरा पॉइंट", "gu": "કચરા પોઇન્ટ"},
    "drainage_issues_sub": {"en": "drainage issues", "hi": "जल निकासी समस्याएं", "gu": "ડ્રેનેજ સમસ્યાઓ"},
    "hotspot_road_btn": {"en": "Inspect Road Cases", "hi": "सड़क मामले देखें", "gu": "રસ્તાના કેસ જુઓ"},
    "hotspot_light_btn": {"en": "Inspect Streetlights", "hi": "लाइट मामले देखें", "gu": "લાઇટના કેસ જુઓ"},
    "hotspot_waste_btn": {"en": "Inspect Waste Cases", "hi": "कचरा मामले देखें", "gu": "કચરાના કેસ જુઓ"},
    "hotspot_drain_btn": {"en": "Inspect Drainage", "hi": "ड्रेनेज मामले देखें", "gu": "ડ્રેનેજના કેસ જુઓ"},
    "street_signals_title": {"en": "Interactive Infrastructure Signals", "hi": "इंटरैक्टिव बुनियादी ढांचा संकेत", "gu": "ઇન્ટરેક્ટિવ ઇન્ફ્રાસ્ટ્રક્ચર સંકેતો"},
    "street_signals_desc": {"en": "Click any infrastructure point to inspect live civic records or report a new problem:", "hi": "सक्रिय नागरिक रिकॉर्ड देखने या नई समस्या दर्ज करने के लिए किसी भी बुनियादी ढांचा बिंदु पर क्लिक करें:", "gu": "સક્રિય નાગરિક રેકોર્ડ જોવા અથવા નવી ફરિયાદ નોંધવા માટે કોઈપણ ઈન્ફ્રાસ્ટ્રક્ચર બિંદુ પર ક્લિક કરો:"},

    # Home / Street Scene Section
    "street_signals_title": {
        "en": "🏘️ Interactive Infrastructure Signals",
        "hi": "🏘️ लाइव नागरिक बुनियादी ढांचा संकेत",
        "gu": "🏘️ લાઈવ નાગરિક ઈન્ફ્રાસ્ટ્રક્ચર સંકેતો",
    },
    "street_signals_desc": {
        "en": "Click any infrastructure point to inspect live civic records or report a new problem:",
        "hi": "सक्रिय नागरिक रिकॉर्ड देखने या नई समस्या दर्ज करने के लिए किसी भी बुनियादी ढांचा बिंदु पर क्लिक करें:",
        "gu": "સક્રિય નાગરિક રેકોર્ડ જોવા અથવા નવી ફરિયાદ નોંધવા માટે કોઈપણ ઈન્ફ્રાસ્ટ્રક્ચર બિંદુ પર ક્લિક કરો:",
    },
    "hotspot_road_title": {
        "en": "Damaged Road Carriage & Potholes",
        "hi": "टूटी सड़क एवं गड्ढे",
        "gu": "ક્ષતિગ્રસ્ત રસ્તો અને ખાડા",
    },
    "hotspot_road_sub": {
        "en": "active reports",
        "hi": "सक्रिय शिकायतें",
        "gu": "સક્રિય ફરિયાદો",
    },
    "hotspot_road_btn": {
        "en": "Inspect Road Cases",
        "hi": "सड़क मामले देखें",
        "gu": "રસ્તાના કેસ જુઓ",
    },
    "hotspot_road_hint": {
        "en": "Road craters, asphalt fissures & pavement degradation",
        "hi": "सड़क के गड्ढे, डामर की दरारें एवं फुटपाथ क्षति",
        "gu": "રસ્તાના ખાડા, ડામરની તિરાડો અને ફૂટપાથ નુકસાન",
    },
    "hotspot_light_title": {
        "en": "Public Lighting & Streetlamps",
        "hi": "स्ट्रीटलाइट्स एवं सार्वजनिक प्रकाश",
        "gu": "સ્ટ્રીટલાઇટ્સ અને જાહેર લાઇટિંગ",
    },
    "hotspot_light_sub": {
        "en": "lighting incidents",
        "hi": "प्रकाश संबंधी मामले",
        "gu": "લાઇટિંગ સંબંધિત કેસ",
    },
    "hotspot_light_btn": {
        "en": "Inspect Streetlights",
        "hi": "लाइट मामले देखें",
        "gu": "લાઇટના કેસ જુઓ",
    },
    "hotspot_light_hint": {
        "en": "Extinguished sodium lamps, broken diffusers & dark corridors",
        "hi": "बंद लैंप, टूटे हुए डिफ्यूज़र और अंधेरे गलियारे",
        "gu": "બંધ લેમ્પ, તૂટેલા ડિફ્યુઝર અને અંધારી શેરીઓ",
    },
    "hotspot_waste_title": {
        "en": "Waste Collection & Sanitation",
        "hi": "कचरा संग्रहण एवं स्वच्छता",
        "gu": "કચરો સંગ્રહ અને સ્વચ્છતા",
    },
    "hotspot_waste_sub": {
        "en": "waste points",
        "hi": "कचरा शिकायतें",
        "gu": "કચરાની ફરિયાદો",
    },
    "hotspot_waste_btn": {
        "en": "Inspect Waste Cases",
        "hi": "कचरा मामले देखें",
        "gu": "કચરાના કેસ જુઓ",
    },
    "hotspot_waste_hint": {
        "en": "Overflowing dumper bins, sidewalk debris & unsegregated refuse",
        "hi": "उफनते डंपर बिन, फुटपाथ पर कचरा और गंदगी",
        "gu": "ઉભરાતી ડમ્પસ્ટર કચરાપેટી, ફૂટપાથ પર કચરો અને ગંદકી",
    },
    "hotspot_drain_title": {
        "en": "Stormwater Drainage & Flood Corridors",
        "hi": "जलभराव एवं ड्रेनेज व्यवस्था",
        "gu": "વરસાદી પાણી ભરાવ અને ડ્રેનેજ",
    },
    "hotspot_drain_sub": {
        "en": "drainage issues",
        "hi": "जल निकासी समस्याएं",
        "gu": "ડ્રેનેજ સમસ્યાઓ",
    },
    "hotspot_drain_btn": {
        "en": "Inspect Drainage",
        "hi": "ड्रेनेज मामले देखें",
        "gu": "ડ્રેનેજના કેસ જુઓ",
    },
    "hotspot_drain_hint": {
        "en": "Clogged roadside culverts, road waterlogging & surface runoff",
        "hi": "अवरुद्ध पुलिया, सड़क पर जलभराव और रुका हुआ पानी",
        "gu": "ભરાયેલી ગટર, રસ્તા પર પાણી ભરાવ અને વરસાદી વહેણ",
    },

    # Hotspot Inspector View
    "hotspot_inspect_tag": {
        "en": "CIVIC INFRASTRUCTURE INSPECTION",
        "hi": "नागरिक बुनियादी ढांचा निरीक्षण",
        "gu": "નાગરિક ઈન્ફ્રાસ્ટ્રક્ચર નિરીક્ષણ",
    },
    "responsible_nodal_body": {
        "en": "Responsible Nodal Body",
        "hi": "जिम्मेदार नोडल विभाग",
        "gu": "જવાબદાર નોડલ વિભાગ",
    },
    "report_at_location": {
        "en": "📸 Report at this Location",
        "hi": "📸 यहाँ समस्या दर्ज करें",
        "gu": "📸 અહીં ફરિયાદ નોંધાવો",
    },
    "active_cases_heading": {
        "en": "Active Cases in Streetview",
        "hi": "सक्रिय नागरिक मामले",
        "gu": "સક્રિય નાગરિક કેસો",
    },
    "no_active_complaints": {
        "en": "✨ No active complaints found. The illustrated infrastructure is in verified clean state!",
        "hi": "✨ कोई सक्रिय शिकायत नहीं मिली। यह बुनियादी ढांचा पूरी तरह स्वच्छ स्थिति में है!",
        "gu": "✨ કોઈ સક્રિય ફરિયાદ મળી નથી. આ ઈન્ફ્રાસ્ટ્રક્ચર સંપૂર્ણપણે સ્વચ્છ સ્થિતિમાં છે!",
    },

    # Case Dossier Drawer
    "case_dossier_tag": {
        "en": "CIVIC CASE DOSSIER",
        "hi": "आधिकारिक नागरिक केस डॉसियर",
        "gu": "સત્તાવાર નાગરિક કેસ ડોઝિયર",
    },
    "ward_label": {
        "en": "Ward",
        "hi": "वार्ड",
        "gu": "વોર્ડ",
    },
    "status_label": {
        "en": "STATUS",
        "hi": "स्थिति",
        "gu": "સ્થિતિ",
    },
    "priority_label": {
        "en": "Priority",
        "hi": "प्राथमिकता",
        "gu": "અગ્રતા",
    },
    "ai_topography_evidence": {
        "en": "AI Visual Topography Evidence",
        "hi": "एआई दृश्य स्थलाकृति साक्ष्य",
        "gu": "AI દ્રશ્ય ટોપોગ્રાફી પુરાવા",
    },
    "citizen_statement": {
        "en": "Citizen Statement:",
        "hi": "नागरिक का बयान:",
        "gu": "નાગરિકનું નિવેદન:",
    },
    "assigned_authority": {
        "en": "Assigned Authority",
        "hi": "आवंटित विभाग",
        "gu": "સોંપાયેલ સત્તામંડળ",
    },
    "filing_timestamp": {
        "en": "Filing Timestamp",
        "hi": "दर्ज करने का समय",
        "gu": "નોંધણી સમય",
    },
    "official_event_trail": {
        "en": "📜 Official Municipal Event Trail",
        "hi": "📜 आधिकारिक नगर निगम घटनाक्रम ऑडिट",
        "gu": "📜 સત્તાવાર મહાનગરપાલિકા ઘટનાક્રમ ઓડિટ",
    },

    # Report / Investigation Studio
    "inv_tag": {
        "en": "AI INVESTIGATION MODE",
        "hi": "एआई अनुसंधान मोड",
        "gu": "AI તપાસ મોડ",
    },
    "inv_headline": {
        "en": "📸 Autonomous Civic Evidence Investigation",
        "hi": "📸 स्वायत्त नागरिक साक्ष्य अनुसंधान",
        "gu": "📸 સ્વાયત્ત નાગરિક પુરાવા તપાસ",
    },
    "inv_desc": {
        "en": "Upload photographic proof to trigger multimodal diagnostic analysis, priority heuristics, and automated ward dispatch.",
        "hi": "मल्टीमॉडल निदान, प्राथमिकता विश्लेषण और स्वचालित वार्ड प्रेषण शुरू करने के लिए फोटो प्रमाण अपलोड करें।",
        "gu": "મલ્ટીમોડલ નિદાન, અગ્રતા વિશ્લેષણ અને સ્વચાલિત વોર્ડ મોકલવા માટે ફોટો પુરાવો અપલોડ કરો.",
    },
    "stage_1_pill": {
        "en": "STAGE 1: Evidence",
        "hi": "चरण 1: साक्ष्य प्रमाण",
        "gu": "તબક્કો 1: પુરાવો",
    },
    "stage_2_pill": {
        "en": "STAGE 2: AI Diagnostic",
        "hi": "चरण 2: एआई निदान",
        "gu": "તબક્કો 2: AI નિદાન",
    },
    "stage_3_pill": {
        "en": "STAGE 3: Autonomous Routing",
        "hi": "चरण 3: स्वायत्त आवंटन",
        "gu": "તબક્કો 3: સ્વાયત્ત રૂટિંગ",
    },
    "stage_4_pill": {
        "en": "STAGE 4: Case File",
        "hi": "चरण 4: केस फाइल",
        "gu": "તબક્કો 4: કેસ ફાઇલ",
    },
    "upload_heading": {
        "en": "1. Upload or Select Sample Incident",
        "hi": "1. फोटो अपलोड करें या नमूना घटना चुनें",
        "gu": "1. ફોટો અપલોડ કરો અથવા નમૂના ઘટના પસંદ કરો",
    },
    "upload_label": {
        "en": "Upload photographic proof",
        "hi": "तस्वीर प्रमाण अपलोड करें",
        "gu": "ફોટોગ્રાફિક પુરાવો અપલોડ કરો",
    },
    "test_cases_label": {
        "en": "Or test with verified scenario cases:",
        "hi": "या सत्यापित परिदृश्य मामलों के साथ परीक्षण करें:",
        "gu": "અથવા ચકાસાયેલ દૃશ્ય કેસો સાથે પરીક્ષણ કરો:",
    },
    "scenario_pothole": {
        "en": "🕳️ Pothole",
        "hi": "🕳️ गड्ढा (Pothole)",
        "gu": "🕳️ ખાડો (Pothole)",
    },
    "scenario_garbage": {
        "en": "🗑️ Garbage",
        "hi": "🗑️ कचरा (Garbage)",
        "gu": "🗑️ કચરો (Garbage)",
    },
    "scenario_light": {
        "en": "💡 Light",
        "hi": "💡 लाइट (Light)",
        "gu": "💡 લાઇટ (Light)",
    },
    "scenario_drain": {
        "en": "🌊 Drain",
        "hi": "🌊 ड्रेनेज (Drain)",
        "gu": "🌊 ડ્રેનેજ (Drain)",
    },
    "locality_heading": {
        "en": "2. Locality Jurisdiction",
        "hi": "2. इलाका एवं क्षेत्राधिकार",
        "gu": "2. વિસ્તાર અને અધિકારક્ષેત્ર",
    },
    "city_select_label": {
        "en": "Municipal City",
        "hi": "नगर निगम शहर",
        "gu": "મહાનગરપાલિકા શહેર",
    },
    "ward_select_label": {
        "en": "Ward / Neighborhood Locality",
        "hi": "वार्ड / स्थानीय इलाका",
        "gu": "વોર્ડ / સ્થાનિક વિસ્તાર",
    },
    "landmark_label": {
        "en": "Landmark / Spot Hint (Optional)",
        "hi": "सीमाचिह्न / स्थान संकेत (वैकल्पिक)",
        "gu": "લેન્ડમાર્ક / સ્થળ સંકેત (વૈકલ્પિક)",
    },
    "photo_placeholder": {
        "en": "📷 Photo preview will appear here.<br>Select a scenario above or upload your photograph.",
        "hi": "📷 फोटो पूर्वावलोकन यहाँ दिखाई देगा।<br>ऊपर एक परिदृश्य चुनें या अपनी तस्वीर अपलोड करें।",
        "gu": "📷 ફોટો પૂર્વાવલોકન અહીં દેખાશે.<br>ઉપરથી એક કેસ પસંદ કરો અથવા તમારો ફોટો અપલોડ કરો.",
    },
    "stage_2_tag": {
        "en": "STAGE 2: AI UNDERSTANDING",
        "hi": "चरण 2: एआई विश्लेषण व समझ",
        "gu": "તબક્કો 2: AI વિશ્લેષણ અને સમજ",
    },
    "diagnosis_label": {
        "en": "Diagnosis",
        "hi": "निदान",
        "gu": "નિદાન",
    },
    "severity_label": {
        "en": "Severity",
        "hi": "गंभीरता",
        "gu": "ગંભીરતા",
    },
    "sla_label": {
        "en": "SLA",
        "hi": "समाधान समय (SLA)",
        "gu": "નિવારણ સમય (SLA)",
    },
    "visual_evidence_label": {
        "en": "Visual Evidence:",
        "hi": "दृश्य साक्ष्य:",
        "gu": "દ્રશ્ય પુરાવો:",
    },
    "citizen_impact_title": {
        "en": "Citizen Impact:",
        "hi": "नागरिकों पर प्रभाव:",
        "gu": "નાગરિકો પર અસર:",
    },
    "action_target_label": {
        "en": "Autonomous Action Target:",
        "hi": "स्वायत्त कार्य योजना:",
        "gu": "સ્વાયત્ત કાર્ય યોજના:",
    },
    "human_affirmation_heading": {
        "en": "3. Citizen Affirmative Authorization",
        "hi": "3. नागरिक आधिकारिक पुष्टि एवं स्वीकृति",
        "gu": "3. નાગરિક સત્તાવાર પુષ્ટિ અને મંજૂરી",
    },
    "human_affirmation_text": {
        "en": "🔒 Strict Human Affirmation Protocol: The AI agent has diagnosed the issue and verified that no active duplicate exists. Please confirm your authorization to officially register this civic case in the municipal ledger.",
        "hi": "🔒 मानवीय पुष्टि प्रोटोकॉल: एआई एजेंट ने समस्या का निदान कर लिया है और पुष्टि की है कि कोई पूर्व डुप्लिकेट शिकायत नहीं है। आधिकारिक तौर पर इसे नगर निगम में दर्ज करने के लिए पुष्टि करें।",
        "gu": "🔒 માનવીય પુષ્ટિ પ્રોટોકોલ: AI એજન્ટે સમસ્યાનું નિદાન કર્યું છે અને ચકાસ્યું છે કે કોઈ અગાઉની ડુપ્લિકેટ ફરિયાદ નથી. સત્તાવાર રીતે મહાનગરપાલિકામાં નોંધવા માટે પુષ્ટિ કરો.",
    },
    "case_created_success": {
        "en": "🎉 Case Created Successfully! Assigned ID:",
        "hi": "🎉 शिकायत सफलतापूर्वक दर्ज की गई! आवंटित आईडी:",
        "gu": "🎉 ફરિયાદ સફળતાપૂર્વક નોંધાઈ ગઈ! સોંપાયેલ ID:",
    },

    # AI Mission Control Workshop
    "mission_tag": {
        "en": "CIVIC AI MISSION CONTROL • AGENT WORKSHOP",
        "hi": "नागरिक एआई मिशन कंट्रोल • एजेंट वर्कशॉप",
        "gu": "નાગરિક AI મિશન કંટ્રોલ • એજન્ટ વર્કશોપ",
    },
    "mission_headline": {
        "en": "🚀 Autonomous Cognitive Perception & Tool Execution Engine",
        "hi": "🚀 स्वायत्त संज्ञानात्मक बोध एवं टूल निष्पादन इंजन",
        "gu": "🚀 સ્વાયત્ત જ્ઞાનાત્મક બોધ અને ટૂલ અમલીકરણ એન્જિન",
    },
    "mission_desc": {
        "en": "Inspect the real 10-stage cognitive perception and autonomous dispatch pipeline. See actual tool arguments, hashes, department routing, and ACID transaction commits.",
        "hi": "वास्तविक 10-चरणीय संज्ञानात्मक बोध और स्वायत्त प्रेषण पाइपलाइन का निरीक्षण करें। वास्तविक टूल तर्क, हैश, विभाग रूटिंग और डेटाबेस लेनदेन देखें।",
        "gu": "વાસ્તવિક 10-તબક્કાના જ્ઞાનાત્મક બોધ અને સ્વાયત્ત મોકલવાની પાઇપલાઇનનું નિરીક્ષણ કરો. વાસ્તવિક ટૂલ દલીલો, હેશ, વિભાગ રૂટિંગ અને ડેટાબેઝ વ્યવહારો જુઓ.",
    },
    "node_observe": {
        "en": "1. OBSERVE",
        "hi": "1. अवलोकन (OBSERVE)",
        "gu": "1. નિરીક્ષણ (OBSERVE)",
    },
    "node_observe_sub": {
        "en": "Perceptual Hash",
        "hi": "पर्सेप्चुअल हैश",
        "gu": "પર્સેપ્ચ્યુઅલ હેશ",
    },
    "node_analyze": {
        "en": "2. ANALYZE",
        "hi": "2. विश्लेषण (ANALYZE)",
        "gu": "2. વિશ્લેષણ (ANALYZE)",
    },
    "node_analyze_sub": {
        "en": "Vision Topography",
        "hi": "दृष्टि स्थलाकृति",
        "gu": "દ્રષ્ટિ ટોપોગ્રાફી",
    },
    "node_locate": {
        "en": "3. LOCATE",
        "hi": "3. स्थान पहचान (LOCATE)",
        "gu": "3. સ્થાન શોધ (LOCATE)",
    },
    "node_locate_sub": {
        "en": "Ward Directory",
        "hi": "वार्ड निर्देशिका",
        "gu": "વોર્ડ ડિરેક્ટરી",
    },
    "node_route": {
        "en": "4. ROUTE",
        "hi": "4. आवंटन (ROUTE)",
        "gu": "4. ફાળવણી (ROUTE)",
    },
    "node_route_sub": {
        "en": "Matrix Dispatch",
        "hi": "मैट्रिक्स प्रेषण",
        "gu": "મેટ્રિક્સ ડિસ્પેચ",
    },
    "node_register": {
        "en": "5. REGISTER",
        "hi": "5. पंजीयन (REGISTER)",
        "gu": "5. નોંધણી (REGISTER)",
    },
    "node_register_sub": {
        "en": "ACID Ledger Commit",
        "hi": "डेटाबेस लेजर कमिट",
        "gu": "ડેટાબેઝ લેજર કમિટ",
    },
    "pipeline_inspector_title": {
        "en": "⚡ Live Autonomous Pipeline Inspector",
        "hi": "⚡ सजीव स्वायत्त पाइपलाइन निरीक्षक",
        "gu": "⚡ લાઇવ સ્વાયત્ત પાઇપલાઇન નિરીક્ષક",
    },
    "pipeline_inspector_desc": {
        "en": "Select a scenario incident to trigger real agent tools and inspect chronological execution states:",
        "hi": "वास्तविक एजेंट टूल्स चलाने और कालानुक्रमिक निष्पादन देखने के लिए एक परिदृश्य चुनें:",
        "gu": "વાસ્તવિક એજન્ટ ટૂલ્સ ચલાવવા અને તબક્કાવાર સ્થિતિ જોવા માટે એક દૃશ્ય પસંદ કરો:",
    },
    "execution_log_title": {
        "en": "📋 Chronological Stage Execution Log",
        "hi": "📋 कालानुक्रमिक चरण निष्पादन लॉग",
        "gu": "📋 કાલક્રમિક તબક્કા અમલીકરણ લોગ",
    },
    "tool_input_label": {
        "en": "Tool Arguments (Input):",
        "hi": "टूल इनपुट तर्क:",
        "gu": "ટૂલ ઇનપુટ દલીલો:",
    },
    "tool_output_label": {
        "en": "Execution Result (Output):",
        "hi": "निष्पादन परिणाम (आउटपुट):",
        "gu": "અમલીકરણ પરિણામ (આઉટપુટ):",
    },

    # 10 Stages
    "stage_1_name": {"en": "Multimodal Visual Perception", "hi": "मल्टीमॉडल दृश्य बोध", "gu": "મલ્ટીમોડલ દ્રશ્ય બોધ"},
    "stage_2_name": {"en": "Topographical Defect Isolation", "hi": "स्थलाकृतिक दोष पृथक्करण", "gu": "ટોપોગ્રાફિકલ ખામી ઓળખ"},
    "stage_3_name": {"en": "Municipal Locality Geo-lookup", "hi": "नगर निगम इलाका भू-स्थान खोज", "gu": "મહાનગરપાલિકા વિસ્તાર ભૌગોલિક શોધ"},
    "stage_4_name": {"en": "Department Matrix Dispatch", "hi": "विभाग मैट्रिक्स प्रेषण", "gu": "વિભાગ મેટ્રિક્સ ડિસ્પેચ"},
    "stage_5_name": {"en": "Perceptual Hash Duplicate Shield", "hi": "पर्सेप्चुअल हैश डुप्लिकेट सुरक्षा ढाल", "gu": "પર્સેપ્ચ્યુઅલ હેશ ડુપ્લિકેટ સુરક્ષા ઢાલ"},
    "stage_6_name": {"en": "Severity & SLA Allocation", "hi": "गंभीरता एवं समाधान समय निर्धारण", "gu": "ગંભીરતા અને સમય મર્યાદા ફાળવણી"},
    "stage_7_name": {"en": "Citizen Impact Synthesis", "hi": "नागरिक प्रभाव विश्लेषण", "gu": "નાગરિક અસર સંશ્લેષણ"},
    "stage_8_name": {"en": "Human Affirmative Authorization", "hi": "मानवीय आधिकारिक पुष्टि", "gu": "માનવીય સત્તાવાર મંજૂરી"},
    "stage_9_name": {"en": "SQLite ACID Ledger Commit", "hi": "डेटाबेस लेजर सुरक्षित पंजीयन", "gu": "ડેટાબેઝ લેજર સુરક્ષિત નોંધણી"},
    "stage_10_name": {"en": "Event Sourcing Timeline Generation", "hi": "घटनाक्रम ऑडिट टाइमलाइन निर्माण", "gu": "ઘટનાક્રમ ઓડિટ ટાઈમલાઈન નિર્માણ"},

    # The Repair Story
    "story_tag": {
        "en": "THE REPAIR STORY",
        "hi": "मरम्मत की कहानी",
        "gu": "સમારકામની વાર્તા",
    },
    "story_headline": {
        "en": "📖 Journey of a Problem Toward Resolution",
        "hi": "📖 समस्या से समाधान तक की यात्रा",
        "gu": "📖 સમસ્યાથી ઉકેલ સુધીની સફર",
    },
    "story_desc": {
        "en": "Every civic incident has a story. Track its progression through 6 verifiable milestone chapters.",
        "hi": "हर नागरिक समस्या की एक कहानी होती है। 6 सत्यापित मील के पत्थर अध्यायों के माध्यम से इसकी प्रगति ट्रैक करें।",
        "gu": "દરેક નાગરિક સમસ્યાની એક વાર્તા હોય છે. 6 ચકાસાયેલ સીમાચિહ્ન પ્રકરણો દ્વારા તેની પ્રગતિ ટ્રેક કરો.",
    },
    "enter_tracking_id": {
        "en": "Enter Complaint Tracking ID",
        "hi": "शिकायत ट्रैकिंग आईडी दर्ज करें",
        "gu": "ફરિયાદ ટ્રેકિંગ ID દાખલ કરો",
    },
    "quick_demo_stories": {
        "en": "Quick Demo Stories:",
        "hi": "त्वरित डेमो कहानियां:",
        "gu": "ઝડપી ડેમો વાર્તાઓ:",
    },
    "complaint_not_found": {
        "en": "Complaint ID was not found in the official registry. Please check the ID.",
        "hi": "शिकायत आईडी आधिकारिक रजिस्ट्री में नहीं मिली। कृपया आईडी की जांच करें।",
        "gu": "ફરિયાદ ID સત્તાવાર રજિસ્ટ્રીમાં મળી નથી. કૃપા કરીને ID તપાસો.",
    },
    "story_chapters_title": {
        "en": "📜 Story Chapters",
        "hi": "📜 कहानी के अध्याय",
        "gu": "📜 વાર્તાના પ્રકરણો",
    },
    "ch1_title": {
        "en": "DISCOVERED",
        "hi": "समस्या की खोज (DISCOVERED)",
        "gu": "સમસ્યાની શોધ (DISCOVERED)",
    },
    "ch1_desc": {
        "en": "Defect spotted and photographed by citizen.",
        "hi": "नागरिक द्वारा समस्या देखी गई और फोटो खींची गई।",
        "gu": "નાગરિક દ્વારા ખામી જોવા મળી અને ફોટો લેવામાં આવ્યો.",
    },
    "ch2_title": {
        "en": "REPORTED",
        "hi": "दर्ज एवं सत्यापित (REPORTED)",
        "gu": "નોંધાયેલ અને ચકાસાયેલ (REPORTED)",
    },
    "ch2_desc": {
        "en": "Photographic evidence submitted & verified by AI agent.",
        "hi": "तस्वीर साक्ष्य प्रस्तुत और एआई एजेंट द्वारा सत्यापित।",
        "gu": "ફોટોગ્રાફિક પુરાવો સબમિટ અને AI એજન્ટ દ્વારા ચકાસાયેલ.",
    },
    "ch3_title": {
        "en": "ASSIGNED",
        "hi": "विभाग को आवंटित (ASSIGNED)",
        "gu": "વિભાગને સોંપાયેલ (ASSIGNED)",
    },
    "ch3_desc": {
        "en": "Dispatched to responsible department and local ward.",
        "hi": "जिम्मेदार विभाग और स्थानीय वार्ड को भेजा गया।",
        "gu": "જવાબદાર વિભાગ અને સ્થાનિક વોર્ડને મોકલવામાં આવ્યું.",
    },
    "ch4_title": {
        "en": "WORK IN PROGRESS",
        "hi": "कार्य प्रगति पर (IN PROGRESS)",
        "gu": "કાર્ય પ્રગતિમાં (IN PROGRESS)",
    },
    "ch4_desc": {
        "en": "Field engineer dispatched; repair materials and crew on site.",
        "hi": "फील्ड इंजीनियर रवाना; मरम्मत सामग्री व टीम कार्यस्थल पर।",
        "gu": "ફીલ્ડ એન્જિનિયર રવાના; સમારકામ સામગ્રી અને ટીમ સ્થળ પર.",
    },
    "ch5_title": {
        "en": "VERIFICATION",
        "hi": "सिविकट्विन सत्यापन (VERIFICATION)",
        "gu": "સિવિકટ્વિન ચકાસણી (VERIFICATION)",
    },
    "ch5_desc": {
        "en": "CivicTwin Before/After physical restoration comparison.",
        "hi": "सिविकट्विन पहले/बाद में भौतिक मरम्मत की तुलना।",
        "gu": "સિવિકટ્વિન પહેલા/પછી ભૌતિક સમારકામની સરખામણી.",
    },
    "ch6_title": {
        "en": "RESOLVED",
        "hi": "समाधान पूर्ण (RESOLVED)",
        "gu": "સંપૂર્ણ ઉકેલ (RESOLVED)",
    },
    "ch6_desc": {
        "en": "Repair verified with municipal administrative confirmation.",
        "hi": "नगर निगम प्रशासनिक पुष्टि के साथ मरम्मत सत्यापित।",
        "gu": "મહાનગરપાલિકા વહીવટી પુષ્ટિ સાથે સમારકામ ચકાસાયેલ.",
    },
    "ask_ai_complaint_title": {
        "en": "🤖 Ask AI Assistant About This Complaint",
        "hi": "🤖 इस शिकायत के बारे में एआई सहायक से पूछें",
        "gu": "🤖 આ ફરિયાદ વિશે AI સહાયકને પૂછો",
    },
    "ask_ai_complaint_caption": {
        "en": "Ask questions about department dispatch, expected completion, or audit events:",
        "hi": "विभाग प्रेषण, अपेक्षित समापन या घटनाक्रम के बारे में प्रश्न पूछें:",
        "gu": "વિભાગ ડિસ્પેચ, અપેક્ષિત સમાપ્તિ અથવા ઓડિટ ઇવેન્ટ્સ વિશે પ્રશ્નો પૂછો:",
    },

    # CivicTwin Studio
    "twin_tag": {
        "en": "CIVICTWIN TRANSFORMATION STUDIO",
        "hi": "सिविकट्विन रूपांतरण स्टूडियो",
        "gu": "સિવિકટ્વિન રૂપાંતરણ સ્ટુડિયો",
    },
    "twin_headline": {
        "en": "♊ Physical Verification & Restoration Inspector",
        "hi": "♊ भौतिक सत्यापन एवं जीर्णोद्धार निरीक्षक",
        "gu": "♊ ભૌતિક ચકાસણી અને પુનઃસંગ્રહ નિરીક્ષક",
    },
    "twin_desc": {
        "en": "Inspect and verify physical infrastructure repairs side-by-side using multimodal computer vision before closing municipal records.",
        "hi": "नगर निगम रिकॉर्ड बंद करने से पहले मल्टीमॉडल कंप्यूटर विज़न का उपयोग करके भौतिक मरम्मत की जांच और सत्यापन करें।",
        "gu": "મહાનગરપાલિકાના રેકોર્ડ બંધ કરતાં પહેલાં મલ્ટીમોડલ કોમ્પ્યુટર વિઝનનો ઉપયોગ કરીને ભૌતિક સમારકામની તપાસ અને ચકાસણી કરો.",
    },
    "twin_select_label": {
        "en": "Select Complaint Case for Verification Inspection",
        "hi": "सत्यापन निरीक्षण हेतु शिकायत केस चुनें",
        "gu": "ચકાસણી નિરીક્ષણ માટે ફરિયાદ કેસ પસંદ કરો",
    },
    "before_photo_label": {
        "en": "Original Damage (Before)",
        "hi": "मूल क्षति (मरम्मत से पहले)",
        "gu": "મૂળ નુકસાન (સમારકામ પહેલાં)",
    },
    "after_photo_label": {
        "en": "Field Restoration Proof (After)",
        "hi": "कार्यस्थल मरम्मत प्रमाण (मरम्मत के बाद)",
        "gu": "ફીલ્ડ રિપેર પુરાવો (સમારકામ પછી)",
    },
    "ai_delta_tag": {
        "en": "AI RESTORATION DELTA ANALYSIS",
        "hi": "एआई मरम्मत अंतर विश्लेषण",
        "gu": "AI સમારકામ તફાવત વિશ્લેષણ",
    },
    "verified_badge": {
        "en": "VERIFIED RESTORATION ✅",
        "hi": "सत्यापित जीर्णोद्धार ✅",
        "gu": "ચકાસાયેલ પુનઃસંગ્રહ ✅",
    },
    "needs_correction_badge": {
        "en": "NEEDS CORRECTION ⚠️",
        "hi": "सुधार आवश्यक ⚠️",
        "gu": "સુધારાની જરૂર ⚠️",
    },
    "match_confidence": {
        "en": "Match Confidence",
        "hi": "सत्यापन विश्वास स्कोर",
        "gu": "ચકાસણી વિશ્વાસ સ્કોર",
    },
    "topography_diff_label": {
        "en": "Topographical Difference:",
        "hi": "स्थलाकृति अंतर:",
        "gu": "ટોપોગ્રાફિકલ તફાવત:",
    },
    "checklist_title": {
        "en": "Structural Quality Checklist:",
        "hi": "संरचनात्मक गुणवत्ता चेकलिस्ट:",
        "gu": "માળખાકીય ગુણવત્તા ચેકલિસ્ટ:",
    },
    "check_1": {
        "en": "Surface Leveling & Uniformity: PASS",
        "hi": "सतह समतलीकरण एवं एकरूपता: सफल (PASS)",
        "gu": "સપાટી લેવલિંગ અને સમાનતા: સફળ (PASS)",
    },
    "check_2": {
        "en": "Edge Compaction & Asphalt Bonding: PASS",
        "hi": "किनारा संघनन एवं डामर बॉन्डिंग: सफल (PASS)",
        "gu": "કિનારી કોમ્પેક્શન અને ડામર બોન્ડિંગ: સફળ (PASS)",
    },
    "check_3": {
        "en": "Debris & Site Clearance: PASS",
        "hi": "मलबा एवं स्थल सफाई: सफल (PASS)",
        "gu": "કાટમાળ અને સ્થળ સફાઈ: સફળ (PASS)",
    },
    "check_4": {
        "en": "Drainage Slope Integrity: PASS",
        "hi": "जल निकासी ढलान अखंडता: सफल (PASS)",
        "gu": "ડ્રેનેજ ઢોળાવ અખંડિતતા: સફળ (PASS)",
    },
    "admin_signoff_title": {
        "en": "🛡️ Municipal Administrative Sign-Off",
        "hi": "🛡️ नगर निगम प्रशासनिक अंतिम अनुमोदन",
        "gu": "🛡️ મહાનગરપાલિકા વહીવટી અંતિમ મંજૂરી",
    },
    "admin_signoff_desc": {
        "en": "Confirm resolution in the official SQLite database ledger with cryptographic audit trail:",
        "hi": "क्रिप्टोग्राफिक ऑडिट ट्रेल के साथ आधिकारिक डेटाबेस में समाधान की पुष्टि करें:",
        "gu": "ક્રિપ્ટોગ્રાફિક ઓડિટ ટ્રેઇલ સાથે સત્તાવાર ડેટાબેઝમાં ઉકેલની પુષ્ટિ કરો:",
    },
    "resolution_committed_success": {
        "en": "officially transitioned to RESOLVED in SQLite!",
        "hi": "आधिकारिक तौर पर डेटाबेस में सुलझा लिया गया (RESOLVED) दर्ज!",
        "gu": "સત્તાવાર રીતે ડેટાબેઝમાં ઉકેલાઈ ગયેલ (RESOLVED) નોંધાયું!",
    },

    # Neighborhood Pulse
    "pulse_tag": {
        "en": "NEIGHBORHOOD PULSE • GROUNDED CIVIC TELEMETRY",
        "hi": "इलाका पल्स • वास्तविक नागरिक टेलीमेट्री",
        "gu": "વિસ્તાર પલ્સ • વાસ્તવિક નાગરિક ટેલિમેટ્રી",
    },
    "pulse_headline": {
        "en": "📊 Localized Civic Memory & Infrastructure Telemetry",
        "hi": "📊 स्थानीय नागरिक स्मृति एवं बुनियादी ढांचा टेलीमेट्री",
        "gu": "📊 સ્થાનિક નાગરિક સ્મૃતિ અને ઈન્ફ્રાસ્ટ્રક્ચર ટેલિમેટ્રી",
    },
    "pulse_desc": {
        "en": "Explore real community telemetry grounded strictly in authentic municipal database rows across supported jurisdictions.",
        "hi": "समर्थित क्षेत्राधिकारों में प्रामाणिक नगर निगम डेटाबेस से सीधे प्राप्त वास्तविक टेलीमेट्री देखें।",
        "gu": "સમર્થિત અધિકારક્ષેત્રોમાં અધિકૃત મહાનગરપાલિકા ડેટાબેઝમાંથી સીધા મેળવેલ વાસ્તવિક ટેલિમેટ્રી જુઓ.",
    },
    "select_neighborhood_label": {
        "en": "Select Neighborhood to Explore",
        "hi": "अन्वेषण हेतु इलाका चुनें",
        "gu": "અન્વેષણ કરવા માટે વિસ્તાર પસંદ કરો",
    },
    "total_reports": {
        "en": "Total Reports",
        "hi": "कुल शिकायतें",
        "gu": "કુલ ફરિયાદો",
    },
    "recorded_in_sqlite": {
        "en": "Recorded in SQLite",
        "hi": "डेटाबेस में दर्ज",
        "gu": "ડેટાબેઝમાં નોંધાયેલ",
    },
    "active_in_progress": {
        "en": "Active In Progress",
        "hi": "प्रगति में सक्रिय",
        "gu": "પ્રગતિમાં સક્રિય",
    },
    "crews_dispatched": {
        "en": "Crews dispatched",
        "hi": "टीमें तैनात",
        "gu": "ટીમો તૈનાત",
    },
    "verified_resolved": {
        "en": "Verified Resolved",
        "hi": "सत्यापित समाधान",
        "gu": "ચકાસાયેલ ઉકેલ",
    },
    "civictwin_verified": {
        "en": "CivicTwin verified",
        "hi": "सिविकट्विन द्वारा सत्यापित",
        "gu": "સિવિકટ્વિન દ્વારા ચકાસાયેલ",
    },
    "resolution_rate": {
        "en": "Resolution Rate",
        "hi": "समाधान दर (Rate)",
        "gu": "ઉકેલ દર (Rate)",
    },
    "overall_velocity": {
        "en": "Overall velocity",
        "hi": "कुल गति",
        "gu": "કુલ ગતિ",
    },
    "civic_intelligence_synthesis": {
        "en": "Civic Intelligence Synthesis",
        "hi": "नागरिक बुद्धिमत्ता संश्लेषण",
        "gu": "નાગરિક બુદ્ધિમત્તા સંશ્લેષણ",
    },
    "active_community_cases": {
        "en": "Active Community Case Files in",
        "hi": "सक्रिय सामुदायिक केस फाइलें:",
        "gu": "સક્રિય સામુદાયિક કેસ ફાઇલો:",
    },

    # Operations Studio (Admin)
    "admin_tag": {
        "en": "CIVIC OPERATIONS STUDIO • DISPATCH CONSOLE",
        "hi": "नागरिक संचालन स्टूडियो • प्रेषण कंसोल",
        "gu": "નાગરિક સંચાલન સ્ટુડિયો • ડિસ્પેચ કન્સોલ",
    },
    "admin_headline": {
        "en": "🛡️ Municipal Grievance Administration & Audit",
        "hi": "🛡️ नगर निगम शिकायत प्रशासन एवं ऑडिट",
        "gu": "🛡️ મહાનગરપાલિકા ફરિયાદ વહીવટ અને ઓડિટ",
    },
    "admin_desc": {
        "en": "Authorized municipal operations console for status transitions, nodal department routing, and audit trail inspection.",
        "hi": "स्थिति परिवर्तन, नोडल विभाग रूटिंग और ऑडिट ट्रेल निरीक्षण के लिए अधिकृत नगर निगम संचालन कंसोल।",
        "gu": "સ્થિતિ સંક્રમણ, નોડલ વિભાગ રૂટિંગ અને ઓડિટ ટ્રેઇલ નિરીક્ષણ માટે અધિકૃત મહાનગરપાલિકા સંચાલન કન્સોલ.",
    },
    "filter_status_label": {
        "en": "Filter by Status",
        "hi": "स्थिति अनुसार फ़िल्टर करें",
        "gu": "સ્થિતિ અનુસાર ફિલ્ટર કરો",
    },
    "search_id_locality": {
        "en": "Search ID or Locality",
        "hi": "आईडी या इलाका खोजें",
        "gu": "ID અથવા વિસ્તાર શોધો",
    },
    "found_matching_complaints": {
        "en": "Found Matching Complaints:",
        "hi": "प्राप्त मेल खाती शिकायतें:",
        "gu": "મળેલી મેળ ખાતી ફરિયાદો:",
    },
    "select_complaint_manage": {
        "en": "Select Complaint to Manage",
        "hi": "प्रबंधन हेतु शिकायत चुनें",
        "gu": "સંચાલન માટે ફરિયાદ પસંદ કરો",
    },
    "update_status_transition": {
        "en": "Update Status Transition",
        "hi": "स्थिति परिवर्तन अपडेट करें",
        "gu": "સ્થિતિ સંક્રમણ અપડેટ કરો",
    },
    "officer_action_notes": {
        "en": "Officer Action Notes",
        "hi": "अधिकारी कार्रवाई नोट्स",
        "gu": "અધિકારી કાર્યવાહી નોંધ",
    },

    # AI Companion
    "companion_tag": {
        "en": "AI CITY COMPANION",
        "hi": "एआई नगर साथी",
        "gu": "AI નગર સાથી",
    },
    "companion_headline": {
        "en": "🤖 Your Grounded Civic Assistant",
        "hi": "🤖 आपका विश्वसनीय नागरिक सहायक",
        "gu": "🤖 તમારો વિશ્વાસુ નાગરિક સહાયક",
    },
    "companion_desc": {
        "en": "Ask questions about complaint routing, department responsibilities, or municipal resolution metrics.",
        "hi": "शिकायत रूटिंग, विभाग जिम्मेदारियों या नगर निगम समाधान मेट्रिक्स के बारे में प्रश्न पूछें।",
        "gu": "ફરિયાદ રૂટિંગ, વિભાગની જવાબદારીઓ અથવા મહાનગરપાલિકાના નિવારણ મેટ્રિક્સ વિશે પ્રશ્નો પૂછો.",
    },
    "prompt_suggestions_label": {
        "en": "Prompt Suggestions:",
        "hi": "सुझाए गए प्रश्न:",
        "gu": "સૂચવેલા પ્રશ્નો:",
    },
    "prompt_1": {
        "en": "Which dept handles potholes?",
        "hi": "गड्ढों का समाधान कौन सा विभाग करता है?",
        "gu": "ખાડાઓનું નિવારણ કયો વિભાગ કરે છે?",
    },
    "prompt_2": {
        "en": "Track NS-DEMO-A101B202",
        "hi": "NS-DEMO-A101B202 ट्रैक करें",
        "gu": "NS-DEMO-A101B202 ટ્રેક કરો",
    },
    "prompt_3": {
        "en": "Neighborhood stats",
        "hi": "इलाके के आंकड़े दिखाएं",
        "gu": "વિસ્તારના આંકડા બતાવો",
    },
    "ask_assistant_placeholder": {
        "en": "e.g. How does NazarSetu verify road repairs?",
        "hi": "उदा. नज़रसेतु सड़क मरम्मत का सत्यापन कैसे करता है?",
        "gu": "દા.ત. નજરસેતુ રસ્તાના સમારકામની ચકાસણી કેવી રીતે કરે છે?",
    },
    "assistant_reply_label": {
        "en": "Autonomous Civic Assistant Response:",
        "hi": "स्वायत्त नागरिक सहायक उत्तर:",
        "gu": "સ્વાયત્ત નાગરિક સહાયક ઉત્તર:",
    },
}


def t(key: str, lang: str = "en") -> str:
    """
    Retrieve translated text by key or direct English phrase with automatic fallback.
    Works bi-directionally: looks up translation codes or natural English strings.
    """
    if not key:
        return ""
    
    # 1. Direct translation key lookup
    item = TRANSLATIONS.get(key)
    if item:
        if lang in item:
            return item[lang]
        return item.get("en", key)

    if lang == "en":
        return str(key)

    # 2. Reverse lookup by matching English phrase directly
    key_str = str(key).strip().lower()
    for code, trans in TRANSLATIONS.items():
        en_val = trans.get("en", "").strip().lower()
        if en_val and en_val == key_str:
            return trans.get(lang, key)

    return key
