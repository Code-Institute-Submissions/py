# Ideate

## Let’s go green
- In the first iteration, our approach will be a B2C e-commerce, starting with one-time payment methods.

### Software Design
- Utilize colors that represent the project's intentions, philosophy, and skills.
- `#3498db`: Calmness and Serenity, Trustworthiness, Strength and Stability, Technology and Modernity, Depth and Wisdom, Communication.
- `#ecf0f1`: Neutrality and Balance, Cleanliness and Modernity, Sophistication, Calmness, Versatility, Background or Secondary.
- As the project grows, introduce relevant physical devices to foster a deeper connection and enhance interactivity.
- Ensure the homepage is neat with ample spacing, prioritizing the most relevant products.
- Implement Bootstrap to structure product cards, ensuring consistency throughout.
- Clearly label products based on software type: ownership or licensing.
- Add a note to each product highlighting its customization possibilities, whether self-driven or through our extended services.
- On the homepage, display key product metrics like current sales, review counts, and comment counts.
- Structure the homepage layout with rows dedicated to mixed products, and separate ones for Licensing and Ownership.
- Incorporate a search bar in or below the header for easier user searches.
- The menu should feature a dropdown for product categories.
- Include a direct link to the service's proprietary social media platform within the menu.
- Add a "Request" button in the menu, streamlining user project requests or inquiries.
- Incorporate a Support section in the menu, with dropdown options for a contact form or FAQ section.
- The footer should encompass an about section, useful links, and social media icons.
- Prioritize concise software descriptions over exhaustive feature listings.
- Engagement, keywords, colors, shapes, interactivity (they are about to change the world): Lottie files, illustrations.

### Transparency Advocate
- Emphasize the distinction between software ownership and licensing across the homepage, menu, product sections, and user dashboard.
- Launch a dedicated section on the differences between software ownership and licensing.
- Address how privacy & security are maintained.
- Feature our plans to bolster small businesses and innovative ideas.
- Enable review and comment features for products and services.
- Detail third-party technologies used, leveraging product documentation.
- Educate users about their product’s components, operations, and expectations.
- Implement email verification and offer social media login options.

### Financial gateways
- Uphold financial inclusivity by supporting payment methods such as Visa, Mastercard, manual payments, Western Union, and cryptocurrencies.
- Implement shopping cart.

### Community Building
- Introduce a proprietary social media account for the project, facilitating interactions beyond mere entertainment.
- In the second phase, integrate a third-party software for social media platform creation under a licensing model.
- Incorporate a newsletter system for marketing and enhanced user engagement.

### Guardian of Trust
- Adopt algorithms ensuring transparent and ethical data handling while safeguarding user privacy.
- Execute thorough testing and integrate features ensuring utmost security, including the incorporation of Blockchain and IPFS.

### Challenge-ready
- Continuously gather insightful data beneficial in the long run: tracking user clicks, page visits, best-selling products, etc.
- Persistently engage in market research to stay updated with industry shifts.
- Regularly refine our marketing, SEO strategies, design thinking, and agile development methodologies.

### Affordability & Community
- Champion initiatives supporting promising yet underfunded ideas, through free developments or fairly-priced productions.
- Promote community competitions and challenges.
- Organize activities promising tangible results for end-users, doubling as opportunities to gather testimonials and bolster reputation.
- Endeavor to provide the most competitive prices and discounts, ensuring our sustainability.
- Offer services assisting users in collating their ideas: design thinking, user-centric design, database modeling, and marketing and market research strategies.

### Support is queen
- Strive for clear and effective communication, possibly leveraging tools like GPT or Bard for assistance. Prioritize robust support systems.
- Regularly update users about software and organizational developments.
- Cultivate a dedicated team to address daily queries, contribute to development, and understand the value of delegation.
- Streamline the contact form with categorized issue listings for efficient backend processing.
- Utilize our proprietary social media platform, along with traditional platforms, for updates, advertisements, and event announcements.
- Propose a structured format for users submitting ideas, bug fixes, or service requests.
- Introduce an academy section educating users about the technologies we employ, especially when rolling out advanced or novel concepts.
- Organize workshops, tutorials, and offer bundled deals, enhancing platform offerings and user experience.
- Develop an RSS feed showcasing high-quality articles on cutting-edge technology trends.

