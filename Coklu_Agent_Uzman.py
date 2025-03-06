import streamlit as st
from openai import OpenAI
import os
import importlib.util

# OpenAI istemcisini başlat
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
)

# Ana sayfa ve asistan yapılandırmaları
ASSISTANTS = {
    "Ana Sayfa": {
        "title": "Asistan Platformu 🤖",
        "description": "İhtiyacınıza göre bir asistan seçin veya genel bir sohbet başlatın.",
        "icon": "🏠",
        "system_message": """Sen kullanıcıya yardımcı olan genel bir asistansın. 
        Kullanıcının sorularını yanıtla ve ihtiyaç duyduğunda uygun asistanı seçmesini öner.
        Örneğin, Python soruları için Python Asistanını, İngilizce kelimeler için Kelime Asistanını önerebilirsin."""
    },
    "Python Asistanı": {
        "title": "Python Programlama Uzmanı 🐍",
        "description": "Python programlama sorularınızı yanıtlar, kod yazar ve problemleri çözer.",
        "icon": "🐍",
        "system_message": """Sen ileri düzey bir Python programlama uzmanı ve mentörsün. 
        Temel görevlerin:
        1. Derinlemesine, doğru Python programlama rehberliği sağlamak
        2. Karmaşık kavramları net, pratik örneklerle açıklamak
        3. En iyi uygulamaları ve gelişmiş programlama tekniklerini sunmak
        4. Kullanıcıların Python becerilerini öğrenmelerine ve geliştirmelerine yardımcı olmak
        5. Kodu hata ayıklamak ve optimizasyonlar önermek
        
        Cevaplarını Türkçe dilinde ver.""",
        "sidebar_elements": [
            {
                "type": "multiselect",
                "key": "python_topics",
                "label": "Python Konuları",
                "options": ["Web Geliştirme", "Veri Bilimi", "Makine Öğrenimi", "Backend Programlama", 
                            "Algoritma Tasarımı", "Performans Optimizasyonu", "Test", "Eşzamansız Programlama"]
            }
        ]
    },
    "SQL Asistanı": {
        "title": "SQL Veritabanı Uzmanı 📊",
        "description": "SQL sorguları, veritabanı tasarımı ve optimizasyon konularında yardım eder.",
        "icon": "📊",
        "system_message": """Sen uzman bir SQL ve veritabanı danışmanısın.
        Kullanıcılara veritabanı tasarımı, SQL sorguları, optimizasyon ve en iyi uygulamalar 
        konusunda yardımcı olursun. MySQL, PostgreSQL, SQLite ve SQL Server hakkında bilgi sahibisin.
        
        Cevaplarını Türkçe dilinde ver.""",
        "sidebar_elements": [
            {
                "type": "radio",
                "key": "sql_db_type",
                "label": "Veritabanı Türü",
                "options": ["MySQL", "PostgreSQL", "SQLite", "SQL Server", "Oracle", "Diğer"]
            }
        ]
    },
    "Web Geliştirme Asistanı": {
        "title": "HTML/CSS Uzmanı 🌐",
        "description": "Web geliştirme, HTML, CSS ve temel frontend konularında yardım eder.",
        "icon": "🌐",
        "system_message": """Sen bir web geliştirme uzmanısın, özellikle HTML ve CSS konusunda deneyimlisin.
        Kullanıcıların web sayfaları oluşturma, tasarım, düzen ve stil konularındaki sorularına 
        yardımcı olursun. Web geliştirmenin temellerini ve modern uygulamalarını açıklarsın.
        
        Cevaplarını Türkçe dilinde ver.""",
        "sidebar_elements": [
            {
                "type": "checkbox",
                "key": "responsive_design",
                "label": "Mobil Uyumlu Tasarım",
                "default": True
            },
            {
                "type": "radio",
                "key": "framework",
                "label": "Framework",
                "options": ["Saf HTML/CSS", "Bootstrap", "Tailwind CSS", "Material Design", "Diğer"]
            }
        ]
    },
    "İngilizce Kelime Asistanı": {
        "title": "İngilizce Kelime Öğretmeni 📚",
        "description": "İngilizce kelimeleri öğrenmek için akılda kalıcı hikayeler ve örnekler sunar.",
        "icon": "📚",
        "system_message": """Sen İngilizce kelime öğrenmeye yardımcı olan yaratıcı bir eğitim asistanısın.
        
        Kullanıcı sana bir İngilizce kelime sorduğunda:
        1. Kelimenin anlamını Türkçe olarak açıkla
        2. Kelimenin telaffuzunu belirt
        3. Kelimeyi akılda kalıcı bir hikaye, metafor veya benzetme ile anlat
        4. Kelimeyi hatırlamayı kolaylaştıracak bir görsel imaj veya bağlantı oluştur
        5. Kelimenin geçtiği örnek bir cümle yaz
        6. Varsa, kelimenin farklı bağlamlardaki kullanımlarını açıkla
        7. Kelimeyle ilgili eşanlamlı ve zıt anlamlı kelimeleri belirt
        
        Tüm cevaplarını kesinlikle Türkçe dilinde ver.""",
        "sidebar_elements": [
            {
                "type": "slider",
                "key": "difficulty_level",
                "label": "Zorluk Seviyesi",
                "min_value": 1,
                "max_value": 5,
                "value": 3
            },
            {
                "type": "radio",
                "key": "word_category",
                "label": "Kelime Kategorisi",
                "options": ["Genel", "İş Dünyası", "Akademik", "Günlük Konuşma", "Seyahat", "Teknik"]
            }
        ]
    },
    "Excel Formülleri Asistanı": {
        "title": "Excel Formülleri Uzmanı 📈",
        "description": "Excel formülleri, makrolar ve veri analizi konularında yardım eder.",
        "icon": "📈",
        "system_message": """Sen Excel ve veri analizi konusunda uzman bir asistansın.
        Excel formülleri, fonksiyonları, pivot tablolar, makrolar ve veri işleme teknikleri 
        konusunda kullanıcılara yardımcı olursun. Karmaşık formülleri basit bir şekilde açıklarsın.
        
        Cevaplarını Türkçe dilinde ver.""",
        "sidebar_elements": [
            {
                "type": "multiselect",
                "key": "excel_topics",
                "label": "Excel Konuları",
                "options": ["Temel Formüller", "İleri Düzey Formüller", "VLOOKUP/XLOOKUP", "Pivot Tablolar", 
                            "Makrolar", "VBA", "Veri Analizi", "Dashboard Oluşturma"]
            }
        ]
    }
}

