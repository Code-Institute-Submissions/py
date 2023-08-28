## Surface Plane - Color, Typography, Effect and Images

After extensive research, strategy formulation, and brainstorming, we've crafted a solid project skeleton. With our groundwork in place, we're poised to initiate the next phase: building the surface plane. While this foundational work is crucial, it's in the actual creation and coding stages that we anticipate uncovering any potential challenges or nuances. Now is the ideal time to transform our ideas into reality and refine them as we progress. We eagerly anticipate witnessing our project evolve.

**Approach:**

We model our project strategy after the wisdom of Nikola Tesla, who once remarked, `"My method is different. I do not rush into actual work. When I get a new idea, I start at once building it up in my imagination, making improvements, and operating the device in my mind. When I have gone so far as to embody everything in my invention, every possible improvement I can think of, and when I see no fault anywhere, I put into concrete form the final product of my brain."` Just as Tesla painstakingly refined his ideas mentally before realization, we meticulously plan and polish our project prior to the actual programming phase.

At this juncture, our primary attention is on the surface plane. This encompasses not just the design of the interface but also the user's entire interaction journey. Our aim is to establish a coherent visual language that shapes each step and touchpoint, ensuring a fluid and intuitive user experience.

Every nuance matters for the project's success, and we are unyieldingly committed to perfecting them.

### Color

|                                                                  | Color Type      | Color Name      | Hex Code  |
| ---------------------------------------------------------------- | --------------- | --------------- | --------- |
| ![Color](https://via.placeholder.com/50x50/34495e/34495e?text=+) | Primary Color   | Shade of Blue   | `#34495e` |
| ![Color](https://via.placeholder.com/50x50/ffffff/ffffff?text=+) | Secondary Color | White   | `#ffffff` |
| ![Color](https://via.placeholder.com/50x50/f8f9fa/f8f9fa?text=+) | Secondary Color | Shade of White      | `#f8f9fa` |
| ![Color](https://via.placeholder.com/50x50/dadada/dadada?text=+) | Secondary Color | Shade of White      | `#dadada` |
| ![Color](https://via.placeholder.com/50x50/333333/333333?text=+) | Secondary Color | Shade of Black  | `#333333` |
| ![Color](https://via.placeholder.com/50x50/2D4F2F/2D4F2F?text=+) | Secondary Color | Shade of Green  | `#2D4F2F` |
| ![Color](https://via.placeholder.com/50x50/763135/763135?text=+) | Secondary Color | Shade of red    | `#763135` |
| ![Color](https://via.placeholder.com/50x50/ffbe00/ffbe00?text=+) | Secondary Color | Shade of orange | `#ffbe00` |
| ![Color](https://via.placeholder.com/50x50/0000000d/0000000d?text=+) | Secondary Color | Shade of black | `#0000000d` |


#### Pallet

The following color palette was used as a reference throughout the project:

- [My Color Space](https://mycolor.space/?hex=%2334495E&sub=1)


### Layout

#### Technologies Used

- Vendor templates (as seen in [Technologies Used](../../tech-used/tech_used.md))
- Bootstrap
- Custom Code

#### Homepage

- Upon entry, users are greeted with an intuitive header with dropdowns and a search engine. Below it is a call-to-action section featuring an video/image and text on the right side, along with a button prompting users to learn more about Plexosoft Marketplace.
- Following the call-to-action section, Products & Services are displayed sequentially: Product & Service (mixed cards), Product (Product cards), Service (Service cards).
- Product & Service sections are organized into rows, each containing 3 columns that showcase 3 cards (styled using Bootstrap), replete with pertinent information and associated call-to-action directives.
- Notably, these cards comprise subparts: card, card header, card body, and card footer, each demarcated by their unique borders.
- The footer consists of a row split into three columns, designated for: About, Useful Links, Newsletter and Contact Information. Situated above this is a discreet row of social media icons.
- All aforementioned elements are responsive, catering to a variety of screen dimensions.

#### Login

- The login page employs columns and rows to maintain layout uniformity, replicating established patterns using Bootstrap's card system wherever feasible.
- Input fields and buttons are provided.
- Social Media login is possible.
- Feedback/messages functionality included.

#### Sign Up

- The sign-up page echoes the aesthetic of the login page, leveraging Bootstrap's card style.
- Input fields and a button are integrated.
- Social Media register is possible
- Feedback/messages functionality included.

#### Product & Service Dedicated Page

- Presented on its dedicated page, the Product & Service offers an in-depth rendition of the primary card observed on the homepage, complete with extensive details and E-commerce functionalities.
- A harmonious style is sustained throughout.
- Feedback/messages functionality included.

#### User & Admin Dashboard

- The admin dashboard, adapted from another vendor template, meshes perfectly with Plexosoft Marketplace.
- We've made minor stylistic tweaks to this template to ensure coherence with the overarching software design.
- Each card's presentation mirrors the ubiquitous Product & Service card format, reinforcing consistency.

#### Contact Page

- The contact page harnesses Bootstrap's card design to encapsulate the form element.
- Input fields and a button are present.
- Topic select option is available.
- The familiar design reassures users of their continuity within Plexosoft.
- Fast access to the conctact page is visible.

#### FAQ

- The FAQ page, while intriguing, remains true to established design and stylistic conventions.
- It features collapsible buttons for each query, whether textual or video-based.
- Authentic content has been embedded, and just like the rest of Plexopost Marketplace, this page is fully responsive.
- Fast access to the FAQ page is visible.

### Fonts

- Our primary font is `Roboto`, except where specified.
- `Fairplay Display` is employed for select titles and subtitles.

### Images

- Key images are found in the call-to-action section, favicon, and placeholders for Products & Services.
- Independent images for Products & Services are stored on AWS3.

### Page Order

- The sequence of main pages is as follows: Homepage > Single VoteCards > Active > Completed > Signup > Login > Dashboard > FAQ > Contact.
- The navbar and footer are consistent across all pages.
- At all times, we've incorporated the principle of progressive disclosure.

### Navigation Flow

- Adhering to `progressive disclosure` enabled a seamless application experience. Users initially land on the `Homepage`. From there, they can choose to `Sign Up` or `Login`. Post login, they're seamlessly redirected to their dashboard. Queries can be addressed via the `Contact` page or the `FAQ`.
- VoteCards are accessible from the `Homepage`, user's `Dashboard`, `Active` page, `Completed` page, and directly via their specific URLs.

Throughout the design, we emphasized simplicity, ensuring that crucial elements stand out. Recognizable patterns in layout and interactions enhance user familiarity. The design ensures readability, with contrasting colors and varied fonts employed judiciously.

Navigational clarity is paramount. We've ensured value is perceivable throughout the platform.

**Key Design Principles:**

- Dynamism
- Repetition
- Contrast
- Proximity
- Alignment
- Accessibility
- Interaction
- Visual Engagement
- User-Friendly Experience

Our goal was straightforwardness. We aimed to present users with fewer, more impactful choices, accentuating specific features and content. This design philosophy facilitated a smoother transition from design to code. The development process was not only streamlined but also more engaging. This efficient approach conserved time, effort, and resources. It minimized human intervention and errors, leading to a refined end product.
