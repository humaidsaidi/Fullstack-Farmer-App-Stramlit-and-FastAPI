import streamlit as st

def about():
    st.title('Tentang Kami')

    st.write('Aplikasi Informasi dan Edukasi Petani adalah sebuah platform yang bertujuan untuk menyediakan informasi terkini dan edukasi yang berguna bagi para petani di seluruh Indonesia. Kami berkomitmen untuk mendukung kemajuan dan kesejahteraan petani dengan menyediakan akses mudah dan cepat kepada berbagai konten yang relevan dan bermanfaat.')

    st.header('Tim Pengembang')
    st.write("""
    Aplikasi ini dikembangkan oleh tim yang terdiri dari para ahli pertanian, pengembang perangkat lunak, dan desainer berbakat yang memiliki visi untuk menghadirkan solusi inovatif bagi para petani di Indonesia. Tim kami berdedikasi untuk menyajikan aplikasi yang berkualitas dan bermanfaat bagi pengguna kami.
    """)

    st.header('Kontak')
    st.write("""
    Jika Anda memiliki pertanyaan, saran, atau masukan, jangan ragu untuk menghubungi kami melalui email di [info@agritechapp.com](mailto:info@agritechapp.com). Kami sangat menghargai setiap umpan balik dari pengguna kami dan akan berusaha untuk merespons dengan cepat.
    """)
    
        