import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# إعدادات صفحة الأدمن
st.set_page_config(page_title="تسجيل دخول الأدمن - أكاديمية HandsOnSite", page_icon="👨‍💻", layout="wide")

# تصميم CSS مخصص لتجميل شكل لوحة التحكم والخلفية الشفافة الزجاجية
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, rgba(13, 110, 253, 0.08) 0%, rgba(244, 246, 249, 0.85) 100%); }
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
graduates_db = "graduates.csv"

# ضمان وجود ملف المدربين الأساسي بالأعمدة الصحيحة
if not os.path.exists(admins_db):
    with open(admins_db, mode="w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["اسم_المستخدم", "كلمة_المرور", "اسم_المدرب"])
        w.writerow(["admin", "admin123", "فارس وائل"])

# نظام تسجيل دخول الأدمن
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px; background: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
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
    "⭐ تقييم المتدربين وملاحظات التحسين",
    "👥 إدارة المتدربين (عرض، إضافة، حذف)",
    "🎓 خريجي التدريب (سجل الخريجين)",
    "🔑 إدارة المدربين والأدمن وتغيير الباسورد",
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
    st.markdown("قم بإنشاء جدول أو مواعيد خاصة بكل مجموعة من مجموعات الشبكات والـ IT.")
    st.divider()

    with st.form("group_schedule_form", clear_on_submit=True):
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
                    df_old_sch.columns = df_old_sch.columns.str.strip()
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
            df_all_sch.columns = df_all_sch.columns.str.strip()
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
            st.error(f"حدث خطأ أثناء قراءة جداول المجموعات: {e}")
    else:
        st.info("لا توجد جداول مجموعات مسجلة.")

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
                            df_att_old.columns = df_att_old.columns.str.strip()
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

    st.markdown("---")
    st.subheader("📊 سجل الحضور السابق:")
    if os.path.exists(attendance_db):
        try:
            df_att_log = pd.read_csv(attendance_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_att_log.columns = df_att_log.columns.str.strip()
            if not df_att_log.empty:
                st.dataframe(df_att_log, use_container_width=True)
                if st.button("🗑️ مسح سجلات الحضور"):
                    os.remove(attendance_db)
                    st.success("تم مسح السجلات بنجاح!")
                    st.rerun()
            else:
                st.info("لا توجد سجلات حضور.")
        except Exception as e:
            st.error(f"خطأ: {e}")

# 3. تقييم المتدربين وملاحظات التحسين
elif admin_menu == "⭐ تقييم المتدربين وملاحظات التحسين":
    st.subheader("⭐ تقييم الأداء الأكاديمي للمتدربين وكتابة الملاحظات الإصلاحية")
    st.markdown("يمكنك تقييم الطالب وكتابة تعليق تفصيلي يوضح المشكلة أو النقاط التي يجب عليه إصلاحها أو تحسينها.")
    
    if os.path.exists(users_db):
        try:
            df_users = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_users.columns = df_users.columns.str.strip()
            if not df_users.empty:
                if not os.path.exists(profile_db):
                    with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f:
                        w = csv.writer(f)
                        w.writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])
                
                df_prof = pd.read_csv(profile_db, encoding="utf-8-sig", on_bad_lines="skip")
                df_prof.columns = df_prof.columns.str.strip()
                
                with st.form("admin_eval_form"):
                    user_options = df_users.apply(lambda row: f"{row['اسم_المتدرب']} ({row['اسم_المستخدم']})", axis=1).tolist()
                    selected_user_display = st.selectbox("اختر المتدرب:", user_options)
                    
                    eval_choices = ["⭐ ممتاز جداً", "⭐ ممتاز", "⭐ جيد جداً", "⭐ جيد", "⭐ يحتاج إلى تحسين عاجل"]
                    chosen_username = selected_user_display.split("(")[-1].replace(")", "").strip()
                    
                    current_user_prof = df_prof[df_prof['اسم_المستخدم'].astype(str).str.strip() == chosen_username]
                    default_eval_val = "⭐ ممتاز"
                    default_notes_val = ""
                    if not current_user_prof.empty:
                        val_found = str(current_user_prof.iloc[0].get('التقييم', ''))
                        if val_found in eval_choices:
                            default_eval_val = val_found
                        notes_found = str(current_user_prof.iloc[0].get('نبذة', ''))
                        if notes_found != "nan":
                            default_notes_val = notes_found
                    
                    new_evaluation = st.selectbox("التقييم الأكاديمي الجديد:", eval_choices, index=eval_choices.index(default_eval_val) if default_eval_val in eval_choices else 0)
                    
                    improvement_comment = st.text_area(
                        "📝 كومنت / ملاحظات المدرب (تحديد المشكلة أو النقاط التي يجب على الطالب حلها):",
                        value=default_notes_val,
                        placeholder="اكتب تفاصيل المشكلة هنا.. (مثال: توجد مشكلة لديك في فهم إعدادات الـ Subnetting أو الـ OSPF يرجى مراجعة محاضرة يوم الإثنين وحلها)"
                    )
                    
                    submit_eval = st.form_submit_button("حفظ وتحديث التقييم والملاحظات")
                    
                    if submit_eval:
                        profiles_list = []
                        for _, r in df_prof.iterrows():
                            if str(r.get('اسم_المستخدم')).strip() != chosen_username:
                                profiles_list.append([r.get('اسم_المستخدم'), r.get('الصورة_الشخصية'), r.get('التقييم'), r.get('نبذة')])
                        
                        old_avatar = ""
                        if not current_user_prof.empty:
                            old_avatar = str(current_user_prof.iloc[0].get('الصورة_الشخصية', ''))
                            
                        profiles_list.append([chosen_username, old_avatar, new_evaluation, improvement_comment.strip()])
                        
                        with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f_p:
                            w_p = csv.writer(f_p)
                            w_p.writerow(["اسم_المستخدم", "الصورة_الشخصية", "التقييم", "نبذة"])
                            w_p.writerows(profiles_list)
                        
                        st.success(f"تم تحديث التقييم والملاحظات الخاصة بالطالب بنجاح!")
            else:
                st.info("لا يوجد متدربين.")
        except Exception as e:
            st.error(f"خطأ: {e}")
    else:
        st.warning("لا توجد بيانات مستخدمين.")

