import json
from pprint import pprint

# PAGE DATA and METADATA
# headers - metadata
website_metadata = {"contacts": "Contacts", "skills": "Skills", "certifications": "Certifications",
                    "education": "Education", "interests": "Interests", "profile_summary": "Profile Summary",
                    "work_experience": "Work Experience", "linkedin": "LinkedIn", "github": "Github",
                    "about_me": "About Me", "page_title": "DEMO HTML FORM"}

# info about the page as a project
footer_about_info = """The page is made up of standard HTML, CSS, some Javascript 
code. However, it is a Flask application and runs fully on AWS Elastic Beansltalk. The components used are; simple 
EC2 instance along with ELB in front of it, DynamoDB as its backend, S3 for media storage, Route53 for DNS and domain 
name registration. I am also utilising AWS CodePipeline to automate deployment when the repo in GitHub gets updated. """

footer_data = {"footer_about_info": footer_about_info}

# text for the navbar
aws_logo_link = "https://d0.awsstatic.com/logos/powered-by-aws-white.png"
aws_link = "https://aws.amazon.com/what-is-cloud-computing"
navbar_metadata = {"aws_logo": aws_logo_link, "aws_link": aws_link}


