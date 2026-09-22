import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# إعدادات صفحة الأدمن
st.set_page_config(page_title="تسجيل دخول الأدمن - أكاديمية HandsOnSite", page_icon="👨‍💻", layout="wide")

# تصميم CSS مخصص لتجميل شكل صفحة الدخول ولوحة التحكم
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
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

# ملفات النظام
admins_db = "admins.csv"
users_db = "users.csv"
profile_db = "profiles.csv"
announcements_db = "announcements.csv"
lectures_db = "lectures.csv"
assignments_db = "assignments.csv"
submissions_db = "submissions.csv"

# إنشاء ملف افتراضي للمدربين إذا لم يكن موجوداً (الحساب الأساسي الافتراضي)
if not os.path.exists(admins_db):
    with open(admins_db, mode="w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["اسم_المستخدم", "كلمة_المرور", "اسم_المدرب"])
        w.writerow(["admin", "admin123", "الأدمن الأساسي"])

# نظام تسجيل دخول الأدمن
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #0d6efd; margin-bottom: 5px;">👨‍💻 لوحة تحكم المدربين</h2>
                <p style="color: #6c757d; font-size: 15px;">أكاديمية HandsOnSite - تسجيل دخول الأدمن</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login_form"):
            st.markdown("🔒 **يرجى إدخال بيانات حساب المدرب الخاص بك**")
            adm_user = st.text_input("اسم المستخدم للمدرب:")
            adm_pass = st.text_input("كلمة المرور:", type="password")
            
            submit_adm_login = st.form_submit_button("تسجيل دخول الأدمن")
            
            if submit_adm_login:
                if adm_user and adm_pass:
                    try:
                        df_admins = pd.read_csv(admins_db, encoding="utf-8-sig", on_bad_lines="skip")
                        match_adm = df_admins[
                            (df_admins['اسم_المستخدم'].astype(str).str.strip() == adm_user.strip()) & 
                            (df_admins['كلمة_المرور'].astype(str).str.strip() == adm_pass.strip())
                        ]
                        
                        if not match_adm.empty:
                            st.session_state.admin_logged_in = True
                            st.session_state.admin_name = match_adm.iloc[0]['اسم_المدرب']
                            st.session_state.admin_username = adm_user.strip()
                            st.success("تم تسجيل الدخول بنجاح! جاري تحويلك لوحة التحكم...")
                            st.rerun()
                        else:
                            st.error("خطأ: اسم المستخدم أو كلمة المرور غير صحيحة.")
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء التحقق من بيانات المدربين: {e}")
                else:
                    st.warning("الرجاء إدخال اسم المستخدم وكلمة المرور.")
    st.stop()

# --- تم تسجيل الدخول بنجاح، عرض لوحة التحكم ---
st.sidebar.markdown(f"### أهلاً بك يا بشمهندس 👋")
st.sidebar.markdown(f"**المدرب الحالي:** {st.session_state.get('admin_name', 'مدرب')}")
st.sidebar.divider()

# القائمة الجانبية للأدمن
admin_menu = st.sidebar.radio("خيارات لوحة التحكم:", [
    "⭐ تقييم المتدربين",
    "👥 إدارة المتدربين (إضافة حسابات)",
    "🔑 إدارة المدربين وحسابات الأدمن",
    "📢 نشر الإعلانات والأخبار",
    "📚 رفع ملفات المحاضرات",
    "📋 إضافة الواجبات والتكاليف",
    "📥 متابعة حلول المتدربين",
    "🚪 تسجيل الخروج"
])

if admin_menu == "🚪 تسجيل الخروج":
    st.session_state.admin_logged_in = False
    st.rerun()

st.title("👨‍💻 لوحة تحكم الأدمن - أكاديمية HandsOnSite")
st.markdown(f"مرحباً بك ({st.session_state.get('admin_name', 'مدرب')}). يمكنك من هنا إدارة المتدربين، المدربين، التقييمات، المحاضرات، الواجبات، والإعلانات.")
st.divider()

# 1. قسم تقييم المتدربين
if admin_menu == "⭐ تقييم المتدربين":
    st.subheader("⭐ تقييم الأداء الأكاديمي للمتدربين")
    st.markdown("اختر أي متدرب لتحديد أو تحديث تقييمه، وسيحفظ التقييم ليظهر له فوراً في حسابه الشخصي.")
    st.divider()
    
    if os.path.exists(users_db):
        try:
            df_users = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
            if not df_users.empty:
                if not os.path.exists(profile_db):
                    with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f:
                        w = csv.writer(f)
                        w.writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])
                
                df_prof = pd.read_csv(profile_db, encoding="utf-8-sig", on_bad_lines="skip")
                
                with st.form("admin_eval_form"):
                    user_options = df_users.apply(lambda row: f"{row['اسم_المتدرب']} ({row['اسم_المستخدم']})", axis=1).tolist()
                    selected_user_display = st.selectbox("اختر المتدرب:", user_options)
                    
                    eval_choices = [
                        "⭐ ممتاز جداً",
                        "⭐ ممتاز",
                        "⭐ جيد جداً",
                        "⭐ جيد",
                        "⭐ يحتاج إلى تحسين",
                        "⭐ تحت المراجعة"
                    ]
                    
                    chosen_username = selected_user_display.split("(")[-1].replace(")", "").strip()
                    
                    current_user_prof = df_prof[df_prof['اسم_المستخدم'].astype(str).str.strip() == chosen_username]
                    default_eval_val = "⭐ ممتاز"
                    if not current_user_prof.empty:
                        val_found = str(current_user_prof.iloc[0].get('التقييم', ''))
                        if val_found in eval_choices:
                            default_eval_val = val_found
                    
                    new_evaluation = st.selectbox("التقييم الأكاديمي الجديد:", eval_choices, index=eval_choices.index(default_eval_val) if default_eval_val in eval_choices else 0)
                    submit_eval = st.form_submit_button("حفظ وتحديث التقييم للمتدرب")
                    
                    if submit_eval:
                        profiles_list = []
                        for _, r in df_prof.iterrows():
                            if str(r.get('اسم_المستخدم')).strip() != chosen_username:
                                profiles_list.append([r.get('اسم_المستخدم'), r.get('الصورة_الشخصية'), r.get('التقييم'), r.get('نبذة')])
                        
                        old_avatar = ""
                        if not current_user_prof.empty:
                            old_avatar = str(current_user_prof.iloc[0].get('الصورة_الشخصية', ''))
                            
                        profiles_list.append([chosen_username, old_avatar, new_evaluation, ""])
                        
                        with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f_p:
                            w_p = csv.writer(f_p)
                            w_p.writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])
                            w_p.writerows(profiles_list)
                        
                        st.success(f"تم تحديث تقييم المتدرب بنجاح إلى: ({new_evaluation}) وسيظهر له في حسابه!")
            else:
                st.info("لا يوجد متدربين مسجلين بعد.")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
    else:
        st.warning("لا يوجد ملف مستخدمين مسجل حتى الآن.")

