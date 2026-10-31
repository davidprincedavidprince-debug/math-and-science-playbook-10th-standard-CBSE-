import streamlit as st
import google.generativeai as genai
import json

# ==========================================
# 1. CBSE 10th Standard Syllabus Data
# ==========================================
CBSE_SCIENCE_CHAPTERS = [
    "Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals",
    "Carbon and its Compounds", "Life Processes", "Control and Coordination",
    "How do Organisms Reproduce?", "Heredity and Evolution", "Light – Reflection and Refraction",
    "The Human Eye and the Colourful World", "Electricity", "Magnetic Effects of Electric Current",
    "Our Environment"
]

CBSE_MATHS_CHAPTERS = [
    "Real Numbers", "Polynomials", "Pair of Linear Equations in Two Variables",
    "Quadratic Equations", "Arithmetic Progressions", "Triangles",
    "Coordinate Geometry", "Introduction to Trigonometry", "Some Applications of Trigonometry",
    "Circles", "Areas Related to Circles", "Surface Areas and Volumes",
    "Statistics", "Probability"
]

# ==========================================
# 2. UI Translations Dictionary (i18n)
# ==========================================
UI_TEXT = {
    "English": {
        "science_title": "🧪 CBSE Science Tutor",
        "maths_title": "📐 CBSE Maths Tutor",
        "quiz_title": "📝 CBSE Chapter Quiz",
        "select_chapter": "Select CBSE Chapter:",
        "doubt_label_science": "What specific concept do you need help with?",
        "doubt_label_maths": "Enter your math problem or theorem:",
        "btn_explain": "Explain Concept",
        "btn_solve": "Help Me Solve This",
        "btn_quiz": "Generate Quiz",
        "btn_submit": "Submit Answers",
        "loading": "Thinking and translating...",
        "warn_empty": "Please enter your doubt first.",
        "welcome_msg": "Welcome to the CBSE 10th Standard AI Playbook. Select a chapter from the sidebar to begin."
    },
    "Hindi (हिन्दी)": {
        "science_title": "🧪 सीबीएसई विज्ञान ट्यूटर",
        "maths_title": "📐 सीबीएसई गणित ट्यूटर",
        "quiz_title": "📝 सीबीएसई अध्याय प्रश्नोत्तरी",
        "select_chapter": "सीबीएसई अध्याय चुनें:",
        "doubt_label_science": "आपको किस विशिष्ट अवधारणा में सहायता चाहिए?",
        "doubt_label_maths": "अपनी गणित की समस्या या प्रमेय दर्ज करें:",
        "btn_explain": "अवधारणा समझाएं",
        "btn_solve": "इसे हल करने में मेरी मदद करें",
        "btn_quiz": "प्रश्नोत्तरी बनाएं",
        "btn_submit": "उत्तर जमा करें",
        "loading": "सोच रहा है और अनुवाद कर रहा है...",
        "warn_empty": "कृपया पहले अपना संदेह दर्ज करें।",
        "welcome_msg": "सीबीएसई 10वीं कक्षा एआई प्लेबुक में आपका स्वागत है। शुरू करने के लिए साइडबार से एक अध्याय चुनें।"
    },
    "Tamil (தமிழ்)": {
        "science_title": "🧪 CBSE அறிவியல் ஆசிரியர்",
        "maths_title": "📐 CBSE கணித ஆசிரியர்",
        "quiz_title": "📝 CBSE அத்தியாயம் வினாடி வினா",
        "select_chapter": "CBSE அத்தியாயத்தைத் தேர்ந்தெடுக்கவும்:",
        "doubt_label_science": "எந்த குறிப்பிட்ட கருத்தில் உங்களுக்கு உதவி தேவை?",
        "doubt_label_maths": "உங்கள் கணித பிரச்சனை அல்லது தேற்றத்தை உள்ளிடவும்:",
        "btn_explain": "கருத்தை விளக்கு",
        "btn_solve": "இதை தீர்க்க எனக்கு உதவுங்கள்",
        "btn_quiz": "வினாடி வினாவை உருவாக்கு",
        "btn_submit": "பதில்களைச் சமர்ப்பி",
        "loading": "சிந்திக்கிறது மற்றும் மொழிபெயர்க்கிறது...",
        "warn_empty": "தயவுசெய்து முதலில் உங்கள் சந்தேகத்தை உள்ளிடவும்.",
        "welcome_msg": "CBSE 10 ஆம் வகுப்பு AI பிளேபுக்கிற்கு வரவேற்கிறோம். தொடங்க பக்கப்பட்டியில் இருந்து ஒரு அத்தியாயத்தைத் தேர்ந்தெடுக்கவும்."
    },
    "Marathi (मराठी)": {
        "science_title": "🧪 CBSE विज्ञान शिक्षक",
        "maths_title": "📐 CBSE गणित शिक्षक",
        "quiz_title": "📝 CBSE धडा प्रश्नमंजुषा",
        "select_chapter": "CBSE धडा निवडा:",
        "doubt_label_science": "तुम्हाला कोणत्या विशिष्ट संकल्पनेसाठी मदत हवी आहे?",
        "doubt_label_maths": "तुमची गणिताची समस्या किंवा प्रमेय प्रविष्ट करा:",
        "btn_explain": "संकल्पना समजावून सांगा",
        "btn_solve": "हे सोडवण्यात मला मदत करा",
        "btn_quiz": "प्रश्नमंजुषा तयार करा",
        "btn_submit": "उत्तरे सबमिट करा",
        "loading": "विचार करत आहे आणि भाषांतर करत आहे...",
        "warn_empty": "कृपया प्रथम तुमची शंका प्रविष्ट करा.",
        "welcome_msg": "CBSE 10 वी AI प्लेबुकमध्ये आपले स्वागत आहे. सुरू करण्यासाठी साइडबारमधून एक धडा निवडा."
    },
    "Gujarati (ગુજરાતી)": {
        "science_title": "🧪 CBSE વિજ્ઞાન શિક્ષક",
        "maths_title": "📐 CBSE ગણિત શિક્ષક",
        "quiz_title": "📝 CBSE પ્રકરણ ક્વિઝ",
        "select_chapter": "CBSE પ્રકરણ પસંદ કરો:",
        "doubt_label_science": "તમારે કયા ચોક્કસ ખ્યાલ માટે મદદની જરૂર છે?",
        "doubt_label_maths": "તમારી ગણિતની સમસ્યા અથવા પ્રમેય દાખલ કરો:",
        "btn_explain": "ખ્યાલ સમજાવો",
        "btn_solve": "આને ઉકેલવામાં મારી મદદ કરો",
        "btn_quiz": "ક્વિઝ બનાવો",
        "btn_submit": "જવાબો સબમિટ કરો",
        "loading": "વિચારી રહ્યા છે અને અનુવાદ કરી રહ્યા છે...",
        "warn_empty": "કૃપા કરીને પહેલા તમારી શંકા દાખલ કરો.",
        "welcome_msg": "CBSE 10મું ધોરણ AI પ્લેબુકમાં આપનું સ્વાગત છે. શરૂ કરવા માટે સાઇડબારમાંથી એક પ્રકરણ પસંદ કરો."
    }
}

