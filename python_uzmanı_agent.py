import streamlit as st
from openai import OpenAI

# OpenAI istemcisini başlat
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
)

# Sayfa yapılandırmasını ayarla
st.set_page_config(
    page_title="Python Uzmanı Yapay Zeka Asistanı",
    page_icon="🐍",
    layout="wide"
)

# Sohbet geçmişi için oturum durumu başlat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """Sen ileri düzey bir Python programlama uzmanı ve mentörsün. 
            Temel görevlerin:
            1. Derinlemesine, doğru Python programlama rehberliği sağlamak
            2. Karmaşık kavramları net, pratik örneklerle açıklamak
            3. En iyi uygulamaları ve gelişmiş programlama tekniklerini sunmak
            4. Kullanıcıların Python becerilerini öğrenmelerine ve geliştirmelerine yardımcı olmak
            5. Kodu hata ayıklamak ve optimizasyonlar önermek
            
            Uzmanlık alanların:
            - Nesne Yönelimli Programlama
            - Veri Yapıları ve Algoritmalar
            - Web Geliştirme (Django, Flask)
            - Veri Bilimi ve Makine Öğrenimi
            - Eşzamansız Programlama
            - Performans Optimizasyonu
            - Test ve Hata Ayıklama
            
            İletişim tarzın:
            - Eğitici ve sabırlı ol
            - Net, özlü açıklamalar kullan
            - Kod örnekleri sağla
            - Öğrenmeyi ve en iyi uygulamaları teşvik et
            
            NOT: Tüm cevaplarını Türkçe dilinde ver. Kullanıcılara Türkçe olarak yanıt ver."""
        }
    ]

# Yan çubuk için konu seçimi
st.sidebar.title("🐍 Python Uzmanı Odak Alanı")
research_topics = st.sidebar.multiselect(
    "Araştırma Alanlarını Seç", 
    [
        "Web Geliştirme", 
        "Veri Bilimi", 
        "Makine Öğrenimi", 
        "Backend Programlama", 
        "Algoritma Tasarımı", 
        "Performans Optimizasyonu", 
        "Test",
        "Eşzamansız Programlama"
    ]
)

# Ana sohbet arayüzü
st.title("Python Programlama Uzmanı Yapay Zeka 🐍")
st.write("İleri düzey Python bilgileri, kod yardımı ve uzman rehberliği alın!")

# Geçmişteki sohbet mesajlarını göster
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sohbet girişi
if prompt := st.chat_input("Python programlama hakkında herhangi bir şey sor..."):
    # Kullanıcı mesajını sohbet geçmişine ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Kullanıcı mesajını göster
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Seçilen konular temelinde bağlam oluştur
    topic_context = ""
    if research_topics:
        topic_context = f"Odak alanları: {', '.join(research_topics)}. "
    
    # Konu bağlamı ile tam istemi hazırla
    full_prompt = topic_context + prompt + " Lütfen cevabını Türkçe dilinde ver."

    # AI yanıtını akış olarak ver
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # OpenRouter API'yi çağır
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-distill-llama-70b:free",
                messages=[
                    {"role": "system", "content": st.session_state.messages[0]["content"]},
                    *[msg for msg in st.session_state.messages[1:] if msg["role"] != "system"],
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
    st.session_state.messages.append({"role": "assistant", "content": full_response})