# 2. قسم إدارة المتدربين (إضافة حسابات)
elif admin_menu == "👥 إدارة المتدربين (إضافة حسابات)":
    st.subheader("👥 إضافة حساب متدرب جديد")
    with st.form("add_user_form"):
        trainee_name = st.text_input("اسم المتدرب الكامل:")
        trainee_username = st.text_input("اسم المستخدم (Username لتسجيل الدخول):")
        trainee_password = st.text_input("كلمة المرور (Password):", type="password")
        trainee_track = st.selectbox("المسار التدريبي:", ["Embeded Systems", "Networks & IT", "Python Development", "Web Development", "Robotics & STEM"])
        
        submit_user = st.form_submit_button("إضافة الحساب")
        
        if submit_user:
            if trainee_name and trainee_username and trainee_password:
                file_exists = os.path.exists(users_db)
                with open(users_db, mode="a", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    if not file_exists:
                        w.writerow(["اسم_المتدرب", "اسم_المستخدم", "كلمة_المرور", "المسار"])
                    w.writerow([trainee_name.strip(), trainee_username.strip(), trainee_password.strip(), trainee_track])
                st.success(f"تم إنشاء حساب للمتدرب ({trainee_name}) بنجاح!")
            else:
                st.warning("الرجاء تعبئة جميع الحقول المطلوبة.")

# 3. قسم إدارة المدربين (عرض، إضافة، وحذف حسابات الأدمن)
elif admin_menu == "🔑 إدارة المدربين وحسابات الأدمن":
    st.subheader("🔑 إدارة حسابات المدربين (الأدمن)")
    st.markdown("يمكنك هنا متابعة جميع المدربين المسجلين، إضافة مدرب جديد، أو حذف أي مدرب بسهولة.")
    st.divider()
    
    # نموذج إضافة مدرب جديد
    with st.form("add_admin_form"):
        st.markdown("### ➕ إضافة مدرب جديد")
        new_adm_name = st.text_input("اسم المدرب (مثل: م. أحمد / م. محمود):")
        new_adm_user = st.text_input("اسم المستخدم الخاص بالمدرب (للدخول به):")
        new_adm_pass = st.text_input("كلمة المرور الخاصة بالمدرب:", type="password")
        
        submit_new_admin = st.form_submit_button("إنشاء حساب المدرب")
        
        if submit_new_admin:
            if new_adm_name and new_adm_user and new_adm_pass:
                try:
                    df_adm_check = pd.read_csv(admins_db, encoding="utf-8-sig", on_bad_lines="skip")
                    if new_adm_user.strip() in df_adm_check['اسم_المستخدم'].astype(str).str.strip().values:
                        st.error("خطأ: اسم المستخدم هذا موجود بالفعل، يرجى اختيار اسم مستخدم آخر.")
                    else:
                        with open(admins_db, mode="a", encoding="utf-8-sig", newline="") as f:
                            w = csv.writer(f)
                            w.writerow([new_adm_user.strip(), new_adm_pass.strip(), new_adm_name.strip()])
                        st.success(f"تم إنشاء حساب المدرب ({new_adm_name}) بنجاح!")
                        st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ أثناء حفظ حساب المدرب: {e}")
            else:
                st.warning("الرجاء تعبئة جميع الحقول المطلوبة.")
                
    st.markdown("---")
    st.subheader("📋 قائمة المدربين الحاليين وخيارات الحذف:")
    
    if os.path.exists(admins_db):
        try:
            df_all_admins = pd.read_csv(admins_db, encoding="utf-8-sig", on_bad_lines="skip")
            if not df_all_admins.empty:
                for idx, row in df_all_admins.iterrows():
                    adm_n = row.get('اسم_المدرب', '')
                    adm_u = row.get('اسم_المستخدم', '')
                    adm_p = row.get('كلمة_المرور', '')
                    
                    col_info1, col_info2, col_info3 = st.columns([2, 2, 1])
                    with col_info1:
                        st.text(f"👤 الاسم: {adm_n}")
                    with col_info2:
                        st.text(f"🔑 اليوزر: {adm_u} | الباسورد: {adm_p}")
                    with col_info3:
                        # منع حذف الأدمن الأساسي لو رغبت في حمايته، أو السماح بحذف الكل
                        if adm_u != "admin":
                            if st.button("🗑️ حذف", key=f"del_adm_{idx}"):
                                # إعادة كتابة الملف بدون هذا المدرب
                                updated_admins = []
                                for _, r in df_all_admins.iterrows():
                                    if str(r.get('اسم_المستخدم')).strip() != str(adm_u).strip():
                                        updated_admins.append([r.get('اسم_المستخدم'), r.get('كلمة_المرور'), r.get('اسم_المدرب')])
                                
                                with open(admins_db, mode="w", encoding="utf-8-sig", newline="") as f_out:
                                    w_out = csv.writer(f_out)
                                    w_out.writerow(["اسم_المستخدم", "كلمة_المرور", "اسم_المدرب"])
                                    w_out.writerows(updated_admins)
                                
                                st.success(f"تم حذف المدرب ({adm_n}) بنجاح!")
                                st.rerun()
                        else:
                            st.caption("الحساب الرئيسي")
                    st.write("---")
            else:
                st.info("لا يوجد مدربين مسجلين.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة بيانات المدربين: {e}")

# 4. نشر الإعلانات
elif admin_menu == "📢 نشر الإعلانات والأخبار":
    st.subheader("📢 نشر إعلان جديد للمتدربين")
    with st.form("announcement_form"):
        title = st.text_input("عنوان الإعلان:")
        content = st.text_area("محتوى الإعلان والتفاصيل:")
        img_file = st.file_uploader("صورة مرفقة مع الإعلان (اختياري):", type=["png", "jpg", "jpeg"])
        
        submit_ann = st.form_submit_button("نشر الإعلان")
        
        if submit_ann:
            if title and content:
                img_path = ""
                if img_file is not None:
                    img_filename = f"ann_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{img_file.name}"
                    img_path = os.path.join("uploads", img_filename)
                    with open(img_path, "wb") as f:
                        f.write(img_file.getbuffer())
                
                file_exists = os.path.exists(announcements_db)
                with open(announcements_db, mode="a", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    if not file_exists:
                        w.writerow(["العنوان", "المحتوى", "صورة_الإعلان", "التاريخ"])
                    w.writerow([title, content, img_path, datetime.now().strftime("%Y-%m-%d")])
                st.success("تم نشر الإعلان بنجاح!")
            else:
                st.warning("الرجاء كتابة العنوان والمحتوى على الأقل.")

# 5. رفع ملفات المحاضرات
elif admin_menu == "📚 رفع ملفات المحاضرات":
    st.subheader("📚 إضافة ملف أو مصدر محاضرة")
    with st.form("lecture_form"):
        track = st.selectbox("المسار المستهدف:", ["الكل", "Embeded Systems", "Networks & IT", "Python Development", "Web Development", "Robotics & STEM"])
        lec_title = st.text_input("عنوان المحاضرة أو الدرس:")
        lec_file = st.file_uploader("ملف المحاضرة (PDF / ZIP / Code):", type=["pdf", "zip", "rar", "py", "txt", "docx"])
        
        submit_lec = st.form_submit_button("رفع الملف")
        
        if submit_lec:
            if lec_title and lec_file is not None:
                file_name = f"lec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{lec_file.name}"
                file_path = os.path.join("uploads", file_name)
                with open(file_path, "wb") as f:
                    f.write(lec_file.getbuffer())
                
                file_exists = os.path.exists(lectures_db)
                with open(lectures_db, mode="a", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    if not file_exists:
                        w.writerow(["المسار", "عنوان_المحاضرة", "مسار_الملف", "التاريخ"])
                    w.writerow([track, lec_title, file_path, datetime.now().strftime("%Y-%m-%d")])
                st.success("تم رفع ملف المحاضرة بنجاح!")
            else:
                st.warning("الرجاء إدخال العنوان واختيار الملف.")

# 6. إضافة الواجبات (مع تحديد الديدلاين)
elif admin_menu == "📋 إضافة الواجبات والتكاليف":
    st.subheader("📋 تكليف المتدربين بواجب جديد مع تحديد موعد تسليم (Deadline)")
    with st.form("assignment_form"):
        asg_title = st.text_input("عنوان الواجب:")
        asg_desc = st.text_area("وصف الواجب والتعليمات:")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            asg_deadline_date = st.date_input("تاريخ آخر موعد للتسليم (Deadline Date):")
        with col_d2:
            asg_deadline_time = st.time_input("وقت آخر موعد للتسليم (Deadline Time):")
            
        asg_file = st.file_uploader("ملف الأسئلة (PDF):", type=["pdf", "docx"])
        
        submit_asg = st.form_submit_button("نشر الواجب بالديدلاين")
        
        if submit_asg:
            if asg_title:
                deadline_str = f"{asg_deadline_date} {asg_deadline_time.strftime('%H:%M')}"
                
                file_path = ""
                if asg_file is not None:
                    file_name = f"asg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{asg_file.name}"
                    file_path = os.path.join("uploads", file_name)
                    with open(file_path, "wb") as f:
                        f.write(asg_file.getbuffer())
                
                file_exists = os.path.exists(assignments_db)
                with open(assignments_db, mode="a", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    if not file_exists:
                        w.writerow(["العنوان", "الوصف", "مسار_ملف_الأسئلة", "الديدلاين", "التاريخ"])
                    w.writerow([asg_title, asg_desc, file_path, deadline_str, datetime.now().strftime("%Y-%m-%d")])
                st.success(f"تم نشر الواجب بنجاح بحد أقصى للتسليم: {deadline_str}!")
            else:
                st.warning("الرجاء إدخال عنوان الواجب على الأقل.")

# 7. متابعة حلول المتدربين
elif admin_menu == "📥 متابعة حلول المتدربين":
    st.subheader("📥 حلول الواجبات المرسلة من المتدربين")
    st.divider()
    
    if os.path.exists(submissions_db):
        try:
            df_subs = pd.read_csv(submissions_db, encoding="utf-8-sig", on_bad_lines="skip")
            if not df_sub.empty if 'df_sub' in locals() else not df_subs.empty:
                for index, row in df_subs.iterrows():
                    st.write(f"👤 **المتدرب:** {row.get('اسم_المتدرب')} | 📋 **الواجب:** {row.get('عنوان_الواجب')} | 📅 **التاريخ:** {row.get('التاريخ')}")
                    sub_file = row.get('مسار_ملف_الحل')
                    if pd.notna(sub_file) and isinstance(sub_file, str) and os.path.exists(sub_file):
                        with open(sub_file, "rb") as sf:
                            st.download_button(
                                label="📥 تحميل ملف حل المتدرب",
                                data=sf,
                                file_name=os.path.basename(sub_file),
                                key=f"dl_sub_{index}"
                            )
                    st.write("---")
            else:
                st.info("لا توجد حلول مرفوعة من المتدربين حتى الآن.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الحلول: {e}")
    else:
        st.info("لا توجد ملفات حلول مسجلة حتى الآن.")
