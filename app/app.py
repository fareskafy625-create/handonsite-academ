import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Student Portal - HandsOnSite Academy", page_icon="💻", layout="wide")

# Custom CSS Styling (UI Enhancements for a Professional Look)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    
    /* Global Card styling */
    .css-1r6slb0, .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Custom Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        height: 45px;
        background-color: #ffffff;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
        margin-bottom: 6px;
        text-align: left;
        padding-left: 16px;
    }
    div.stButton > button:hover { 
        background-color: #0f172a; 
        color: white; 
        border-color: #0f172a;
        transform: translateY(-1px);
    }
    
    /* Sidebar styling enhancements */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Success / Info box styling */
    .stSuccess {
        background-color: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        color: #166534 !important;
    }
    </style>
""", unsafe_allow_html=True)

os.makedirs("uploads", exist_ok=True)

# Login System
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.3, 1])
    
    with col2:
        st.markdown("""
            <div style="background: white; padding: 35px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; text-align: center; margin-bottom: 20px;">
                <h2 style="color: #0f172a; margin-bottom: 8px; font-weight: 700;">💻 HandsOnSite Academy</h2>
                <p style="color: #64748b; font-size: 14px; margin: 0;">Student Portal Secure Login</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("🔒 **Please enter your account credentials**")
            username = st.text_input("Username:")
            password = st.text_input("Password:", type="password")
            
            submit_login = st.form_submit_button("Login to Portal")
            
            if submit_login:
                if username and password:
                    if os.path.exists("users.csv"):
                        try:
                            df_users = pd.read_csv("users.csv", encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                            df_users.columns = df_users.columns.str.strip()
                            
                            user_match = df_users[
                                (df_users['username'].str.strip() == username.strip()) & 
                                (df_users['password'].str.strip() == password.strip())
                            ]
                            
                            if not user_match.empty:
                                st.session_state.logged_in = True
                                st.session_state.username = username.strip()
                                st.session_state.current_user = user_match.iloc[0]['student_name']
                                st.session_state.user_track = user_match.iloc[0]['track']
                                st.session_state.active_page = "📢 Announcements"
                                st.success("Logged in successfully! Redirecting...")
                                st.rerun()
                            else:
                                st.error("Error: Incorrect username or password.")
                        except Exception as e:
                            st.error(f"Error reading users database: {e}")
                    else:
                        st.error("No active accounts found in the system. Please contact the administrator.")
                else:
                    st.warning("Please enter both username and password.")
    st.stop()

if 'active_page' not in st.session_state:
    st.session_state.active_page = "📢 Announcements"

# Read Profile Data
profile_db = "profiles.csv"
if not os.path.exists(profile_db):
    with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["username", "avatar", "evaluation", "notes"])

