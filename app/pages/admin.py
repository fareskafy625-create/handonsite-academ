from datetime import datetime
import os
import csv
import pandas as pd
import streamlit as st

# إعدادات صفحة الأدمن
st.set_page_config(
    page_title='تسجيل دخول الأدمن - أكاديمية HandsOnSite',
    page_icon='👨‍💻',
    layout='wide',
)

# تصميم CSS مخصص لتجميل شكل لوحة التحكم
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

os.makedirs('uploads', exist_ok=True)

# ملفات النظام
admins_db = 'admins.csv'
admin_logs_db = 'admin_logs.csv'
users_db = 'users.csv'
profile_db = 'profiles.csv'
announcements_db = 'announcements.csv'
lectures_db = 'lectures.csv'
assignments_db = 'assignments.csv'
submissions_db = 'submissions.csv'
attendance_db = 'attendance.csv'
groups_schedule_db = 'groups_schedule.csv'


# دالة تسجيل نشاطات الأدمن (Audit Trail)
def log_admin_action(admin_username, action_type, details):
  try:
    file_exists = os.path.exists(admin_logs_db)
    with open(admin_logs_db, mode='a', encoding='utf-8-sig', newline='') as f:
      w = csv.writer(f)
      if not file_exists:
        w.writerow(['التوقيت', 'اسم_المستخدم', 'نوع_النشاط', 'التفاصيل'])
      w.writerow([
          datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          admin_username,
          action_type,
          details,
      ])
  except Exception as e:
    st.error(f'خطأ في تسجيل النشاط: {e}')


# إنشاء ملف افتراضي للأدمنز والمشرفين إذا لم يكن موجوداً (مع دعم الدور والصلاحية)
if not os.path.exists(admins_db):
  with open(admins_db, mode='w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(
        ['اسم_المستخدم', 'كلمة_المرور', 'اسم_المدرب', 'الدور']
    )  # الدور: Super Admin أو Sub Admin
    w.writerow(['admin', 'admin123', 'الأدمن الأساسي', 'Super Admin'])