# Sayfa yapılandırmasını ayarla
st.set_page_config(
    page_title="Çoklu Asistan Platformu",
    page_icon="🤖",
    layout="wide"
)

# Session state başlatma
if "current_assistant" not in st.session_state:
    st.session_state.current_assistant = "Ana Sayfa"

if "assistant_chat_history" not in st.session_state:
    st.session_state.assistant_chat_history = {name: [] for name in ASSISTANTS.keys()}

# Her asistan için ayrı sistem mesajı başlatma
if "assistant_system_messages" not in st.session_state:
    st.session_state.assistant_system_messages = {
        name: [{"role": "system", "content": config["system_message"]}] 
        for name, config in ASSISTANTS.items()
    }

# Asistan seçim fonksiyonu
def change_assistant():
    st.session_state.current_assistant = st.session_state.assistant_selector

# Yan menü
with st.sidebar:
    st.title("Asistan Seçimi")
    
    # Asistan seçim kutusu
    assistant_selector = st.selectbox(
        "Hangi asistanla konuşmak istersiniz?",
        options=list(ASSISTANTS.keys()),
        key="assistant_selector",
        on_change=change_assistant,
        index=list(ASSISTANTS.keys()).index(st.session_state.current_assistant)
    )
    
    st.divider()
    
    # Mevcut asistanın yan menü öğeleri
    current_asst = ASSISTANTS[st.session_state.current_assistant]
    if "sidebar_elements" in current_asst:
        st.subheader(f"{current_asst['icon']} {current_asst['title']} Ayarları")
        
        sidebar_context = {}
        for element in current_asst["sidebar_elements"]:
            element_type = element["type"]
            key = element["key"]
            label = element["label"]
            
            if element_type == "multiselect":
                sidebar_context[key] = st.multiselect(label, element["options"])
            elif element_type == "radio":
                sidebar_context[key] = st.radio(label, element["options"])
            elif element_type == "checkbox":
                default = element.get("default", False)
                sidebar_context[key] = st.checkbox(label, default)
            elif element_type == "slider":
                sidebar_context[key] = st.slider(
                    label, 
                    min_value=element["min_value"], 
                    max_value=element["max_value"], 
                    value=element["value"]
                )
        
        st.session_state[f"{st.session_state.current_assistant}_context"] = sidebar_context

