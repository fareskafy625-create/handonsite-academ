import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="HandsOnSite - لوحة تحكم الأدمن", layout="wide")

# ملفات حفظ البيانات
ADMINS_FILE = "admins.csv"
STUDENTS_FILE = "students.csv"
GRADUATES_FILE = "graduates.csv"

# --- التحقق من صحة الملفات والأعمدة وتحديثها تلقائياً لتجنب KeyError ---
if os.path.exists(ADMINS_FILE):
    try:
        df_check = pd.read_csv(ADMINS_FILE)
        if not all(col in df_check.columns for col, type in [("username", str), ("password", str), ("name", str), ("avatar", str)]):
            raise Exception("Missing columns")
    except:
        os.remove(ADMINS_FILE)

if not os.path.exists(ADMINS_FILE):
    df_default_admin = pd.DataFrame([
        {"username": "admin", "password": "123", "name": "المدير الرئيسي", "avatar": ""}
    ])
    df_default_admin.to_csv(ADMINS_FILE, index=False)

if os.path.exists(STUDENTS_FILE):
    try:
        df_check = pd.read_csv(STUDENTS_FILE)
        if not all(col in df_check.columns for col in ["name", "email", "phone", "diploma", "status"]):
            raise Exception("Missing columns")
    except:
        os.remove(STUDENTS_FILE)

if not os.path.exists(STUDENTS_FILE):
    pd.DataFrame(columns=["name", "email", "phone", "diploma", "status"]).to_csv(STUDENTS_FILE, index=False)

if os.path.exists(GRADUATES_FILE):
    try:
        df_check = pd.read_csv(GRADUATES_FILE)
        if not all(col in df_check.columns for col in ["name", "email", "phone", "diploma", "graduation_date"]):
            raise Exception("Missing columns")
    except:
        os.remove(GRADUATES_FILE)

if not os.path.exists(GRADUATES_FILE):
    pd.DataFrame(columns=["name", "email", "phone", "diploma", "graduation_date"]).to_csv(GRADUATES_FILE, index=False)

