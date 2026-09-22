import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="بوابة المتدرب - أكاديمية HandsOnSite", page_icon="💻", layout="wide")

# تصميم CSS مخصص لتجميل شكل الموقع وصفحة الدخول بالكامل
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    
    /* تصميم صندوق تسجيل الدخول ليكون في المنتصف وبشكل أنيق */
    .login-container {
        max-width: 420px;
        margin: 50px auto;
        padding: 30px;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* تنسيق الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        height: 45px;
        background-color: #0d6efd;
        color: white;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #0b5ed7; 
        color: white; 
    }
    </style>
""", unsafe_allow_html=True)

os.makedirs("uploads", exist_ok=True)

# نظام تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #0d6efd; margin-bottom: 5px;">💻 أكاديمية HandsOnSite</h2>
                <p style="color: #6c757d; font-size: 15px;">بوابة تسجيل دخول المتدربين</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("🔒 **يرجى إدخال بيانات الحساب الخاص بك**")
            username = st.text_input("اسم المستخدم (Username):")
            password = st.text_input("كلمة المرور (Password):", type="password")
            
            submit_login = st.form_submit_button("تسجيل الدخول")
            
            if submit_login:
                if username and password:
                    if os.path.exists("users.csv"):
                        try:
                            df_users = pd.read_csv("users.csv", encoding="utf-8-sig", on_bad_lines="skip")
                            
                            user_match = df_users[
                                (df_users['اسم_المستخدم'].astype(str).str.strip() == username.strip()) & 
                                (df_users['كلمة_المرور'].astype(str).str.strip() == password.strip())
                            ]
                            
                            if not user_match.empty:
                                st.session_state.logged_in = True
                                st.session_state.username = username.strip()
                                st.session_state.current_user = user_match.iloc[0]['اسم_المتدرب']
                                st.session_state.user_track = user_match.iloc[0]['المسار']
                                st.success("تم تسجيل الدخول بنجاح! جاري تحويلك...")
                                st.rerun()
                            else:
                                st.error("خطأ: اسم المستخدم أو كلمة المرور غير صحيحة.")
                        except Exception as e:
                            st.error(f"حدث خطأ أثناء قراءة ملف المستخدمين: {e}")
                    else:
                        st.error("لا توجد حسابات مفعلة في النظام حالياً. يرجى مراجعة الأدمن.")
                else:
                    st.warning("الرجاء إدخال اسم المستخدم وكلمة المرور.")
        
        st.markdown("""
            <div style="text-align: center; margin-top: 15px;">
                <p style="color: #adb5bd; font-size: 13px;">إذا لم يكن لديك حساب، يرجى التواصل مع إدارة الأكاديمية.</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.stop()

# جلب أو إنشاء ملف خاص ببيانات الملف الشخصي الإضافية
profile_db = "profiles.csv"
if not os.path.exists(profile_db):
    with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])

df_prof = pd.read_csv(profile_db, encoding="utf-8-sig", on_bad_lines="skip")
user_prof_row = df_prof[df_prof['اسم_المستخدم'].astype(str).str.strip() == str(st.session_state.username)]

current_avatar = ""
current_eval = "ممتاز (تحت المراجعة)"
if not user_prof_row.empty:
    current_avatar = str(user_prof_row.iloc[0].get('الصورة_الشخصية', ''))
    current_eval = str(user_prof_row.iloc[0].get('التقييم', 'ممتاز (تحت المراجعة)'))

# عرض الصورة الشخصية في القائمة الجانبية إن وجدت
if pd.notna(current_avatar) and os.path.exists(current_avatar):
    st.sidebar.image(current_avatar, width=120)

st.sidebar.markdown(f"### أهلاً بك، {st.session_state.get('current_user', 'متدرب')} 👋")
st.sidebar.markdown(f"**المسار التدريبي:** {st.session_state.get('user_track', 'عام')}")
st.sidebar.divider()

menu = st.sidebar.radio("القائمة الرئيسية:", [
    "📢 الإعلانات والأخبار",
    "📚 ملفات ومصادر المحاضرات",
    "📋 الواجبات والتكاليف (Assignments)",
    "⚙️ الملف الشخصي وتقييمي",
    "🚪 تسجيل الخروج"
])

if menu == "🚪 تسجيل الخروج":
    st.session_state.logged_in = False
    st.rerun()