df_prof = pd.read_csv(profile_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
df_prof.columns = df_prof.columns.str.strip()
user_prof_row = df_prof[df_prof['username'].str.strip() == str(st.session_state.username)]

current_avatar = ""
current_eval = "Excellent"
improvement_notes = "No corrective notes at the moment. Keep up the great work!"
if not user_prof_row.empty:
    current_avatar = str(user_prof_row.iloc[0].get('avatar', ''))
    val_eval = str(user_prof_row.iloc[0].get('evaluation', ''))
    if val_eval != "nan" and val_eval.strip() != "":
        current_eval = val_eval
    val_notes = str(user_prof_row.iloc[0].get('notes', ''))
    if val_notes != "nan" and val_notes.strip() != "":
        improvement_notes = val_notes

# Sidebar Navigation
if pd.notna(current_avatar) and os.path.exists(current_avatar):
    st.sidebar.image(current_avatar, width=110)

st.sidebar.markdown(f"### Welcome, {st.session_state.get('current_user', 'Student')} 👋")
st.sidebar.markdown(f"**Track:** <span style='color: #0d6efd;'>{st.session_state.get('user_track', 'General')}</span>", unsafe_allow_html=True)
st.sidebar.divider()

st.sidebar.markdown("### 🎛️ Navigation Menu")

if st.sidebar.button("📢 Announcements"):
    st.session_state.active_page = "📢 Announcements"
    st.rerun()

if st.sidebar.button("📚 Lectures & Resources"):
    st.session_state.active_page = "📚 Lectures & Resources"
    st.rerun()

if st.sidebar.button("📋 Assignments"):
    st.session_state.active_page = "📋 Assignments"
    st.rerun()

if st.sidebar.button("⚙️ Profile & Evaluation"):
    st.session_state.active_page = "⚙️ Profile & Evaluation"
    st.rerun()

st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

menu = st.session_state.active_page

# 1. Announcements Section
if menu == "📢 Announcements":
    st.title("📢 HandsOnSite Academy Announcements")
    st.markdown("Stay updated with the latest news and important announcements regarding your training track.")
    st.divider()
    
    if os.path.exists("announcements.csv"):
        try:
            df_an = pd.read_csv("announcements.csv", encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
            df_an.columns = df_an.columns.str.strip()
            if not df_an.empty:
                for index, row in df_an.iterrows():
                    st.info(f"### 📌 {row.get('title', '')}\n\n{row.get('content', '')}\n\n*Published Date: {row.get('date', '')}*")
                    img_path = row.get('image')
                    if pd.notna(img_path) and isinstance(img_path, str) and os.path.exists(img_path):
                        st.image(img_path, width=350)
                    st.write("---")
            else:
                st.info("No announcements published yet.")
        except Exception:
            st.info("Updating announcements...")
    else:
        st.info("No announcements available.")

# 2. Lectures Section
elif menu == "📚 Lectures & Resources":
    st.title("📚 Lectures & Study Resources")
    st.markdown("Download lecture materials and resources for your sessions.")
    st.divider()
    
    if os.path.exists("lectures.csv"):
        try:
            df_lec = pd.read_csv("lectures.csv", encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
            df_lec.columns = df_lec.columns.str.strip()
            if not df_lec.empty:
                for index, row in df_lec.iterrows():
                    st.write(f"- **Track:** {row.get('track')} | **Lecture:** {row.get('title')}")
                    file_path = row.get('file_path')
                    if pd.notna(file_path) and isinstance(file_path, str) and os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 Download Lecture File",
                                data=f,
                                file_name=os.path.basename(file_path),
                                key=f"lec_dl_{index}"
                            )
                    st.write("---")
            else:
                st.info("No lectures uploaded yet.")
        except Exception:
            st.info("No lectures available at the moment.")
    else:
        st.info("No lecture files added yet.")

# 3. Assignments Section
elif menu == "📋 Assignments":
    st.title("📋 Available Assignments & Tasks")
    st.markdown("View your assignments, download the questions file, and submit your solutions easily.")
    st.divider()
    
    if os.path.exists("assignments.csv"):
        try:
            df_asg = pd.read_csv("assignments.csv", encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
            df_asg.columns = df_asg.columns.str.strip()
            
            submitted_asgs = []
            sub_db = "submissions.csv"
            if os.path.exists(sub_db):
                df_subs_check = pd.read_csv(sub_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                df_subs_check.columns = df_subs_check.columns.str.strip()
                my_subs = df_subs_check[df_subs_check['username'].str.strip() == str(st.session_state.username)]
                submitted_asgs = my_subs['assignment_title'].str.strip().tolist()

            if not df_asg.empty:
                for index, row in df_asg.iterrows():
                    asg_title = str(row.get('title', '')).strip()
                    asg_date = row.get('date', '')
                    asg_deadline = row.get('deadline', 'Not specified')
                    asg_file = row.get('questions_file')

                    is_submitted = asg_title in submitted_asgs

                    with st.expander(f"📌 Assignment: {asg_title} {' | (✔️ Submitted)' if is_submitted else ' | (⚠️ Pending Submission)'}"):
                        
                        col_info1, col_info2 = st.columns([2, 1])
                        with col_info1:
                            st.markdown(f"**⏰ Deadline:** <span style='color: #dc3545;'>{asg_deadline}</span>", unsafe_allow_html=True)
                            st.caption(f"Published Date: {asg_date}")
                        with col_info2:
                            if is_submitted:
                                st.success("✔️ Submitted")
                            else:
                                st.warning("⚠️ Pending")

                        st.markdown("---")

                        if pd.notna(asg_file) and isinstance(asg_file, str) and os.path.exists(asg_file):
                            with open(asg_file, "rb") as af:
                                st.download_button(
                                    label="📥 Download Assignment Questions (PDF)",
                                    data=af,
                                    file_name=os.path.basename(asg_file),
                                    key=f"dl_asg_{index}"
                                )
                        
                        with st.form(f"submit_form_{index}"):
                            uploaded_ans = st.file_uploader("📤 Upload Assignment Solution File:", type=["pdf", "png", "jpg", "zip", "rar", "pkt", "txt"], key=f"ans_{index}")
                            submit_ans = st.form_submit_button("Submit Solution to Admin")
                            
                            if submit_ans:
                                if uploaded_ans is not None:
                                    ans_filename = f"sub_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_ans.name}"
                                    ans_path_str = os.path.join("uploads", ans_filename)
                                    with open(ans_path_str, "wb") as sf:
                                        sf.write(uploaded_ans.getbuffer())
                                    
                                    sub_exists = os.path.exists(sub_db)
                                    sub_records = []
                                    if sub_exists:
                                        df_s_old = pd.read_csv(sub_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                                        df_s_old.columns = df_s_old.columns.str.strip()
                                        for _, r in df_s_old.iterrows():
                                            if not (str(r.get('username')).strip() == str(st.session_state.username) and str(r.get('assignment_title')).strip() == asg_title):
                                                sub_records.append([r.get('student_name'), r.get('username'), r.get('assignment_title'), r.get('solution_file'), r.get('date')])
                                    
                                    sub_records.append([st.session_state.current_user, st.session_state.username, asg_title, ans_path_str, datetime.now().strftime("%Y-%m-%d %H:%M")])

                                    with open(sub_db, mode="w", encoding="utf-8-sig", newline="") as sf_csv:
                                        w = csv.writer(sf_csv)
                                        w.writerow(["student_name", "username", "assignment_title", "solution_file", "date"])
                                        w.writerows(sub_records)
                                    
                                    st.success("🎉 Assignment solution uploaded and submitted successfully!")
                                    st.rerun()
                                else:
                                    st.warning("Please choose a solution file before clicking submit.")
            else:
                st.info("No assignments published yet by the admin.")
        except Exception as e:
            st.error(f"Error reading assignments: {e}")
    else:
        st.info("No assignment files registered currently.")

# 4. Profile Section
elif menu == "⚙️ Profile & Evaluation":
    st.title("⚙️ Profile & Performance Evaluation")
    st.markdown("Here you can update your username, password, profile picture, and view your evaluation and instructor guidance.")
    st.divider()
    
    # Check if there's a stored success message to display
    if 'profile_success_msg' in st.session_state:
        st.success(st.session_state.profile_success_msg)
        del st.session_state.profile_success_msg

    col_p1, col_p2 = st.columns([1, 2])
    
    with col_p1:
        st.subheader("🖼️ Your Profile Picture")
        if pd.notna(current_avatar) and os.path.exists(current_avatar):
            st.image(current_avatar, width=180, caption="Current Picture")
        else:
            st.info("You haven't uploaded a profile picture yet.")
            
        st.markdown("---")
        st.subheader("⭐ Academic Evaluation")
        st.metric(label="General Evaluation Status", value=current_eval)
        
        st.markdown(f"""
            <div style="background-color: #fffbeb; padding: 16px; border-radius: 8px; border-left: 4px solid #f59e0b; margin-top: 15px;">
                <h4 style="color: #b45309; margin-top: 0; font-size: 15px;">📌 Instructor Feedback & Notes:</h4>
                <p style="color: #92400e; font-size: 14px; line-height: 1.5; margin-bottom: 0;">{improvement_notes}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.subheader("✏️ Edit Username & Password")
        
        with st.form("update_profile_form", clear_on_submit=True):
            new_name_input = st.text_input("New Username:")
            new_password_input = st.text_input("New Password (leave blank if unchanged):", type="password")
            new_avatar_file = st.file_uploader("Choose a new profile picture (JPG/PNG):", type=["jpg", "jpeg", "png"])
            
            submit_update = st.form_submit_button("Save All Changes")
            
            if submit_update:
                if new_name_input.strip() or new_password_input.strip() or new_avatar_file is not None:
                    saved_avatar_path = current_avatar
                    if new_avatar_file is not None:
                        avatar_filename = f"avatar_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{new_avatar_file.name}"
                        saved_avatar_path = os.path.join("uploads", avatar_filename)
                        with open(saved_avatar_path, "wb") as av_f:
                            av_f.write(new_avatar_file.getbuffer())
                    
                    old_username = str(st.session_state.username).strip()
                    new_username = str(new_name_input).strip() if new_name_input.strip() else old_username
                    
                    # Update users.csv
                    if os.path.exists("users.csv"):
                        df_u = pd.read_csv("users.csv", encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                        df_u.columns = df_u.columns.str.strip()
                        
                        mask = df_u['username'].str.strip() == old_username
                        
                        if mask.any():
                            df_u['password'] = df_u['password'].astype(str)
                            df_u['student_name'] = df_u['student_name'].astype(str)
                            df_u['username'] = df_u['username'].astype(str)
                            
                            if new_name_input.strip():
                                df_u.loc[mask, 'username'] = new_username
                                df_u.loc[mask, 'student_name'] = new_username
                                st.session_state.username = new_username
                                st.session_state.current_user = new_username
                                
                            if new_password_input.strip():
                                df_u.loc[mask, 'password'] = str(new_password_input).strip()
                                
                            df_u.to_csv("users.csv", index=False, encoding="utf-8-sig")
                    
                    # Update profiles.csv
                    profiles_list = []
                    if os.path.exists(profile_db):
                        df_p_old = pd.read_csv(profile_db, encoding="utf-8-sig", dtype=str, on_bad_lines="skip")
                        df_p_old.columns = df_p_old.columns.str.strip()
                        for _, r in df_p_old.iterrows():
                            if str(r.get('username')).strip() != old_username:
                                profiles_list.append([r.get('username'), r.get('avatar'), r.get('evaluation'), r.get('notes')])
                    
                    profiles_list.append([st.session_state.username, saved_avatar_path, current_eval, improvement_notes])
                    
                    with open(profile_db, mode="w", encoding="utf-8-sig", newline="") as f_p:
                        w_p = csv.writer(f_p)
                        w_p.writerow(["username", "avatar", "evaluation", "notes"])
                        w_p.writerows(profiles_list)
                    
                    # Set success message in session state and reload
                    st.session_state.profile_success_msg = "Successfully updated!"
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter the data you want to modify first.")
