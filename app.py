import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import time

page_bg_img = """
            <style>
            [data-testid="stAppViewContainer"] {
            background: linear-gradient(to top, #00ffff, #ffffff);
            opacity: 1;}
            </style>
            """
st.markdown(page_bg_img, unsafe_allow_html=True)
github_urls = {
    "Deep Patel": "https://github.com/coderkage",
    "Prayas Raj": "https://github.com/Prayas7632",
    "Shivanshu Gupta": "https://github.com/ShivanshuKGupta"
}

sidebar_content = """
# Rules

The rules are simple. You'll have to make the following your routine and give updates after every single period of 24 hrs. Failing to do so, will get you out from the challenge. Penalty to get you back in the challenge can be decided later.

### To-do:
1. Pick a language for next 75 days. Learn a new concept or brush up an already learnt concept.
2. Pick any domain of your interest (ex., app dev, web dev, AI/ML etc.) and learn or practice it for minimum 2 hrs/day.
3. Pick any coding platform and do a problem everyday + upload into GitHub repo.
4. Define an industry level project and work on it.

### GitHub Links:
"""
for user, github_url in github_urls.items():
    sidebar_content += f"- [{user}]({github_url})\n"
# Display sidebar
st.sidebar.markdown(sidebar_content)

users = ['Deep', 'Prayas', 'Shivanshu']
task_files = {user: f"{user}_tasks.csv" for user in users}

def is_submission_allowed(user):
    current_time = datetime.now()
    start_time_today = current_time.replace(hour=5, minute=30, second=0, microsecond=0)
    
    if start_time_today <= current_time:
        if user in task_files:
            if os.path.exists(task_files[user]):
                last_submission_time = pd.read_csv(task_files[user])['Submission Time'].max()
                if pd.isnull(last_submission_time) or pd.to_datetime(last_submission_time) < start_time_today:
                    return True
    return False


def main():
    st.title('75-Hard Challenge : Geek Edition🤓')
    for user, task_file in task_files.items():
        if os.path.exists(task_file):
            last_submission_time = pd.read_csv(task_file)['Submission Time'].max()
            if pd.isnull(last_submission_time) or (datetime.now() - pd.to_datetime(last_submission_time)) >= timedelta(days=1):
                st.error(f"{user} broke the streak!") 
           
    current_time = datetime.now()
    start_time_today = current_time.replace(hour=5, minute=30, second=0)
    end_time_today = (current_time + timedelta(days=1)).replace(hour=5, minute=29, second=59)
    time_left = end_time_today - current_time
    
    st.info(f"Time left to submit today's work: {time_left}")
    st.subheader("Streak Progress")
    for user, task_file in task_files.items():
        if os.path.exists(task_file):
            task_df = pd.read_csv(task_file)
            streak_count = len(task_df)
            st.write(f"{user}: {streak_count}")

            if streak_count >= 75:
                st.success(f"Congratulations! {user} has achieved a 75-day streak!")
                st.progress(1.0)
            else:
                progress = streak_count / 75
                st.progress(progress)

    selected_user = st.selectbox('Select User:', users)
    task = st.text_input('Write your today's work:')
    
    if selected_user and task:
        if st.button('Submit'):
            if is_submission_allowed(selected_user):
                task_df = pd.DataFrame({'Task': [task], 'Submission Time': [datetime.now()]})
                if os.path.exists(task_files[selected_user]):
                    task_df.to_csv(task_files[selected_user], mode='a', header=False, index=False)
                else:
                    task_df.to_csv(task_files[selected_user], index=False)
                st.success('Work updated successfully!')
            else:
                st.error('You have already submitted today\'s work. Edit your response if you think it was a mistake.')

    st.header('Work done by Users')

    for user, task_file in task_files.items():
        if os.path.exists(task_file):
            st.subheader(user)
            task_df = pd.read_csv(task_file)
            st.table(task_df)

    selected_user = st.selectbox('Select User to Edit Work:', users)
    if selected_user:
        task_file = task_files[selected_user]
        if os.path.exists(task_file):
            task_df = pd.read_csv(task_file)
            last_task_index = len(task_df) - 1
            last_task_text = task_df.iloc[last_task_index]['Task']
            with st.expander(f"Edit Last Task for {selected_user}"):
                edited_task = st.text_input(f'Edit Work:', value=last_task_text, key=f"edit_{selected_user}")
                if st.button(f'Update Last Work for {selected_user}'):
                    task_df.at[last_task_index, 'Task'] = edited_task
                    task_df.to_csv(task_file, index=False)
                    st.success('Work updated successfully!')


    st.subheader("Streak Counts")
    progress_html1 = f""" <hr>  """
    st.markdown(progress_html1, unsafe_allow_html=True)
    for user, task_file in task_files.items():
        if os.path.exists(task_file):
            task_df = pd.read_csv(task_file)
            streak_count = len(task_df)
            # st.write(f"{user}: {streak_count}/75")

            progress = min(streak_count / 75, 1.0)
            
            progress_html = f"""
            
                <div class="circular-progress-container">
                    <div class="progress-name">{user}</div>
                    <div class="progress-circle">
                        <svg class="progress-ring" width="120" height="120">
                            <circle class="progress-ring-circle" cx="60" cy="60" r="54" fill="#ffffcc" stroke-width="10" 
                                stroke-dasharray="339.292" 
                                stroke-dashoffset="{339.292 * (1 - progress)}" />
                        </svg>
                        <div class="progress-text1">🔥</div>
                        <div class="progress-text2">{streak_count}/75</div>
                    </div>
                </div>
                <hr>
            """
            st.markdown(progress_html, unsafe_allow_html=True)

    
                
    st.markdown(
        """
        <style>
            .circular-progress-container {
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .progress-name {
                margin-top: 10px;
                font-size: 16px;
            }

            .progress-circle {
                position: relative;
                width: 120px;
                height: 120px;
            }

            .progress-ring {
                position: absolute;
                top: 0;
                left: 0;
                transform: rotate(-90deg);
            }

            .progress-ring-circle {
                stroke: #ffa500; /* blue color */
                stroke-linecap: round;
                transition: stroke-dashoffset 0.35s;
            }

            .progress-text1 {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 50px;
                font-weight: bold;
                color: #f06624; /* orange color */
                opacity: 80%;
            }

            .progress-text2 {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 25px;
                font-weight: bold;
                color: #000000; /* black color */
                opacity: 75%;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    footer_html = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #333;
    color: #fff;
    text-align: center;
    padding: 10px 0;
}
</style>

<div class="footer">
    <p>Made with ❤️ by Deep Patel.</p>
</div>
"""

# Display footer
    st.markdown(footer_html, unsafe_allow_html=True)

    

if __name__ == '__main__':
    main()