# 1. قسم الإعلانات
if menu == "📢 الإعلانات والأخبار":
    st.title("📢 إعلانات أكاديمية HandsOnSite")
    st.markdown("تابع أحدث الأخبار والإعلانات المهمة الخاصة بمسارك التدريبي.")
    st.divider()
    
    if os.path.exists("announcements.csv"):
        try:
            df_an = pd.read_csv("announcements.csv", encoding="utf-8-sig", on_bad_lines="skip")
            if not df_an.empty:
                for index, row in df_an.iterrows():
                    st.info(f"### 📌 {row.get('العنوان', '')}\n\n{row.get('المحتوى', '')}\n\n*تاريخ النشر: {row.get('التاريخ', '')}*")
                    img_path = row.get('صورة_الإعلان')
                    if pd.notna(img_path) and isinstance(img_path, str) and os.path.exists(img_path):
                        st.image(img_path, width=350)
                    st.write("---")
            else:
                st.info("لا توجد إعلانات منشورة حتى الآن.")
        except Exception:
            st.info("جاري تحديث الإعلانات...")
    else:
        st.info("لا توجد إعلانات حالياً.")

# 2. قسم المحاضرات
elif menu == "📚 ملفات ومصادر المحاضرات":
    st.title("📚 ملفات ومصادر المحاضرات")
    st.markdown("قم بتحميل ملفات الشرح والمصادر الخاصة بمحاضراتك.")
    st.divider()
    
    if os.path.exists("lectures.csv"):
        try:
            df_lec = pd.read_csv("lectures.csv", encoding="utf-8-sig", on_bad_lines="skip")
            if not df_lec.empty:
                for index, row in df_lec.iterrows():
                    st.write(f"- **المسار:** {row.get('المسار')} | **المحاضرة:** {row.get('عنوان_المحاضرة')}")
                    file_path = row.get('مسار_الملف')
                    if pd.notna(file_path) and isinstance(file_path, str) and os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 تحميل ملف المحاضرة",
                                data=f,
                                file_name=os.path.basename(file_path),
                                key=f"lec_dl_{index}"
                            )
                    st.write("---")
            else:
                st.info("لا توجد محاضرات مرفوعة حالياً.")
        except Exception:
            st.info("لا توجد محاضرات متاحة حالياً.")
    else:
        st.info("لا توجد ملفات محاضرات مضافة بعد.")

# 3. قسم الواجبات والأسئلة (Assignments)
elif menu == "📋 الواجبات والتكاليف (Assignments)":
    st.title("📋 الواجبات والتكاليف المطلوبة")
    st.markdown("قم بالاطلاع على الواجبات المنشورة، تحميل ملف الأسئلة، ورفع حل الواجب الخاص بك بسهولة.")
    st.divider()
    
    if os.path.exists("assignments.csv"):
        try:
            df_asg = pd.read_csv("assignments.csv", encoding="utf-8-sig", on_bad_lines="skip")
            if not df_asg.empty:
                for index, row in df_asg.iterrows():
                    st.subheader(f"📌 {row.get('العنوان', '')}")
                    st.write(f"**التعليمات:** {row.get('الوصف', '')}")
                    st.write(f"*تاريخ النشر: {row.get('التاريخ', '')}*")
                    
                    asg_file = row.get('مسار_ملف_الأسئلة')
                    if pd.notna(asg_file) and isinstance(asg_file, str) and os.path.exists(asg_file):
                        with open(asg_file, "rb") as af:
                            st.download_button(
                                label="📥 تحميل ملف أسئلة الواجب (PDF)",
                                data=af,
                                file_name=os.path.basename(asg_file),
                                key=f"dl_asg_{index}"
                            )
                    
                    with st.form(f"submit_form_{index}"):
                        uploaded_ans = st.file_uploader("رفـع ملف حل الواجب (PDF أو صور):", type=["pdf", "png", "jpg", "zip"], key=f"ans_{index}")
                        submit_ans = st.form_submit_button("إرسال الحل للأدمن")
                        
                        if submit_ans:
                            if uploaded_ans is not None:
                                ans_filename = f"sub_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_ans.name}"
                                ans_path_str = os.path.join("uploads", ans_filename)
                                with open(ans_path_str, "wb") as sf:
                                    sf.write(uploaded_ans.getbuffer())
                                
                                sub_db = "submissions.csv"
                                sub_exists = os.path.exists(sub_db)
                                with open(sub_db, mode="a", encoding="utf-8-sig", newline="") as sf_csv:
                                    w = csv.writer(sf_csv)
                                    if not sub_exists:
                                        w.writerow(["اسم_المتدرب", "عنوان_الواجب", "مسار_ملف_الحل", "التاريخ"])
                                    w.writerow([st.session_state.current_user, row.get('العنوان'), ans_path_str, datetime.now().strftime("%Y-%m-%d")])
                                
                                st.success("تم إرسال حل الواجب بنجاح وسيراه الأدمن في لوحة التحكم!")
                            else:
                                st.warning("الرجاء اختيار ملف الحل قبل الإرسال.")
                    st.write("---")
            else:
                st.info("لا توجد واجبات منشورة حتى الآن من قبل الأدمن.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الواجبات: {e}")
    else:
        st.info("لا توجد ملفات واجبات مسجلة حالياً.")

