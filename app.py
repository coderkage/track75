import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import time

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: var(--background-color);
        transition: background 0.3s ease;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# JavaScript to detect dark mode and set CSS variable
st.markdown(
    """
    <script>
    (function() {
        const root = document.documentElement;
        const observer = new MutationObserver(() => {
            const darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
            # root.style.setProperty('--background-color', darkMode ? 'linear-gradient(to top, #000000, #333333)' : 'linear-gradient(to top, #ffffff, #00ff00)');
        });
        observer.observe(root, { attributes: true, attributeFilter: ['class'] });
        observer.disconnect();
    })();
    </script>
    """,
    unsafe_allow_html=True
)


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
    current_date = datetime.now().date()
    
    if user in task_files:
        task_file_path = task_files[user]
        
        if os.path.exists(task_file_path):
            submission_times = pd.read_csv(task_file_path)['Submission Time']
            
            if not submission_times.empty:
                last_submission_time = pd.to_datetime(submission_times).max()
                if last_submission_time.date() != current_date:
                    return True
            else:
                return False
    return False

def count_streak(task_file):
    if os.path.exists(task_file):
            task_df = pd.read_csv(task_file)
            task_df['Submission Time'] = pd.to_datetime(task_df['Submission Time'])
            task_df = task_df.sort_values(by='Submission Time', ascending=False)

            current_time = datetime.now()
            today = current_time.date()
            yesterday = today - timedelta(days=1)

            streak_count = 0
            for submission_time in task_df['Submission Time']:
                submission_date = submission_time.date()
                if streak_count == 0:
                    if submission_date in [today, yesterday]:
                        streak_count = 1
                        current_streak_day = submission_date
                    else:
                        break
                else:
                    if current_streak_day - timedelta(days=streak_count) == submission_date:
                        streak_count += 1
                    else:
                        break
    return streak_count

def main():
    st.title('75-Hard Challenge: Geek Edition🤓')

    current_time = datetime.now()
    start_time_today = current_time.replace(hour=0, minute=0, second=0)
    end_time_today = current_time.replace(hour=23, minute=59, second=59)
    time_left = end_time_today - current_time

    st.info(f"Time left to submit today\'s work: {time_left} hours")


    for user, task_file in task_files.items():
        if os.path.exists(task_file):
            last_submission_time = pd.read_csv(task_file)['Submission Time'].max()
            if pd.isnull(last_submission_time):
                st.warning(f"{user} haven't started the challenege yet!")
            else:
                last_submission_date = pd.to_datetime(last_submission_time).date()
                today = datetime.now().date()
                yesterday = today - timedelta(days=1)
                if last_submission_date != today and last_submission_date != yesterday:
                    st.error(f"{user} broke the streak!")
 
    st.subheader("Streak Progress")
    for user, task_file in task_files.items():
        streak_count = count_streak(task_file)

        st.write(f"{user}: {streak_count}")

        if streak_count >= 75:
            st.success(f"Congratulations! {user} has achieved a 75-day streak!")
            st.progress(1.0)
        else:
            progress = streak_count / 75
            st.progress(progress)


    selected_user = st.selectbox('Select User:', users)
    task = st.text_input('Write your task:')
    
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
            csv = task_df.to_csv(index=False).encode('utf-8')
        
            st.download_button(
                label=f"Download {user}'s data as CSV",
                data=csv,
                file_name=f'{user}_tasks.csv',
                mime='csv',
            )

    selected_user = st.selectbox('Select User to Edit Work:', users)
    if selected_user:
        task_file = task_files[selected_user]
        if os.path.exists(task_file):
            task_df = pd.read_csv(task_file)
            last_task_index = len(task_df) - 1
            if last_task_index != -1:
                last_task_text = task_df.iloc[last_task_index]['Task']
                with st.expander(f"Edit Last Task for {selected_user}"):
                    edited_task = st.text_input(f'Edit Work:', value=last_task_text, key=f"edit_{selected_user}")
                    if st.button(f'Update Last Work for {selected_user}'):
                        task_df.at[last_task_index, 'Task'] = edited_task
                        task_df.to_csv(task_file, index=False)
                        st.success('Work updated successfully!')
            else:            
                st.warning('The task list is empty!')


    st.subheader("Streak Counts")
    progress_html1 = f""" <hr>  """
    st.markdown(progress_html1, unsafe_allow_html=True)
    for user, task_file in task_files.items():
        streak_count = count_streak(task_file)
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
                color: #f06624;
                opacity: 80%;
            }

            .progress-text2 {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 25px;
                font-weight: bold;
                color: #000000;
                opacity: 75%;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    footer_html = """

        <div class="footer">
            <p>Made with ❤️ by Deep Patel.</p>
        </div>

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

        """

# Display footer
    st.markdown(footer_html, unsafe_allow_html=True)

    

if __name__ == '__main__':
    main()
