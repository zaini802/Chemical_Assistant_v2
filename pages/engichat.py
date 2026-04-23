import streamlit as st
from groq import Groq
import os
import ssl
import certifi

# SSL Fix
os.environ['SSL_CERT_FILE'] = certifi.where()

def show_chatbot():
    # --- 1. SESSION STATE (No Sidebar Needed) ---
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {} 
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = "Session 1"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "reply_context" not in st.session_state:
        st.session_state.reply_context = None

    # --- 2. MAIN HEADER & BRANDING ---
    st.markdown("""
    <div style="text-align: center; background: #0e2027; padding: 25px; border-radius: 15px; border: 1px solid #2a5298; margin-bottom: 20px;">
        <h1 style="color: white; margin-bottom: 5px;">🤖 EngiChat</h1>
        <p style="font-size: 17px; margin-top: 10px;">
            <span style="color: #2ecc71;">Developed by</span> <span style="color: white; font-weight: bold;">ZUNAIR SHAHZAD</span> 
            <span style="color: white;"> | </span> <span style="color: #f1c40f; font-weight: bold;">Chemical Engineering</span> 
            <span style="color: white;"> | </span> <span style="color: white;">UET Lahore (New Campus)</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- 3. QUICK ACTIONS (On-Page History & New Chat) ---
    st.markdown("### ⚡ Quick Actions")
    col_a, col_b, col_c = st.columns([2, 2, 6])
    
    with col_a:
        if st.button("➕ New Chat", use_container_width=True):
            if st.session_state.messages:
                st.session_state.chat_sessions[st.session_state.current_chat_id] = st.session_state.messages
            new_id = f"Session {len(st.session_state.chat_sessions) + 1}"
            st.session_state.current_chat_id = new_id
            st.session_state.messages = []
            st.rerun()

    with col_b:
        # Dropdown to select history on the main page
        history_list = list(st.session_state.chat_sessions.keys())
        if history_list:
            selected_history = st.selectbox("📚 Load History", ["Select Session"] + history_list, label_visibility="collapsed")
            if selected_history != "Select Session":
                st.session_state.chat_sessions[st.session_state.current_chat_id] = st.session_state.messages
                st.session_state.current_chat_id = selected_history
                st.session_state.messages = st.session_state.chat_sessions[selected_history]
                st.rerun()
        else:
            st.button("No History", disabled=True, use_container_width=True)

    st.markdown("---")

    # --- 4. WELCOME MESSAGE ---
    if not st.session_state.messages:
        welcome_text = (
            f"🤖 **Current Session: {st.session_state.current_chat_id}**\n\n"
            "Hello! I'm **EngiChat**, developed by **Zunair Shahzad Chemical Engineering from UET Lahore (New Campus)**. "
            "How can I assist you with Chemical Engineering today?"
        )
        st.session_state.messages.append({"role": "assistant", "content": welcome_text})

    # --- 5. CHAT DISPLAY ---
    for i, msg in enumerate(st.session_state.messages):
        is_user = msg["role"] == "user"
        bg = "#1e3c72" if is_user else "#142429"
        align = "right" if is_user else "left"
        margin = "margin-left: 15%;" if is_user else "margin-right: 15%;"

        st.markdown(f"""
            <div style="background: {bg}; color: white; padding: 15px; border-radius: 12px; margin: 10px 0; 
                        text-align: {align}; {margin}">
                {msg['content']}
            </div>
        """, unsafe_allow_html=True)

        # Inline Copy/Reply
        c1, c2, c3 = st.columns([10, 1, 1])
        with c2:
            if st.button("📋", key=f"c_{i}"): st.code(msg["content"])
        with c3:
            if st.button("💬", key=f"r_{i}"):
                st.session_state.reply_context = msg["content"]
                st.rerun()

    # Reply Indicator
    if st.session_state.reply_context:
        st.info(f"Replying to: {st.session_state.reply_context[:50]}...")
        if st.button("❌ Cancel"): 
            st.session_state.reply_context = None
            st.rerun()

    # --- 6. INPUT & IDENTITY ---
    user_input = st.chat_input("Type your message...")

    if user_input:
        prompt = f"Context: {st.session_state.reply_context}\n\nUser: {user_input}" if st.session_state.reply_context else user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            # Massive System Instruction (Always Included)
            sys_msg = (
                "You are EngiChat, developed by Zunair Shahzad, a Chemical Engineering student from UET Lahore New Campus (KSK). "
                "Zunair is the architect of this system. You are a professional Chemical Engineering expert. "
                "Always credit Zunair and UET Lahore proudly. Answer in the user's language."
            )
            
            with st.spinner("Thinking..."):
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    temperature=0.4
                )
                st.session_state.messages.append({"role": "assistant", "content": res.choices[0].message.content})
                st.session_state.reply_context = None
                st.session_state.chat_sessions[st.session_state.current_chat_id] = st.session_state.messages
                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    show_chatbot()