# ==========================================
# 3. Page Configuration & Header
# ==========================================
st.set_page_config(page_title="Child Fund AI Playbook", layout="centered", page_icon="📚")
st.markdown("## 📚 10th Standard CBSE AI Playbook")
st.info("**Prototype developed for Child Fund India by Prince David Kirubakaran S**")
st.markdown("---")

# ==========================================
# 4. Sidebar Navigation & Global Settings
# ==========================================
st.sidebar.title("⚙️ Settings & Navigation")
languages = list(UI_TEXT.keys())
target_lang = st.sidebar.selectbox("🌐 Choose Language / भाषा", languages)
t = UI_TEXT[target_lang]

st.sidebar.markdown("---")
chapter = st.sidebar.radio("📖 Select Chapter", ["Home", "Science Tutor", "Maths Tutor", "Dynamic Quiz"])

# ==========================================
# 5. API Configuration (Strict Secrets)
# ==========================================
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

text_model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction="You are an expert Indian CBSE high school teacher. Use standard academic terminology strictly aligned with the NCERT 10th-standard syllabus. Format any mathematical equations using standard LaTeX syntax ($ or $$) so they render properly in Markdown."
)

json_model = genai.GenerativeModel(
    'gemini-1.5-flash', 
    generation_config={"response_mime_type": "application/json"},
    system_instruction="You are an expert Indian CBSE high school examiner."
)

