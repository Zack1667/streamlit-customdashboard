# Custom Streamlit Dashboard to display S3 buckets in a table


## What does it do?

```
This will create a dashboard with 3 tabs that can grab CSV Data from 3 Buckets of your choice, it will grab the latest file date from S3 and use it in the information it displays in the tables.
```

## How can I modify it to use myself? 

```
Simply ammend the code as below:
```

```python
# Change the page title, icon, and layout to your choice:
st.set_page_config( # this must be at the top of your code, below your imported modules.
        page_title="My Custom Streamlit Dashboard",
        page_icon="🧊",
        layout="wide",
    )
```
```python
# Below you can choose add an image or not, and change the title also:
image = Image.open('Myimage.png') 

st.image(image) 
st.title("My Awesome Custom Dashboard!")
```
```python
# Change the Bucket names to your Bucket names:
buckets = ['an-aws-s3-bucket', 'another-s3-bucket', 'and-another-s3-bucket']
```
```python
# Set up your boto3 session to use sso and set up the s3 client:
sess = boto3.Session(profile_name="sso-profile-here", region_name="eu-west-1")
s3 = sess.client("s3")
```
## Run the file

Before you run the file, make sure you sign into your sso profile or there is already a session active:
```
aws sso login --profile my-sso-profile 
```
also ensure you have some data available in CSV format in your buckets, it could be some dumb data if you like just to test with:

you could even user the faker Python module to generate some awesome fake data for you, I have an example below in my repo: 

[Faker Module](https://github.com/Zack1667/faker-python-module) - then you can just upload them into your S3 buckets. 




An Example of the Dashboard in Use:

![Bucket1](/pics/dashboard1.png "First Bucket")

There is also a dropdown box on the side for choosing which bucket to view data from: 

![Dropdown](/pics/dashboardropdown.png "Dropdown Selector")

If you have more data in another bucket than others, no problem, it will re-size for you:

![Bucket2](/pics/dashboard2.png "Second Bucket with more data")

![Bucket3](/pics/dashboard3.png "Third Bucket with even more data") 

The data can be anything you like really, for example I have some Lambdas that fetch data each week from an endpoint API based on users on services we provide in my company. 

