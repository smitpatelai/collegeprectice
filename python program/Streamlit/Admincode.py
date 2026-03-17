import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="Role Base Login", page_icon="🧿")

# -------------------------------
# USERS , CURRENT USER , LOGIN STATE
# -------------------------------
if "users" not in st.session_state:
    st.session_state.users = []

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------------
# EXTRA DATA STORAGE
# -------------------------------
if "exam_forms" not in st.session_state:
    st.session_state.exam_forms = []

# -------------------------------
# CUSTOM UI CSS
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}
.stTextInput>div>div>input {
    border-radius: 10px;
}
.stButton>button {
    border-radius: 10px;
    background-color: #00c6ff;
    color: black;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# REGISTER
# -------------------------------
def register():
    if st.session_state.reg_user == "" or st.session_state.reg_password == "":
        st.warning("⚠ Please fill all fields")
        return

    st.session_state.users.append({
        "username": st.session_state.reg_user,
        "password": st.session_state.reg_password,
        "role": st.session_state.reg_role
    })

    st.success("✅ Registration Successful")

# -------------------------------
# LOGIN
# -------------------------------
def login():
    for user in st.session_state.users:
        if user["username"] == st.session_state.log_user and user["password"] == st.session_state.log_pass:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            return
    else:
        st.error("❌ Invalid Credentials")

# -------------------------------
# LOGOUT
# -------------------------------
def logout():
    st.session_state.current_user = None
    st.session_state.logged_in = False

# -------------------------------
# LOGIN / REGISTER UI
# -------------------------------
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab2:
        st.subheader("📝 Create New Account")

        st.text_input("👤 Username", key="reg_user", placeholder="Enter username")
        st.text_input("🔑 Password", type="password", key="reg_password", placeholder="Enter password")
        st.selectbox("🎭 Role", ["Student", "Teacher"], key="reg_role")

        st.button("🚀 Register", on_click=register)

    with tab1:
        st.subheader("🔐 Login to Your Account")

        st.text_input("👤 Username", key="log_user", placeholder="Enter username")
        st.text_input("🔑 Password", key="log_pass", type="password", placeholder="Enter password")

        st.button("🔓 Login", on_click=login)

# -------------------------------
# AFTER LOGIN
# -------------------------------
else:
    user = st.session_state.current_user

    with st.sidebar:
        st.header(f"👋 Welcome {user['username']}")

        if user["role"] == "Student":
            selected = option_menu(
                "🎓 Student Panel",
                ["Dashboard", "My Result", "Exam Form"],
                icons=["house", "book", "file"]
            )

        elif user["role"] == "Teacher":
            selected = option_menu(
                "👨‍🏫 Teacher Portal",
                ["Dashboard", "Approval Exam Form", "Upload Result"],
                icons=["bar-chart", "check", "table"]
            )

        st.button("🚪 Logout", on_click=logout)

    # -------------------------------
    # DASHBOARD
    # -------------------------------
    if selected == "Dashboard":
        st.title("📊 Dashboard")

        col1, col2, col3 = st.columns(3)

        total = len(st.session_state.exam_forms)
        approved = sum(1 for f in st.session_state.exam_forms if f["status"] == "Approved")
        pending = sum(1 for f in st.session_state.exam_forms if f["status"] == "Pending")

        col1.metric("📄 Total Forms", total)
        col2.metric("✅ Approved", approved)
        col3.metric("⏳ Pending", pending)

        st.info("📌 This dashboard shows overall system activity.")

    # -------------------------------
    # STUDENT: EXAM FORM
    # -------------------------------
    if user["role"] == "Student" and selected == "Exam Form":
        st.title("📝 Exam Form Submission")

        name = st.text_input("👤 Student Name")
        course = st.text_input("📘 Course Name")

        if st.button("📤 Submit Form"):
            if name == "" or course == "":
                st.warning("⚠ Fill all details")
            else:
                st.session_state.exam_forms.append({
                    "name": name,
                    "course": course,
                    "status": "Pending"
                })
                st.success("✅ Form Submitted Successfully")

    # -------------------------------
    # TEACHER: APPROVAL
    # -------------------------------
    if user["role"] == "Teacher" and selected == "Approval Exam Form":
        st.title("✅ Approval Exam Form")

        if len(st.session_state.exam_forms) == 0:
            st.warning("No forms available")
        else:
            for i, form in enumerate(st.session_state.exam_forms):
                st.write(f"👤 {form['name']} | 📘 {form['course']} | Status: {form['status']}")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Approve {i}"):
                        st.session_state.exam_forms[i]["status"] = "Approved"

                with col2:
                    if st.button(f"Reject {i}"):
                        st.session_state.exam_forms[i]["status"] = "Rejected"

                st.divider()