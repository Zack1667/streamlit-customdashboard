import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import boto3
from PIL import Image
import chardet
from io import BytesIO
import streamlit as st
st.set_page_config( # set_page_config must remain on this line for this to work.
        page_title="My Custom Streamlit Dashboard",
        page_icon="🧊",
        layout="wide",
    )

#image = Image.open('Myimage.png') # here you can place a corporate image of some sorts.

#st.image(image) # call the image varbiable above and use that particular image 
st.title("My Awesome Custom Dashboard!")

buckets = ['an-aws-s3-bucket', 'another-s3-bucket', 'and-another-s3-bucket']

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame): Source dataframe

    Returns:
        Tuple[AgGrid, int]: The interactive table and the row count.
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enable_row_group=True, enable_value=True, enable_pivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    options.configure_default_column(
        groupable=True,
        aggFunc="sum",
        editable=False,
        enableRowGroup=True,
        enablePivot=True,
        sortable=True,
        resizable=True,
    )
    options.configure_column(
        "column_name", editable=False, aggFunc="", enableRowGroup=True
    )

    ag_grid = AgGrid(
        df,
        enable_enterprise_modules=True,
        grid_options=options.build(),
        theme="alpine",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )
    row_count = len(df)
    return ag_grid, row_count

# boto3 components - if you have an iDP you can use sso similar to below:

sess = boto3.Session(profile_name="sso-profile-name-here", region_name="eu-west-1")
s3 = sess.client("s3")


def read_buckets(buckets):
    """Reads the latest CSV file from each of the given S3 buckets.

    Args:
        bucket_names (List[str]): A list of S3 bucket names.

    Returns:
        List[pd.DataFrame]: The contents of the latest CSV file in each bucket.
    """
    dfs = []
    for bucket_name in buckets:
        # list all objects in the bucket, sorted by LastModified in descending order
        result = s3.list_objects_v2(Bucket=bucket_name)
        objects = result.get('Contents', [])
        objects.sort(key=lambda x: x['LastModified'], reverse=True)

        # get the latest object
        latest_object = objects[0]

        # retrieve the object using get_object
        response = s3.get_object(Bucket=bucket_name, Key=latest_object['Key'])
        try:
            f = response['Body'].read()
            result = chardet.detect(f)
            encoding = result['encoding'] # use chardet to detect the encoding easier
            df = pd.read_csv(BytesIO(f), encoding=encoding)
            df = df.rename(columns=lambda x: x.strip()) # remove leading/trailing whitespaces from column names
            dfs.append(df)
        finally:
            response['Body'].close()

    return dfs

# read the CSV files from each bucket
dfs = read_buckets(buckets)

# display each dataframe as a separate tab
tabs = []
for i, df in enumerate(dfs):
    tab_name = f"{buckets[i]} ({i+1})"
    tabs.append(tab_name)

with st.container():
    # add a selector to switch between tabs
    selected_tab = st.sidebar.selectbox("Select a bucket", tabs)
    st.write(f"You selected {selected_tab}")

    # display the selected table
    if selected_tab == tabs[0]:
        table_data = dfs[0]
        aggrid_interactive_table(table_data)
        st.write(f"Total Users: {len(table_data)}")
    elif selected_tab == tabs[1]:
        table_data = dfs[1]
        aggrid_interactive_table(table_data)
        st.write(f"Total Users: {len(table_data)}")
    elif selected_tab == tabs[2]:
        table_data = dfs[2]
        aggrid_interactive_table(table_data)
        st.write(f"Total Users: {len(table_data)}")

