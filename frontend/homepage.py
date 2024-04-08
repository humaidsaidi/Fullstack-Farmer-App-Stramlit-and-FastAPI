import streamlit as st
from streamlit_option_menu import option_menu
import article, diagnose, about, login

# st.set_page_config(
#     page_title="Farmer Information App",
#     page_icon="🧑‍🌾"
# )


with st.sidebar: # add this if you want to make sidebar
    selected = option_menu(
        menu_title=None,
        options=["🏠 Home", "📰 Article", "🩺 Diagnose", "🙋‍♂️ About", "🔐 Login"],
        icons=["🏠", "📰", "🩺", "🙋‍♂️", "🔐"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={ 
            "nav-link": {"font-size": "18px", "text-align": "center", "margin":"0px", "white-space": "nowrap"}
        }
    )


if selected == "🏠 Home":
    # Header
    st.title('Selamat Datang di Aplikasi Informasi dan Edukasi Petani')

    # Deskripsi
    st.write('Selamat datang di aplikasi yang didedikasikan untuk memberikan informasi terbaru dan edukasi yang berguna bagi para petani. Aplikasi ini dirancang untuk memberikan akses mudah dan cepat kepada berbagai konten yang relevan dengan dunia pertanian, mulai dari teknik bertani terkini hingga tips-tips praktis untuk meningkatkan hasil panen Anda.')

    # Fitur Utama
    st.header('Fitur Utama:')
    st.markdown("""
    1. **Berita Terkini:** Dapatkan update terbaru seputar dunia pertanian, termasuk perkembangan terkini dalam teknologi pertanian, berita pasar, dan informasi penting lainnya.
    2. **Diagnosa tanaman:** Temukan penyakit yang menerpa tanaman anda.
   """)

    # Bergabung Bersama Kami
    st.header('Bergabung Bersama Kami!')
    st.write('Mari bergabung dalam komunitas aplikasi informasi dan edukasi petani ini. Jadilah bagian dari perubahan menuju pertanian yang lebih berkelanjutan dan produktif. Dapatkan akses tak terbatas kepada informasi terbaru dan sumber daya yang dapat membantu meningkatkan hasil panen Anda. Selamat menjelajahi aplikasi ini dan semoga sukses selalu dalam setiap usaha pertanian Anda!')

if selected == "📰 Article":
    article.article()

if selected == "🩺 Diagnose":
    diagnose.diagnose()

if selected == "🙋‍♂️ About":
    about.about()

if selected == "🔐 Login":
    
    login.login_page()