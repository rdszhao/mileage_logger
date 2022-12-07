import streamlit as st
from re import compile, fullmatch
from strava import header, authenticate, select_strava_activity
from forms import submit
    

if __name__ == '__main__':
    st.set_page_config(
        page_title='mileage logger',
        page_icon=':circus_tent:',
    )

    st.image('https://analytics.gssns.io/pixel.png')

    strava_header = header()

    st.markdown(
        '''
        # :dragon: mileage logger
        this is built on top of Aart Goossens' [activity viewer](https://github.com/AartGoossens/streamlit-activity-viewer), the source code is located [here](https://github.com/rdszhao/mileage-logger) 

        usage is simple: fill in your email, select your activity, select the craft, and then submit
        '''
    )

    strava_auth = authenticate(header=strava_header, stop_if_unauthenticated=False)

    if strava_auth is None:
        st.markdown('Click the \'Connect with Strava\' button at the top to login with your Strava account and get started.')
        st.image(
            'https://files.gssns.io/public/streamlit-activity-viewer-demo.gif',
            caption='Streamlit Activity Viewer demo',
            use_column_width='always',
        )
        st.stop()

    with st.form('email'):
            email = st.text_input('email')
            saved_email = st.form_submit_button('save')
            regex = compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
            valid_email = fullmatch(regex, email)
    if valid_email:
        st.markdown('**email saved**')
    else:
        st.markdown('**please enter a valid email**')

    activity = select_strava_activity(strava_auth)

    crafts = [
        'Dragon Boat',
        'OC1',
        'V1',
        'OC6',
        'OC2',
        'SUP',
        'Surfski',
        'Kayak',
        'paddleErg',
        'rowErg',
        'Run'
    ]
    with st.form('submission'):
        craft = st.selectbox('craft', crafts)
        submitted = st.form_submit_button('submit')
    if submitted:
        name = f"{strava_auth['athlete']['firstname']} {strava_auth['athlete']['lastname']}"
        if valid_email:
            submit(name, email, craft, activity, debug=True)
            # submit(name, email, craft, activity)
        else:
            st.markdown('**remember to fill in an email**')