# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import os
from dotenv import load_dotenv
import re
from flask import Flask, redirect, url_for, request
import requests
import time


app = Flask(__name__)

load_dotenv()

app_secret = os.getenv("app_secret", None)
watsonx_projectid = os.getenv("watsonx_projectid", None)
cloud_apikey = os.getenv("cloud_apikey", None)
context = """Last updated: May 22, 2024 10:33 AM
Search
About IBM Technology Zone
•	How do I change my preferences GDPR sign off (i.e participate in notifications)?
To change your preferences:
1.	Select your profile icon located at the top of your navigation bar to the far right, then select 'Profile’.
2.	Select the ‘My opt-ins’ tab.
3.	Change your opt-in settings and click 'Save’.
To learn how you can change your preferences, view the following https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/ibmer-bp-gdpr-runbook.md.
•	What are the GDPR Guidelines and Features offered at IBM Technology Zone?
IBM Technology Zone is algined with IBM GDPR standards to properly capture your sign off on the data that we capture from you logging in and using the site.
In order to use IBM Technology Zone, you have to agree to the terms and conditions by checking the checkbox at the bottom left of the page. To view or change your opt-ins, view this https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/GDPR-client-runbook.md to get step-by-step instructions.
•	What do I do if I have issues registering my IBMid?
If you are having issues getting your IBM Cloud account created, it is most likely due to using a personal email account that was detected by IBM Cloud as a fraud account. It is recommended by IBM Cloud support to try registering again with a company email account.
•	What is the IBM Technology Zone?
IBM Technology Zone is the single destination for our technical go-to-market teams, business partner ecosystem, and customers to easily learn, build, customize, and share live environments with IBM technology that solve real customer problems and showcase the value of IBM. IBM created the IBM Technology Zone for our selling team and business partner ecosystem, however TechZone has evolved into the one-stop-shop for all infrastructure and demo environment needs such as workshops for IBM TechXchange conferences globally, self-learning environments, and of course, client demonstrations.
Users of Technology Zone can find and reserve a wide range of live environments across infrastructures and platforms with only a few clicks. Get started by visiting the IBM TechZone https://techzone.ibm.com/collection/onboarding or dive right into IBM Technology Zone and experience featured IBM base-images first-hand in the https://techzone.ibm.com/collection/5fb3200cec8dd00017c57f20.
•	How can I leverage IBM Technology Zone?
IBM Technology Zone can be leveraged in multiple ways:
o	Consume content - leverage the https://techzone.ibm.com/collection/onboarding materials to learn how to effectively navigate and consume content
o	Build content – use the environments provided to build a ‘Show Me’ demo for your customers utilizing the various branding standards for https://ibm.box.com/s/5oc5vww7j5pf9w9r7e5tgvsrcev7t7x6 content
o	Share content – take advantage of the IBM Technology Zone https://ibm.box.com/s/5oc5vww7j5pf9w9r7e5tgvsrcev7t7x6 by sharing your branded content and earn points towards Blue Points rewards!
o	Curate content – earn points for rating, flagging favorite, and bookmarking site content
•	How do I get IBM Technology Zone certified?
This badge earner will have a foundational understanding of what IBM Technology Zone is, how to effectively leverage to drive deal progression, and has successfully demonstrated an IBM product or solution using a live IBM Technology Zone environment.
To get IBM certified, click on the following link:
o	https://yourlearning.ibm.com/activity/PLAN-312D48375968
o	https://learn.ibm.com/course/view.php?id=12725
•	I have this environment and need to replicate in TechZone.
Please make absolutely sure that your environment or something similar doesn’t already exist in TechZone. There are over 700 technical assets available in TechZone today, built by SMEs and IBM product practitioners. If you are positive there’s nothing that can be used in TechZone, then you should consider porting your application into TechZone by leveraging a https://techzone.ibm.com/collection/tech-zone-certified-base-images.
•	What is Model Home?
Model Home showcases a suite of IBM solutions that provide visibility, control, and automation of IBM Technology Zone's hybrid cloud infrastructure and the workloads it runs. Check out the Model Home collection to learn more about the IBM solutions that IBM Technology Zone uses and get immediate read-only access to production environments to see IBM products at work.
Model Home: https://ibm.biz/tzmodelhome
•	Who can access TechZone?
IBM Technology Zone is accessible to IBMers, Business Partners, and Customers.
o	IBMers can log in with their W3id credentials.
o	Business Partners can log in with the IBMid associated with their Partner Plus account. Partners having issues logging into IBM Technology Zone should reach out to their company authorized profile administrators (APA) to have their IBMid associated with their company partner account.
o	Customers can log in with an IBMid.
To get started with TechZone, navigate to the onboarding page for either IBMers or Business Partners:
Welcome https://techzone.ibm.com/collection/onboarding/journey-welcome-ibmers (https://techzone.ibm.com/collection/onboarding/journey-welcome-ibmers)
Welcome https://techzone.ibm.com/collection/onboarding/journey-welcome-partners (https://techzone.ibm.com/collection/onboarding/journey-welcome-partners)
For Business Partners who need further assistance accessing TechZone, view the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/BusinessPartnersAccess.md. (https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/BusinessPartnersAccess.md)
•	My Cloud account is being cancelled can you stop it?
Cloud accounts are between the IBM Cloud team and individual owners. The IBM Technology Zone Customer Care team is unable to assist with this request.
If you received a notice of suspension and believe there is a justified purpose for your Cloud account, please review the ‘Internal Account Suspension’ email to understand the next steps.
•	How do I move my account over to TechZone?
Private accounts cannot be moved under TechZone. If you wish to retain the content, please review the process for https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/how-to-submit-itz-enhancements.md in TechZone.
•	How can I effectively onboard to the IBM Technology Zone?
An https://techzone.ibm.com/collection/onboarding has been created containing a series of helpful how-to videos to showcase new and existing site features, how to navigate the site, how to search for content, how to search & reserve an environment.
If you would like to suggest new videos and topics for the onboarding collection, comment on the onboarding collection page itself located towards the bottom of the page.
•	What can business partners access on IBM Technology Zone?
Business Partners have access to a wide range of collections and environments on IBM Technology Zone. IBMrs can leverage this https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/bp-visibility.md to help navigate what partners can and can not access on the site.
o	Leverage visibility filters on every search page to see what is visible to business partners
o	Reference every collection, resource, environment tile to see what is visible to business partners
o	If you have questions for the author about why a collection or environment is not visible to business partners, contact the author for additional support on this inquiry
All referenced within the business partner visibility runbook.
•	What languages does IBM Technology Zone support?
o	English
o	Spanish
o	Portuguese
o	Japanese
o	German
o	French
o	Chinese
o	Korean
•	What industries are supported on IBM Technology Zone?
o	Financial Services Sector - Banking, Insurance
o	Communications Sector - Telco, Media, Entertainment, Energy, Environment, Utilities
o	Distribution Sector - Consumer Industries (Agribusiness, Consumer Products, Retail), Travel & Transportation
o	Industrial Sector - Automotive, Aerospace &
o	Defense, Chemicals, Petroleum & Industrial Products, Electronics
o	Public Sector - Government, Healthcare & Life Sciences
•	Is content on IBM Technology Zone kept current?
Per the IBM Technology Zone Contributor Guidelines, all content contributors must adhere to quality, maintainance and support guidelines before publishing content on the site.
•	Who do I contact for content support?
Content is supported by the Content Contributor. There is a help icon located at the top of every page for you to get in contact directly with the content owners through options of a direct email modal option from the site, a community-monitored Slack channel or collaborators that support the content for you to get in contact with your content support questions.
For site or environment support, send an issue or inquiry to https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com. Business Partners should use mailto:techzone.help@ibm.com for all of their support requirements.
All support offerings are outlined under the Help page from the top navigation bar.
For further instructions on how to proceed with getting support on collection, leverage our runbook https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/How to get support.md.
•	Who can create content on IBM Technology Zone?
IBMers & Business Partners can contribute content.
IBMers - Get started by visiting our https://techzone.ibm.com/collection/onboarding page for helpful how-to videos and guidance.
Business Partners - Review the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/bp-contribution-agreement.md and contact the appropriate https://ibm.box.com/v/squad-leader to start collaborating today.
•	How can I provide feedback about IBM Technology Zone?
Feedback can be provided via the https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com. Business Partners should use mailto:techzone.help@ibm.com for all of their support requirements.
If your feedback is relative to a request for enhancement or system requirement, please use the https://itz-enhancements.ideas.aha.io/portal_session/new portal.
•	How can I engage with the support team as an IBMer?
IBMers can log any issues or feedback via https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com and the support team will address them according to our SLAs. If you have a requirement or enhancement request please log via the https://itz-enhancements.ideas.aha.io/portal_session/new (accessible by IBMers only).
Business Partners should use mailto:techzone.help@ibm.com for all of their support requirements.
•	Will using the IBM Technology Zone cost me/my department, i.e. are there charge backs?
Use of the IBM Technology Zone is free of charge to Technical Sellers, Technology Garage, Technology Enablement, Customer Success Managers, GBS, and Business Partners. At this time all usage/reservations made through Technology Zone infrastructure options are free of charge.
•	How can clients gain access to content on the IBM Technology Zone?
Clients cannot access all of IBM Technology Zone as this portal is currently for internal IBMers and Business Partners. However, clients can access environments that are shared with them by IBMers and Business Partners. If you would like your clients to view an environment, they need to create an IBMid to be able to access the environment that you want to share with them.
Please send them to this https://www.ibm.com/account/reg/us-en/signup?formid=urx-19776&target=https%3A%2F%2Flogin.ibm.com%2Foidc%2Fendpoint%2Fdefault%2Fauthorize%3FqsId%3D1156c9eb-c357-471b-a524-9ae38869e775%26client_id%3DODllMDk4YzItMjgxOC00 to get started with creating their IBMid.
•	What are the Terms and Conditions for using IBM Technology Zone?
When IBM Technology Zone users first log in to TechZone, they were prompted with a terms and conditions page. To re-review the content that you agreed to, please visit: https://techzone.ibm.com/terms
Contribute
•	Is experience required to create an entry with GitOps? Terraform?
Having experience using GitOps or Terraform experience is not required to add environments to collections. This is only required if you need new patterns that don’t currently exist.
•	How do I publish my collection and/or resource on TechZone?
Collection status change:
On the edit collection form, navigate to the bottom right of the collection to the 'Collection status' field. Then change the status from draft to active. 
Resource status change (Journeys and environments have a similar process):
On the resource edit form, navigate to the bottom right of the resource to the 'Status' field. Then change the status from disabled to enabled. 
View our https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/how-to-publish-on-itz.md runbook for screenshots and step-by-step instructions.
•	How can I create a resource?
Steps to create the a resource:
1.	Navigate to ‘My Resources’
2.	Click the ‘Edit’ button on the top right corner of the screen
3.	Scroll down until you see the ‘Resources’ section and click the 'Add a Resource’.
For a demo, watch this video to learn https://ibm.box.com/s/t1k31yr2ylygkdaaolbwvjut9tkgks4k.
•	How long does it typically take for a contribution to a collection to be approved?
Anyone can contribute a collection of Gold, Silver, Bronze. A collection will only have an approval process if it goes through the platinum review board. Platinum is where the additional review comes in. Approval timeline is unique to the collection and can be determined by your Squad Lead.
•	How do I add my collection to a TDP on the Technical decision points tab?
At this time, only selected Activation Kits and Platinum Demo Collections will represent a TDP on the Technical decision points tab. People can no longer flag their own content under a TDP. If you feel as though your content should be part of a TDP, reach out to the https://ibm.box.com/v/tdp-allocations-and-owners who will review and determine if your content should be included. If approved, your content will either be added to the Activation Kit or Platinum Live Demos collection for that TDP and not as a standalone collection.
•	How do I create advanced Mermaid journeys on my collections?
The main purpose of Mermaid is to help with Visualizing Documentation and resources using text and code.
To learn how you can create them, view our runbook https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/mermaid-docs.md to receive support and step-by-step instructions.
•	How do I create a journey?
Before you get started, you must already have created a collection.
Here are the steps to create a journey:
1.	Once on the edit collection page scroll down to the journeys section.
2.	Select “Add a journey” button to create your first journey.
3.	Fill in the minimum required journey fields: Title, description, visibility and status.
4.	Now, lets associate which resources and environments that you would like to display in this collection. Drag and drop the resources and environments that you want on the journey tab to the right hand Journey section.
5.	Select ‘Save’ to capture this newly created journey.
6.	Navigate to the ‘Preview’ button at the bottom of the edit collection form to see how your new journey will display.
7.	Then proceed down to the bottom of your edit collection form to save the entire collection with this newly added journey.
You have now created your first journey.
For more step-by-step instructions with images, view our https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/journey-creation-process.md runbook
•	Can we test a collection (environments) before it is published?
Yes, you can test environments in a collection by adding a user/tester as a collaborators to the collection and leave collection status in “draft”
Additional details in https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/testing-collections-before-launch.md
•	What if a Business Partner does not want to contribute content on ITZ because they don’t want the competitors see what they are doing?
This is not a problem. Business Partners can create their own collections and leave them in a status of draft if they do not want other partners or IBMrs to see their resources and environments. If they want only specific people to be able to access their collection, they can add them as collaborators to the collection.
•	How do I transfer my collection to another user?
Here are the steps on how to transfer a collection:
1.	Go to “My Library” tab on the top of IBM Technology Zone > Click “My created resources” from the dropdown options.
2.	Locate the collection you would like to transfer and click on the tile to navigate to the edit collection form.
3.	Scroll down to the Owner field and input the new email of the person you would like to transfer this collection to.
4.	Click "Save".
5.	Allow time for the collection fields to update through the cache layer of Technology Zone and have the new owner check their “My created resources” page to confirm the transfer was a success.
Additional questions? Contact the IBM Technology Zone support team via email: mailto:techzone.help@ibm.com
•	What is the turnaround time for an inquiry I post in Open a Case or Email: techzone.help@ibm.com?
https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.comt are monitored by support staff. Inquiries are addressed the same day as they are posted. If level one support cannot answer the inquiry themselves, they will escalate to SMEs who can respond and/or fix the issue. This escalation process is automated and issues are captured in GitHub for developers to manage as part of their development priorities. SLAs and services are posted in the Help section of the site.
•	Are there existing demos I can leverage?
Yes, Platinum content is considered the highest quality offerings on the site today and there is one Platinum Live Demos collection per IBM Technology brand. You can access Platinum content from the Platinum or Featured tab on the home page. As well, you can contribute to an existing Live Demos collection by following the instructions in the https://ibm.box.com/s/5oc5vww7j5pf9w9r7e5tgvsrcev7t7x6.
•	How do I give feedback on a collection?
1.	Use the star ratings option found at the top of each page to rate the collection.
2.	Add a comment at the bottom of the page for others reviewing this content to see.
3.	Email the Content Author directly by using the help icon at the top of the page.
•	How can I give feedback because content is wrong?
Contact the Content Author directly by selecting the help icon located at the top of the page. This will either direct you to a slack channel that the author has set up to support this content or an email modal will pop up to allow you to email them directly from the site.
•	Is there a mandated time to respond to content support inquiries?
Content Contributors are responsible for supporting and maintaining their assets in the portal. There is no mandated timeline for response. If you have not received a response within an acceptable timeframe, it is suggested that you escalate your concerns to their Blue Pages manager.
The portal is supported via a community moderated Slack channel where Subject Matter Experts (SMEs) are mandated to respond in a timely manner. The https://ibm.box.com/v/dte-support-slas for support can be found under the Help page menu.
•	Who do I contact if something is broken on the site?
You should initially check the https://w3.ibm.com/w3publisher/dte-cms-guidance/dte-platform-support to ensure there isn’t a planned outage. If not, report this by creating a support case by click on the https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or sending a mail mailto:techzone.help@ibm.com.
•	How can I request content to be added to a Platinum collection?
To request a demo be added to an existing Live Demos Platinum collection:
1.	Ensure your demo collection or resource(s) meet https://ibm.box.com/s/rw6lxuoor1q2vvrdy3r194a96bhwjt6u.
2.	Review the available Live Demo Collections to see if your resource and/or collection would help make that collection more robust.
3.	If yes, select the appropriate https://ibm.box.com/v/brand-squad-leads.
4.	Send the Product Squad leader an email with your request to add content to their Platinum collection.
5.	If approved, the Product Squad Leader will work with you to add your content to their Platinum collection.
6.	The Product Squad Leader will make you a Collaborator of that collection so that you can manage and maintain your resources. Your name will also show on the Live Demos Collection as a Collaborator.
•	I found broken links in a collection. How do I get them fixed?
Use the Ask for Help icon at the top of the page and post your concerns. This will be directed to the Content Owner directly or a community monitored Slack channel for action. If you do not receive any response, you can try contacting the Collaborators listed on the page or escalate to the Content Owners Blue Pages manager.
•	Can I see usage metrics for my content?
Yes, As consumers begin to search and curate content, Content Authors can view the following metrics to track content usage: pageviews, unique users, type of users (IBMer or BP), and region of user. To get started, review the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/content-metrics.mdrunbook.
•	How do I ensure the content URL I share does not change when sending to others?
We recommend using vanity URLs when sharing any content. When or if a URL changes, a vanity URL gives you the power to control where the user gets redirected. Start creating your custom vanity URLs https://snip.innovate.ibm.com/ and take control of any changing links.
•	How can I create a Collection?
All IBMrs and Business Partners can create a Collection. To create a collection, from the home page, select the Share your content button in the top right corner, then follow the guidance outlined in the submission form.
View this video on https://ibm.ent.box.com/s/r9ywt10xjl47d2sfmtk4gxtc2e07jhqh for more details.
•	How can I benefit from leveraging the IBM Technology Zone?
o	Option 1: You can build your own demo using our hosted environments.
o	Option 2: You can engage in a conversation with your customer in the discovery phase ("show" them vs. "tell" them).
o	Option 3: You can share the newly created demo for others to leverage and earn points towards big rewards!
•	How do I add to an existing Activation Kit?
If you would like to add to an existing Activation Kit, use the Ask for Help icon at the top of the Kit page to work with the Content Author.
•	Is there an API I can leverage for my upload of content?
Yes. You can access the API swagger documentation here https://api.techzone.ibm.com/swagger/.
Most API interactions will require an API token. Your API token is tied to your current SSO session and it can be acquired from the https://techzone.ibm.com/my/profile page.
Environments
•	How long can I reserve an environment for?
View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/reservation-duration-policy.md runbook to know more about the specific duration of reservation of specific infrastructures.
•	Why don’t all my environments show up at once?
Often the workload of these templates is rather large. Workshop Manager staggers the deployment of these environments so that by the time you’ve reached the start time that you requested, you will have the number of environments that you requested.
•	How do I extend my reservation?
Here are the simple steps to extend your reservation:
1.	Locate ‘My library’ on the top of the page > Click ‘My reservations’ in the dropdown options.
2.	Locate the reservation you want to extend and click on the 3 dots > Click 'Extend’.
3.	Select new date and time and click extend (Maximum extension: One week)
View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/extend-a-reservation.md runbook for screenshots of the step-by-step instructions.
If the “Extend” option is not available from the reservation tile options, you did not provide an opportunity number on the reservation. Edit your reservation to include a valid opportunity number.
For questions about the environment or support, reach out to the author of the collection.
•	What opportunities are valid when making a reservation?
Sales Cloud, Atlas, ESA, and soon to be Gainsite relationship IDs in Q3 2021.
•	What cost do I pay to get access to the environments on IBM Technology Zone?
IBM Technology Zone team bears all the costs of the environments you reserve on the site. All we ask is that you provide the valid opportunity code when filling out the reservation form so that we can show the impact of engagements that these environments are being used for. Soon 3rd party cloud environments will have an additional approval step for GEO market leader approval. This will free up capacity of 3rd party cloud environments for only top priority client opportunities. If you have additional questions please contact: mailto:brooke.jones@ibm.com
•	What is the min/max number of multiple environments allowed?
The min number of environment's is 5 (Five) while max number of environments depends on the template size and resource availability.
Example: Template less than 1 TB maximum 70 environments, greater than 1TB maximum 20 environments, greater than 4TB maximum 8 environment and greater than 10TB maximum 5 environments.
•	How do I delete a reservation?
Here are the simple steps to delete your reservation:
1.	Locate ‘My library’ on the top of the page > Click ‘My reservations’ in the dropdown options.
2.	Locate the reservation you want to extend and click on the 3 dots > Click 'Delete’.
3.	Confirm your action by entering the value shown in bold (you can select the copy icon to copy and paste) and selecting 'Delete’. Your reservation will be automatically deleted.
View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/delete-reservation.mdhttps://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/extend-a-reservation.md runbook for step-by-step instructions.
For questions about the environment or support, reach out to the author of the collection.
•	How do I transfer my reservation to another user?
Here are the steps on how to transfer a reservation:
1.	Go to "My Library" tab on the top of IBM Technology Zone > Click "My reservations" from the dropdown options >
2.	Locate what you would like to transfer and click on the 3 dots > Select 'Transfer' from the dropdown.
3.	Enter the IBMid to transfer to and enter the resource name. Note: all fields have to be field for "Transfer" to turn red.
4.	Click on "Transfer".
5.	The resource will now appear in the 'My reservations' of the person you transferred it to.
View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/transfer_environment.mdhttps://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/extend-a-reservation.md runbook for step-by-step instructions.
For questions about the environment or support, reach out to the author of the collection.
•	Why have my environments not been provisioned?
Environments are provisioned at least 2 hours before the requested start date and time
•	How can I request multiple environments for group reservations, group engagements or workshops?
Group reservations, group engagements or workshops can be scheduled on IBM Technology Zone using the “schedule a workshop” feature which allows you the ability to request multiple environment using the Workshop Manager tool. On a Workshop Manager request, you may select the desired environment, specify the number of environments and attendees, and choose the start and end dates. You can also save draft requests for later.
At this time, workshops support VMWare, IBM Cloud, SaaS, and Hosted environment requests.
For more information about requesting a multiple environments for group reservations, group engagements or workshops, view the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/How-to-schedule-a-hosted-workshop.md runbook.
(https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/How-to-schedule-a-hosted-workshop.md)
For more information about the maximum number of environments, view the https://github.com/IBM/itz-support-public/blob/eaf03a72d78dc771c0b46d6c3404b230d8edb2c4/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/reservation-duration-policy.md runbook.
•	I asked for 15 environments and was told I’d get 15, why am I only seeing 7 right now?
Your workshop was set to autogrow**
**autogrow- is a feature where environments are automatically provisioned on a need base until the maximum number of environments have been deployed. Once you start to claim environments, as fewer become available, more will begin to deploy automatically until you have the full number of environments that you requested.
•	How do I catalog an environment?
Here are the steps to cataloguing an environment:
1.	Navigate to the resource that is cataloging the environment you want to reproduce.
2.	Click on the resource > It will take you to a Box Folder url where you will find an image/screenshot of the environment settings.
3.	Mimic the same environment settings as the screenshot to achieve your desired environment.
4.	To customize your environment further, view this https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/gitops-tf-override.md to learn how you can override your environment setting.
View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/catalog-your-environment.md runbook for step-by-step instructions.
For questions about the environment or support, reach out to the author of the collection.
•	What are some valid opportunity code to input on reservation form?
View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/valid-opportunity-codes.md runbook to learn how opportunity codes are validated and what systems/portals we work with to validate them when users are making a reservation.
For questions about the environment or support, reach out to the author of the collection.
•	How can I search for an environment?
View this video to learn https://ibm.ent.box.com/s/h8m5hvyr1ikexq8b3jfpdnxbvglnqgg2.
•	How do I update my reservation to enable the self-service extension option?
Here are the simple steps to extend your reservation:
1.	Locate ‘My library’ on the top of the page > Click ‘My reservations’ in the dropdown options.
2.	Locate the reservation you want to edit and click on the 3 dots > Click 'Reservation details'.
3.	Select the 'Edit' button from the reservation details page.
4.	Select the new purpose that you would like to update for this reservation.
5.	Include the opportunity code from IBM Sales Cloud or relationship ID from Gainsite.
6.	Select the 'Save' button to capture the changes to your reservation.
7.	Wait a few minutes for your changes to process, then return to the 'My reservations' page.
8.	Locate the reservation you want to extend and click on the 3 dots > and see now the 'Extend' option will not display after updating the reservation details.
9.	Click the 'Extend' button and extend the reservation one week out from today's date.
View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/extend-self-education-into-sales-demo.md purpose and opportunity code runbook for screenshots with step-by-step instructions.
Additional runbook option: View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/extend-a-reservation.md runbook for screenshots of the step-by-step instructions.
For questions about the environment or support, reach out to the author of the collection.
•	Can I request a Custom Environment?
Yes, you can request a custom environment using our https://ibm.biz/dte-environment-requests
This https://ibm.ent.box.com/s/8gx9dohzo0ie3sxfxm89ofs99x071b8z has instructions for making a request.
•	How can I extend my environment without an opportunity number?
You can extend your environment without an opportunity number by requesting an exception using our https://custom-requests.ideas.aha.io/ideas/new.
•	Can I template my reservations?
Yes, you can now create a template for your IBM Cloud Classic reservations.
•	How can I extend my environment outside the standard reservation duration policies?
If you require extensions outside the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/reservation-duration-policy.md, make use of our https://ibm.biz/dte-environment-requests
•	Can I recover a deleted environment?
We do not store backups for deleted environments, they cannot be recovered. Kindly ensure you extend your environments before they expire.
•	What environments require approval?
Not all but some Premium environments tab found from the https://techzone.ibm.com/collection/tech-zone-certified-base-images/journey-premium-aws-azure-roks: https://techzone.ibm.com/collection/tech-zone-certified-base-images/journey-premium-aws-azure-roks
o	ROKS environments and a select set of third part cloud environments like AWS and Azure. Not all go through an approval process so reference the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/approval-workflow.md on how to identify which environments require approval. These requests have a two day review process. https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/approval-workflow.md
Additionally, all workshop request must go through approval process and details on review process can be found in the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/reservation-duration-policy.md runbook. https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/reservation-duration-policy.md
•	I have an opportunity code, but I did not capture it on the initial reservation form. How do I get an extension?
Send an email to mailto:techzone.help@ibm.com with the opportunity code and the name of the environment that you reserved and need the extension on.
•	What if I do not have an opportunity code, but I know I will need the environment longer for my client engagement?
Send an email to mailto:techzone.help@ibm.com requesting an exception.
•	Where can I go to get support for an environment?
If the issue pertains to your particular environment, i.e., a particular program or command not working, then reach out directly to the content owner using the help icon located at the top of the IBM Technology Zone asset page. Whether IBMer or Business Partner, please contact us at mailto:techzone.help@ibm.com so that we can connect you to the correct individual for support.
•	How do I reserve an environment?
We suggest you leverage the https://techzone.ibm.com/collection/onboarding as there is a great self-help video outlining how to search and reserve an environment.
•	How many environments can I reserve, and for how long?
Each request is different in terms of the size of the environment, time requested, and what other events are planned during your requested time. For a very large environment such as Cloud Pak for Data, we cannot support more than 10 environments in a given region for up to 2 days. For smaller environments such as Cognos, we have the ability to support more than 20 for over a week.
Unfortunately, there is no set standard response to any given request, so we suggest limiting the number of environments and the amount of time you need them for your workshop. Please make sure to plan your workshop through Workshop manager tool before confirming dates with clients to ensure we have the capacity for the workshop.
•	Can I use customer data in an IBM Technology Zone environment?
IBM Technology Zone allows a select set of environments that will support specific classifications of customer data. For unsupported customer data classifications, self-generated data is recommended to avoid any PI/SPI data being injected into a Technology Zone environment. Dummy, fake, or sample data is allowed. For more information including exceptions, view the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/Customer-data on TechZone.md runbook.https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/Customer-data on TechZone.md
Supported Customer Data Classifications:
o	Publicly available (example of data available through the web is https://seti.berkeley.edu/listen/data.html)
o	Anonymized / Obfuscated / Masked
o	Non-PI
NOT Supported Customer Data Classifications:
o	No regulated data allowed. Regulated - PI, SPI, PCI, PHI, Financial Data, Other.
o	Governed by a plethora of global/federal/local regulations- GDPR, HIPAA, GLB, FTC, CCPA, Sarbanes-Oxley, + many others. Regulated data requires engaging Legal & BISO.
•	How can I get access to an environment and its related content?
From the Environments tab located in the top navigation bar, utilize the search to filter options that match your environment criteria. To see related content, select the title of the collection under the Collection column. This will take you to the content page where the environment and all related resources reside. If no additional resources are provided, you can use the Ask for Help icon at the top of the page to request further assistance from the Content Author.
•	What do I do when I get a certificate issue?
Follow this method to resolve this issue:
o	Run check-expiration.sh script to see if certs expired. Only then, run resetcert.sh
o	Run check-csr.sh to see if there are pending CSRs. Approve all the pending CSRs
o	Check nodes status using “oc get nodes”. Some nodes may be in “NotReady” state because of previous errors (pending CSRs). They are supposed to recover automatically and go into Ready state within 3-5 minutes. If this does not occur, try restating the environment.
If you are still having issues email https://techzone.ibm.com/techzone.help@ibm.com for further support or visit https://ibm-techzone.slack.com/archives/CTA2MV9AM slack channel so we can assist with additional troubleshooting.
•	What do I do when I have memory issues?
This is an issue that occurs with some Cloud Pak instances. It has been shown to resolve itself in time, but if you are still having issues after a significant amount of time please contact mailto:techzone.help@ibm.com for further assistance.
•	Where can I find the VM login credentials?
VM credentials can be found by clicking the “keys” symbol on the VM. See "viewing saved credentials " some Demo assets have their VM credentials stored in lab guides and documentation provided.
•	Can I get an IP for my environment?
No, public IPs are not allowed for environment access. Some VMs in environments have opened ports and can be accessed using published services. If ports are opened for a VM you will receive the details when the activation email was received.
•	How can I improve performance of my environment?
You can improve performance during Secure Remote Access (SRA) browser client session by
o	Using Google Chrome
o	Changing the display quality settings in the browser client toolbar
o	Reducing other connections that may be consuming bandwidth
o	Trying to improve your network connection.
See "Improving performance during a browser client session " for additional details
•	Does bandwidth and latency affect performance?
Yes, bandwidth and latency do affect performance. Run a quick "http://speedtest.skytap.com/" and learn about the results of your speed test by reviewing "https://ibm.box.com/s/38llr9rdxijhhloxc8hbv444uu2rdst5.” section for additional details.
•	How do I request a specific environment that is not listed on the IBM Technology Zone?
If you are looking for an environment option that the IBM Technology Zone does not have already on the site, submit your infrastructure request through https://itz-enhancements.ideas.aha.io/portal_session/new .
IBM Technology Zone
•	I have this environment and need to replicate in TechZone.
Please make absolutely sure that your environment or something similar doesn’t already exist in TechZone. There are over 700 technical assets available in TechZone today, built by SMEs and IBM product practitioners. If you are positive there’s nothing that can be used in TechZone, then you should consider porting your application into TechZone by leveraging a https://techzone.ibm.com/collection/tech-zone-certified-base-images.
Infrastructure
•	Why can’t I see my cluster in IBM Cloud web dashboard?
Sometimes users can not see their clusters in IBM Cloud web dashboard, so before leveraging support, run the following commands:
1.	Log in IBM Cloud via CLI: 
ibmcloud login --sso
2.	Select the account with this problem.
3.	Switch to 
itzroks
resource group: 
ibmcloud target -g itzroks
4.	List clusters: 
ibmcloud ks cluster ls
Now you should be able to see your cluster in the CLI and Web.
Follow the instructions in this https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/iam-fix.md to see your cluster in CLI and Web.
For any questions, contact ITZ support.
o	Business Partners - Contact ITZ Support - mailto:techzone.help@ibm.com
o	IBMers - Make a post on https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com
•	How do I change self-signed SSL certs for **CP4I** on ROKS?
Here are the steps to change your self-signed SSL certs for CP4I:
1.	Log in to your cluster with your IBMid.
2.	Switch to the Cloud Pak for Integration project (
cp4i
 by default).
3.	Extract ROKS ingress certificates to your local folder.
4.	Split CA and cert.
5.	Delete the IBM Common Services route certificate.
6.	Delete the IBM Common Services route secret.
7.	Create a new route-tls-secret from the extracted certs.
8.	Patch the Automation UI config.
9.	Delete the IAF CA certificate.
10.	Delete the IAF certificate.
11.	Delete the external TLS secret:
12.	Create a new external TLS secret from the extracted certs.
13.	Restart all auth-idp pods.
14.	Restart all ibm-nginx pods.
Now check if you check your Cloud Pak for Integration dashboard route, you should see valid ROKS SSL certificates.
The command lines for each step can be found in our https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/cp4i-certs.md runbook.
•	How do I share my ROKS cluster environment with another user?
Here are the steps to share a ROKS Cluster Environment:
1.	Go to "My Library" and click on "My reservations"
2.	Find the reservation that needs to be shared.
3.	Click on the three dots and select 'Share' from the dropdown options.
4.	Enter the IBMid you want to share your cluster with.
5.	Click on "Share" blue button
The cluster will automatically become available to the another user on IBM Cloud.
View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/share_environment.md runbook for step-by-step instructions with screenshots.
•	How do I upgrade configurations on my reserved environment?
Here are ways you can upgrade your environment’s configurations:
o	Adding VMs
o	[Adding worker nodes](itz-support-public/resizing-roks-cluster-worker-pool.md at main · IBM/itz-support-public)
o	Adding storage
To make any of these upgrades, follow the runbooks or request help from ITZ support:
A Business Partner can leverage: mailto:techzone.help@ibm.com
An IBMer can leverage the slack channel: https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com
•	How do I report ROKS Issues?
Please provide this information to support to help speed up the process:
o	Minimum Information Needed:
o	cluster name or cluster ID
o	environment/reservation owner if not yourself
o	short description of the issues
o	Additional information if related:
o	worker name or IP address if you need help reloading or rebooting a worker
o	cloud pak name if the issue is related to a cloud pak install or usage
o	user name/id if the issue is related to acess
Business Partners - Contact ITZ Support - mailto:techzone.help@ibm.com
IBMers - Make a post on https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com
•	How do I resize my ROKS cluster worker pool?
View https://github.ibm.com/dte-support/private/blob/master/IBM-Cloud/ROKS/resizing-roks-cluster-worker-pool.md runbook for step-by-step instructions.
•	How do I change self-signed SSL certs for **CP4D** on ROKS?
Here are the steps to change self-signed SSL certs for CP4D:
1.	Log in to your cluster with your IBMid.
2.	Switch to the Cloud Pak for Data project (
zen
 by default):
3.	Extract ROKS ingress certificates to your local folder:
4.	Create a new external-tls-secret from the extracted certs:
5.	Restart all ibm-nginx pods:
Now you should be able to check Cloud Pak for Data dashboard route and see valid ROKS SSL certificates.
For more details, check out our https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/cp4d-certs.md runbook.
•	How do I add an ODF/OCS storage cluster to a ROKS cluster?
Please contact our support team for https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.como to increase your storage cluster. Disclaimer: At this time, this is only available for ROKS on VPC. Increasing storage cluster for ROKs on Classic is not supported.
View the https://github.ibm.com/dte-support/private/blob/master/IBM-Cloud/ROKS/adding-odf-storage-cluster-to-roks.md runbook for additional help and clarification.
•	I'm having trouble setting up/cataloging an environment, can anyone help?
For any questions or concerns pertaining to setting up or cataloging an environment, reach out to the content author on the collection for help.
•	Can I share my environments/reservation?
Yes, you can share your environments with an IBMr, Business Partners or Client. Additional information on "https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/share_environment.md"
•	I persist MVP workloads for a client that purchases IBM Cloud?
a commercial POC account free for up to 90 days utilizing the following instructions, https://ibm.box.com/v/commercial-poc-process
•	Can memory be added to the nodes of an existing cluster?
No, memory cannot be added to the nodes of an existing cluster. Worker memory is fixed based on “flavor” of the node.
Workaround
1.	Add more worker nodes to your existing worker pool, detail on how to can be found [here](itz-support-public/resizing-roks-cluster-worker-pool.md at main · IBM/itz-support-public)
2.	Create a new worker pool with a flavor that has more CPU and memory
•	How to accept an IBM Cloud invite?
To accept an IBM Cloud invite, you can accept it through your email or through your IBM Cloud account.
To see the step-by-step instructions (with screenshots) of these two ways of accepting an invite, view our https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/ibm-cloud-accept-invite.md.
•	Can I transfer my environment/reservation to another user?
Yes, you can transfer an environment/reservation to another user. Guide on "https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/transfer_environment.md?
•	Can I provision clusters directly on IBM Cloud?
No, clusters cannot be provisioned directly from IBM Cloud, you will need to select from our wide variety of https://techzone.ibm.com/environments on IBM Technology Zone.
•	Are there token limits for Watsonx.ai?
No there are no limits, if you are hitting a limit for a TechZone reserved environment you may be pointing to a WML service in your personal IBM cloud account. Learn more in the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/watsonx_troubleshooting_guide.md
•	I need to provision an OpenShift Container Platform (ROKS) environment to validate a client scenario. How can I get access to this?
IBM Technology Zone does have OpenShift options available, labeled as ROKS infrastructure options. Select the ‘Environments’ tab located in the top navigation bar and select the ‘Infrastructure’ filter drop down to filter on ROKS specific options. Select the blue desktop icon located to the right to start your reservation request.
Known Issues
•	I got an IBM ID Sign in Error, can anyone help?
Check to see if there is an IBMid outage:
1.	Refer to the IBMid status page: https://w3.ibm.com/w3publisher/ibmid-home/ibmid-service-status
2.	Additionally see the IBMid outage history page: https://w3.ibm.com/w3publisher/ibmid-home/ibmid-outages-history
3.	If there is an outage, create a ticket from the IBMid support page: https://w3.ibm.com/help/
If you are still having issues signing in, c****ontact the IBMid helpdesk for support:https://www.ibm.com/ibmid/myibm/help/us/helpdesk.html
Additional resource for IBMers to contact IBMid support team on slack: https://ibm-cio.slack.com/archives/C0MBSS9SA
•	How do I fix an internal server error?
Cause: VMware on IBM Cloud-associated template has been retired or deleted.
Resolution: Verify the status of the resource/collection with ITZ Support.
Business Partners - Contact ITZ Support - mailto:techzone.help@ibm.com
IBMers - Make a post on the https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com
View our https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/Internal-server-error.md runbook to double-check that the error message you are seeing corresponds to the one in our runbook.
•	I couldn’t get the requested template, can anyone help?
Cause: VMware on IBM Cloud associated template has been retired or deleted
Resolution: Verify the status of the environment with ITZ Support
Business Partners - Contact ITZ Support - mailto:techzone.help@ibm.com
IBMers - Can https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com
•	How do I fix a network error when attempting to fetch resource?
Cause: A timeout or a failure to communicate with the back-end servers like reservations, database, auth, or even the DTE2 api server
Resolution: Clear cache and retry the reservation
View our https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/NetworkError-when-attempting-to-fetch-resource.md runbook to see if the error you saw corresponds with the screenshot in our runbook to properly diagnose the issue.
•	I got a “Reservation: Not a Production Template” error, can anyone help?
Cause of error: The template associated with the collection has not been onboarded.
Resolution: Contact ITZ support:
Business Partners - Contact ITZ Support - mailto:techzone.help@ibm.com
IBMers - Make a post on the https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com
•	Why doesn’t the ‘Reservations’ option display on my collection options list?
Answer: ‘Reservations’ option will only display if there is an environment catalogued on your collection.
Here are the steps to check:
1.	Select the collection edit button
2.	Scroll down to the Environments section to see if there are any environments catalogued on this collection.
o	If there are no environments catalogued on this collection that need to be, please use the ‘Create an environment’ runbook for next steps on how to add an environment to your collection.
o	If there is an environment catalogued on this collection, then please contact support with the collection URL so we can create an issue and further investigate this issue.
•	Why are no reservation metrics displaying after selecting the ‘Reservations’ option?
Answer: Reservation metrics are captured from environments that are catalogued on a collection and the provisioning pipeline has to be one that IBM Technology Zone team currently supports. If you have an environment catalogued on your collection that is of infrastructure type: Systems Redirect, or Hosted Redirect then please note that these environment options are merely a redirect to another site where then the reservation is to be provisioned from. As we consolidate additional environments from CECC, ISCEP, SCS and more these metrics will start to display on your collections once they are reserved directly from an IBM Technology Zone collection.
Here are the steps to check:
1.	Select the collection edit button
2.	Scroll down to the Environments section
3.	Select an Environment to see the ‘Infrastructure’ field.
o	If you have an environment catalogued as one of the infrastructure redirect types and would like to know when the environment is planned to be migrated, please contact mailto:brooke.jones@ibm.com. We are currently working with CECC, ISCEP, SCS and SBaaS portals to consolidate environments to IBM Technology Zone.
If you have an environment that is not of the infrastructure redirect types, as mentioned above, then please contact support as there might be an issue with how the environment is catalogued or there could be issues with the environment itself not taking reservations.
Navigation & Features
•	What is a collection?
A collection is a group of related resources. It may include multiple collections and is owned by the contributor.
View https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/techzone-content.md runbook to learn more.
•	What is the difference between Bronze, Silver, Gold and Platinum Content?
Tiles are branded as Bronze, Silver, Gold or Platinum to differentiate content based on different quality standards. As you level-up, so does the quality of the content. NOTE: Bronze, Silver, and Gold allocations are part of the crowdsourcing model and can be allocated by the contributor with the below standards as guidance. Platinum content is currently only provided by Bob Kalka’s Product Squads and Eddie Daghelian’s Activation Kit teams. We are opening up the ability for crowdsourced content to become Platinum in September.
Bronze - Buyer Beware (may not be current and/or supported), grouped resources facilitating experiential activity, may be IBMer only
Silver - Buyer Beware (shared ‘as is’ without any testing or vetting), author supported (best effort to respond), use case driven, may have a reservable environment, may have a defined journey, should be Business Partner accessible
Gold - Author or community supported (24 hours to acknowledge), guided demo script, FAQ and/or troubleshooting guide, reservable environment, defined journey, community reviewed & tested, must be Business Partner accessible
Platinum - Community supported via Slack (same day acknowledgement), lead-with or growth offering, IBM Cloud reservable environment, utilizes most recent version release, technical review & sign off by a product squad member, reviewed & updated every 30 days, approved by Technical Sales brand executive
•	How do I find collection resources related to an environment reservation?
There are three easy ways to navigate to an environments collection of resources:
1.	Finding collection of resources before reserving by navigating to the environment tab.
2.	Finding collection of resources when filling out reservation form by selecting "Related Collection" in the top right banner.
3.	Finding collection of resources after you have already reserved the environment by navigating to "My Reservations" page and clicking on the ellipsis of the reservation card and click "View Collection"
View the following runbook https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/reservation-collection-linkage.md for step-by-step instructions.
•	Where can I find the existing GitOps patterns?
All IBMers can access our existing gitOps patterns https://github.ibm.com/dte2-0/ccp-gitops-patterns.
•	When can we expect enhancement requests to be reviewed and implemented?
Enhancements requests submitted through our https://itz-enhancements.ideas.aha.io/portal_session/new are reviewed weekly. Depending on the request and difficulty will depend on turnaround time. Our team will be putting an enhancements roadmap together in Q3 so that idea submitters can see when we plan to implement their request on the site. If you have questions about the process or want a status update on an idea you submitted, please contact mailto:brooke.jones@ibm.com.
•	How can I view the metrics of my collection?
View this https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/content-metrics.md to learn how to view environment reservation metrics tied to a collection on IBM Technology Zone.
•	How do I find collections with Technical Decision Points?
You can find them by clicking on the first journey on the IBM Technology Zone home page. You can also find them by filtering your search by clicking on “Show Advanced” and then locating the “Technical Decision Points” category.
•	How do I search for Platinum content?
There are two ways you can browse through Platinum Content:
1.	Locate the “Platinum” tab on the IBM Technology Zone banner.
2.	On the “Environment” page there is a button "Advanced Filter", navigate to the “Contributor Flags” option and click the option "Platinum".
•	How do I get content support?
Content Support for all Collections, resources and environments are handled by the Content Author.
To report/log a content issue follow steps listed below.
1.	Go to the Collection/resource > Click on the Question Mark “Ask for help” > Select the “Ask for help or report a problem with the content on this page”
2.	Fill out the form with details and click send. This will go directly to the content author, collaborators or the support contact listed for the collection/resource.
Note: By clicking on the “Ask for Help” button for some collection/resource instances, this will direct you to slack channels for support.
View this https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/ContentSupport.md for step-by-step with screenshots to learn how to leverage content support.
•	What is a Hands-on Lab?
It’s a set of tasks with included steps that users follow to review or build a use case. Targets pre-sale situation, which typically require reservation of an environment.
Disclaimer: The term "Hands-on Lab" has now been retired and the correct term is "live environment". This update will soon be applied across all IBM Technology Zone.
•	What is TechZone Deployer?
IBM TechZone Deployer or Technology Zone Deployer is a complementary system that works together to enable technical sellers to build and deploy IBM software quickly and easily. Deployer also enables Technical sellers to use the same automation technology in both TechZone and customer infrastructure. Additional details can be found https://pages.github.ibm.com/skol/itz-deployer-docs/
•	What is a resource?
A resource is a discrete piece of content used in a collection. A collection is made up of multiple resources.
•	How do I know what permissions I have as an IBMer?
All IBMers have default permission to create a collection and view technical content on the site.
•	What is a journey?
A journey is simply a tab. For example, the tabs inside a collection are called journeys as they essentially help guide users through the content.
View the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/intro-collection-journey.md runbook to learn more about them.
•	How do I search for technical content?
We suggest you leverage the https://techzone.ibm.com/collection/onboarding as there is a great self-help video outlining how to effectively search for content.
•	What is an Activation Kit?
Activation Kits are collections with predefined tabs, tied to products and solutions defined by brand technical executives and may be aligned to a Technology Decision Point (TDP), that consolidates and organizes other Technology Zone collections, as well resources, from multiple repositories so that technical go-to-market teams and the Business Partner ecosystem can "show", progress client opportunities, and implement solutions.
•	What is a bookmark search?
A bookmark is used to save a search, as it saves any keyword or filters. Leverage the https://techzone.ibm.com/collection/onboarding to watch a self-help video outlining how to use this feature and others on the site.
•	How can I find out about site outages, announcements, and/or important news about IBM Technology Zone?
Join the https://ibm-dte.slack.com/app_redirect?channel=itz-techzone-announcements Slack channel for all things IBM Technology Zone. From news, announcements, roadmaps, webinar events, user surveys, contests, and more. The announcements channel is your one-stop shop!
Check out other https://ibm.box.com/s/so63jezi3xmiwl56enn0vh4ghaq2beyc our team has in place today and their purpose breakouts. The list includes: https://techzone.ibm.com/notifications, https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com, https://ibm-dte.slack.com/app_redirect?channel=itz-workshop-support, home page banner, and home page alert.
•	How can I request an enhancement or redesign for IBM Technology Zone?
As an IBMer, you can use the https://itz-enhancements.ideas.aha.io/portal_session/new to log any enhancement or redesign requests.
Workshop
•	Can you use Workshop Manager to run a workshop for a client?
You can reserve multiple environments for internal or external workshop opportunity. External meaning for a  customer engagement. All we ask on the workshop request form is for the opportunity code and customer names associated with this request so that we can prioritize capacity accordingly. All customer will need to have an IBMid to access the student page once the workshop has been scheduled. The student page will allow customers to see the environment they are assigned to and other workshop details, like start date, end date, and description of the workshop.
•	Where can I get help for “Content”, “Application” relating to my environments requested through Workshop Manager?
Reach out to the Content Author on IBM Technology for all inquiries related to the content, product, and application.
•	How far in advance should I submit a Custom/ new VM template request?
If you need to go this route, do so well in advance of your workshop. We suggest at least 2 weeks out.
•	How do I extend my workshop reservation?
For IBMers Make use of https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US, for Business Partner Email: mailto:techzone.help@ibm.comto request extensions. When making an extension request please provide the following information
1.) Opportunity number 2.) Presale or postsale 3.) Your role (techsales, CSM, etc).
Note: extensions are granted based on resource availability and should be requested before the scheduled end date/time. Expired workshops cannot be extended.
•	What infrastructure does Workshop Manager support?
VMware, Hosted, and IBM Cloud environments today are an option to reserve multiple of for a workshop setting. If you have a workshop and need another template on another infrastructure, please fill out the custom request form with the dates that you need the environments for and how many. Our team will review the request based on capacity and budget to support this request and upon an approval can put aside capacity for your environments for your upcoming workshop. Please start with this https://ibm.biz/dte-environment-requests.
•	How long can I request a workshop for?
The maximum durations for requesting multiple environments is 5 days. Some durations are shorter depending on the template size and resource availability.
•	How soon in advance should I make a Workshop request?
All workshop request needs to come in at least 7 days before the required start date and time.
•	How does the Student get their environment?
Students make use of the student url sent to them by their instructor. They will need to enter their IBM ID (email) to claim an environment. Note: Instructors receive the “Student url” via email or can view it using the instructor url.
•	Why was my workshop environment shutdown?
Environments are set to shut down when idle for 180 mins/3hours. This can only be selected when making a request
•	What do I do when I have memory issues?
This is an issue that sometimes comes across in some Cloud Pak instances. It has been shown to resolve itself with time, so we ask that you be patient.
•	Where do I find my reserved Workshops?
You can find requested Workshops in “My library” tab on the IBM Technology Zone page, click on “My Workshops”.
•	Where can I get help for Workshop Manager?
Contact the support team https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com for all Workshop Manager help/inquiries.
Business Partners can report the issue using https://techzone.ibm.com/techzone.help@ibm.com
Support Hours - 24/7.
•	My Workshop was rejected what do I do?
Requesters are sent details for why their workshop was rejected and what is required to have it approved via https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or Email: mailto:techzone.help@ibm.com
Business Partners - Contact ITZ Support - mailto:techzone.help@ibm.com
•	If a workshop needs to be rescheduled, will it still be subject to the 72 hour lead time?
Yes, we need 72 hours notice to ensure we have capacity available for your workshop. Please contact support as soon as you have a shift in schedule so that we can work to the best of our ability to get you the environments you need based on capacity we have at that time.
•	How do I manage my workshop as an Instructor
You manage your workshop directly from the “My Workshop” page. See box folder https://ibm.box.com/s/o4879elzfn78pa6x6fvzj7hcbaninssa
•	Can additional instructors be added later to a Workshop?
At this moment, additional instructors can be added by yourself up till the workshop is approved. If you would like to add an additional instructor after that time, please contact support with the email of the instructor that you would like to add.
•	Workshop Manager Support
Workshop Manager allows you to reserve multiple instances of a demo environment for your internal and client needs. Workshop Manager provides the ability to schedule your environments in advance to ensure they are available and ready to use. As the Workshop owner, you will have the ability to manage your environments, including starting, stopping, or adding more as needed. Leverage our 24 x 7 Support IBMers - Click on https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US to create a support case, runbook on “How to Open a Case” can be found https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/open_case_web_internal.md
Business Partners - Contact ITZ Support - mailto:techzone.help@ibm.com
•	How do I request a Workshop on IBM Technology zone?
Leverage the “Request multiple environments for workshop” option on the “Create a reservation page”. Go to the “Environments” tab on the IBM Technology Zone Page, Search for the required resource and click “reserve”
•	Who can request a workshop using Workshop Manager?
IBMrs are the only users that we currently support with Workshop Manager at this time. IBMrs can request workshops on behalf of business partners or setup a workshop to do enablement sessions with business partners, but business partners accessing the site will not see the request or schedule a workshop option today.
•	I have submitted my workshop what next?
Workshop request are reviewed (approved/rejected) within 72 hours from when they where submitted
•	How do I onboard an environment to be used for Workshop Manager requests?
To onboard a template at this time, please fill out our https://custom-requests.ideas.aha.io/ and provide the template information that you would like onboarded. Select the request type: Template onboarding request. Our team will review and upon approval work with you to determine next steps on how to catalog the environment to the site.
•	I have multiple instructors how do I give them access?
Add all required instructors to the required instructor email field which can be found in step 4: "workshop information".
•	How do I manage my Workshop?
You manage your workshop from the “My Workshop” tab. Select the Workshop Name from the list to see Information details.
•	How to schedule a Hosted workshop?
Here are the steps to schedule a workshop:
1.	From the IBM Technology Home page > Click ‘Environments’
2.	Filter for the desired Infrastructure (Hosted)
3.	Find the environment you would like to use for your workshop > Click on the ‘Reserve’ icon
4.	Select ‘Schedule a workshop’ > You will be taken to the “Request a workshop” page.
5.	After going through each step filling out your workshop details > Click Done.
For Hosted: For more details and instructions, view our https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/How-to-schedule-a-hosted-workshop.md runbook.
•	When does my workshop get approved?
Workshop request are reviewed (approved/rejected) within 72 hours from when they were submitted
•	Why have my workshop environments not been provisioned?
1.    Environments are provisioned at least 4 hours before the requested start date and time
•	Can a Business Partner "Schedule a workshop"?
No, that option is not available to a Business Partner
•	Can infrastructure be physically isolated once the resources are reserved for a specific workshop?
If the resources are for a workshop the workshop owner should have capacity dedicated to them for their customer facing purpose. TechZone cannot provision an entire bare metal server for every user.
•	How do I request extensions?
 IBMers should open a mailto:Open a case, and Business Partners can report the issue using Email: mailto:techzone.help@ibm.com for support to request extensions. Note: Opportunity numbers or valid use cases are required for all extension requests. Extensions are also granted based on resource availability.
•	How to enable an IBM Cloud environment for workshop requests?
Workshop Manager can now manage requests for IBM Cloud environments, but not all IBM Cloud environments are enabled today.
IBM Cloud environments enabled for workshop requests today: https://techzone.ibm.com/collection/custom-roks-vmware-requests collection
o	Managed OpenShift cluster (ROKS) in IBM Cloud (“classic infrastructure”) with NFS
o	Managed OpenShift cluster (ROKS) in IBM Cloud on VPC Gen2 infrastructure with ODF (OCS) support.
To request an additional IBM Cloud environment that is live on IBM Technology Zone today to allow for workshop requests, please reference the https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/enable-ibmcloud-workshop.md documentation to understand the request and testing process needed before enabling a new IBM Cloud workshop request option.
•	How can I request multiple environments for a workshop?
Leverage the “Schedule a worksop” option on the “Create a reservation page”.
Go to the “Environments” tab on the IBM Technology Zone Page, Search for the required resource, click “reserve” and Schedule a Workshop
•	When trying to submit the workshop request form I get this error: “Error submitting Form”. What should I do?
There are two common reasons why this error is showing:
o	Duplicate title – If you or someone else has already used the very same title of your workshop before, then the form will not submit. Add a unique identifier to your title (perhaps date, customer, etc.) to resolve this.
o	Not logged in - Make sure you are logged into the IBM Demos site. Try adding /logout to the end of the URL and log back in.
If none of these resolve the issue, IBMers should open a mailto:Open a case, and Business Partners can report the issue using Email: mailto:techzone.help@ibm.com  for support.
How can we help?
Please review the listed support resources before opening a case:
Infrastructure Support Resources
•	Self-service support - Leverage our https://github.ibm.com/dte-support/public library for documentation and troubleshooting guides
•	Site issues - Click https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US or email: mailto:techzone.help@ibm.com
•	System Status - Think something is down? Check the applicable status pages for current updates https://techzone.status.io/, https://cloud.ibm.com/status (ensure you are logged into IBM Cloud) and https://ibm-dte.slack.com/archives/C09EJRGHH
•	Enhancements, Feedback, Feature Requests - https://ibm.biz/techzone-enhancements
•	Custom Request (Proof of Concept, Project Template onboarding, New infrastructure) - fill the custom request https://techzone.ibm.com/my/reservations/create/654ea5837958d10017a0bccc This https://ibm.ent.box.com/s/8gx9dohzo0ie3sxfxm89ofs99x071b8z which is IBMer only will provide instructions on custom requests
•	Content Metrics - Click on https://ibm.biz/itz-content-metrics to report on your collections, resources, and environments. Leverage the "https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/content-metrics.md" runbook for additional guidance.
•	Reservation Duration Policy - Click here to view https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/reservation-duration-policy.md
Content Support Resources
•	Onboarding - leverage the https://ibm.biz/techzone-onboarding collection for helpful how-to videos and guidance
•	Collections & Activation Kits - Contact the Author by clicking on the Ask for Help icon at the top of the page
•	Live Demos Platinum Collections - utilize the Ask for Help icon on the page to be routed to the brand’s Slack channel
•	https://techzone.ibm.com/terms
Didn’t find what you are looking for?
Click on https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US to create a support case, runbook on “How to Open a Case” can be found https://github.com/IBM/itz-support-public/blob/main/IBM-Technology-Zone/IBM-Technology-Zone-Runbooks/open_case_web_internal.md

"""

