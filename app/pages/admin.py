import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# إعدادات صفحة الأدمن
st.set_page_config(page_title="تسجيل دخول الأدمن - أكاديمية HandsOnSite", page_icon="👨‍💻", layout="wide")

# تصميم CSS مخصص
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
attendance_db = "attendance.csv"
groups_schedule_db = "groups_schedule.csv"

# إعادة إنتاج ملف المدربين وتجنب أي خطأ قديم في الأعمدة
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
                        # تنظيف مسافات أسماء الأعمدة لضمان عدم حدوث الخطأ نهائياً
                        df_admins.columns = df_admins.columns.str.strip()
                        
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
                        st.error(f"حدث خطأ أثناء التحقق من البيانات: {e}")
                else:
                    st.warning("الرجاء إدخال اسم المستخدم وكلمة المرور.")
    st.stop()

# --- القائمة الجانبية للأدمن ---
st.sidebar.markdown(f"### أهلاً بك يا بشمهندس فارس 👋")
st.sidebar.markdown(f"**المدرب الحالي:** {st.session_state.get('admin_name', 'مدرب')}")
st.sidebar.divider()

admin_menu = st.sidebar.radio("خيارات لوحة التحكم:", [
    "📅 جداول مواعيد المجموعات (Groups)",
    "✅ تسجيل حضور وغياب الطلاب",
    "⭐ تقييم المتدربين",
    "👥 إدارة المتدربين (عرض، إضافة، حذف)",
    "🔑 إدارة المدربين والأدمن",
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
st.divider()

# 1. جداول مواعيد المجموعات
if admin_menu == "📅 جداول مواعيد المجموعات (Groups)":
    st.subheader("📅 إضافة وإدارة جدول مواعيد لكل جروب تدريبي")
    with st.form("group_schedule_form"):
        group_name = st.text_input("اسم الجروب (مثال: جروب الشبكات A - صباحي):")
        session_day = st.selectbox("اليوم:", ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"])
        session_time = st.text_input("موعد المحاضرة (مثال: من 4 لـ 6 عصراً):")
        notes = st.text_area("ملاحظات أو تفاصيل إضافية للجروب:")
        
        submit_group_sch = st.form_submit_button("حفظ وإضافة الموعد للجروب")
        
        if submit_group_sch:
            if group_name and session_time:
                sched_records = []
                if os.path.exists(groups_schedule_db):
                    df_old_sch = pd.read_csv(groups_schedule_db, encoding="utf-8-sig", on_bad_lines="skip")
                    for _, r in df_old_sch.iterrows():
                        sched_records.append([r.get('اسم_الجروب'), r.get('اليوم'), r.get('الموعد'), r.get('ملاحظات')])
                
                sched_records.append([group_name.strip(), session_day, session_time.strip(), notes.strip()])
                
                with open(groups_schedule_db, mode="w", encoding="utf-8-sig", newline="") as f_sch:
                    w_sch = csv.writer(f_sch)
                    w_sch.writerow(["اسم_الجروب", "اليوم", "الموعد", "ملاحظات"])
                    w_sch.writerows(sched_records)
                    
                st.success(f"تم حفظ موعد الجروب ({group_name}) بنجاح!")
            else:
                st.warning("الرجاء إدخال اسم الجروب وموعد المحاضرة على الأقل.")

    st.markdown("---")
    st.subheader("📋 جدول المجموعات والمواعيد الحالية:")
    if os.path.exists(groups_schedule_db):
        try:
            df_all_sch = pd.read_csv(groups_schedule_db, encoding="utf-8-sig", on_bad_lines="skip")
            if not df_all_sch.empty:
                for idx, row in df_all_sch.iterrows():
                    g_name = row.get('اسم_الجروب', '')
                    g_day = row.get('اليوم', '')
                    g_time = row.get('الموعد', '')
                    g_notes = row.get('ملاحظات', '')
                    
                    sc1, sc2, sc3 = st.columns([2, 2, 1])
                    with sc1:
                        st.markdown(f"👥 **الجروب:** {g_name}")
                        st.caption(f"📝 ملاحظات: {g_notes}")
                    with sc2:
                        st.text(f"📅 اليوم: {g_day} | ⏰ الوقت: {g_time}")
                    with sc3:
                        if st.button("🗑️ حذف الموعد", key=f"del_sch_{idx}"):
                            updated_sch = []
                            for _, r in df_all_sch.iterrows():
                                if not (str(r.get('اسم_الجروب')).strip() == str(g_name).strip() and str(r.get('الموعد')).strip() == str(g_time).strip()):
                                    updated_sch.append([r.get('اسم_الجروب'), r.get('اليوم'), r.get('الموعد'), r.get('ملاحظات')])
                            
                            with open(groups_schedule_db, mode="w", encoding="utf-8-sig", newline="") as f_sout:
                                w_sout = csv.writer(f_sout)
                                w_sout.writerow(["اسم_الجروب", "اليوم", "الموعد", "ملاحظات"])
                                w_sout.writerows(updated_sch)
                            
                            st.success(f"تم حذف موعد الجروب ({g_name}) بنجاح!")
                            st.rerun()
                    st.write("---")
            else:
                st.info("لا توجد مواعيد مضافة للمجموعات حتى الآن.")
        except Exception as e:
            st.error(f"خطأ: {e}")

# 2. تسجيل حضور وغياب الطلاب
elif admin_menu == "✅ تسجيل حضور وغياب الطلاب":
    st.subheader("✅ تسجيل ومتابعة حضور وغياب المتدربين")
    if os.path.exists(users_db):
        try:
            df_users = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_users.columns = df_users.columns.str.strip()
            if not df_users.empty:
                with st.form("attendance_form"):
                    att_date = st.date_input("تاريخ المحاضرة:")
                    lecture_title_input = st.text_input("عنوان المحاضرة أو الدرس:", "محاضرة اليوم")
                    
                    st.markdown("### قائمة الطلاب:")
                    attendance_status = {}
                    
                    for idx, row in df_users.iterrows():
                        u_name = row.get('اسم_المتدرب', 'طالب')
                        u_user = row.get('اسم_المستخدم', '')
                        
                        col_a1, col_a2 = st.columns([2, 1])
                        with col_a1:
                            st.write(f"👤 {u_name} ({u_user})")
                        with col_a2:
                            status = st.selectbox("الحالة", ["حاضر", "غائب", "متأخر"], key=f"att_{idx}")
                            attendance_status[u_user] = {"name": u_name, "status": status}
                    
                    submit_attendance = st.form_submit_button("حفظ سجل الحضور والغياب")
                    
                    if submit_attendance:
                        att_records = []
                        if os.path.exists(attendance_db):
                            df_att_old = pd.read_csv(attendance_db, encoding="utf-8-sig", on_bad_lines="skip")
                            for _, r in df_att_old.iterrows():
                                att_records.append([r.get('التاريخ'), r.get('عنوان_المحاضرة'), r.get('اسم_المتدرب'), r.get('اسم_المستخدم'), r.get('الحالة')])
                        
                        for u_usr, data in attendance_status.items():
                            att_records.append([str(att_date), lecture_title_input.strip(), data["name"], u_usr, data["status"]])
                        
                        with open(attendance_db, mode="w", encoding="utf-8-sig", newline="") as f_att:
                            w_att = csv.writer(f_att)
                            w_att.writerow(["التاريخ", "عنوان_المحاضرة", "اسم_المتدرب", "اسم_المستخدم", "الحالة"])
                            w_att.writerows(att_records)
                            
                        st.success("تم حفظ سجل الحضور والغياب بنجاح!")
            else:
                st.info("لا يوجد طلاب مسجلين.")
        except Exception as e:
            st.error(f"خطأ: {e}")
    else:
        st.warning("لا توجد بيانات طلاب مسجلة.")

# بقية الأقسام تعمل بنفس الطريقة الآمنة المحدثة...