# إنشاء ملف سجل النشاطات إذا لم يكن موجوداً
if not os.path.exists(admin_logs_db):
  with open(admin_logs_db, mode='w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['التوقيت', 'اسم_المستخدم', 'نوع_النشاط', 'التفاصيل'])

# نظام تسجيل دخول الأدمن
if 'admin_logged_in' not in st.session_state:
  st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
  st.markdown('<br><br>', unsafe_allow_html=True)
  col1, col2, col3 = st.columns([1, 1.2, 1])

  with col2:
    st.markdown(
        """
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #0d6efd; margin-bottom: 5px;">👨‍💻 لوحة تحكم المدربين</h2>
                <p style="color: #6c757d; font-size: 15px;">أكاديمية HandsOnSite - تسجيل دخول الأدمن</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form('admin_login_form'):
      st.markdown('🔒 **يرجى إدخال بيانات حساب المدرب الخاص بك**')
      adm_user = st.text_input('اسم المستخدم للمدرب:')
      adm_pass = st.text_input('كلمة المرور:', type='password')

      submit_adm_login = st.form_submit_button('تسجيل دخول الأدمن')

      if submit_adm_login:
        if adm_user and adm_pass:
          try:
            df_admins = pd.read_csv(
                admins_db, encoding='utf-8-sig', on_bad_lines='skip'
            )
            match_adm = df_admins[
                (
                    df_admins['اسم_المستخدم'].astype(str).str.strip()
                    == adm_user.strip()
                )
                & (
                    df_admins['كلمة_المرور'].astype(str).str.strip()
                    == adm_pass.strip()
                )
            ]

            if not match_adm.empty:
              st.session_state.admin_logged_in = True
              st.session_state.admin_name = match_adm.iloc[0]['اسم_المدرب']
              st.session_state.admin_username = adm_user.strip()
              if 'الدور' in match_adm.columns:
                st.session_state.admin_role = (
                    str(match_adm.iloc[0]['الدور']).strip()
                )
              else:
                st.session_state.admin_role = (
                    'Super Admin' if adm_user.strip() == 'admin' else 'Sub Admin'
                )

              log_admin_action(
                  adm_user.strip(), 'تسجيل دخول', 'تم تسجيل الدخول بنجاح'
              )
              st.success('تم تسجيل الدخول بنجاح! جاري تحويلك لوحة التحكم...')
              st.rerun()
            else:
              st.error('خطأ: اسم المستخدم أو كلمة المرور غير صحيحة.')
          except Exception as e:
            st.error(f'حدث خطأ أثناء التحقق من البيانات: {e}')
        else:
          st.warning('الرجاء إدخال اسم المستخدم وكلمة المرور.')
  st.stop()

# --- القائمة الجانبية للأدمن ---
st.sidebar.markdown(f'### أهلاً بك يا بشمهندس 👋')
st.sidebar.markdown(
    f'**المدرب الحالي:** {st.session_state.get("admin_name", "مدرب")}'
)
st.sidebar.markdown(
    f"**الصلاحية:** {'المسؤول الأساسي (Super Admin)' if st.session_state.get('admin_role') == 'Super Admin' else 'مسؤول فرعي'}"
)
st.sidebar.divider()

# القائمة الأساسية
menu_options = [
    '📅 جداول مواعيد المجموعات (Groups)',
    '✅ تسجيل حضور وغياب الطلاب',
    '⭐ تقييم المتدربين',
    '👥 إدارة المتدربين (عرض، إضافة، حذف)',
    '🔑 إدارة المدربين والأدمن',
    '📢 نشر الإعلانات والأخبار',
]

if st.session_state.get('admin_role') == 'Super Admin':
  menu_options.append('📊 سجل نشاطات الأدمن (Activity Logs)')

admin_menu = st.sidebar.radio('خيارات لوحة التحكم:', menu_options)

if st.sidebar.button('تسجيل الخروج'):
  log_admin_action(
      st.session_state.get('admin_username', 'unknown'),
      'تسجيل خروج',
      'تم تسجيل الخروج',
  )
  st.session_state.admin_logged_in = False
  st.session_state.admin_username = ''
  st.session_state.admin_name = ''
  st.session_state.admin_role = ''
  st.rerun()

# --- تنفيذي للأقسام داخل اللوحة ---

# 1. قسم إدارة المدربين والأدمن
if admin_menu == '🔑 إدارة المدربين والأدمن':
  st.title('🔑 إدارة المدربين وصلاحيات الأدمن')

  current_role = st.session_state.get('admin_role', 'Sub Admin')
  current_username = st.session_state.get('admin_username', '')

  if current_role == 'Super Admin':
    st.info(
        'بصفتك المسؤول الرئيسي، يمكنك إضافة أدمن جديد وتحديد صلاحيته للنظام.'
    )

    with st.form('add_new_admin_form'):
      st.subheader('إضافة مسؤول أو مدرب جديد')
      new_user = st.text_input('اسم المستخدم الجديد (بالإنجليزية):')
      new_pass = st.text_input('كلمة المرور:', type='password')
      new_name = st.text_input('اسم المدرب/المسؤول الكامل:')
      new_role = st.selectbox(
          'الدور والصلاحية:', ['Sub Admin', 'Super Admin']
      )

      submit_new_adm = st.form_submit_button('حفظ وإنشاء الحساب')

      if submit_new_adm:
        if new_user and new_pass and new_name:
          try:
            df_adm = pd.read_csv(admins_db, encoding='utf-8-sig')
            if new_user.strip() in df_adm['اسم_المستخدم'].values:
              st.error('اسم المستخدم موجود مسبقاً، اختر اسمًا آخر.')
            else:
              new_row = pd.DataFrame(
                  [[new_user.strip(), new_pass.strip(), new_name.strip(), new_role]],
                  columns=['اسم_المستخدم', 'كلمة_المرور', 'اسم_المدرب', 'الدور'],
              )
              df_adm = pd.concat([df_adm, new_row], ignore_index=True)
              df_adm.to_csv(admins_db, index=False, encoding='utf-8-sig')

              log_admin_action(
                  current_username,
                  'إنشاء أدمن',
                  f'تم إنشاء حساب جديد باسم {new_user.strip()} بدور {new_role}',
              )
              st.success(f'تم إنشاء المسؤول {new_name} بنجاح!')
          except Exception as e:
            st.error(f'حدث خطأ أثناء الحفظ: {e}')
        else:
          st.warning('الرجاء إكمال جميع الحقول المطلوبة.')

    st.markdown('---')
    st.subheader('📋 قائمة جميع المسؤولين والمدربين الحاليين')
    if os.path.exists(admins_db):
      df_current_admins = pd.read_csv(admins_db, encoding='utf-8-sig')
      display_df = df_current_admins.copy()
      if 'كلمة_المرور' in display_df.columns:
        display_df['كلمة_المرور'] = '********'
      st.dataframe(display_df, use_container_width=True)
  else:
    st.warning('عذراً، هذه الصفحة متاحة للمسؤول الرئيسي (Super Admin) فقط.')
    if os.path.exists(admins_db):
      df_current_admins = pd.read_csv(admins_db, encoding='utf-8-sig')
      display_df = df_current_admins[['اسم_المستخدم', 'اسم_المدرب']].copy()
      st.subheader('قائمة المدربين النشطين:')
      st.dataframe(display_df, use_container_width=True)

# 2. قسم سجل نشاطات الأدمن (Activity Logs)
elif (
    admin_menu == '📊 سجل نشاطات الأدمن (Activity Logs)'
    and st.session_state.get('admin_role') == 'Super Admin'
):
  st.title('📊 سجل نشاطات وحركات المسؤولين (Audit Trail)')
  st.markdown(
      'من هنا يمكنك متابعة كل إجراء قام به أي أدمن (نشر إعلان، إضافة أدمن،'
      ' إلخ) مع التوقيت بالدقيقة.'
  )

  if os.path.exists(admin_logs_db):
    df_logs = pd.read_csv(admin_logs_db, encoding='utf-8-sig')
    if not df_logs.empty:
      df_logs = df_logs.iloc[::-1].reset_index(drop=True)
      st.dataframe(df_logs, use_container_width=True)

      if st.button('🗑️ مسح السجلات القديمة'):
        with open(admin_logs_db, mode='w', encoding='utf-8-sig', newline='') as f:
          w = csv.writer(f)
          w.writerow(['التوقيت', 'اسم_المستخدم', 'نوع_النشاط', 'التفاصيل'])
        log_admin_action(
            st.session_state.get('admin_username', 'admin'),
            'مسح السجلات',
            'تم مسح سجل النشاطات',
        )
        st.success('تم مسح السجلات بنجاح!')
        st.rerun()
    else:
      st.info('لا توجد أي نشاطات مسجلة حتى الآن.')
  else:
    st.info('ملف السجلات غير موجود.')

# 3. قسم نشر الإعلانات والأخبار
elif admin_menu == '📢 نشر الإعلانات والأخبار':
  st.title('📢 نشر الإعلانات والأخبار للطلاب')

  with st.form('announcement_form'):
    ann_title = st.text_input('عنوان الإعلان:')
    ann_content = st.text_area('محتوى الإعلان:')
    submit_ann = st.form_submit_button('نشر الإعلان للطلاب')

    if submit_ann:
      if ann_title and ann_content:
        try:
          file_exists = os.path.exists(announcements_db)
          with open(
              announcements_db, mode='a', encoding='utf-8-sig', newline=''
          ) as f:
            w = csv.writer(f)
            if not file_exists:
              w.writerow(['التاريخ', 'العنوان', 'المحتوى', 'الناشر'])
            w.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ann_title,
                ann_content,
                st.session_state.get('admin_name', 'مدير النظام'),
            ])

          log_admin_action(
              st.session_state.get('admin_username', 'admin'),
              'نشر إعلان',
              f"تم نشر إعلان بعنوان: '{ann_title}'",
          )
          st.success('تم نشر الإعلان وتسجيله في النظام بنجاح!')
        except Exception as e:
          st.error(f'حدث خطأ أثناء حفظ الإعلان: {e}')
      else:
        st.warning('يرجى ملء عنوان ومحتوى الإعلان.')

# باقي الأقسام الأساسية
elif admin_menu == '📅 جداول مواعيد المجموعات (Groups)':
  st.title('📅 إدارة جداول مواعيد المجموعات')
  st.info('هنا يتم إدارة جداول ومواعيد المجموعات الدراسية.')

elif admin_menu == '✅ تسجيل حضور وغياب الطلاب':
  st.title('✅ تسجيل حضور وغياب الطلاب')
  st.info('هنا يتم تسجيل ومتابعة حضور الطلاب للمحاضرات.')

elif admin_menu == '⭐ تقييم المتدربين':
  st.title('⭐ تقييم المتدربين')
  st.info('هنا يتم تقييم مستوى المتدربين ودرجاتهم.')

elif admin_menu == '👥 إدارة المتدربين (عرض، إضافة، حذف)':
  st.title('👥 إدارة المتدربين')
  st.info('هنا يتم عرض وإدارة بيانات الطلاب والمتدربين المسجلين.')
