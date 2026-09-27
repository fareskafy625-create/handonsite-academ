import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Admin Dashboard - HandsOnSite Academy", page_icon="⚡", layout="wide")

# Custom Modern & Sleek CSS Styling (Custom Animations & Polish)
st.markdown("""
    <style>
    /* Global Background & Font */
    .main { background-color: #f3f4f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Sleek Sidebar Design */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Modern Button Styling with Smooth Hover Animations */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        height: 48px;
        background-color: #ffffff;
        color: #4f46e5;
        border: 1px solid #e0e7ff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 6px;
        text-align: left;
        padding-left: 18px;
    }
    div.stButton > button:hover { 
        background-color: #4f46e5; 
        color: white; 
        border-color: #4f46e5;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(79, 70, 229, 0.2);
    }
    
    /* Inputs and Forms Aesthetic Polish */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        background-color: #ffffff !important;
    }
    
    /* Custom Cards Container Effect */
    .css-1r6slb0, .element-container {
        animation: fadeIn 0.4s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

os.makedirs("uploads", exist_ok=True)

# Admin Login System
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("""
            <div style="background: white; padding: 35px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center;">
                <h2 style="color: #4f46e5; margin-bottom: 8px; font-weight: 700;">⚡ HandsOnSite Academy</h2>
                <p style="color: #6b7280; font-size: 14px; margin-bottom: 25px;">Secure Administrative Control Center</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login_form"):
            st.markdown("🔒 **Authentication Required**")
            admin_user = st.text_input("Username:")
            admin_pass = st.text_input("Password:", type="password")
            
            submit_admin_login = st.form_submit_button("Access Dashboard")
            
            if submit_admin_login:
                if admin_user == "admin" and admin_pass == "admin123":
                    st.session_state.admin_logged_in = True
                    st.success("Welcome back, Administrator!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
    st.stop()

if 'admin_page' not in st.session_state:
    st.session_state.admin_page = "👥 Manage Students"

# Sidebar Navigation for Admin
st.sidebar.markdown("""
    <div style="padding: 10px 0 15px 0; text-align: center;">
        <h3 style="color: #111827; font-size: 18px; margin: 0;">🛡️ Admin Portal</h3>
        <p style="color: #9ca3af; font-size: 12px; margin: 0;">Management Dashboard</p>
    </div>
""", unsafe_allow_html=True)
st.sidebar.divider()

if st.sidebar.button("👥 Manage Students"):
    st.session_state.admin_page = "👥 Manage Students"
    st.rerun()

if st.sidebar.button("📅 Attendance Tracking"):
    st.session_state.admin_page = "📅 Attendance Tracking"
    st.rerun()

if st.sidebar.button("🎓 Completed Training"):
    st.session_state.admin_page = "🎓 Completed Training"
    st.rerun()

if st.sidebar.button("📢 Post Announcements"):
    st.session_state.admin_page = "📢 Post Announcements"
    st.rerun()

if st.sidebar.button("📚 Upload Lectures"):
    st.session_state.admin_page = "📚 Upload Lectures"
    st.rerun()

if st.sidebar.button("📋 Add Assignments"):
    st.session_state.admin_page = "📋 Add Assignments"
    st.rerun()

if st.sidebar.button("📥 Student Submissions"):
    st.session_state.admin_page = "📥 Student Submissions"
    st.rerun()

if st.sidebar.button("⭐ Student Evaluation & Notes"):
    st.session_state.admin_page = "⭐ Student Evaluation & Notes"
    st.rerun()

st.sidebar.divider()

if st.sidebar.button("🚪 Logout Session"):
    st.session_state.admin_logged_in = False
    st.rerun()

admin_menu = st.session_state.admin_page

# 1. Manage Students Section
if admin_menu == "👥 Manage Students":
    st.title("👥 Student Accounts Management")
    st.markdown("Easily onboard new students, oversee active profiles, or manage system records.")
    st.divider()

    users_db = "users.csv"
    if not os.path.exists(users_db):
        with open(users_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["student_name", "username", "password", "track"])

    col_u1, col_u2 = st.columns([1, 1], gap="large")

    with col_u1:
        st.subheader("➕ Add New Student")
        with st.form("add_student_form", clear_on_submit=True):
            new_s_name = st.text_input("Student Full Name:")
            new_s_user = st.text_input("Username:")
            new_s_pass = st.text_input("Password:", type="password")
            new_s_track = st.selectbox("Training Track:", ["Networking", "Cybersecurity", "Programming", "General"])
            
            submit_new_student = st.form_submit_button("Create Student Account")
            
            if submit_new_student:
                if new_s_name and new_s_user and new_s_pass:
                    df_u = pd.read_csv(users_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                    df_u.columns = df_u.columns.str.strip()
                    
                    if not df_u.empty and (df_u['username'].str.strip() == new_s_user.strip()).any():
                        st.error("Error: This username already exists in the system.")
                    else:
                        with open(users_db, mode="a", encoding="utf-8-sig", newline="") as f_app:
                            w_app = csv.writer(f_app)
                            w_app.writerow([new_s_name.strip(), new_s_user.strip(), new_s_pass.strip(), new_s_track])
                        st.success(f"تم اضافته بنجاح! Student account ({new_s_user}) created successfully.")
                else:
                    st.warning("Please fill in all mandatory fields.")

    with col_u2:
        st.subheader("📋 Registered Students Directory")
        if os.path.exists(users_db):
            df_u_show = pd.read_csv(users_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
            df_u_show.columns = df_u_show.columns.str.strip()
            if not df_u_show.empty:
                st.dataframe(df_u_show[['student_name', 'username', 'track']], use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.subheader("🗑️ Remove Account")
                del_username = st.selectbox("Select account to delete:", options=df_u_show['username'].tolist(), key="del_stu_select")
                if st.button("Delete Selected Account"):
                    df_filtered = df_u_show[df_u_show['username'].str.strip() != del_username.strip()]
                    df_filtered.to_csv(users_db, index=False, encoding="utf-8-sig")
                    st.success(f"Account ({del_username}) removed successfully!")
                    st.rerun()
            else:
                st.info("No student accounts registered yet.")

# 2. Attendance Tracking Section
elif admin_menu == "📅 Attendance Tracking":
    st.title("📅 Student Attendance Tracking")
    st.markdown("Record daily attendance linked precisely with lecture titles.")
    st.divider()

    att_db = "attendance.csv"
    if not os.path.exists(att_db):
        with open(att_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "lecture_title", "username", "student_name", "status"])

    users_db = "users.csv"
    if os.path.exists(users_db):
        df_u_att = pd.read_csv(users_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
        df_u_att.columns = df_u_att.columns.str.strip()

        if not df_u_att.empty:
            col_date, col_title = st.columns(2)
            with col_date:
                selected_date = st.date_input("Attendance Date:", value=datetime.now().date())
            with col_title:
                lecture_title_input = st.text_input("Lecture Title / Subject:")

            date_str = selected_date.strftime("%Y-%m-%d")

            st.markdown(f"**Session Overview:** `{date_str}` — `{lecture_title_input if lecture_title_input else 'General Session'}`")
            
            with st.form("attendance_form"):
                attendance_status = {}
                for idx, row in df_u_att.iterrows():
                    u_name = row.get('username')
                    s_name = row.get('student_name')
                    status = st.selectbox(f"👤 {s_name} ({u_name})", ["Not Marked", "Present", "Absent", "Late"], key=f"att_{u_name}")
                    if status != "Not Marked":
                        attendance_status[u_name] = {"student_name": s_name, "status": status}

                submit_att = st.form_submit_button("Save Attendance Records")

                if submit_att:
                    if not lecture_title_input.strip():
                        st.warning("Please provide the lecture title before saving.")
                    elif not attendance_status:
                        st.warning("Please mark at least one student's attendance.")
                    else:
                        att_records = []
                        if os.path.exists(att_db):
                            df_old_att = pd.read_csv(att_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                            df_old_att.columns = df_old_att.columns.str.strip()
                            for _, r in df_old_att.iterrows():
                                if not (str(r.get('date')) == date_str and str(r.get('lecture_title')) == lecture_title_input.strip()):
                                    att_records.append([r.get('date'), r.get('lecture_title'), r.get('username'), r.get('student_name'), r.get('status')])

                        for u_name, data in attendance_status.items():
                            att_records.append([date_str, lecture_title_input.strip(), u_name, data["student_name"], data["status"]])

                        with open(att_db, mode="w", encoding="utf-8-sig", newline="") as f_att:
                            w_att = csv.writer(f_att)
                            w_att.writerow(["date", "lecture_title", "username", "student_name", "status"])
                            w_att.writerows(att_records)

                        st.success(f"Attendance successfully recorded for {date_str}!")
                        st.rerun()

            st.markdown("---")
            st.subheader("📊 Past Attendance History")
            if os.path.exists(att_db):
                df_all_att = pd.read_csv(att_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                df_all_att.columns = df_all_att.columns.str.strip()
                if not df_all_att.empty:
                    st.dataframe(df_all_att, use_container_width=True, hide_index=True)
                else:
                    st.info("No historical attendance data recorded.")
        else:
            st.info("No students found in the database.")
    else:
        st.info("Users database file missing.")

# 3. Completed Training Section
elif admin_menu == "🎓 Completed Training":
    st.title("🎓 Completed Training / Alumni")
    st.markdown("Track graduates who have successfully completed their program milestones.")
    st.divider()

    completed_db = "completed_students.csv"
    if not os.path.exists(completed_db):
        with open(completed_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["student_name", "username", "track", "completion_date", "certificate_notes"])

    users_db = "users.csv"
    col_c1, col_c2 = st.columns([1, 1], gap="large")

    with col_c1:
        st.subheader("🏅 Graduate Student")
        if os.path.exists(users_db):
            df_u_comp = pd.read_csv(users_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
            df_u_comp.columns = df_u_comp.columns.str.strip()

            if not df_u_comp.empty:
                with st.form("complete_student_form"):
                    comp_username = st.selectbox("Select Student Username:", options=df_u_comp['username'].tolist(), key="comp_sel")
                    cert_notes = st.text_area("Completion Remarks / Certificate Notes:")
                    submit_comp = st.form_submit_button("Mark as Completed")

                    if submit_comp:
                        selected_row = df_u_comp[df_u_comp['username'].str.strip() == str(comp_username).strip()]
                        if not selected_row.empty:
                            s_name = selected_row.iloc[0].get('student_name')
                            s_track = selected_row.iloc[0].get('track')
                            comp_date = datetime.now().strftime("%Y-%m-%d")

                            with open(completed_db, mode="a", encoding="utf-8-sig", newline="") as f_comp:
                                w_comp = csv.writer(f_comp)
                                w_comp.writerow([s_name, comp_username, s_track, comp_date, cert_notes])

                            st.success(f"Student ({s_name}) successfully marked as graduated!")
                            st.rerun()
            else:
                st.info("No students available.")
        else:
            st.info("Users database not found.")

    with col_c2:
        st.subheader("🎓 Graduation List")
        if os.path.exists(completed_db):
            df_comp_show = pd.read_csv(completed_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
            df_comp_show.columns = df_comp_show.columns.str.strip()
            if not df_comp_show.empty:
                st.dataframe(df_comp_show[['student_name', 'username', 'track', 'completion_date']], use_container_width=True, hide_index=True)
            else:
                st.info("No graduated students recorded yet.")

# 4. Announcements Section
elif admin_menu == "📢 Post Announcements":
    st.title("📢 Post Academy Announcements")
    st.markdown("Broadcast important updates and news directly to student portals.")
    st.divider()

    ann_db = "announcements.csv"
    if not os.path.exists(ann_db):
        with open(ann_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["title", "content", "date", "image"])

    with st.form("announcement_form"):
        ann_title = st.text_input("Announcement Title:")
        ann_content = st.text_area("Announcement Details:")
        ann_image = st.file_uploader("Attach Image (Optional):", type=["jpg", "jpeg", "png"])
        
        submit_ann = st.form_submit_button("Publish Announcement")
        
        if submit_ann:
            if ann_title and ann_content:
                img_path_str = ""
                if ann_image is not None:
                    img_filename = f"ann_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{ann_image.name}"
                    img_path_str = os.path.join("uploads", img_filename)
                    with open(img_path_str, "wb") as img_f:
                        img_f.write(ann_image.getbuffer())
                
                ann_records = []
                if os.path.exists(ann_db):
                    df_old_ann = pd.read_csv(ann_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                    df_old_ann.columns = df_old_ann.columns.str.strip()
                    for _, r in df_old_ann.iterrows():
                        ann_records.append([r.get('title'), r.get('content'), r.get('date'), r.get('image')])
                
                ann_records.insert(0, [ann_title, ann_content, datetime.now().strftime("%Y-%m-%d %H:%M"), img_path_str])

                with open(ann_db, mode="w", encoding="utf-8-sig", newline="") as f_ann:
                    w_ann = csv.writer(f_ann)
                    w_ann.writerow(["title", "content", "date", "image"])
                    w_ann.writerows(ann_records)
                
                st.success("📢 Announcement published successfully!")
                st.rerun()
            else:
                st.warning("Please fill in both the title and content.")

# 5. Lectures Section
elif admin_menu == "📚 Upload Lectures":
    st.title("📚 Upload Lecture Materials")
    st.markdown("Share course files, slides, and resources with students.")
    st.divider()

    lec_db = "lectures.csv"
    if not os.path.exists(lec_db):
        with open(lec_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["track", "title", "file_path", "date"])

    with st.form("lecture_form"):
        lec_track = st.selectbox("Target Training Track:", ["Networking", "Cybersecurity", "Programming", "General"])
        lec_title = st.text_input("Lecture Subject / Title:")
        lec_file = st.file_uploader("Upload Lecture File:", type=["pdf", "pptx", "docx", "zip", "rar", "txt"])
        
        submit_lec = st.form_submit_button("Upload Resource")
        
        if submit_lec:
            if lec_title and lec_file is not None:
                lec_filename = f"lec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{lec_file.name}"
                lec_path_str = os.path.join("uploads", lec_filename)
                with open(lec_path_str, "wb") as lf:
                    lf.write(lec_file.getbuffer())
                
                with open(lec_db, mode="a", encoding="utf-8-sig", newline="") as f_lec:
                    w_lec = csv.writer(f_lec)
                    w_lec.writerow([lec_track, lec_title, lec_path_str, datetime.now().strftime("%Y-%m-%d %H:%M")])
                
                st.success("📚 Lecture file successfully uploaded!")
                st.rerun()
            else:
                st.warning("Please provide the lecture title and attach a file.")

# 6. Assignments Section
elif admin_menu == "📋 Add Assignments":
    st.title("📋 Publish Assignments")
    st.markdown("Create and assign tasks or assignments for student evaluation.")
    st.divider()

    asg_db = "assignments.csv"
    if not os.path.exists(asg_db):
        with open(asg_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["title", "deadline", "questions_file", "date"])

    with st.form("assignment_form"):
        asg_title = st.text_input("Assignment Title:")
        asg_deadline = st.text_input("Deadline (e.g., 2026-04-15):")
        asg_file = st.file_uploader("Upload Assignment Questions (PDF):", type=["pdf", "docx", "txt", "zip"])
        
        submit_asg = st.form_submit_button("Publish Assignment")
        
        if submit_asg:
            if asg_title and asg_file is not None:
                asg_filename = f"asg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{asg_file.name}"
                asg_path_str = os.path.join("uploads", asg_filename)
                with open(asg_path_str, "wb") as af:
                    af.write(asg_file.getbuffer())
                
                with open(asg_db, mode="a", encoding="utf-8-sig", newline="") as f_asg:
                    w_asg = csv.writer(f_asg)
                    w_asg.writerow([asg_title, asg_deadline, asg_path_str, datetime.now().strftime("%Y-%m-%d %H:%M")])
                
                st.success("📋 Assignment published successfully!")
                st.rerun()
            else:
                st.warning("Please enter the title and attach the questions file.")

# 7. Student Submissions Section
elif admin_menu == "📥 Student Submissions":
    st.title("📥 Review Student Submissions")
    st.markdown("Examine and download solutions uploaded by students.")
    st.divider()

    sub_db = "submissions.csv"
    if os.path.exists(sub_db):
        df_subs = pd.read_csv(sub_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
        df_subs.columns = df_subs.columns.str.strip()
        if not df_subs.empty:
            for index, row in df_subs.iterrows():
                st.markdown(f"""
                    <div style="background: white; padding: 15px; border-radius: 10px; border-left: 4px solid #4f46e5; margin-bottom: 10px;">
                        <h4 style="margin: 0; color: #111827;">👤 {row.get('student_name')} ({row.get('username')})</h4>
                        <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 13px;"><b>Assignment:</b> {row.get('assignment_title')} &nbsp;|&nbsp; <b>Submitted:</b> {row.get('date')}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                sol_file = row.get('solution_file')
                if pd.notna(sol_file) and isinstance(sol_file, str) and os.path.exists(sol_file):
                    with open(sol_file, "rb") as sf:
                        st.download_button(
                            label=f"📥 Download Solution File",
                            data=sf,
                            file_name=os.path.basename(sol_file),
                            key=f"dl_sub_{index}"
                        )
                st.write("")
        else:
            st.info("No student submissions received yet.")
    else:
        st.info("Submissions database not found.")

# 8. Student Evaluation & Notes Section
elif admin_menu == "⭐ Student Evaluation & Notes":
    st.title("⭐ Student Performance & Evaluation")
    st.markdown("Update academic grades and leave constructive feedback for individual students.")
    st.divider()

    users_db = "users.csv"
    if os.path.exists(users_db):
        df_u_eval = pd.read_csv(users_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
        df_u_eval.columns = df_u_eval.columns.str.strip()
        
        if not df_u_eval.empty:
            selected_student_user = st.selectbox("Select Student Profile:", options=df_u_eval['username'].tolist(), key="eval_stu_select")
            
            profile_db = "profiles.csv"
            if not os.path.exists(profile_db):
                with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["username", "avatar", "evaluation", "notes"])

            df_p_eval = pd.read_csv(profile_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
            df_p_eval.columns = df_p_eval.columns.str.strip()
            
            student_prof_row = df_p_eval[df_p_eval['username'].str.strip() == str(selected_student_user)]
            
            current_stu_avatar = ""
            current_stu_eval = "Excellent"
            current_stu_notes = ""
            
            if not student_prof_row.empty:
                current_stu_avatar = str(student_prof_row.iloc[0].get('avatar', ''))
                val_e = str(student_prof_row.iloc[0].get('evaluation', ''))
                if val_e != "nan" and val_e.strip() != "":
                    current_stu_eval = val_e
                val_n = str(student_prof_row.iloc[0].get('notes', ''))
                if val_n != "nan":
                    current_stu_notes = val_n

            with st.form("eval_form"):
                eval_options = ["Excellent", "Very Good", "Good", "Needs Improvement"]
                default_idx = eval_options.index(current_stu_eval) if current_stu_eval in eval_options else 0
                
                new_eval = st.selectbox("Academic Evaluation Status:", options=eval_options, index=default_idx)
                new_notes = st.text_area("Corrective Notes / Instructor Feedback:", value=current_stu_notes)
                
                submit_eval = st.form_submit_button("Save Evaluation")
                
                if submit_eval:
                    profiles_records = []
                    if os.path.exists(profile_db):
                        df_p_old = pd.read_csv(profile_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                        df_p_old.columns = df_p_old.columns.str.strip()
                        for _, r in df_p_old.iterrows():
                            if str(r.get('username')).strip() != str(selected_student_user):
                                profiles_records.append([r.get('username'), r.get('avatar'), r.get('evaluation'), r.get('notes')])
                    
                    profiles_records.append([str(selected_student_user), current_stu_avatar, new_eval, new_notes])
                    
                    with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f_p:
                        w_p = csv.writer(f_p)
                        w_p.writerow(["username", "avatar", "evaluation", "notes"])
                        w_p.writerows(profiles_records)
                    
                    st.success(f"Evaluation updated successfully for student ({selected_student_user})!")
                    st.rerun()
        else:
            st.info("No students available for evaluation.")
    else:
        st.info("No student accounts registered yet.")