# إدارة حالة تسجيل الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- نظام تسجيل الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 تسجيل دخول لوحة تحكم الأدمن")
    admins_df = pd.read_csv(ADMINS_FILE)
    
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    
    if st.button("دخول"):
        user = admins_df[(admins_df["username"] == username) & (admins_df["password"] == password)]
        if not user.empty:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("تم تسجيل الدخول بنجاح!")
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
else:
    # --- القائمة الجانبية ---
    st.sidebar.title(f"مرحباً، {st.session_state.username}")
    menu = st.sidebar.radio("القائمة الرئيسية", [
        "إدارة الطلاب الحاليين", 
        "خريجو الدبلومات (الأرشيف)", 
        "إدارة حسابات الأدمن", 
        "إعدادات الحساب الشخصي"
    ])
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # --- 1. إدارة الطلاب الحاليين ---
    if menu == "إدارة الطلاب الحاليين":
        st.header("👨‍🎓 إدارة الطلاب والمتدربين")
        students_df = pd.read_csv(STUDENTS_FILE)
        
        with st.form("add_student_form"):
            st.subheader("إضافة طالب جديد")
            s_name = st.text_input("اسم الطالب")
            s_email = st.text_input("البريد الإلكتروني")
            s_phone = st.text_input("رقم الهاتف")
            s_diploma = st.text_input("اسم الدبلومة")
            submit_student = st.form_submit_button("إضافة الطالب")
            
            if submit_student and s_name:
                new_row = pd.DataFrame([{"name": s_name, "email": s_email, "phone": s_phone, "diploma": s_diploma, "status": "قيد الدراسة"}])
                students_df = pd.concat([students_df, new_row], ignore_index=True)
                students_df.to_csv(STUDENTS_FILE, index=False)
                st.success(f"تم إضافة الطالب {s_name} بنجاح!")
                st.rerun()

        st.subheader("قائمة الطلاب الحاليين ونقلهم للخريجين")
        if not students_df.empty:
            for idx, row in students_df.iterrows():
                col1, col2, col3 = st.columns([3, 2, 2])
                col1.write(f"**{row['name']}** - {row['diploma']}")
                
                # زر تخرج الطالب ونقله للأرشيف
                if col2.button(f"تخرج / نقل للأرشيف", key=f"grad_{idx}"):
                    grads_df = pd.read_csv(GRADUATES_FILE)
                    new_grad = pd.DataFrame([{
                        "name": row["name"], 
                        "email": row["email"], 
                        "phone": row["phone"], 
                        "diploma": row["diploma"], 
                        "graduation_date": pd.Timestamp.now().strftime("%Y-%m-%d")
                    }])
                    grads_df = pd.concat([grads_df, new_grad], ignore_index=True)
                    grads_df.to_csv(GRADUATES_FILE, index=False)
                    
                    # حذف الطالب من قائمة الحاليين
                    students_df = students_df.drop(idx)
                    students_df.to_csv(STUDENTS_FILE, index=False)
                    st.success(f"تم نقل الطالب {row['name']} إلى قائمة الخريجين بنجاح!")
                    st.rerun()
        else:
            st.info("لا يوجد طلاب مسجلين حالياً.")

    # --- 2. خريجو الدبلومات (الأرشيف) ---
    elif menu == "خريجو الدبلومات (الأرشيف)":
        st.header("🏆 أرشيف الخريجين")
        grads_df = pd.read_csv(GRADUATES_FILE)
        
        if not grads_df.empty:
            search_query = st.text_input("بحث عن خريج (بالاسم أو الدبلومة):")
            if search_query:
                grads_df = grads_df[grads_df['name'].str.contains(search_query, na=False) | grads_df['diploma'].str.contains(search_query, na=False)]
            
            st.dataframe(grads_df, use_container_width=True)
            
            # زر لتحميل البيانات كملف CSV
            csv_data = grads_df.to_csv(index=False).encode('utf-8')
            st.download_button("تحميل قائمة الخريجين (CSV)", data=csv_data, file_name="graduates.csv", mime="text/csv")
        else:
            st.info("لا يوجد خريجون مسجلون حتى الآن.")

    # --- 3. إدارة حسابات الأدمن ---
    elif menu == "إدارة حسابات الأدمن":
        st.header("👥 إدارة حسابات المشرفين (Admins)")
        admins_df = pd.read_csv(ADMINS_FILE)
        
        with st.form("new_admin_form"):
            st.subheader("إضافة أدمن جديد")
            new_adm_user = st.text_input("اسم المستخدم للأدمن الجديد")
            new_adm_pass = st.text_input("كلمة المرور", type="password")
            new_adm_name = st.text_input("الاسم الكامل")
            submit_adm = st.form_submit_button("إنشاء حساب الأدمن")
            
            if submit_adm and new_adm_user and new_adm_pass:
                if new_adm_user in admins_df["username"].values:
                    st.warning("اسم المستخدم موجود مسبقاً!")
                else:
                    new_row = pd.DataFrame([{"username": new_adm_user, "password": new_adm_pass, "name": new_adm_name, "avatar": ""}])
                    admins_df = pd.concat([admins_df, new_row], ignore_index=True)
                    admins_df.to_csv(ADMINS_FILE, index=False)
                    st.success(f"تم إنشاء حساب الأدمن {new_adm_user} بنجاح!")
                    st.rerun()
                    
        st.subheader("المشرفون الحاليون في النظام:")
        st.dataframe(admins_df[["username", "name"]], use_container_width=True)

    # --- 4. إعدادات الحساب الشخصي ---
    elif menu == "إعدادات الحساب الشخصي":
        st.header("⚙️ إعدادات الحساب وتغيير البيانات")
        admins_df = pd.read_csv(ADMINS_FILE)
        
        current_admin_idx = admins_df.index[admins_df["username"] == st.session_state.username][0]
        current_data = admins_df.loc[current_admin_idx]
        
        with st.form("update_profile"):
            st.subheader("تعديل بياناتك الشخصية")
            new_name = st.text_input("الاسم الكامل", value=current_data["name"])
            new_password = st.text_input("كلمة المرور الجديدة (اتركها فارغة لو لا تريد تغييرها)", type="password")
            
            uploaded_avatar = st.file_uploader("رفع صورة شخصية (Avatar)", type=["png", "jpg", "jpeg"])
            
            submit_update = st.form_submit_button("حفظ التعديلات")
            
            if submit_update:
                admins_df.loc[current_admin_idx, "name"] = new_name
                if new_password:
                    admins_df.loc[current_admin_idx, "password"] = new_password
                
                if uploaded_avatar is not None:
                    avatar_path = f"avatar_{st.session_state.username}.png"
                    with open(avatar_path, "wb") as f:
                        f.write(uploaded_avatar.getbuffer())
                    admins_df.loc[current_admin_idx, "avatar"] = avatar_path
                    
                admins_df.to_csv(ADMINS_FILE, index=False)
                st.success("تم تحديث بيانات الحساب بنجاح!")
                st.rerun()
