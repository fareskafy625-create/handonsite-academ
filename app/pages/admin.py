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
        height: 40px;
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
    with st.form("group_schedule_form", clear_on_submit=True):
        group_name = st.text_input("اسم الجروب (مثال: جروب الشبكات A):")
        session_day = st.selectbox("اليوم:", ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"])
        session_time = st.text_input("موعد المحاضرة:")
        notes = st.text_area("ملاحظات إضافية:")
        
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
                st.warning("الرجاء إدخال اسم الجروب وموعد المحاضرة.")

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
                    
                    sc1, sc2, sc3 = st.columns([2, 2, 1])
                    with sc1:
                        st.markdown(f"👥 **الجروب:** {g_name}")
                    with sc2:
                        st.text(f"📅 اليوم: {g_day} | ⏰ الوقت: {g_time}")
                    with sc3:
                        if st.button("🗑️ حذف", key=f"del_sch_{idx}"):
                            updated_sch = []
                            for _, r in df_all_sch.iterrows():
                                if not (str(r.get('اسم_الجروب')).strip() == str(g_name).strip() and str(r.get('الموعد')).strip() == str(g_time).strip()):
                                    updated_sch.append([r.get('اسم_الجروب'), r.get('اليوم'), r.get('الموعد'), r.get('ملاحظات')])
                            with open(groups_schedule_db, mode="w", encoding="utf-8-sig", newline="") as f_sout:
                                w_sout = csv.writer(f_sout)
                                w_sout.writerow(["اسم_الجروب", "اليوم", "الموعد", "ملاحظات"])
                                w_sout.writerows(updated_sch)
                            st.rerun()
                    st.write("---")
        except Exception as e:
            st.error(f"خطأ: {e}")

# 2. تسجيل حضور وغياب الطلاب (بالبحث الفردي السريع والزر المستقل لكل طالب)
elif admin_menu == "✅ تسجيل حضور وغياب الطلاب":
    st.subheader("✅ تسجيل حضور وغياب الطلاب (بالبحث الفردي السريع)")
    st.markdown("حدد التاريخ وعنوان المحاضرة، ثم ابحث عن اسم الطالب في شريط البحث أدناه، واضغط على زر الإضافة الخاص به فقط.")
    
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        att_date = st.date_input("📅 تاريخ اليوم:")
    with col_date2:
        lecture_title_input = st.text_input("📝 عنوان المحاضرة أو الدرس:", "محاضرة اليوم")

    st.divider()
    
    # شريط البحث عن الطالب لتسجيل حضوره
    search_att_query = st.text_input("🔍 ابحث عن اسم الطالب لتسجيل حضوره (مثال: منه، نور، عمر):", "").strip()

    if os.path.exists(users_db):
        try:
            df_users = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_users.columns = df_users.columns.str.strip()
            
            if not df_users.empty:
                if search_att_query:
                    df_filtered_users = df_users[
                        df_users['اسم_المتدرب'].astype(str).str.contains(search_att_query, case=False, na=False) | 
                        df_users['اسم_المستخدم'].astype(str).str.contains(search_att_query, case=False, na=False)
                    ]
                else:
                    df_filtered_users = pd.DataFrame(columns=df_users.columns) # لا تظهر الكل إلا إذا كتب شيئاً لتسهيل البحث
                    st.info("💡 اكتب اسم الطالب في شريط البحث أعلاه ليظهر لك وتتمكن من تسجيل حضوره.")

                if not df_filtered_users.empty:
                    st.markdown("### نتائج البحث والطلاب المطابقين:")
                    for idx, row in df_filtered_users.iterrows():
                        u_name = row.get('اسم_المتدرب', 'طالب')
                        u_user = row.get('اسم_المستخدم', '')
                        u_track = row.get('المسار', '')
                        
                        with st.container():
                            c1, c2, c3 = st.columns([2, 1, 1])
                            with c1:
                                st.markdown(f"**👤 الطالب:** {u_name} <br><span style='color:gray; font-size:12px;'>يوزر: {u_user} | المسار: {u_track}</span>", unsafe_allow_html=True)
                            with c2:
                                status_choice = st.selectbox("الحالة", ["حاضر", "غائب", "متأخر"], key=f"status_search_{idx}")
                            with c3:
                                st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
                                btn_add_search = st.button("➕ إضافة الحضور", key=f"btn_search_{idx}")
                                
                                if btn_add_search:
                                    att_records = []
                                    if os.path.exists(attendance_db):
                                        df_att_old = pd.read_csv(attendance_db, encoding="utf-8-sig", on_bad_lines="skip")
                                        df_att_old.columns = df_att_old.columns.str.strip()
                                        for _, r in df_att_old.iterrows():
                                            att_records.append([r.get('التاريخ'), r.get('عنوان_المحاضرة'), r.get('اسم_المتدرب'), r.get('اسم_المستخدم'), r.get('الحالة')])
                                    
                                    # إزالة أي سجل قديم لنفس الطالب في نفس التاريخ لمنع التكرار وتحديث حالته
                                    att_records = [r for r in att_records if not (str(r[0]) == str(att_date) and str(r[3]).strip() == str(u_user).strip())]
                                    
                                    # إضافة سجل الطالب المحدد فقط
                                    att_records.append([str(att_date), lecture_title_input.strip(), u_name, u_user, status_choice])
                                    
                                    with open(attendance_db, mode="w", encoding="utf-8-sig", newline="") as f_att:
                                        w_att = csv.writer(f_att)
                                        w_att.writerow(["التاريخ", "عنوان_المحاضرة", "اسم_المتدرب", "اسم_المستخدم", "الحالة"])
                                        w_att.writerows(att_records)
                                        
                                    st.success(f"✅ تم تسجيل الطالب ({u_name}) - الحالة: ({status_choice}) بتاريخ ({att_date}) بنجاح!")
                            st.divider()
                elif search_att_query:
                    st.warning("⚠️ عذراً، لا يوجد طالب مطابَق لاسم البحث.")
            else:
                st.info("لا يوجد طلاب مسجلين في النظام.")
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
                if st.button("🗑️ مسح سجلات الحضور بالكامل"):
                    os.remove(attendance_db)
                    st.success("تم مسح السجلات بنجاح!")
                    st.rerun()
            else:
                st.info("لا توجد سجلات حضور مسجلة.")
        except Exception as e:
            st.error(f"خطأ: {e}")

# 3. تقييم المتدربين وملاحظات التحسين
elif admin_menu == "⭐ تقييم المتدربين وملاحظات التحسين":
    st.subheader("⭐ تقييم الأداء الأكاديمي للمتدربين وكتابة الملاحظات الإصلاحية")
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
                        placeholder="اكتب تفاصيل المشكلة هنا.."
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
        except Exception as e:
            st.error(f"خطأ: {e}")

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
    search_query = st.text_input("🔍 ابحث عن طالب (اكتب اسم الطالب أو اسم المستخدم):", "").strip()

    if os.path.exists(users_db):
        try:
            df_all_users = pd.read_csv(users_db, encoding="utf-8-sig", on_bad_lines="skip")
            df_all_users.columns = df_all_users.columns.str.strip()
            
            if not df_all_users.empty:
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
        except Exception as e:
            st.error(f"خطأ: {e}")

# 5. خريجي التدريب (سجل الخريجين)
elif admin_menu == "🎓 خريجي التدريب (سجل الخريجين)":
    st.subheader("🎓 سجل خريجي التدريب والطلاب الذين أكملوا الكورس بنجاح")
    with st.form("add_graduate_form", clear_on_submit=True):
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            grad_name = st.text_input("اسم الخريج / المتدرب بالكامل:")
            grad_phone = st.text_input("رقم التليفون / الموبايل:")
        with col_g2:
            grad_track = st.selectbox("المسار أو الكورس:", ["Networks & IT", "Cisco CCNA", "Routing & Switching", "Network Security", "برمجة وروبوتات"])
            grad_eval = st.selectbox("التقييم النهائي بنهاية الكورس:", ["⭐ ممتاز جداً مع مرتبة الشرف", "⭐ ممتاز", "⭐ جيد جداً", "⭐ جيد", "⭐ مجتاز التدريب بنجاح"])
        
        grad_notes = st.text_area("ملاحظات إضافية:")
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
                st.success(f"تم حفظ الخريج ({grad_name}) بنجاح!")

# 6. إدارة المدربين والأدمن وتغيير الباسورد
elif admin_menu == "🔑 إدارة المدربين والأدمن وتغيير الباسورد":
    st.subheader("🔑 إدارة حسابات المدربين (الأدمن)")
    col_adm1, col_adm2 = st.columns(2)

    with col_adm1:
        st.markdown("### ➕ إضافة أدمن / مدرب جديد")
        with st.form("add_new_admin_form", clear_on_submit=True):
            new_adm_name = st.text_input("اسم المدرب الكامل:")
            new_adm_user = st.text_input("اسم المستخدم (Username):")
            new_adm_pass = st.text_input("كلمة المرور:", type="password")
            
            submit_new_admin = st.form_submit_button("إضافة حساب المدرب")
            if submit_new_admin:
                if new_adm_name and new_adm_user and new_adm_pass:
                    try:
                        df_adm_check = pd.read_csv(admins_db, encoding="utf-8-sig", on_bad_lines="skip")
                        df_adm_check.columns = df_adm_check.columns.str.strip()
                        if new_adm_user.strip() in df_adm_check['اسم_المستخدم'].astype(str).str.strip().values:
                            st.error("خطأ: اسم المستخدم موجود بالفعل.")
                        else:
                            with open(admins_db, mode="a", encoding="utf-8-sig", newline="") as f_add:
                                w_add = csv.writer(f_add)
                                w_add.writerow([new_adm_user.strip(), new_adm_pass.strip(), new_adm_name.strip()])
                            st.success(f"تم إضافة حساب المدرب ({new_adm_name}) بنجاح!")
                    except Exception as e:
                        st.error(f"خطأ: {e}")

    with col_adm2:
        st.markdown("### 🔒 تغيير كلمة المرور لحسابك")
        with st.form("change_admin_password_form", clear_on_submit=True):
            old_pass_input = st.text_input("كلمة المرور الحالية:", type="password")
            new_pass_input = st.text_input("كلمة المرور الجديدة:", type="password")
            confirm_pass_input = st.text_input("تأكيد كلمة المرور الجديدة:", type="password")
            
            submit_change_pass = st.form_submit_button("تحديث كلمة المرور")
            if submit_change_pass:
                if old_pass_input and new_pass_input and confirm_pass_input:
                    if new_pass_input != confirm_pass_input:
                        st.error("كلمة المرور الجديدة غير متطابقة.")
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
                                st.success("تم تغيير كلمة المرور بنجاح!")
                            else:
                                st.error("كلمة المرور الحالية غير صحيحة.")
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
                st.success("تم نشر الإعلان بنجاح!")

# 8. رفع ملفات المحاضرات
elif admin_menu == "📚 رفع ملفات المحاضرات":
    st.subheader("📚 رفع ملفات ومصادر المحاضرات للمتدربين")
    with st.form("lecture_upload_form", clear_on_submit=True):
        lec_track = st.selectbox("المسار المستهدف:", ["Networks & IT", "Cisco CCNA", "Routing & Switching", "Network Security"])
        lec_title = st.text_input("عنوان المحاضرة أو الشرح:")
        lec_file = st.file_uploader("اختر ملف الشرح:", type=["pdf", "zip", "rar", "txt", "pptx"])
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
                st.success("تم رفع ملف المحاضرة بنجاح!")

# 9. إضافة الواجبات والتكاليف
elif admin_menu == "📋 إضافة الواجبات والتكاليف":
    st.subheader("📋 نشر Assignment (واجب أو تكليف جديد للمتدربين)")
    with st.form("assignment_upload_form", clear_on_submit=True):
        asg_title = st.text_input("عنوان الـ Assignment:")
        asg_deadline = st.text_input("الموعد النهائي للتسليم (Deadline):")
        asg_file = st.file_uploader("رفـع ملف أسئلة الـ Assignment:", type=["pdf", "png", "jpg", "zip", "txt"])
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
                st.success("تم نشر الـ Assignment بنجاح!")

# 10. متابعة حلول المتدربين
elif admin_menu == "📥 متابعة حلول المتدربين":
    st.subheader("📥 متابعة حلول الـ Assignments المرفوعة من المتدربين")
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
                    st.write("---")
        except Exception as e:
            st.error(f"خطأ: {e}")
