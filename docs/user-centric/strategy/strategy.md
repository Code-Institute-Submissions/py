## Strategy Plane - Reason, Solution, and Value

In this phase, we analyze the data obtained from conducting 4 different interviews with individuals from diverse backgrounds. This time we included the author's opinions. These interviews have provided valuable insights into the general and specific aspects of a {==Software Marketplace==}.

Based on our findings from the {==Design Thinking==} process, we have reached the following conclusions, which will serve as our official source of information for Plexosoft's MVP:

- Although our users may not have had a complete understanding of their needs, we made every effort to comprehend their requirements and propose the best possible solutions.

- Recognizing that users are the key stakeholders, our primary focus is to create a platform that benefits both business professionals and future users.

- ??? info "Critical Concerns"
    - Clear Product & Service Descriptions.
    - Transparency, Trust-enhancing, Privacy & Security.
    - Solutions, Customization,  Distinct Offerings & Extended Services.
    - Affordability, Presentation, Accessibility & Performance.
    - Education, Inclusion, Opportunities, Peers Endorsement & User Reviews. 

To address these issues, we will tackle specific problems and fulfill their desires, enabling them to thrive within the ecosystem. For this iteration, we have identified the following core technologies to utilize:

- ??? info "Core Technologies"
    - Django
    - JQuery
    - Bootstrap
    - PostgreSQL
    - psycopg2
    - SQLAlchemy
    - Font Awesome
    - Lottie Files
    - Social Media Login
    - Stripe
    - Mailchimp (Newsletter)
    - Google Analytics
    - RSS
    - Allauth
    - AWS S3
    - EmailJS
    - Vendor-specific Templates

To address individual issues, tasks, or desires, please refer to the following resources (Design Thinking):

- [Conclusion](../../design-thinking/conclusion/conclusion.md)
- [Prototype](../../design-thinking/PoC/poc.md)


Our insights are grounded in sufficient research, supported by the accompanying table and graphic:

- From this table, we can extract the themes, epics, and potential ideas for user stories.

### Research Table

| Goals                                         | Relevancy (0-5) | Viability (0-5) | N. Items (0-~) |
| --------------------------------------------- | --------------- | --------------- | -------------- |
| Display Products & Labels on Homepage         | 5               | 5               | 1              |
| Search Bar & Filtering                        | 5               | 4               | 1              |
| Menu & Dropdowns                              | 5               | 5               | 1              |
| Product & Service Page                        | 5               | 5               | 1              |
| Sign in/up option                             | 5               | 5               | 1              |
| Social Media Login                            | 5               | 3               | 1              |
| Email Verification                            | 5               | 4               | 1              |
| Abstract User (roles, etc.)                   | 5               | 5               | 1              |
| User Feedback                                 | 5               | 5               | 1              |
| Metrics                                       | 5               | 5               | 1              |
| Reviews & Comments                            | 5               | 4               | 1              |
| Cart, Purchase & Download                     | 5               | 4               | 1              |
| User & Admin Dashboard                        | 5               | 4               | 1              |
| Support Button                                | 5               | 4               | 1              |
| Contact Form                                  | 5               | 4               | 1              |
| Request Formats                               | 3               | 4               | 1              |
| FAQ                                           | 4               | 4               | 1              |
| Newsletter                                    | 5               | 4               | 1              |
| RSS                                           | 3               | 4               | 1              |
| Caching                                       | 5               | 4               | 1              |
| Google Analytics                              | 4               | 4               | 1              |
| AWS S3                                        | 5               | 4               | 1              |
| EmailJS                                       | 4               | 4               | 1              |
| Lottie Files                                  | 3               | 5               | 1              |
| Terms of Service & Privacy Policy (GDPR)      | 5               | 4               | 1              |
| Database Model                                | 5               | 5               | 1              |
| N. Items                                      |                 |                 | 26             |
| Max. Points                                   |                 |                 | 130            |
| Results                                       | 121             | 112             |                |
| Percentage                                    | 93.07% (Strategy) | 86.15% (Scope) |               |

We've conducted an estimation based on our experience, and we are pleasantly surprised by the `design thinking` results. The decisions about which features to implement felt grounded in real factors and user needs, rather than personal assumptions or ideas:

- As indicated in the table and the graphic, most of the features have high relevancy for this iteration. An exception is the {==Request Formats==} feature, which received a '3' for relevancy and '4' for viability. the same for {==RSS==} and {==Lottie Files==} with '3' and '5' respectevely. These features could take various forms, and its style and functionality is subject to continuous changes to improve the user experience.

- Looking at the viability column, the most important features range from 4 to 5, which isn't a significant difference. This slight variation represents our ability to fulfill potential requirements within our time and resource constraints. The lowest score was {==Social Media Login==} with '3' due to the fact that this is an MVP and to be accepted by Google or Facebook may require extra features and formalities.

- Despite being powerful features, their full implementation might be constrained by our limited resources and time. However, we will strive to add functional aspects for each to meet the Minimum Viable Product (MVP) requirements.

We should highlight that achieving most of the features described above doesn't necessarily mean they are all perfect or that the development process has come to an end. On the contrary, this MVP is the foundation for a much more robust and reliable software marketplace.

### Research Graphic

![Research Graphic](../../assets/img/graph-1.png)

- **Relevancy**: As seen from the research graphic, there is a difference of '9' points between the maximum point value of '130' and the relevancy results. This suggests that we might be omitting almost the amount of 2 features, with each feature being 5 points, due to a lack of relevancy or the partial development of some features.

- **Viability**: As observed from the research graphic, there's a difference of '18' points between the maximum point value of '130' and the viability results. This indicates that we might be developing almost the amount of 3.6 features partially, with each feature being 5 points, due to a lack of viability.

- **Conclusion**: From the research graphic, there's a difference of '9' points between the relevancy and viability sections. This implies that roughly 2 features might be partially developed or that some features might not be fully completed due to constraints in resources and time. A gap of '9' isn't substantial, representing only a 7.43% impact on all crucial features. This indicates that most of our desired features for our MVP are entirely achievable.

## E-commerce App Blueprint

1. **Target Audience** - Who:

    - Primarily B2C (Business to Consumer)
    - B2B (Business to Business) - Possible with further expansion and customization

2. **Offerings** - What:

    - Digital Products
    - Services

3. **Payment Methods** - How:

    - One-time Payment

4. **Key Features & Information Display**:

    - Refer to the above section for details.

5. **Essential Data Tables**:

    - Product
    - Category
    - Abstract User
    - Transaction
    - Download
    - Review
    - Newsletter

## SEO Plan

### Keywords Selection
The right keywords for out application
### Tech Implementations
To implement within our code
### Content Creation
Great content & importance

Armed with this information, we can now move to the next stage, which is defining the `scope` of our project.