# 4. إدارة المتدربين (إضافة + بحث سريع + جدول عرض وحذف الطلاب)
elif admin_menu == "👥 إدارة المتدربين (عرض، إضافة، حذف)":
    st.subheader("👥 إدارة الطلاب المتدربين")
    
    try:
        total_trainees = 0
        if os.path.exists(users_db):
            df_u_cnt = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_u_cnt.columns = df_u_cnt.columns.str.strip()
            total_trainees = len(df_u_cnt)
            
        total_ann = 0
        if os.path.exists(announcements_db):
            df_a_cnt = pd.read_csv(announcements_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_a_cnt.columns = df_a_cnt.columns.str.strip()
            total_ann = len(df_a_cnt)
            
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="👥 إجمالي الطلاب المتدربين", value=total_trainees)
        with col_m2:
            st.metric(label="📢 إجمالي الإعلانات المنشورة", value=total_ann)
    except Exception:
        pass
        
    st.divider()
    
    with st.expander("➕ إضافة طالب متدرب جديد", expanded=False):
        # استخدام clear_on_submit=True لتفريغ الخانات تلقائياً بعد الحفظ لإضافة الطالب التالي مباشرة
        with st.form("add_user_form", clear_on_submit=True):
            trainee_name = st.text_input("اسم المتدرب الكامل:")
            trainee_username = st.text_input("اسم المستخدم (Username):")
            trainee_password = st.text_input("كلمة المرور:", type="password")
            trainee_track = st.selectbox("المسار التدريبي:", ["Networks & IT", "Cisco CCNA", "Routing & Switching", "Network Security"])
            
            submit_user = st.form_submit_button("إضافة الطالب وتفريغ الخانات")
            
            if submit_user:
                if trainee_name and trainee_username and trainee_password:
                    file_exists = os.path.exists(users_db)
                    with open(users_db, mode="a", encoding="utf-8-sig", newline="") as f:
                        w = csv.writer(f)
                        if not file_exists:
                            w.writerow(["اسم_المتدرب", "اسم_المستخدم", "كلمة_المرور", "المسار"])
                        w.writerow([trainee_name.strip(), trainee_username.strip(), trainee_password.strip(), trainee_track])
                    
                    st.success(f"✅ تم إضافة الطالب ({trainee_name}) بنجاح! الخانات جاهزة لإضافة الطالب التالي.")
                else:
                    st.warning("الرجاء تعبئة جميع الحقول المطلوبة.")
                    
    st.markdown("### 📋 جدول الطلاب المتدربين والبحث السريع:")
    
    # شريط البحث الذكي
    search_query = st.text_input("🔍 ابحث عن طالب (اكتب اسم الطالب أو اسم المستخدم):", "").strip()

    if os.path.exists(users_db):
        try:
            df_all_users = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_all_users.columns = df_all_users.columns.str.strip()
            
            if not df_all_users.empty:
                # تصفية الطلاب بناءً على شريط البحث
                if search_query:
                    df_filtered = df_all_users[
                        df_all_users['اسم_المتدرب'].astype(str).str.contains(search_query, case=False, na=False) | 
                        df_all_users['اسم_المستخدم'].astype(str).str.contains(search_query, case=False, na=False)
                    ]
                else:
                    df_filtered = df_all_users

                if not df_filtered.empty:
                    for idx, row in df_filtered.iterrows():
                        u_name = row.get('اسم_المتدرب', '')
                        u_user = row.get('اسم_المستخدم', '')
                        u_track = row.get('المسار', '')
                        
                        uc1, uc2, uc3 = st.columns([2, 2, 1])
                        with uc1:
                            st.text(f"👤 الطالب: {u_name}")
                        with uc2:
                            st.text(f"💻 اليوزر: {u_user} | المسار: {u_track}")
                        with uc3:
                            if st.button("🗑️ حذف", key=f"del_user_{idx}"):
                                updated_users = []
                                for _, r in df_all_users.iterrows():
                                    if str(r.get('اسم_المستخدم')).strip() != str(u_user).strip():
                                        updated_users.append([r.get('اسم_المتدرب'), r.get('اسم_المستخدم'), r.get('كلمة_المرور'), r.get('المسار')])
                                
                                with open(users_db, mode="w", encoding="utf-8-sig", newline="") as f_uout:
                                    w_uout = csv.writer(f_uout)
                                    w_uout.writerow(["اسم_المتدرب", "اسم_المستخدم", "كلمة_المرور", "المسار"])
                                    w_uout.writerows(updated_users)
                                
                                st.success(f"تم حذف الطالب ({u_name}) بنجاح!")
                                st.rerun()
                        st.write("---")
                else:
                    st.warning("⚠️ عذراً، لا يوجد طالب مطابق لبحثك.")
            else:
                st.info("لا يوجد طلاب متدربين.")
        except Exception as e:
            st.error(f"خطأ: {e}")
    else:
        st.info("لا توجد بيانات طلاب.")

