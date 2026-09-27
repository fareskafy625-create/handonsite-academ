import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Admin Panel - HandsOnSite Academy", page_icon="⚙️", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        height: 45px;
        background-color: #ffffff;
        color: #dc3545;
        border: 2px solid #dc3545;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        margin-bottom: 8px;
        text-align: left;
        padding-left: 15px;
    }
    div.stButton > button:hover { 
        background-color: #dc3545; 
        color: white; 
        border-color: #dc3545;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

os.makedirs("uploads", exist_ok=True)

# Admin Login System
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #dc3545; margin-bottom: 5px;">🛡️ HandsOnSite Academy</h2>
                <p style="color: #6c757d; font-size: 15px;">Admin Dashboard Login</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login_form"):
            st.markdown("🔒 **Please enter admin credentials**")
            admin_user = st.text_input("Admin Username:")
            admin_pass = st.text_input("Password:", type="password")
            
            submit_admin_login = st.form_submit_button("Login to Dashboard")
            
            if submit_admin_login:
                # Default admin credentials (you can change them)
                if admin_user == "admin" and admin_pass == "admin123":
                    st.session_state.admin_logged_in = True
                    st.success("Logged in successfully to Admin Panel!")
                    st.rerun()
                else:
                    st.error("Error: Incorrect admin username or password.")
    st.stop()

if 'admin_page' not in st.session_state:
    st.session_state.admin_page = "👥 Manage Students"

# Sidebar Navigation for Admin
st.sidebar.markdown("### 🛡️ Admin Dashboard")
st.sidebar.divider()
st.sidebar.markdown("### 🎛️ Control Panel:")

if st.sidebar.button("👥 Manage Students"):
    st.session_state.admin_page = "👥 Manage Students"
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

if st.sidebar.button("🚪 Logout"):
    st.session_state.admin_logged_in = False
    st.rerun()

admin_menu = st.session_state.admin_page

# 1. Manage Students Section
if admin_menu == "👥 Manage Students":
    st.title("👥 Student Accounts Management")
    st.markdown("Add new students, view existing student accounts, or delete accounts.")
    st.divider()

    users_db = "users.csv"
    if not os.path.exists(users_db):
        with open(users_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["student_name", "username", "password", "track"])

    col_u1, col_u2 = st.columns([1, 1])

    with col_u1:
        st.subheader("➕ Add New Student")
        with st.form("add_student_form"):
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
                        st.error("Error: This username already exists. Please choose another one.")
                    else:
                        with open(users_db, mode="a", encoding="utf-8-sig", newline="") as f_app:
                            w_app = csv.writer(f_app)
                            w_app.writerow([new_s_name.strip(), new_s_user.strip(), new_s_pass.strip(), new_s_track])
                        st.success(f"Student account ({new_s_user}) created successfully!")
                        st.rerun()
                else:
                    st.warning("Please fill in all required fields.")

    with col_u2:
        st.subheader("📋 Registered Students List")
        if os.path.exists(users_db):
            df_u_show = pd.read_csv(users_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
            df_u_show.columns = df_u_show.columns.str.strip()
            if not df_u_show.empty:
                st.dataframe(df_u_show[['student_name', 'username', 'track']], use_container_width=True)
                
                st.markdown("---")
                st.subheader("🗑️ Delete Student Account")
                del_username = st.selectbox("Select username to delete:", options=df_u_show['username'].tolist())
                if st.button("Delete Selected Account"):
                    df_filtered = df_u_show[df_u_show['username'].str.strip() != del_username.strip()]
                    df_filtered.to_csv(users_db, index=False, encoding="utf-8-sig")
                    st.success(f"Account ({del_username}) deleted successfully!")
                    st.rerun()
            else:
                st.info("No student accounts registered yet.")

# 2. Announcements Section
elif admin_menu == "📢 Post Announcements":
    st.title("📢 Post Academy Announcements")
    st.markdown("Publish important news and announcements for students.")
    st.divider()

    ann_db = "announcements.csv"
    if not os.path.exists(ann_db):
        with open(ann_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["title", "content", "date", "image"])

    with st.form("announcement_form"):
        ann_title = st.text_input("Announcement Title:")
        ann_content = st.text_area("Announcement Details / Content:")
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
                st.warning("Please enter both the announcement title and content.")

# 3. Lectures Section
elif admin_menu == "📚 Upload Lectures":
    st.title("📚 Upload Lecture Files")
    st.markdown("Upload lecture files and resources for students to download.")
    st.divider()

    lec_db = "lectures.csv"
    if not os.path.exists(lec_db):
        with open(lec_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["track", "title", "file_path", "date"])

    with st.form("lecture_form"):
        lec_track = st.selectbox("Target Training Track:", ["Networking", "Cybersecurity", "Programming", "General"])
        lec_title = st.text_input("Lecture Title / Subject:")
        lec_file = st.file_uploader("Upload Lecture File (PDF, PPTX, ZIP, etc.):", type=["pdf", "pptx", "docx", "zip", "rar", "txt"])
        
        submit_lec = st.form_submit_button("Upload Lecture")
        
        if submit_lec:
            if lec_title and lec_file is not None:
                lec_filename = f"lec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{lec_file.name}"
                lec_path_str = os.path.join("uploads", lec_filename)
                with open(lec_path_str, "wb") as lf:
                    lf.write(lec_file.getbuffer())
                
                with open(lec_db, mode="a", encoding="utf-8-sig", newline="") as f_lec:
                    w_lec = csv.writer(f_lec)
                    w_lec.writerow([lec_track, lec_title, lec_path_str, datetime.now().strftime("%Y-%m-%d %H:%M")])
                
                st.success("📚 Lecture file uploaded successfully!")
                st.rerun()
            else:
                st.warning("Please enter the lecture title and select a file to upload.")

# 4. Assignments Section
elif admin_menu == "📋 Add Assignments":
    st.title("📋 Create & Add Assignments")
    st.markdown("Publish new assignments and tasks for students.")
    st.divider()

    asg_db = "assignments.csv"
    if not os.path.exists(asg_db):
        with open(asg_db, mode="w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["title", "deadline", "questions_file", "date"])

    with st.form("assignment_form"):
        asg_title = st.text_input("Assignment Title:")
        asg_deadline = st.text_input("Deadline (e.g., 2026-04-10 or Next Thursday):")
        asg_file = st.file_uploader("Upload Assignment Questions File (PDF):", type=["pdf", "docx", "txt", "zip"])
        
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
                st.warning("Please enter the assignment title and upload the questions file.")

# 5. Student Submissions Section
elif admin_menu == "📥 Student Submissions":
    st.title("📥 Review Student Submissions")
    st.markdown("Review and download solutions submitted by students.")
    st.divider()

    sub_db = "submissions.csv"
    if os.path.exists(sub_db):
        df_subs = pd.read_csv(sub_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
        df_subs.columns = df_subs.columns.str.strip()
        if not df_subs.empty:
            for index, row in df_subs.iterrows():
                st.write(f"### 👤 Student: {row.get('student_name')} ({row.get('username')})")
                st.write(f"**Assignment:** {row.get('assignment_title')} | **Submission Date:** {row.get('date')}")
                
                sol_file = row.get('solution_file')
                if pd.notna(sol_file) and isinstance(sol_file, str) and os.path.exists(sol_file):
                    with open(sol_file, "rb") as sf:
                        st.download_button(
                            label=f"📥 Download Solution ({os.path.basename(sol_file)})",
                            data=sf,
                            file_name=os.path.basename(sol_file),
                            key=f"dl_sub_{index}"
                        )
                st.write("---")
        else:
            st.info("No submissions received from students yet.")
    else:
        st.info("No submissions database found.")

# 6. Student Evaluation & Notes Section
elif admin_menu == "⭐ Student Evaluation & Notes":
    st.title("⭐ Student Evaluation & Instructor Notes")
    st.markdown("Update academic evaluation and write corrective notes for students.")
    st.divider()

    users_db = "users.csv"
    if os.path.exists(users_db):
        df_u_eval = pd.read_csv(users_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
        df_u_eval.columns = df_u_eval.columns.str.strip()
        
        if not df_u_eval.empty:
            selected_student_user = st.selectbox("Select Student:", options=df_u_eval['username'].tolist())
            
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
                
                submit_eval = st.form_submit_button("Save Student Evaluation")
                
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
                    
                    st.success(f"Evaluation and notes updated successfully for student ({selected_student_user})!")
                    st.rerun()
        else:
            st.info("No students available to evaluate.")
    else:
        st.info("No student accounts registered yet.")