# Ana içerik
current_assistant = ASSISTANTS[st.session_state.current_assistant]

# Başlık ve açıklama
st.title(f"{current_assistant['icon']} {current_assistant['title']}")
st.write(current_assistant['description'])

# Ana sayfada asistan kartları görüntüleme
if st.session_state.current_assistant == "Ana Sayfa":
    st.subheader("Kullanılabilir Asistanlar")
    
    cols = st.columns(3)
    
    for i, (name, asst) in enumerate(ASSISTANTS.items()):
        if name != "Ana Sayfa":
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(f"{asst['icon']} {asst['title']}")
                    st.write(asst['description'])
                    
                    if st.button(f"{asst['icon']} Bu Asistanı Seç", key=f"select_{name}"):
                        st.session_state.current_assistant = name
                        st.rerun()

# Geçmiş mesajları görüntüleme
current_messages = st.session_state.assistant_system_messages[st.session_state.current_assistant] + \
                   st.session_state.assistant_chat_history[st.session_state.current_assistant]

for message in current_messages:
    if message["role"] != "system":  # Sistem mesajını gösterme
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Kullanıcı giriş alanı
if prompt := st.chat_input(f"{current_assistant['icon']} Nasıl yardımcı olabilirim?"):
    # Kullanıcı mesajını ekle
    st.session_state.assistant_chat_history[st.session_state.current_assistant].append(
        {"role": "user", "content": prompt}
    )
    
    # Kullanıcı mesajını göster
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Bağlam bilgisini ekle
    context_info = ""
    sidebar_context_key = f"{st.session_state.current_assistant}_context"
    
    if sidebar_context_key in st.session_state and st.session_state[sidebar_context_key]:
        context = st.session_state[sidebar_context_key]
        context_parts = []
        
        for key, value in context.items():
            if value:  # Boş olmayan değerleri ekle
                if isinstance(value, list):
                    if value:  # Boş liste değilse
                        context_parts.append(f"{key.replace('_', ' ').title()}: {', '.join(value)}")
                else:
                    context_parts.append(f"{key.replace('_', ' ').title()}: {value}")
        
        if context_parts:
            context_info = "Bağlam bilgisi: " + "; ".join(context_parts) + ". "
    
    # AI yanıtını akış olarak ver
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # İngilizce Kelime Asistanı için özel talimatlar
        if st.session_state.current_assistant == "İngilizce Kelime Asistanı":
            full_prompt = f"{prompt} (Lütfen yanıtını Türkçe dilinde ver. Bu kelimenin anlamını, kullanımını ve hatırlamak için ipuçlarını Türkçe olarak açıkla.)"
        else:
            full_prompt = context_info + prompt + " (Lütfen yanıtını Türkçe dilinde ver.)"
        
        # API çağrısı
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-distill-llama-70b:free",
                messages=[
                    *current_messages,
                    {"role": "user", "content": full_prompt}
                ],
                stream=True
            )
            
            # Yanıtı akış olarak al
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
            full_response = f"Üzgünüm, bir hata oluştu: {e}"
    
    # Asistan yanıtını geçmişe ekle
    st.session_state.assistant_chat_history[st.session_state.current_assistant].append(
        {"role": "assistant", "content": full_response}
    )
