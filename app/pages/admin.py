import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# ظبط صفحة الأدمن
st.set_page_config(page_title="لوحة التحكم - HandsOnSite", page_icon="👨‍💻", layout="wide")

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
    }
    </style>
""", unsafe_allow_html=True)

os.makedirs("uploads", exist_ok=True)

# تعريف ملفات الداتا بيز المستخدمة
admins_db = "admins.csv"
users_db = "users.csv"
profile_db = "profiles.csv"
announcements_db = "announcements.csv"
lectures_db = "lectures.csv"
assignments_db = "assignments.csv"
submissions_db = "submissions.csv"
attendance_db = "attendance.csv"
groups_schedule_db = "groups_schedule.csv"

# إنشاء حساب الأدمن الافتراضي لو الملف مش موجود
if not os.path.exists(admins_db):
    with open(admins_db, mode="w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["اسم_المستخدم", "كلمة_المرور", "اسم_المدرب"])
        w.writerow(["admin", "admin123", "الأدمن الأساسي"])

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# شاشة تسجيل الدخول
if not st.session_state.admin_logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<h3 style='text-align: center; color: #0d6efd;'>تسجيل دخول لوحة التحكم</h3>", unsafe_allow_html=True)
        with st.form("login"):
            adm_user = st.text_input("اسم المستخدم:")
            adm_pass = st.text_input("كلمة المرور:", type="password")
            btn = st.form_submit_button("دخول")
            
            if btn:
                if adm_user and adm_pass:
                    try:
                        df = pd.read_csv(admins_db, encoding="utf-8-sig", on_bad_lines="skip")
                        match = df[(df['اسم_المستخدم'].astype(str).str.strip() == adm_user.strip()) & 
                                   (df['كلمة_المرور'].astype(str).str.strip() == adm_pass.strip())]
                        
                        if not match.empty:
                            st.session_state.admin_logged_in = True
                            st.session_state.admin_name = match.iloc[0]['اسم_المدرب']
                            st.success("تم الدخول بنجاح")
                            st.rerun()
                        else:
                            st.error("بيانات الدخول غير صحيحة")
                    except Exception as e:
                        st.error(f"خطأ في قراءة البيانات: {e}")
                else:
                    st.warning("من فضلك دخل البيانات كاملة")
    st.stop()

# القائمة الجانبية
st.sidebar.markdown(f"**أهلاً يا بشمهندس:** {st.session_state.get('admin_name', '')}")
st.sidebar.divider()

menu = st.sidebar.radio("القائمة الرئيسية:", [
    "📅 مواعيد المجموعات",
    "✅ الحضور والغياب",
    "⭐ تقييم الطلاب",
    "👥 إدارة الطلاب",
    "🔑 المدربين",
    "📢 الإعلانات",
    "📚 المحاضرات",
    "📋 الواجبات",
    "📥 حلول الواجبات",
    "🚪 خروج"
])

if menu == "🚪 خروج":
    st.session_state.admin_logged_in = False
    st.rerun()

st.title("لوحة تحكم الأكاديمية - Networks & IT")
st.divider()

# 1. جداول المجموعات
if menu == "📅 مواعيد المجموعات":
    st.subheader("إدارة مواعيد الجروبات")
    
    with st.form("sch_form"):
        g_name = st.text_input("اسم الجروب (مثال: جروب CCNA 1):")
        g_day = st.selectbox("اليوم:", ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"])
        g_time = st.text_input("الموعد (مثال: من 4 لـ 6):")
        g_notes = st.text_area("ملاحظات:")
        save_sch = st.form_submit_button("حفظ الموعد")
        
        if save_sch:
            if g_name and g_time:
                rows = []
                if os.path.exists(groups_schedule_db):
                    df_old = pd.read_csv(groups_schedule_db, encoding="utf-8-sig", on_bad_lines="skip")
                    for _, r in df_old.iterrows():
                        rows.append([r.get('اسم_الجروب'), r.get('اليوم'), r.get('الموعد'), r.get('ملاحظات')])
                
                rows.append([g_name.strip(), g_day, g_time.strip(), g_notes.strip()])
                with open(groups_schedule_db, mode="w", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["اسم_الجروب", "اليوم", "الموعد", "ملاحظات"])
                    w.writerows(rows)
                st.success("تم الحفظ بنجاح")
            else:
                st.warning("دخل اسم الجروب والموعد على الأقل")

    st.markdown("---")
    if os.path.exists(groups_schedule_db):
        df_sch = pd.read_csv(groups_schedule_db, encoding="utf-8-sig", on_bad_lines="skip")
        if not df_sch.empty:
            for idx, row in df_sch.iterrows():
                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    st.write(f"**الجروب:** {row.get('اسم_الجروب')}")
                    st.caption(f"ملاحظات: {row.get('ملاحظات')}")
                with c2:
                    st.write(f"اليوم: {row.get('اليوم')} - الوقت: {row.get('الموعد')}")
                with c3:
                    if st.button("حذف", key=f"d_sch_{idx}"):
                        new_rows = []
                        for _, r in df_sch.iterrows():
                            if not (str(r.get('اسم_الجروب')) == str(row.get('اسم_الجروب')) and str(r.get('الموعد')) == str(row.get('الموعد'))):
                                new_rows.append([r.get('اسم_الجروب'), r.get('اليوم'), r.get('الموعد'), r.get('ملاحظات')])
                        with open(groups_schedule_db, mode="w", encoding="utf-8-sig", newline="") as f:
                            w = csv.writer(f)
                            w.writerow(["اسم_الجروب", "اليوم", "الموعد", "ملاحظات"])
                            w.writerows(new_rows)
                        st.rerun()
                st.write("---")

# 2. الحضور والغياب
elif menu == "✅ الحضور والغياب":
    st.subheader("تسجيل الحضور")
    if os.path.exists(users_db):
        df_u = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
        if not df_u.empty:
            with st.form("att_form"):
                d_input = st.date_input("التاريخ:")
                lec_name = st.text_input("اسم المحاضرة:", "محاضرة اليوم")
                
                status_dict = {}
                for idx, r in df_u.iterrows():
                    name = r.get('اسم_المتدرب', '')
                    username = r.get('اسم_المستخدم', '')
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.write(name)
                    with c2:
                        st = st.selectbox("الحالة", ["حاضر", "غائب", "متأخر"], key=f"st_{idx}")
                        status_dict[username] = {"name": name, "status": st}
                
                if st.form_submit_button("حفظ الحضور"):
                    att_rows = []
                    if os.path.exists(attendance_db):
                        df_att = pd.read_csv(attendance_db, encoding="utf-8-sig", on_bad_lines="skip")
                        for _, r in df_att.iterrows():
                            att_rows.append([r.get('التاريخ'), r.get('عنوان_المحاضرة'), r.get('اسم_المتدرب'), r.get('اسم_المستخدم'), r.get('الحالة')])
                    
                    for usr, data in status_dict.items():
                        att_rows.append([str(d_input), lec_name, data["name"], usr, data["status"]])
                    
                    with open(attendance_db, mode="w", encoding="utf-8-sig", newline="") as f:
                        w = csv.writer(f)
                        w.writerow(["التاريخ", "عنوان_المحاضرة", "اسم_المتدرب", "اسم_المستخدم", "الحالة"])
                        w.writerows(att_rows)
                    st.success("تم حفظ الحضور")

# 3. التقييمات
elif menu == "⭐ تقييم الطلاب":
    st.subheader("تقييم المتدربين")
    if os.path.exists(users_db):
        df_u = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
        if not df_u.empty:
            if not os.path.exists(profile_db):
                with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f:
                    csv.writer(f).writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])
            
            df_p = pd.read_csv(profile_db, encoding="utf-8-sig", on_bad_lines="skip")
            with st.form("eval_form"):
                opts = [f"{r['اسم_المتدرب']} ({r['اسم_المستخدم']})" for _, r in df_u.iterrows()]
                selected = st.selectbox("الطالب:", opts)
                usr_target = selected.split("(")[-1].replace(")", "").strip()
                
                grades = ["⭐ ممتاز جداً", "⭐ ممتاز", "⭐ جيد جداً", "⭐ جيد", "⭐ يحتاج إلى تحسين"]
                new_grade = st.selectbox("التقييم:", grades)
                
                if st.form_submit_button("تحديث التقييم"):
                    profiles = []
                    for _, r in df_p.iterrows():
                        if str(r.get('اسم_المستخدم')).strip() != usr_target:
                            profiles.append([r.get('اسم_المستخدم'), r.get('الصورة_الشخصية'), r.get('التقييم'), r.get('نبذة')])
                    
                    profiles.append([usr_target, "", new_grade, ""])
                    with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f:
                        w = csv.writer(f)
                        w.writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])
                        w.writerows(profiles)
                    st.success("تم التحديث")

# 4. إدارة الطلاب
elif menu == "👥 إدارة الطلاب":
    st.subheader("الطلاب المسجلين")
    with st.expander("إضافة طالب جديد"):
        with st.form("add_student"):
            s_name = st.text_input("الاسم:")
            s_user = st.text_input("اسم المستخدم:")
            s_pass = st.text_input("كلمة المرور:", type="password")
            s_track = st.selectbox("المسار:", ["Networks & IT", "Cisco CCNA", "Routing & Switching", "Network Security"])
            
            if st.form_submit_button("إضافة"):
                if s_name and s_user and s_pass:
                    exists = os.path.exists(users_db)
                    with open(users_db, mode="a", encoding="utf-8-sig", newline="") as f:
                        w = csv.writer(f)
                        if not exists:
                            w.writerow(["اسم_المتدرب", "اسم_المستخدم", "كلمة_المرور", "المسار"])
                        w.writerow([s_name, s_user, s_pass, s_track])
                    st.success("تمت الإضافة")
                    st.rerun()

    if os.path.exists(users_db):
        df_all = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
        if not df_all.empty:
            for idx, r in df_all.iterrows():
                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    st.write(r.get('اسم_المتدرب'))
                with c2:
                    st.write(f"اليوزر: {r.get('اسم_المستخدم')}")
                with c3:
                    if st.button("حذف", key=f"del_u_{idx}"):
                        new_u = []
                        for _, row in df_all.iterrows():
                            if str(row.get('اسم_المستخدم')) != str(r.get('اسم_المستخدم')):
                                new_u.append([row.get('اسم_المتدرب'), row.get('اسم_المستخدم'), row.get('كلمة_المرور'), row.get('المسار')])
                        with open(users_db, mode="w", encoding="utf-8-sig", newline="") as f:
                            w = csv.writer(f)
                            w.writerow(["اسم_المتدرب", "اسم_المستخدم", "كلمة_المرور", "المسار"])
                            w.writerows(new_u)
                        st.rerun()
                st.write("---")

# 5. المدربين
elif menu == "🔑 المدربين":
    st.subheader("حسابات المدربين")
    if os.path.exists(admins_db):
        df_adm = pd.read_csv(admins_db, encoding="utf-8-sig", on_bad_lines="skip")
        for _, r in df_adm.iterrows():
            st.write(f"المدرب: {r.get('اسم_المدرب')} (اليوزر: {r.get('اسم_المستخدم')})")

# 6. الإعلانات
elif menu == "📢 الإعلانات":
    st.subheader("نشر إعلان")
    with st.form("ann_form"):
        title = st.text_input("العنوان:")
        body = st.text_area("المحتوى:")
        img = st.file_uploader("صورة (اختياري):", type=["png", "jpg", "jpeg"])
        if st.form_submit_button("نشر"):
            if title and body:
                img_path = ""
                if img:
                    img_path = os.path.join("uploads", f"ann_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{img.name}")
                    with open(img_path, "wb") as f:
                        f.write(img.getbuffer())
                
                exists = os.path.exists(announcements_db)
                with open(announcements_db, mode="a", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    if not exists:
                        w.writerow(["العنوان", "المحتوى", "صورة_الإعلان", "التاريخ"])
                    w.writerow([title, body, img_path, datetime.now().strftime("%Y-%m-%d")])
                st.success("تم النشر")

# 7. المحاضرات
elif menu == "📚 المحاضرات":
    st.subheader("رفع ملفات المحاضرات")
    with st.form("lec_form"):
        track = st.selectbox("المسار:", ["الكل", "Networks & IT", "Cisco CCNA", "Routing & Switching", "Network Security"])
        l_title = st.text_input("عنوان المحاضرة:")
        l_file = st.file_uploader("الملف (PDF / Packet Tracer):", type=["pdf", "zip", "rar", "pkt", "txt", "docx"])
        if st.form_submit_button("رفع"):
            if l_title and l_file:
                path = os.path.join("uploads", f"lec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{l_file.name}")
                with open(path, "wb") as f:
                    f.write(l_file.getbuffer())
                
                exists = os.path.exists(lectures_db)
                with open(lectures_db, mode="a", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    if not exists:
                        w.writerow(["المسار", "عنوان_المحاضرة", "مسار_الملف", "التاريخ"])
                    w.writerow([track, l_title, path, datetime.now().strftime("%Y-%m-%d")])
                st.success("تم الرفع")

# 8. الواجبات
elif menu == "📋 الواجبات":
    st.subheader("إضافة واجب جديد")
    with st.form("asg_form"):
        a_title = st.text_input("عنوان الواجب:")
        a_desc = st.text_area("التفاصيل:")
        d_date = st.date_input("تاريخ التسليم:")
        d_time = st.time_input("وقت التسليم:")
        a_file = st.file_uploader("ملف الأسئلة:", type=["pdf", "docx"])
        
        if st.form_submit_button("نشر الواجب"):
            if a_title:
                deadline = f"{d_date} {d_time.strftime('%H:%M')}"
                path = ""
                if a_file:
                    path = os.path.join("uploads", f"asg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{a_file.name}")
                    with open(path, "wb") as f:
                        f.write(a_file.getbuffer())
                
                exists = os.path.exists(assignments_db)
                with open(assignments_db, mode="a", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    if not exists:
                        w.writerow(["العنوان", "الوصف", "مسار_ملف_الأسئلة", "الديدلاين", "التاريخ"])
                    w.writerow([a_title, a_desc, path, deadline, datetime.now().strftime("%Y-%m-%d")])
                st.success("تم نشر الواجب")

# 9. حلول الطلاب
elif menu == "📥 حلول الواجبات":
    st.subheader("متابعة الحلول المرسلة")
    if os.path.exists(submissions_db):
        df_sub = pd.read_csv(submissions_db, encoding="utf-8-sig", on_bad_lines="skip")
        if not df_sub.empty:
            for idx, r in df_sub.iterrows():
                st.write(f"الطالب: {r.get('اسم_المتدرب')} - الواجب: {r.get('عنوان_الواجب')}")
                sub_path = r.get('مسار_ملف_الحل')
                if pd.notna(sub_path) and os.path.exists(sub_path):
                    with open(sub_path, "rb") as sf:
                        st.download_button("تحميل الحل", data=sf, file_name=os.path.basename(sub_path), key=f"dl_{idx}")
                st.write("---")
        else:
            st.info("مفيش حلول مرفوعة لحد دلوقتي")
    else:
        st.info("مفيش حلول مرفوعة لحد دلوقتي")
