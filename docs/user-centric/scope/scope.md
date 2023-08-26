## Scope Plane - Features and Capabilities

In this plane, we must approach decisions with realism and give careful consideration to the features we plan to implement. As we brainstorm, it's crucial to remember that we have less than two weeks for the first iteration of our Minimum Viable Product (MVP). Time, technology, and expertise will all significantly influence our final decisions.

It's important to note that in Agile Development, nothing is set in stone. Our estimations are flexible, and they can evolve, either increasing or decreasing. We remain open to adjustments throughout any stage of the development process.

Luckily, we are utilizing the **Django framework**, which embodies the philosophy of 
??? quote "For perfectionists with deadlines"
    - Visit [Djangoproject](https://www.djangoproject.com/)
This framework equips us to develop a functional application in an impressively short amount of time.

## Criteria & Objectives
For this iteration, our decisions on features and functionalities are guided by the following criteria and objectives:

??? abstract "Table: Criteria and Objectives"

    | Condition                     | Iteration                                                          | Goals                         |
    |------------------------------|--------------------------------------------------------------------|-------------------------------|
    | MVP Version                  | Display digital products & services on the homepage<br>Sign in/up option<br>Purchase Product page<br>User Profile (roles)<br>Metrics for products<br>Search Bar & Filtering<br>Menu & Dropdowns<br>Social Media Login<br>Email Verification<br>User Feedback<br>Reviews & Comments<br>Cart, Purchase & Download<br>User & Admin Dashboard<br>Support Button<br>Contact Form<br>Request Formats<br>FAQ<br>Newsletter<br>RSS | Culture Acquisition & Tech Showcase            |
    | Simple design                | Contact Form<br>User/Admin Dashboard<br>FAQ<br>User Feedback<br>Previous features* |                 |
    | Low leading rates<br>& Non-functional | Social Media Login, Request Formats, Lottie Files                              | Long-term Investment<br>& Future Implementation |

- As illustrated in the table, the features specified under the **MVP Version** row are slated for inclusion in our development process. It's crucial to understand, however, that while these features will be fully functional and meet the essential criteria, their level of sophistication might not be the highest from an objective standpoint.

- For the **Simple Design** row, the elements listed are also pivotal for our project. However, they may not be given the same emphasis as the core functional features. This prioritization holds for all the features, as our main objective is to spotlight our cutting-edge technology while ensuring a top-notch user experience.

- As for the **Low leading rates & Non-functional** row, integrating the mentioned features will undoubtedly be challenging. We'll strive to incorporate them, but given our tight schedule, it's unfeasible to guarantee their inclusion. Nevertheless, they will be high on the list for consideration in the next iteration.

## User Stories

The following table is a well-equipped draft designed to facilitate the development process. Some user stories may be disregarded, while new ones may be added. This table has been motivated and fed by the results of the **design thinking**, **strategy plane**, and **scope plane**, as well as some elements of agile development philosophy.

- **User Stories:** 34
- **Total Points:** 150
- **Capability:** 20 story points per iteration/sprint
- **Sprint/Iteration Duration:** 1 day
- **Estimation:** 15 to 20 user story points per day
- **Total Duration:** 7.5 to 9 days

??? abstract "Scope: User Stories"

    | Theme | Epics | User Stories | Story Point |
    |-------|-------|--------------|-------------|
    | Homepage | Design Header | As a user, I want a clean, user-friendly header at the top of the page, so I can navigate easily and access the system's key features through the menu and dropdowns. | **2** |
    | | Arrange Mixed Products & Service Cards in Rows | As a user, I want a prominent 'Product & Service' section under the header, displaying a mix of 'products' and 'services' so I can quickly overview current entries. | **4** |
    | | | As a user, I want each card to display key product information, so I can click on what interests me. | **2** |
    | | | As a user, I want a 'see more' button under the 'Product & Service' section, so I can view expanded results on a separate page. | **1** |
    | | Present Product Cards in Rows | As a user, I want a 'Product' section below the 'Product & Service' row that showcases only products, enabling me to preview them. | **4** |
    | | | As a user, I want each card to display key 'Product' information, so I know what I'm clicking on. | **2** |
    | | | As a user, I want a 'see more' button under the 'Product' section, so I can view additional results on another page. | **1** |
    | | Display Service Cards in Rows | As a user, I want a 'Service' section below the 'Product' row, focusing exclusively on services, allowing me to preview them. | **4** |
    | | | As a user, I want each card to display key 'Service' information, so I understand what I'm selecting. | **2** |
    | | | As a user, I want a 'see more' button under the 'Service' section, so I can access further results on a different page. | **1** |
    | | Construct Footer | As a user, I want to see a footer at the page's end, granting me access to additional vital information, useful links, and legal data. | **2** |
    | Sign in/up & Dashboard | Link to Header | As a user or admin, I want a header link to 'sign in or sign up', allowing me to validate my login details on a separate page and access my dashboard. | **2** |
    | | Social Media Login | As a user or admin, I want the option to log in or sign up using a social media account, ensuring a secure and smooth interaction with the system. | **7** |
    | | Create User & Admin Dashboard | As a user or admin, after logging in or signing up, I want a useful dashboard with key stats & menu options relevant to my role, enabling secure and efficient system interaction. | **7** |
    | | Build User & Admin Profile Management | As a user or admin, I want a section on the dashboard where I can edit and manage my profile, maintaining control over my data and safeguarding my privacy. | **7** |
    | | Implement Verification System & Badge | As a user or admin, I want to verify my account via email to access the software marketplace. | **4** |
    | | Delete Account Option | As a user, I want the option to delete my account from the dashboard, preserving my privacy. | **4** |
    | Product & Service Management | Establish Admin 'Product & Service' Creation | As an admin, I want to create digital products & services from my dashboard and showcase them on the homepage, leveraging the software marketplace's potential. | **7** |
    | | Design Product & Service Page | As a user, I want a separate page detailing the product or service I click on 'Buy Now', enabling me to initiate the purchase process and access more detailed information not present on the homepage. | **7** |
    | | Enable System Feedback | As a user or admin, I want to receive success alerts or messages after certain system actions, like account creation or product purchase, enhancing my awareness of the actions taken. | **7** |
    | | Develop Product & Service Metrics | As a user or admin, I want visibility on product or service metrics, such as purchase counts, likes, and comments, both on the homepage and dedicated pages. This provides insight into the product's popularity and additional data. | **13** |
    | | Configure Role Visualization | As a user, visitor, or admin, I want a visual representation of my privileges based on my role, helping me realize the website's full potential. | **13** |
    | | Integrate Cart, Purchase & Download | As a user, I want to add products to my cart, experience a smooth payment process, and download the digital product immediately after payment, minimizing friction in my purchasing journey. | **7** |
    | | Develop Support Button | As a user, I want a support button on the product & service page that redirects me to a contact form with pre-filled information based on my prior selection, reducing repetitive input. | **4** |
    | Search & Filter | Develop Category Menu | As a user, I want a 'Category' menu to streamline my search for products & services. | **2** |
    | | Incorporate Search Bar | As a user, I want a search engine to pinpoint specific products or services. | **4** |
    | | Integrate Filter Function | As a user, I want a filter section on the same page, allowing me to sort by categories, price, license, ownership, etc. | **4** |
    | Reviews & Comments | Implement Reviews & Comments | As a user, after a purchase, I want to like and comment on my product or service, sharing my thoughts and contributing to the community. | **4** |
    | Accountability | Construct Contact Form | As a user, I desire a well-crafted contact page to reach the support team. | **4** |
    | | Implement Request Formats in Contact Form | As a user, I want predefined request formats in the contact form, ensuring effective communication of my ideas. | **2** |
    | | Assemble FAQ Section | As a user, I seek a FAQ section on the support page, offering videos or articles for troubleshooting or answering Plexosoft Marketplace-related questions. | **4** |
    | | Assemble Newsletter | As a user, I wish to subscribe to the site's newsletter with ease, staying updated with top offers, educational articles, and software news. | **4** |
    | | Integrate RSS Articles | As a user, I aspire to read top-quality articles from various sources within the marketplace, aiding my present and future decision-making. | **4** |
    | | Terms of Service & Privacy Policy (GDPR) | As a user, I want to easily access the terms of service & privacy policy (GDPR) pages, understanding my obligations and rights. | **4** |

???+ tip "Final User Stories"

    - The **Scope: User Story** is **NOT** the same as the [Final User Story](../../agile-development/agile_development.md) found in the **Agile Development** section.

Consequently, we've aligned our scope with the insights gathered from our research in the **Strategy** plane. It's clear at this stage that our goal is to implement a Minimum Viable Product (MVP) iteration. This will effectively assist us in laying the groundwork for our next phase, the **Structure** stage.