### Extended services
- Ensure capabilities to address bug fixes, hosting & domain setups, DNS, SEO, Google services, API integrations, customizations, and more.
- Offer design thinking, user-centric planning, and marketing along with SEO as distinct services.

### User & Admin Dashboard
- Incorporate a comprehensive User Profile, gathering essential data. User roles and admin roles will influence the dashboard's appearance.
- After payment completion, users should be able to immediately download their purchased product and access it from their dashboard, along with pertinent license or service details.
- In subsequent iterations, consider implementing a ticketing support system to enhance issue resolution.
- The user's dashboard should feature sections like: settings, my products, my services, my reviews, and comments.
- The admin dashboard should encompass: site general settings, product & service creation tools, listings of published products & services, product & service CRUD (Create, Read, Update, Delete) functionalities, an SEO section, and more.

### Technologies to Employ
- Utilize Django, Bootstrap, jQuery, RSS, Allauth, AWS S3, EmailJS, PostgreSQL, Psycopg2, ElephantSQL, vendor-specific templates, Lottie files, among others.
- Image compression, lazy loading, caching, DNS, Cloudflare.

### Database
- Product, Service, Category, Abstract User, Transaction, Download, Like, Comment, Newsletter

## Let’s go red
- Not all may be applied in the first MVP iteration.

### Must-haves

- **Front-end:** 
  - Colors: `#3498db` & `#ecf0f1`.
  - Homepage spacing, Bootstrap for layout with cards for mixed and specific products (Licensing and Ownership).
  - Product labeling (ownership or licensing).
  - Notes on products regarding customization options.
  - Display key metrics: current sales, review counts, comment counts.
  - Search bar, menu with dropdowns: Category, Service, Support, Request button.
  - Footer details: about section, useful links, social media icons.
  - Dedicated product description page.
  - Engagement elements: Lottie files, illustrations, shopping cart, review and comment functionality, newsletter and RSS feed sections, contact form, request formats, download functionality, user dashboard (settings, products, services, reviews(likes), comments), and admin dashboard.

- **Back-end:** 
  - Features: email verification, social media login options, Stripe for payment, newsletter system, tracking (user clicks, page visits), B2C e-commerce with one-time payment methods.
  - Databases: Product, Service, Category, Abstract User, Transaction, Download, Review, Newsletter.
  - Technologies: Django, Bootstrap, jQuery, RSS, Allauth, AWS S3, EmailJS, PostgreSQL, Psycopg2, ElephantSQL, vendor-specific templates, Lottie files, etc.

- **Culture:** Emphasizing ease of use, quality, affordability, robust support, clear communication, transparency, financial inclusion, and inclusivity of services.

### Considerations

- **Must-have prototype:** Proof-of-concept, Database model.
- **Next steps:** Develop the proof-of-concept, refine the database model.
- **Questions:** Which features will be included in our MVP's first iteration/release?
- **Session name:** Internet Authority
- **Reminder:** Revisit detailed documents for:
  - Distinctions between software ownership and licensing.
  - Privacy & security measures.
  - Documentation of third-party technologies.
  - User education on product components and operations.
  - Financial inclusivity with diverse payment methods.
  - Algorithms for data transparency, ethical handling, and privacy.
  - Extended service capabilities and distinct offerings.

### Final word on this session
Using Darek Cabrera's measure of difficulty, our product complexity lies between Complicated and Complex. User variables can be unpredictable, thus:

1. **Financial Inclusion Matters:** To be globally accessible, especially in regions with internet connectivity.
2. **Filtering options:** Allow users to tailor their experiences for a more personalized and relevant journey.
3. **Cultural resonance:** The product should resonate with users' cultural values and aesthetics for a sense of purpose and pride.

Addressing challenges extends beyond just the technical. Understanding underlying concepts, logical thinking, sound design decisions, and considering legal and cultural ramifications are crucial. By integrating these facets, the product can better cater to its users, fostering an inclusive and user-centric atmosphere.