# 4. قسم الملف الشخصي وتغيير البيانات وكلمة المرور
elif menu == "⚙️ الملف الشخصي وتقييمي":
    st.title("⚙️ الملف الشخصي وتقييم الأداء")
    st.markdown("يمكنك هنا تعديل اسمك، تغيير كلمة المرور، رفع صورتك الشخصية، والاطلاع على تقييمك في الأكاديمية.")
    st.divider()
    
    col_p1, col_p2 = st.columns([1, 2])
    
    with col_p1:
        st.subheader("🖼️ صورتك الشخصية")
        if pd.notna(current_avatar) and os.path.exists(current_avatar):
            st.image(current_avatar, width=180, caption="صورتك الحالية")
        else:
            st.info("لم تقم برفع صورة شخصية بعد.")
            
        st.markdown("---")
        st.subheader("⭐ تقييمك الأكاديمي")
        st.metric(label="حالة التقييم العام", value=current_eval)
        st.info("💡 يتم تحديث هذا التقييم بناءً على أداءك وتسليمك للواجبات.")

    with col_p2:
        st.subheader("✏️ تعديل البيانات الشخصية وكلمة المرور")
        with st.form("update_profile_form"):
            new_name_input = st.text_input("تعديل الاسم:", value=st.session_state.current_user)
            new_password_input = st.text_input("كلمة المرور الجديدة (اتركها فارغة إذا لم ترد التغيير):", type="password")
            new_avatar_file = st.file_uploader("اختر صورة شخصية جديدة (JPG/PNG):", type=["jpg", "jpeg", "png"])
            
            submit_update = st.form_submit_button("حفظ جميع التعديلات")
            
            if submit_update:
                saved_avatar_path = current_avatar
                if new_avatar_file is not None:
                    avatar_filename = f"avatar_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{new_avatar_file.name}"
                    saved_avatar_path = os.path.join("uploads", avatar_filename)
                    with open(saved_avatar_path, "wb") as av_f:
                        av_f.write(new_avatar_file.getbuffer())
                
                st.session_state.current_user = new_name_input.strip()
                
                # تحديث الاسم وكلمة المرور في ملف users.csv
                if os.path.exists("users.csv"):
                    df_u = pd.read_csv("users.csv", encoding="utf-8-sig", on_bad_lines="skip")
                    mask = df_u['اسم_المستخدم'].astype(str).str.strip() == str(st.session_state.username)
                    
                    df_u.loc[mask, 'اسم_المتدرب'] = new_name_input.strip()
                    if new_password_input.strip():
                        df_u.loc[mask, 'كلمة_المرور'] = new_password_input.strip()
                        
                    df_u.to_csv("users.csv", index=False, encoding="utf-8-sig")
                
                # تحديث الصورة والبيانات في profiles.csv
                profiles_list = []
                if os.path.exists(profile_db):
                    df_p_old = pd.read_csv(profile_db, encoding="utf-8-sig", on_bad_lines="skip")
                    for _, r in df_p_old.iterrows():
                        if str(r.get('اسم_المستخدم')).strip() != str(st.session_state.username):
                            profiles_list.append([r.get('اسم_المستخدم'), r.get('الصورة_الشخصية'), r.get('التقييم'), r.get('نبذة')])
                
                profiles_list.append([st.session_state.username, saved_avatar_path, current_eval, ""])
                
                with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f_p:
                    w_p = csv.writer(f_p)
                    w_p.writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])
                    w_p.writerows(profiles_list)
                
                st.success("تم تحديث بياناتك الشخصية وكلمة المرور بنجاح!")
                st.rerun()