# ==========================================
# 6. Routing Logic (Chapters)
# ==========================================
if chapter == "Home":
    st.write(t["welcome_msg"])
    st.markdown("""
    ### Playbook Modules:
    *   **🧪 Science Tutor**: Explains NCERT concepts using real-world analogies.
    *   **📐 Maths Tutor**: Provides step-by-step guidance for solving CBSE math problems.
    *   **📝 Dynamic Quiz**: Generates chapter-specific JSON-structured quizzes.
    """)

elif chapter == "Science Tutor":
    st.title(t["science_title"])
    selected_science_chap = st.selectbox(t["select_chapter"], CBSE_SCIENCE_CHAPTERS)
    concept = st.text_area(t["doubt_label_science"])

    if st.button(t["btn_explain"]):
        if concept:
            prompt = f"""
            Act as a CBSE 10th Standard Science Teacher.
            The student is asking about '{concept}' from the chapter '{selected_science_chap}'.
            Explain it simply using a relatable, real-world analogy. Keep it under 150 words.
            CRITICAL INSTRUCTION: Output your entire response fluently in {target_lang}.
            """
            with st.spinner(t["loading"]):
                response = text_model.generate_content(prompt)
                st.success(response.text)
        else:
            st.warning(t["warn_empty"])

elif chapter == "Maths Tutor":
    st.title(t["maths_title"])
    selected_maths_chap = st.selectbox(t["select_chapter"], CBSE_MATHS_CHAPTERS)
    problem = st.text_area(t["doubt_label_maths"])

    if st.button(t["btn_solve"]):
        if problem:
            prompt = f"""
            Act as a CBSE 10th Standard Maths Teacher.
            The student needs help with the following problem/concept: '{problem}' from the chapter '{selected_maths_chap}'.
            Provide a step-by-step breakdown of how to solve it. Do not just give the final answer; show the working steps clearly.
            CRITICAL INSTRUCTION: Output your entire response, including the mathematical steps and text explanations, fluently in {target_lang}. Make sure to use standard LaTeX ($...$ or $$...$$) for all math formulas and equations.
            """
            with st.spinner(t["loading"]):
                response = text_model.generate_content(prompt)
                # Using markdown specifically to render the LaTeX equations returned by Gemini
                st.markdown(response.text)
        else:
            st.warning(t["warn_empty"])

elif chapter == "Dynamic Quiz":
    st.title(t["quiz_title"])
    subject = st.radio("Select Subject:", ["Science", "Maths"])
    
    if subject == "Science":
        selected_quiz_chap = st.selectbox(t["select_chapter"], CBSE_SCIENCE_CHAPTERS)
    else:
        selected_quiz_chap = st.selectbox(t["select_chapter"], CBSE_MATHS_CHAPTERS)

    if st.button(t["btn_quiz"]):
        prompt = f"""
        Create a 3-question multiple-choice quiz for a CBSE 10th-grade student on the {subject} chapter: '{selected_quiz_chap}'.
        CRITICAL: The questions, options, and explanations MUST be written fluently in {target_lang}.
        If there are any math equations, format them using LaTeX ($...$).
        Return ONLY a JSON array with this exact structure:
        [{{ "question": "...", "options": ["...", "...", "...", "..."], "answer": "...", "explanation": "..." }}]
        """
        with st.spinner(t["loading"]):
            try:
                response = json_model.generate_content(prompt)
                st.session_state['quiz'] = json.loads(response.text)
                st.session_state['user_answers'] = {} 
            except Exception as e:
                st.error("Failed to generate quiz. The AI response was not valid JSON. Please try again.")

    if 'quiz' in st.session_state:
        st.markdown("---")
        quiz_data = st.session_state['quiz']
        
        for i, q in enumerate(quiz_data):
            st.markdown(f"**{i+1}. {q['question']}**")
            st.session_state['user_answers'][i] = st.radio(
                "Options", 
                q['options'], 
                key=f"q_{i}", 
                index=None, 
                label_visibility="collapsed"
            )
            st.markdown("---")

        if st.button(t["btn_submit"]):
            score = 0
            for i, q in enumerate(quiz_data):
                user_ans = st.session_state['user_answers'].get(i)
                if user_ans == q['answer']:
                    st.success(f"✅ Q{i+1}: Correct! ({user_ans})")
                    score += 1
                else:
                    st.error(f"❌ Q{i+1}: Incorrect. You chose: {user_ans}. Correct Answer: {q['answer']}")
                st.info(f"💡 Explanation: {q['explanation']}")
            
            st.metric(label="Final Score", value=f"{score} / {len(quiz_data)}")
