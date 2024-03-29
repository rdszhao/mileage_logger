import base64
import os
import arrow
import httpx
import streamlit as st
import pandas as pd
from stravalib.client import Client
from bokeh.models.widgets import Div
from dotenv import load_dotenv

load_dotenv()
APP_URL = os.environ['APP_URL']
STRAVA_CLIENT_ID = os.environ['STRAVA_CLIENT_ID']
STRAVA_CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']
STRAVA_AUTHORIZATION_URL = 'https://www.strava.com/oauth/authorize'
STRAVA_API_BASE_URL = 'https://www.strava.com/api/v3'
DEFAULT_ACTIVITY_LABEL = 'NO_ACTIVITY_SELECTED'
STRAVA_ORANGE = '#fc4c02'


@st.cache(show_spinner=False)
def load_image_as_base64(image_path):
    with open(image_path, "rb") as f:
        contents = f.read()
    return base64.b64encode(contents).decode("utf-8")


def powered_by_strava_logo():
    base64_image = load_image_as_base64("./static/api_logo_pwrdBy_strava_horiz_light.png")
    st.markdown(
        f"<img src='data:image/png;base64,{base64_image}' width='100%' alt='powered by strava'>",
        unsafe_allow_html=True,
    )


def authorization_url():
    request = httpx.Request(
        method="GET",
        url=STRAVA_AUTHORIZATION_URL,
        params={
            "client_id": STRAVA_CLIENT_ID,
            "redirect_uri": APP_URL,
            "response_type": "code",
            "approval_prompt": "auto",
            "scope": "activity:read_all"
        }
    )

    return request.url


def login_header(header=None):
    strava_authorization_url = authorization_url()

    if header is None:
        base = st
    else:
        col1, _, _, button = header
        base = button

    with col1:
        powered_by_strava_logo()

    base64_image = load_image_as_base64("./static/btn_strava_connectwith_orange@2x.png")
    base.markdown(
        (
            f"<a href=\"{strava_authorization_url}\">"
            f"  <img alt=\"strava login\" src=\"data:image/png;base64,{base64_image}\" width=\"100%\">"
            f"</a>"
        ),
        unsafe_allow_html=True,
    )


def logout_header(header=None):
    if header is None:
        base = st
    else:
        _, col2, _, button = header
        base = button


    with col2:
        powered_by_strava_logo()

    if base.button("Log out"):
        js = f"window.location.href = '{APP_URL}'"
        html = f"<img src onerror=\"{js}\">"
        div = Div(text=html)
        st.bokeh_chart(div)


def logged_in_title(strava_auth, header=None):
    if header is None:
        base = st
    else:
        col, _, _, _ = header
        base = col

    first_name = strava_auth["athlete"]["firstname"]
    last_name = strava_auth["athlete"]["lastname"]
    col.markdown(f"*hi, {first_name} {last_name}!*")


@st.cache(show_spinner=False, suppress_st_warning=True)
def exchange_authorization_code(authorization_code):
    response = httpx.post(
        url="https://www.strava.com/oauth/token",
        json={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "code": authorization_code,
            "grant_type": "authorization_code",
        }
    )
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError:
        st.error("Something went wrong while authenticating with Strava. Please reload and try again")
        st.experimental_set_query_params()
        st.stop()
        return

    strava_auth = response.json()

    return strava_auth


def authenticate(header=None, stop_if_unauthenticated=True):
    query_params = st.experimental_get_query_params()
    authorization_code = query_params.get("code", [None])[0]

    if authorization_code is None:
        authorization_code = query_params.get("session", [None])[0]

    if authorization_code is None:
        login_header(header=header)
        if stop_if_unauthenticated:
            st.stop()
        return
    else:
        logout_header(header=header)
        strava_auth = exchange_authorization_code(authorization_code)
        logged_in_title(strava_auth, header)
        st.experimental_set_query_params(session=authorization_code)

        return strava_auth


def header():
    col1, col2, col3 = st.beta_columns(3)

    with col3:
        strava_button = st.empty()

    return col1, col2, col3, strava_button


@st.cache(show_spinner=False)
def get_activities(auth, page=1):
    access_token = auth["access_token"]
    response = httpx.get(
        url=f"{STRAVA_API_BASE_URL}/athlete/activities",
        params={
            "page": page,
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return response.json()


def activity_label(activity):
    if activity["name"] == DEFAULT_ACTIVITY_LABEL:
        return ""

    start_date = arrow.get(activity["start_date_local"])
    human_readable_date = start_date.humanize(granularity=["day"])
    if human_readable_date == '0 days ago':
        human_readable_date = 'today'
    date_string = start_date.format("MM-DD-YYYY")

    return f"{activity['name']} - {date_string} ({human_readable_date})"


def select_strava_activity(auth):
    col1, col2 = st.beta_columns([1, 3])
    with col1:
        page = st.number_input(
            label="activities page",
            min_value=1,
            help="the Strava API returns your activities in chunks of 30. Increment this field to go to the next page.",
        )

    with col2:
        activities = get_activities(auth=auth, page=page)
        if not activities:
            st.info("this Strava account has no activities or you ran out of pages.")
            st.stop()
        default_activity = {"name": DEFAULT_ACTIVITY_LABEL, "start_date_local": ""}

        activity = st.selectbox(
            label="select an activity",
            options=[default_activity] + activities,
            format_func=activity_label,
        )

    if activity["name"] == DEFAULT_ACTIVITY_LABEL:
        st.write("no activity selected")
        return
    return activity


STREAM_TYPES = [
    "time",
    "latlng",
    "distance",
    "altitude",
    "velocity_smooth",
    "heartrate",
    "cadence",
    "watts",
    "temp",
    "moving",
    "grade_smooth",
]

COLUMN_TRANSLATIONS = {
    "altitude": "elevation",
    "velocity_smooth": "speed",
    "watts": "power",
    "temp": "temperature",
    "grade_smooth": "grade",
}

def read_strava(
    activity_id: int,
    access_token: str,
    refresh_token: str = None,
    client_id: int = None,
    client_secret: str = None,
    ) -> pd.DataFrame:
    """This method lets you retrieve activity data from Strava.
    Columns names are translated to sweat terminology (e.g. "heart_rate" > "heartrate").
    Two API calls are made to the Strava API: 1 to retrieve activity metadata, 1 to retrieve the raw data ("streams").

    Args:
        activity_id: The id of the activity
        access_token: The Strava access token
        refresh_token: The Strava refresh token. Optional.
        client_id: The Strava client id. Optional. Used for token refresh.
        client_secret: The Strava client secret. Optional. Used for token refresh.

    Returns:
        A pandas data frame with all the data.
    """
    client = Client()
    client.access_token = access_token
    client.refresh_token = refresh_token

    activity = client.get_activity(activity_id)
    return activity



@st.cache(show_spinner=False, max_entries=30, allow_output_mutation=True)
def download_activity(activity, strava_auth):
    with st.spinner(f"Downloading activity \"{activity['name']}\"..."):
        return read_strava(activity["id"], strava_auth["access_token"])