def gettoken(key):
    url = "https://iam.cloud.ibm.com/identity/token"

    payload = 'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey=' + key
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    data = json.loads(response.text)
    # print(data['access_token'])

    access_token = data['access_token']

    return access_token


def callwatsonx(question, model):

    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    token = gettoken(key=cloud_apikey)

    prompt = f"""first identify the language the question is in.
    after identifying the language answer the user question in that language using the context between <<<>>>.
    answer must be short and accurate according to the context. If answer can not be provided with the context just say "I do not know"
    
    <<<{context}>>> 
    question: {question} 
    answer:"""

    payload = json.dumps({
        #"model_id": "google/flan-t5-xxl",
        #"model_id": "meta-llama/llama-2-70b-chat",
        #"model_id": "google/flan-ul2",
        "model_id": model,
        #"model_id": "mistralai/mixtral-8x7b-instruct-v01",
        #"model_id": "ibm/granite-13b-chat-v1",
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "min_new_tokens": 1,
            "stop_sequences": ["\n", "/n"],
            "temperature": 0.5,
            "repetition_penalty": 1
        },
        "project_id": watsonx_projectid
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    #print(payload)
    for i in range(0, 10):
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            break
        except Exception:
            print("retrying call watsonx.ai ....")
            time.sleep(0.2)
            if i == 10:
                print("too many attempts, killing app")
                exit()

    print(response.text)
    data = json.loads(response.text)
    #print(data['results'][0]['generated_text'])
    res = {'watsonx_answer': data['results'][0]['generated_text']}
    rta_generada = data['results'][0]['generated_text']

    return rta_generada


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
