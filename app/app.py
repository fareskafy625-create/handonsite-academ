import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="بوابة المتدرب - أكاديمية HandsOnSite", page_icon="💻", layout="wide")

# تصميم CSS مخصص لخلفية شفافة وزجاجية عصرية وأزرار جانبية احترافية
st.markdown("""
    <style>
    /* خلفية شفافة وتدرج ألوان احترافي للصفحة بالكامل */
    .stApp {
        background: linear-gradient(135deg, rgba(13, 110, 253, 0.08) 0%, rgba(244, 246, 249, 0.85) 100%);
    }

    /* تأثير زجاجي شفاف (Glassmorphism) للعناصر والكروت الرئيسية */
    .assignment-card, .stInfo, div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    }
    
    /* تصميم أزرار القائمة الجانبية لتكون بشكل مربعات وأزرار شفافة واحترافية */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        height: 48px;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(5px);
        color: #0d6efd;
        border: 1px solid rgba(13, 110, 253, 0.3);
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
        margin-bottom: 8px;
        text-align: right;
        padding-right: 20px;
    }
    div.stButton > button:hover { 
        background-color: #0d6efd; 
        color: white; 
        border-color: #0d6efd;
        transform: translateY(-2px);
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
            <div style="text-align: center; margin-bottom: 20px; background: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
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
                                st.session_state.active_page = "📢 الإعلانات والأخبار"
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

# تتبع الصفحة الحالية في الـ Session State
if 'active_page' not in st.session_state:
    st.session_state.active_page = "📢 الإعلانات والأخبار"

# جلب أو إنشاء ملف خاص ببيانات الملف الشخصي الإضافية
profile_db = "profiles.csv"
if not os.path.exists(profile_db):
    with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])

df_prof = pd.read_csv(profile_db, encoding="utf-8-sig", on_bad_lines="skip")
user_prof_row = df_prof[df_prof['اسم_المستخدم'].astype(str).str.strip() == str(st.session_state.username)]

current_avatar = ""
current_eval = "ممتاز"
improvement_notes = "لا توجد ملاحظات إصلاحية حالياً. استمر في التميز!"
if not user_prof_row.empty:
    current_avatar = str(user_prof_row.iloc[0].get('الصورة_الشخصية', ''))
    val_eval = str(user_prof_row.iloc[0].get('التقييم', ''))
    if val_eval != "nan" and val_eval.strip() != "":
        current_eval = val_eval
    val_notes = str(user_prof_row.iloc[0].get('نبذة', ''))
    if val_notes != "nan" and val_notes.strip() != "":
        improvement_notes = val_notes

# تصميم القائمة الجانبية الاحترافية (مربعات وأزرار)
if pd.notna(current_avatar) and os.path.exists(current_avatar):
    st.sidebar.image(current_avatar, width=120)

st.sidebar.markdown(f"### أهلاً بك، {st.session_state.get('current_user', 'متدرب')} 👋")
st.sidebar.markdown(f"**المسار التدريبي:** {st.session_state.get('user_track', 'عام')}")
st.sidebar.divider()

st.sidebar.markdown("### 🎛️ الأقسام الرئيسية:")

if st.sidebar.button("📢 الإعلانات والأخبار"):
    st.session_state.active_page = "📢 الإعلانات والأخبار"
    st.rerun()

if st.sidebar.button("📚 ملفات ومصادر المحاضرات"):
    st.session_state.active_page = "📚 ملفات ومصادر المحاضرات"
    st.rerun()

if st.sidebar.button("📋 Assignments (الأسامينتس)"):
    st.session_state.active_page = "📋 Assignments (الأسامينتس)"
    st.rerun()

if st.sidebar.button("⚙️ الملف الشخصي وتقييمي"):
    st.session_state.active_page = "⚙️ الملف الشخصي وتقييمي"
    st.rerun()

st.sidebar.divider()

if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.logged_in = False
    st.rerun()

menu = st.session_state.active_page

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

# 3. قسم الـ Assignments (الأسامينتس) - بتصميم مدمج وموفر للمساحة
elif menu == "📋 Assignments (الأسامينتس)":
    st.title("📋 Assignments المتاحة والتكاليف")
    st.markdown("يمكنك الاطلاع على الـ Assignments، تحميل ملف الأسئلة، ورفع الحلول الخاصة بك بسهولة.")
    st.divider()
    
    if os.path.exists("assignments.csv"):
        try:
            df_asg = pd.read_csv("assignments.csv", encoding="utf-8-sig", on_bad_lines="skip")
            df_asg.columns = df_asg.columns.str.strip()
            
            submitted_asgs = []
            sub_db = "submissions.csv"
            if os.path.exists(sub_db):
                df_subs_check = pd.read_csv(sub_db, encoding="utf-8-sig", on_bad_lines="skip")
                df_subs_check.columns = df_subs_check.columns.str.strip()
                my_subs = df_subs_check[df_subs_check['اسم_المستخدم'].astype(str).str.strip() == str(st.session_state.username)]
                submitted_asgs = my_subs['عنوان_الواجب'].astype(str).str.strip().tolist()

            if not df_asg.empty:
                for index, row in df_asg.iterrows():
                    asg_title = str(row.get('العنوان', '')).strip()
                    asg_date = row.get('التاريخ', '')
                    asg_deadline = row.get('الديدلاين', 'غير محدد')
                    asg_file = row.get('مسار_ملف_الأسئلة')

                    is_submitted = asg_title in submitted_asgs

                    with st.expander(f"📌 Assignment: {asg_title} {' | (✔️ تم التسليم)' if is_submitted else ' | (⚠️ في انتظار التسليم)'}"):
                        
                        col_info1, col_info2 = st.columns([2, 1])
                        with col_info1:
                            st.markdown(f"**⏰ الموعد النهائي (Deadline):** <span style='color: #dc3545;'>{asg_deadline}</span>", unsafe_allow_html=True)
                            st.caption(f"تاريخ النشر: {asg_date}")
                        with col_info2:
                            if is_submitted:
                                st.success("✔️ تم التسليم")
                            else:
                                st.warning("⚠️ لم يُسلم بعد")

                        st.markdown("---")

                        if pd.notna(asg_file) and isinstance(asg_file, str) and os.path.exists(asg_file):
                            with open(asg_file, "rb") as af:
                                st.download_button(
                                    label="📥 تحميل ملف أسئلة الـ Assignment (PDF)",
                                    data=af,
                                    file_name=os.path.basename(asg_file),
                                    key=f"dl_asg_{index}"
                                )
                        
                        with st.form(f"submit_form_{index}"):
                            uploaded_ans = st.file_uploader("📤 رفـع ملف حل الـ Assignment:", type=["pdf", "png", "jpg", "zip", "rar", "pkt", "txt"], key=f"ans_{index}")
                            submit_ans = st.form_submit_button("إرسال الحل وتسليمه للأدمن")
                            
                            if submit_ans:
                                if uploaded_ans is not None:
                                    ans_filename = f"sub_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_ans.name}"
                                    ans_path_str = os.path.join("uploads", ans_filename)
                                    with open(ans_path_str, "wb") as sf:
                                        sf.write(uploaded_ans.getbuffer())
                                    
                                    sub_exists = os.path.exists(sub_db)
                                    sub_records = []
                                    if sub_exists:
                                        df_s_old = pd.read_csv(sub_db, encoding="utf-8-sig", on_bad_lines="skip")
                                        df_s_old.columns = df_s_old.columns.str.strip()
                                        for _, r in df_s_old.iterrows():
                                            if not (str(r.get('اسم_المستخدم')).strip() == str(st.session_state.username) and str(r.get('عنوان_الواجب')).strip() == asg_title):
                                                sub_records.append([r.get('اسم_المتدرب'), r.get('اسم_المستخدم'), r.get('عنوان_الواجب'), r.get('مسار_ملف_الحل'), r.get('التاريخ')])
                                    
                                    sub_records.append([st.session_state.current_user, st.session_state.username, asg_title, ans_path_str, datetime.now().strftime("%Y-%m-%d %H:%M")])

                                    with open(sub_db, mode="w", encoding="utf-8-sig", newline="") as sf_csv:
                                        w = csv.writer(sf_csv)
                                        w.writerow(["اسم_المتدرب", "اسم_المستخدم", "عنوان_الواجب", "مسار_ملف_الحل", "التاريخ"])
                                        w.writerows(sub_records)
                                    
                                    st.success("🎉 تم رفع وتسجيل حل الـ Assignment بنجاح!")
                                    st.rerun()
                                else:
                                    st.warning("الرجاء اختيار ملف الحل قبل النقر على زر الإرسال.")
            else:
                st.info("لا توجد Assignments منشورة حتى الآن من قبل الأدمن.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الـ Assignments: {e}")
    else:
        st.info("لا توجد ملفات Assignments مسجلة حالياً.")

# 4. قسم الملف الشخصي وتغيير البيانات وكلمة المرور
elif menu == "⚙️ الملف الشخصي وتقييمي":
    st.title("⚙️ الملف الشخصي وتقييم الأداء")
    st.markdown("يمكنك هنا تعديل اسمك، تغيير كلمة المرور، رفع صورتك الشخصية، والاطلاع على تقييمك وتوجيهات المدرب.")
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
        
        st.markdown(f"""
            <div style="background-color: rgba(255, 243, 205, 0.9); padding: 15px; border-radius: 8px; border-right: 4px solid #ffc107; margin-top: 15px;">
                <h4 style="color: #856404; margin-top: 0; font-size: 15px;">📌 ملاحظات وتوجيهات المدرب لحل المشاكل:</h4>
                <p style="color: #533f03; font-size: 14px; line-height: 1.5; margin-bottom: 0;">{improvement_notes}</p>
            </div>
        """, unsafe_allow_html=True)

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
                
                if os.path.exists("users.csv"):
                    df_u = pd.read_csv("users.csv", encoding="utf-8-sig", on_bad_lines="skip")
                    mask = df_u['اسم_المستخدم'].astype(str).str.strip() == str(st.session_state.username)
                    
                    df_u.loc[mask, 'اسم_المتدرب'] = new_name_input.strip()
                    if new_password_input.strip():
                        df_u.loc[mask, 'كلمة_المرور'] = new_password_input.strip()
                        
                    df_u.to_csv("users.csv", index=False, encoding="utf-8-sig")
                
                profiles_list = []
                if os.path.exists(profile_db):
                    df_p_old = pd.read_csv(profile_db, encoding="utf-8-sig", on_bad_lines="skip")
                    for _, r in df_p_old.iterrows():
                        if str(r.get('اسم_المستخدم')).strip() != str(st.session_state.username):
                            profiles_list.append([r.get('اسم_المستخدم'), r.get('الصورة_الشخصية'), r.get('التقييم'), r.get('نبذة')])
                
                profiles_list.append([st.session_state.username, saved_avatar_path, current_eval, improvement_notes])
                
                with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f_p:
                    w_p = csv.writer(f_p)
                    w_p.writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])
                    w_p.writerows(profiles_list)
                
                st.success("تم تحديث بياناتك الشخصية وكلمة المرور بنجاح!")
                st.rerun()