# 5. خريجي التدريب (سجل الخريجين والمدربين المنتهين)
elif admin_menu == "🎓 خريجي التدريب (سجل الخريجين)":
    st.subheader("🎓 سجل خريجي التدريب والطلاب الذين أكملوا الكورس بنجاح")
    st.markdown("يمكنك إضافة اسم الخريج/المدرب، رقم التليفون، والتقييم النهائي بنهاية التدريب.")
    st.divider()

    with st.form("add_graduate_form", clear_on_submit=True):
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            grad_name = st.text_input("اسم الخريج / المتدرب بالكامل:")
            grad_phone = st.text_input("رقم التليفون / الموبايل:")
        with col_g2:
            grad_track = st.selectbox("المسار أو الكورس:", ["Networks & IT", "Cisco CCNA", "Routing & Switching", "Network Security", "برمجة وروبوتات"])
            grad_eval = st.selectbox("التقييم النهائي بنهاية الكورس:", ["⭐ ممتاز جداً مع مرتبة الشرف", "⭐ ممتاز", "⭐ جيد جداً", "⭐ جيد", "⭐ مجتاز التدريب بنجاح"])
        
        grad_notes = st.text_area("ملاحظات إضافية (أو مكان العمل/المهارة المكتسبة):")
        
        submit_grad = st.form_submit_button("حفظ وإضافة إلى سجل الخريجين")
        
        if submit_grad:
            if grad_name and grad_phone:
                grad_records = []
                if os.path.exists(graduates_db):
                    df_old_grad = pd.read_csv(graduates_db, encoding="utf-8-sig", on_bad_lines="skip")
                    df_old_grad.columns = df_old_grad.columns.str.strip()
                    for _, r in df_old_grad.iterrows():
                        grad_records.append([r.get('الاسم'), r.get('رقم_التليفون'), r.get('المسار'), r.get('التقييم'), r.get('ملاحظات')])
                
                grad_records.append([grad_name.strip(), grad_phone.strip(), grad_track, grad_eval, grad_notes.strip()])
                
                with open(graduates_db, mode="w", encoding="utf-8-sig", newline="") as f_g:
                    w_g = csv.writer(f_g)
                    w_g.writerow(["الاسم", "رقم_التليفون", "المسار", "التقييم", "ملاحظات"])
                    w_g.writerows(grad_records)
                    
                st.success(f"تم حفظ الخريج ({grad_name}) في السجل بنجاح!")
            else:
                st.warning("الرجاء إدخال اسم الخريج ورقم التليفون على الأقل.")

    st.markdown("---")
    st.subheader("📋 قائمة خريجي التدريب المسجلين:")
    if os.path.exists(graduates_db):
        try:
            df_all_grads = pd.read_csv(graduates_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_all_grads.columns = df_all_grads.columns.str.strip()
            if not df_all_grads.empty:
                for idx, row in df_all_grads.iterrows():
                    g_name = row.get('الاسم', '')
                    g_phone = row.get('رقم_التليفون', '')
                    g_track = row.get('المسار', '')
                    g_eval = row.get('التقييم', '')
                    g_notes = row.get('ملاحظات', '')
                    
                    gc1, gc2, gc3 = st.columns([2, 2, 1])
                    with gc1:
                        st.markdown(f"🎓 **الخريج:** {g_name}")
                        st.text(f"📞 هاتف: {g_phone}")
                    with gc2:
                        st.text(f"💻 المسار: {g_track}")
                        st.markdown(f"**التقييم:** {g_eval}")
                        if g_notes:
                            st.caption(f"📝 ملاحظات: {g_notes}")
                    with gc3:
                        if st.button("🗑️ حذف من السجل", key=f"del_grad_{idx}"):
                            updated_grads = []
                            for _, r in df_all_grads.iterrows():
                                if not (str(r.get('الاسم')).strip() == str(g_name).strip() and str(r.get('رقم_التليفون')).strip() == str(g_phone).strip()):
                                    updated_grads.append([r.get('الاسم'), r.get('رقم_التليفون'), r.get('المسار'), r.get('التقييم'), r.get('ملاحظات')])
                            
                            with open(graduates_db, mode="w", encoding="utf-8-sig", newline="") as f_gout:
                                w_gout = csv.writer(f_gout)
                                w_gout.writerow(["الاسم", "رقم_التليفون", "المسار", "التقييم", "ملاحظات"])
                                w_gout.writerows(updated_grads)
                            
                            st.success(f"تم حذف الخريج ({g_name}) من السجل بنجاح!")
                            st.rerun()
                    st.write("---")
            else:
                st.info("لا يوجد خريجون مسجلون حتى الآن.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة سجل الخريجين: {e}")
    else:
        st.info("سجل الخريجين فارغ حالياً.")

# 6. إدارة المدربين والأدمن وتغيير الباسورد
elif admin_menu == "🔑 إدارة المدربين والأدمن وتغيير الباسورد":
    st.subheader("🔑 إدارة حسابات المدربين (الأدمن)")
    st.markdown("يمكنك هنا إضافة حسابات للمدربين الزملاء معك، أو تغيير كلمة المرور لحسابك الحالي.")
    st.divider()

    col_adm1, col_adm2 = st.columns(2)

    with col_adm1:
        st.markdown("### ➕ إضافة أدمن / مدرب جديد")
        with st.form("add_new_admin_form", clear_on_submit=True):
            new_adm_name = st.text_input("اسم المدرب الرباعي/الكامل:")
            new_adm_user = st.text_input("اسم المستخدم لتسجيل الدخول (Username):")
            new_adm_pass = st.text_input("كلمة المرور:", type="password")
            
            submit_new_admin = st.form_submit_button("إضافة حساب المدرب")
            
            if submit_new_admin:
                if new_adm_name and new_adm_user and new_adm_pass:
                    try:
                        df_adm_check = pd.read_csv(admins_db, encoding="utf-8-sig", on_bad_lines="skip")
                        df_adm_check.columns = df_adm_check.columns.str.strip()
                        
                        if new_adm_user.strip() in df_adm_check['اسم_المستخدم'].astype(str).str.strip().values:
                            st.error("خطأ: اسم المستخدم هذا موجود بالفعل، اختر اسماً آخر.")
                        else:
                            with open(admins_db, mode="a", encoding="utf-8-sig", newline="") as f_add:
                                w_add = csv.writer(f_add)
                                w_add.writerow([new_adm_user.strip(), new_adm_pass.strip(), new_adm_name.strip()])
                            st.success(f"تم إضافة حساب المدرب ({new_adm_name}) بنجاح!")
                    except Exception as e:
                        st.error(f"حدث خطأ: {e}")
                else:
                    st.warning("الرجاء ملء جميع الحقول المطلوبة.")

    with col_adm2:
        st.markdown("### 🔒 تغيير كلمة المرور لحسابك الحالي")
        with st.form("change_admin_password_form", clear_on_submit=True):
            st.info(f"الحساب الحالي: {st.session_state.get('admin_name', '')} ({st.session_state.get('admin_username', '')})")
            old_pass_input = st.text_input("كلمة المرور الحالية:", type="password")
            new_pass_input = st.text_input("كلمة المرور الجديدة:", type="password")
            confirm_pass_input = st.text_input("تأكيد كلمة المرور الجديدة:", type="password")
            
            submit_change_pass = st.form_submit_button("تحديث كلمة المرور")
            
            if submit_change_pass:
                if old_pass_input and new_pass_input and confirm_pass_input:
                    if new_pass_input != confirm_pass_input:
                        st.error("خطأ: كلمة المرور الجديدة غير متطابقة في الحقلين.")
                    else:
                        try:
                            df_change = pd.read_csv(admins_db, encoding="utf-8-sig", on_bad_lines="skip")
                            df_change.columns = df_change.columns.str.strip()
                            current_uname = st.session_state.get('admin_username', '')
                            
                            user_row = df_change[df_change['اسم_المستخدم'].astype(str).str.strip() == current_uname]
                            if not user_row.empty and str(user_row.iloc[0]['كلمة_المرور']).strip() == old_pass_input.strip():
                                updated_admins = []
                                for _, r in df_change.iterrows():
                                    uname = str(r.get('اسم_المستخدم')).strip()
                                    upass = str(r.get('كلمة_المرور')).strip()
                                    uname_full = str(r.get('اسم_المدرب')).strip()
                                    
                                    if uname == current_uname:
                                        upass = new_pass_input.strip()
                                    updated_admins.append([uname, upass, uname_full])
                                
                                with open(admins_db, mode="w", encoding="utf-8-sig", newline="") as f_up:
                                    w_up = csv.writer(f_up)
                                    w_up.writerow(["اسم_المستخدم", "كلمة_المرور", "اسم_المدرب"])
                                    w_up.writerows(updated_admins)
                                    
                                st.success("تم تغيير كلمة المرور بنجاح! يرجى إعادة تسجيل الدخول لتطبيق التغيير.")
                            else:
                                st.error("خطأ: كلمة المرور الحالية غير صحيحة.")
                        except Exception as e:
                            st.error(f"حدث خطأ: {e}")
                else:
                    st.warning("الرجاء تعبئة جميع حقول كلمة المرور.")

    st.markdown("---")
    st.markdown("### 📋 قائمة المدربين المسجلين في النظام:")
    if os.path.exists(admins_db):
        try:
            df_all_admins = pd.read_csv(admins_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_all_admins.columns = df_all_admins.columns.str.strip()
            if not df_all_admins.empty:
                for idx, row in df_all_admins.iterrows():
                    a_name = row.get('اسم_المدرب', '')
                    a_user = row.get('اسم_المستخدم', '')
                    
                    ac1, ac2 = st.columns([3, 1])
                    with ac1:
                        st.text(f"👤 المدرب: {a_name} | 💻 اسم المستخدم: {a_user}")
                    with ac2:
                        if a_user != "admin" and a_user != st.session_state.get('admin_username', ''):
                            if st.button("🗑️ حذف الحساب", key=f"del_adm_{idx}"):
                                updated_admins_list = []
                                for _, r in df_all_admins.iterrows():
                                    if str(r.get('اسم_المستخدم')).strip() != str(a_user).strip():
                                        updated_admins_list.append([r.get('اسم_المستخدم'), r.get('كلمة_المرور'), r.get('اسم_المدرب')])
                                
                                with open(admins_db, mode="w", encoding="utf-8-sig", newline="") as f_aout:
                                    w_aout = csv.writer(f_aout)
                                    w_aout.writerow(["اسم_المستخدم", "كلمة_المرور", "اسم_المدرب"])
                                    w_aout.writerows(updated_admins_list)
                                
                                st.success(f"تم حذف حساب المدرب ({a_name}) بنجاح!")
                                st.rerun()
        except Exception as e:
            st.error(f"خطأ: {e}")

# 7. نشر الإعلانات والأخبار
elif admin_menu == "📢 نشر الإعلانات والأخبار":
    st.subheader("📢 نشر إعلان أو خبر جديد للمتدربين")
    with st.form("announcement_form", clear_on_submit=True):
        ann_title = st.text_input("عنوان الإعلان:")
        ann_content = st.text_area("محتوى الإعلان:")
        ann_img = st.file_uploader("صورة مرفقة للإعلان (اختياري):", type=["jpg", "jpeg", "png"])
        
        submit_ann = st.form_submit_button("نشر الإعلان الآن")
        
        if submit_ann:
            if ann_title and ann_content:
                img_path_str = ""
                if ann_img is not None:
                    img_filename = f"ann_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{ann_img.name}"
                    img_path_str = os.path.join("uploads", img_filename)
                    with open(img_path_str, "wb") as imf:
                        imf.write(ann_img.getbuffer())
                
                ann_records = []
                if os.path.exists(announcements_db):
                    df_old_ann = pd.read_csv(announcements_db, encoding="utf-8-sig", on_bad_lines="skip")
                    df_old_ann.columns = df_old_ann.columns.str.strip()
                    for _, r in df_old_ann.iterrows():
                        ann_records.append([r.get('العنوان'), r.get('المحتوى'), r.get('صورة_الإعلان'), r.get('التاريخ')])
                
                ann_records.append([ann_title.strip(), ann_content.strip(), img_path_str, datetime.now().strftime("%Y-%m-%d %H:%M")])
                
                with open(announcements_db, mode="w", encoding="utf-8-sig", newline="") as f_an:
                    w_an = csv.writer(f_an)
                    w_an.writerow(["العنوان", "المحتوى", "صورة_الإعلان", "التاريخ"])
                    w_an.writerows(ann_records)
                
                st.success("تم نشر الإعلان بنجاح لجميع المتدربين!")
            else:
                st.warning("الرجاء إدخال عنوان ومحتوى الإعلان على الأقل.")

    st.markdown("---")
    st.subheader("📋 الإعلانات النشطة الحالية:")
    if os.path.exists(announcements_db):
        try:
            df_curr_ann = pd.read_csv(announcements_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_curr_ann.columns = df_curr_ann.columns.str.strip()
            if not df_curr_ann.empty:
                for idx, row in df_curr_ann.iterrows():
                    st.info(f"### 📌 {row.get('العنوان', '')}\n\n{row.get('المحتوى', '')}\n\n*تاريخ النشر: {row.get('التاريخ', '')}*")
                    if pd.notna(row.get('صورة_الإعلان')) and os.path.exists(str(row.get('صورة_الإعلان'))):
                        st.image(row.get('صورة_الإعلان'), width=300)
                    if st.button("🗑️ حذف هذا الإعلان", key=f"del_ann_{idx}"):
                        updated_anns = []
                        for _, r in df_curr_ann.iterrows():
                            if str(r.get('العنوان')).strip() != str(row.get('العنوان')).strip():
                                updated_anns.append([r.get('العنوان'), r.get('المحتوى'), r.get('صورة_الإعلان'), r.get('التاريخ')])
                        with open(announcements_db, mode="w", encoding="utf-8-sig", newline="") as f_aout:
                            w_aout = csv.writer(f_aout)
                            w_aout.writerow(["العنوان", "المحتوى", "صورة_الإعلان", "التاريخ"])
                            w_aout.writerows(updated_anns)
                        st.success("تم حذف الإعلان بنجاح!")
                        st.rerun()
                    st.write("---")
            else:
                st.info("لا توجد إعلانات نشطة.")
        except Exception as e:
            st.error(f"خطأ: {e}")

# 8. رفع ملفات المحاضرات
elif admin_menu == "📚 رفع ملفات المحاضرات":
    st.subheader("📚 رفع ملفات ومصادر المحاضرات للمتدربين")
    with st.form("lecture_upload_form", clear_on_submit=True):
        lec_track = st.selectbox("المسار المستهدف:", ["Networks & IT", "Cisco CCNA", "Routing & Switching", "Network Security"])
        lec_title = st.text_input("عنوان المحاضرة أو الشرح:")
        lec_file = st.file_uploader("اختر ملف الشرح (PDF / ZIP / TXT):", type=["pdf", "zip", "rar", "txt", "pptx"])
        
        submit_lec = st.form_submit_button("رفع ملف المحاضرة")
        
        if submit_lec:
            if lec_title and lec_file is not None:
                lec_filename = f"lec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{lec_file.name}"
                lec_path_str = os.path.join("uploads", lec_filename)
                with open(lec_path_str, "wb") as lf:
                    lf.write(lec_file.getbuffer())
                
                lec_records = []
                if os.path.exists(lectures_db):
                    df_old_lec = pd.read_csv(lectures_db, encoding="utf-8-sig", on_bad_lines="skip")
                    df_old_lec.columns = df_old_lec.columns.str.strip()
                    for _, r in df_old_lec.iterrows():
                        lec_records.append([r.get('المسار'), r.get('عنوان_المحاضرة'), r.get('مسار_الملف'), r.get('التاريخ')])
                
                lec_records.append([lec_track, lec_title.strip(), lec_path_str, datetime.now().strftime("%Y-%m-%d %H:%M")])
                
                with open(lectures_db, mode="w", encoding="utf-8-sig", newline="") as f_lc:
                    w_lc = csv.writer(f_lc)
                    w_lc.writerow(["المسار", "عنوان_المحاضرة", "مسار_الملف", "التاريخ"])
                    w_lc.writerows(lec_records)
                
                st.success("تم رفع ملف المحاضرة بنجاح لجميع طلاب المسار!")
            else:
                st.warning("الرجاء إدخال عنوان المحاضرة واختيار الملف.")

    st.markdown("---")
    st.subheader("📋 المحاضرات والملفات المرفوعة:")
    if os.path.exists(lectures_db):
        try:
            df_curr_lec = pd.read_csv(lectures_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_curr_lec.columns = df_curr_lec.columns.str.strip()
            if not df_curr_lec.empty:
                for idx, row in df_curr_lec.iterrows():
                    st.write(f"- **المسار:** {row.get('المسار')} | **المحاضرة:** {row.get('عنوان_المحاضرة')} | *تاريخ الرفع: {row.get('التاريخ')}*")
                    if st.button("🗑️ حذف هذا الملف", key=f"del_lec_{idx}"):
                        updated_lecs = []
                        for _, r in df_curr_lec.iterrows():
                            if str(r.get('عنوان_المحاضرة')).strip() != str(row.get('عنوان_المحاضرة')).strip():
                                updated_lecs.append([r.get('المسار'), r.get('عنوان_المحاضرة'), r.get('مسار_الملف'), r.get('التاريخ')])
                        with open(lectures_db, mode="w", encoding="utf-8-sig", newline="") as f_lout:
                            w_lout = csv.writer(f_lout)
                            w_lout.writerow(["المسار", "عنوان_المحاضرة", "مسار_الملف", "التاريخ"])
                            w_lout.writerows(updated_lecs)
                        st.success("تم حذف الملف بنجاح!")
                        st.rerun()
                    st.write("---")
            else:
                st.info("لا توجد ملفات محاضرات مرفوعة.")
        except Exception as e:
            st.error(f"خطأ: {e}")

# 9. إضافة الواجبات والتكاليف (Assignments)
elif admin_menu == "📋 إضافة الواجبات والتكاليف":
    st.subheader("📋 نشر Assignment (واجب أو تكليف جديد للمتدربين)")
    with st.form("assignment_upload_form", clear_on_submit=True):
        asg_title = st.text_input("عنوان الـ Assignment:")
        asg_deadline = st.text_input("الموعد النهائي للتسليم (Deadline - مثال: الخميس القادم 11 مساءً):")
        asg_file = st.file_uploader("رفـع ملف أسئلة الـ Assignment (PDF أو صور):", type=["pdf", "png", "jpg", "zip", "txt"])
        
        submit_asg = st.form_submit_button("نشر الـ Assignment للمتدربين")
        
        if submit_asg:
            if asg_title:
                asg_path_str = ""
                if asg_file is not None:
                    asg_filename = f"asg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{asg_file.name}"
                    asg_path_str = os.path.join("uploads", asg_filename)
                    with open(asg_path_str, "wb") as af:
                        af.write(asg_file.getbuffer())
                
                asg_records = []
                if os.path.exists(assignments_db):
                    df_old_asg = pd.read_csv(assignments_db, encoding="utf-8-sig", on_bad_lines="skip")
                    df_old_asg.columns = df_old_asg.columns.str.strip()
                    for _, r in df_old_asg.iterrows():
                        asg_records.append([r.get('العنوان'), r.get('الديدلاين'), r.get('مسار_ملف_الأسئلة'), r.get('التاريخ')])
                
                asg_records.append([asg_title.strip(), asg_deadline.strip(), asg_path_str, datetime.now().strftime("%Y-%m-%d %H:%M")])
                
                with open(assignments_db, mode="w", encoding="utf-8-sig", newline="") as f_as:
                    w_as = csv.writer(f_as)
                    w_as.writerow(["العنوان", "الديدلاين", "مسار_ملف_الأسئلة", "التاريخ"])
                    w_as.writerows(asg_records)
                
                st.success("تم نشر الـ Assignment بنجاح لجميع المتدربين في بواباتهم!")
            else:
                st.warning("الرجاء إدخال عنوان الـ Assignment على الأقل.")

    st.markdown("---")
    st.subheader("📋 الـ Assignments المنشورة حالياً:")
    if os.path.exists(assignments_db):
        try:
            df_curr_asg = pd.read_csv(assignments_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_curr_asg.columns = df_curr_asg.columns.str.strip()
            if not df_curr_asg.empty:
                for idx, row in df_curr_asg.iterrows():
                    st.write(f"- **Assignment:** {row.get('العنوان')} | **الموعد النهائي:** {row.get('الديدلاين')} | *تاريخ النشر: {row.get('التاريخ')}*")
                    if st.button("🗑️ حذف هذا الـ Assignment", key=f"del_asg_{idx}"):
                        updated_asgs = []
                        for _, r in df_curr_asg.iterrows():
                            if str(r.get('العنوان')).strip() != str(row.get('العنوان')).strip():
                                updated_asgs.append([r.get('العنوان'), r.get('الديدلاين'), r.get('مسار_ملف_الأسئلة'), r.get('التاريخ')])
                        with open(assignments_db, mode="w", encoding="utf-8-sig", newline="") as f_asout:
                            w_asout = csv.writer(f_asout)
                            w_asout.writerow(["العنوان", "الديدلاين", "مسار_ملف_الأسئلة", "التاريخ"])
                            w_asout.writerows(updated_asgs)
                        st.success("تم حذف الـ Assignment بنجاح!")
                        st.rerun()
                    st.write("---")
            else:
                st.info("لا توجد Assignments منشورة حالياً.")
        except Exception as e:
            st.error(f"خطأ: {e}")

# 10. متابعة حلول المتدربين
elif admin_menu == "📥 متابعة حلول المتدربين":
    st.subheader("📥 متابعة حلول الـ Assignments المرفوعة من المتدربين")
    st.markdown("استعرض هنا حلول الواجبات التي قام المتدربين برفعها مع إمكانية تحميلها ومراجعتها.")
    st.divider()

    if os.path.exists(submissions_db):
        try:
            df_subs = pd.read_csv(submissions_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_subs.columns = df_subs.columns.str.strip()
            if not df_subs.empty:
                for idx, row in df_subs.iterrows():
                    t_name = row.get('اسم_المتدرب', '')
                    t_user = row.get('اسم_المستخدم', '')
                    asg_title = row.get('عنوان_الواجب', '')
                    sub_file = row.get('مسار_ملف_الحل', '')
                    sub_date = row.get('التاريخ', '')

                    st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 8px; border-right: 4px solid #198754; margin-bottom: 10px;">
                            <h4 style="color: #198754; margin-top: 0;">👤 المتدرب: {t_name} ({t_user})</h4>
                            <p><b>Assignment:</b> {asg_title} | <b>تاريخ الرفع:</b> {sub_date}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    if pd.notna(sub_file) and isinstance(sub_file, str) and os.path.exists(sub_file):
                        with open(sub_file, "rb") as sf:
                            st.download_button(
                                label=f"📥 تحميل حل الـ Assignment ({os.path.basename(sub_file)})",
                                data=sf,
                                file_name=os.path.basename(sub_file),
                                key=f"dl_sub_{idx}"
                            )
                    else:
                        st.warning("ملف الحل غير موجود على الخادم.")

                    if st.button("🗑️ حذف هذا التسليم", key=f"del_sub_{idx}"):
                        updated_subs = []
                        for _, r in df_subs.iterrows():
                            if not (str(r.get('اسم_المستخدم')).strip() == str(t_user).strip() and str(r.get('عنوان_الواجب')).strip() == str(asg_title).strip()):
                                updated_subs.append([r.get('اسم_المتدرب'), r.get('اسم_المستخدم'), r.get('عنوان_الواجب'), r.get('مسار_ملف_الحل'), r.get('التاريخ')])
                        with open(submissions_db, mode="w", encoding="utf-8-sig", newline="") as f_sout:
                            w_sout = csv.writer(f_sout)
                            w_sout.writerow(["اسم_المتدرب", "اسم_المستخدم", "عنوان_الواجب", "مسار_ملف_الحل", "التاريخ"])
                            w_sout.writerows(updated_subs)
                        st.success("تم حذف التسليم بنجاح!")
                        st.rerun()
                    st.write("---")
            else:
                st.info("لا توجد حلول مرفوعة من المتدربين حتى الآن.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الحلول: {e}")
    else:
        st.info("لا توجد تسليمات مسجلة حتى الآن.")
