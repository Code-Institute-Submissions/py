## Tests
We have run the following manual tests:

### Homepage
| Component                | Action (Steps)                                                                          | Expected Result (Granular)                                                     | Issues Found & Resolved | Test |
|--------------------------|-----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|-------------------------|------|
| Header       | 1. Navigate to homepage <br> 2. Check header at Account | Header contains Logo, Navigation Menu, Account, Sign In | NA                      | PASS |
| Call to Action Section   | 1. Navigate to the homepage <br> 2. Read the Call to Action text                        | Text "Dive into the sea of universal software solutions" should be visible     | NA                      | PASS |
| Video Embed              | 1. Navigate to homepage <br> 2. Play the embedded video                                 | Video should play without any issues                                            | NA                      | PASS |
| Sorting Element          | 1. Navigate to homepage <br> 2. Sort items using different sorting options               | Items should be sorted according to the selected option                         | NA                      | PASS |
| Product & Service Cards  | 1. Navigate to homepage <br> 2. Check displayed products and services                    | Each card should display title, author, price, likes, and purchases count      | NA                      | PASS |
| "See More" Button        | 1. Navigate to homepage <br> 2. Scroll down to "See More" button <br> 3. Click on it     | The user should be redirected to the 'combined_items_all' page                  | NA                      | PASS |
| "No Records" Text        | 1. Navigate to homepage with no available records <br> 2. Check "No records found" text | "No records found so far" text should be visible if no records are available   | NA                      | PASS |
| "Buy Now" & "Hire Now"   | 1. Navigate to homepage <br> 2. Click "Buy Now" or "Hire Now" on a product/service card | The user should be redirected to the respective single product or service page | NA                      | PASS |

### Bag

| Component                | Action (Steps)                                                                          | Expected Result (Granular)                                                                        | Issues Found & Resolved | Test |
|--------------------------|-----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|-------------------------|------|
| Title Block              | 1. Open the shopping cart page <br> 2. Check the title                                  | Title should read "- Shopping Cart"                                                               | NA                      | PASS |
| Shopping Cart Header     | 1. Open the shopping cart page <br> 2. Look at the cart header                          | "Shopping Cart" should be displayed in header                                                     | NA                      | PASS |
| Cart Table               | 1. Open the shopping cart page <br> 2. Check if table is displayed                      | Table headers (Item Info, Price, Qty, Subtotal, Action) should be visible                         | NA                      | PASS |
| Item Display             | 1. Open the shopping cart page with items in cart <br> 2. View items                     | Items should be listed with image, title, SKU, price, and quantity                                | NA                      | PASS |
| Cart Emptiness           | 1. Open the shopping cart page with no items <br> 2. Check the display                   | "Your cart is empty." should be visible if no items in the cart                                   | NA                      | PASS |
| Update Quantity          | 1. Open the shopping cart page with items <br> 2. Update item quantity                   | Quantity should be updated and reflected in subtotal                                              | NA                      | PASS |
| Remove Item              | 1. Open the shopping cart page with items <br> 2. Click "Remove"                         | Item should be removed from the cart                                                              | NA                      | PASS |
| Item Count Display       | 1. Open the shopping cart page with items <br> 2. Check item count                       | Item count should be displayed                                                                    | NA                      | PASS |
| Cart Subtotal            | 1. Open the shopping cart page <br> 2. Check cart subtotal                               | Cart subtotal should be displayed and accurate                                                    | NA                      | PASS |
| Discount                 | 1. Open the shopping cart page <br> 2. Check discount                                    | Discount should be displayed if applicable                                                        | NA                      | PASS |
| Grand Total              | 1. Open the shopping cart page <br> 2. Check grand total                                 | Grand Total should be displayed and accurate                                                      | NA                      | PASS |
| Checkout Button          | 1. Open the shopping cart page <br> 2. Click the "Secure Checkout" or "Guest Checkout"  | Redirects to 'checkout_page'                                                                      | NA                      | PASS |
| Keep Shopping Button     | 1. Open the shopping cart page <br> 2. Click "Keep Shopping"                             | Redirects to 'combined_items_all' page                                                            | NA                      | PASS |

### Checkout Page

| Component                        | Action (Steps)                                                                                       | Expected Result (Granular)                                                                        | Issues Found & Resolved | Test |
|----------------------------------|------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|-------------------------|------|
| Order Details Section            | 1. Navigate to checkout page <br> 2. Check 'Order Details' section                                   | Section with fields for full name, email, phone number, and country should be visible             | NA                      | PASS |
| Form Fields                      | 1. Navigate to checkout page <br> 2. Fill out all fields in 'Order Details'                           | All fields should be fillable and data should be retained                                        | NA                      | PASS |
| Save Info Checkbox (Authenticated)| 1. Login to the website <br> 2. Navigate to checkout page <br> 3. Check 'Save this delivery information to my profile' | Checkbox should be visible and checked by default                                                | NA                      | PASS |
| Save Info Checkbox (Guest)       | 1. Navigate to checkout page as a guest <br> 2. Check for 'Create an account or login to save this information'  | Links to create an account or login should be visible                                            | NA                      | PASS |
| Payment Gateway Section          | 1. Navigate to checkout page <br> 2. Check 'Payment Gateway' section                                  | Button options for Manual Payment, Stripe Payment, and Crypto Payment should be visible           | NA                      | PASS |
| Manual Payment Toggle            | 1. Navigate to checkout page <br> 2. Click on 'Manual Payment' button                                 | Payment section for manual payment should expand                                                  | NA                      | PASS |
| Stripe Payment Toggle            | 1. Navigate to checkout page <br> 2. Click on 'Stripe Payment' button                                 | Payment section for Stripe should expand                                                          | NA                      | PASS |
| Crypto Payment Toggle            | 1. Navigate to checkout page <br> 2. Click on 'Crypto Payment' button                                 | Payment section for Crypto should expand                                                          | NA                      | PASS |
| Total Charge Display             | 1. Navigate to checkout page <br> 2. Check the total charge message                                   | Total charge should match with cart grand total and be displayed                                  | NA                      | PASS |
| Manual Checkout Button           | 1. Navigate to checkout page <br> 2. Expand Manual Payment <br> 3. Click 'Manual Checkout' button      | Should proceed to the next step of manual payment                                                 | NA                      | PASS |
| Stripe Checkout Button           | 1. Navigate to checkout page <br> 2. Expand Stripe Payment <br> 3. Click 'Stripe Checkout' button      | Should proceed to the Stripe payment gateway                                                      | NA                      | PASS |
| Crypto Checkout Button           | 1. Navigate to checkout page <br> 2. Expand Crypto Payment <br> 3. Click 'Crypto Checkout' button      | Should proceed to the next step of crypto payment                                                 | NA                      | PASS |

### Stripe Redirect

| Component                         | Action (Steps)                                                                                             | Expected Result (Granular)                                                                      | Issues Found & Resolved | Test |
|-----------------------------------|------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|-------------------------|------|
| Page Title                        | 1. Navigate to the Stripe Redirect page                                                                    | Page title should be '- Stripe Redirect'                                                        | NA                      | PASS |
| CSS Load                          | 1. Navigate to the Stripe Redirect page                                                                    | The page should load with styles from 'checkout/css/checkout.css'                               | NA                      | PASS |
| Redirect Header                   | 1. Navigate to the Stripe Redirect page <br> 2. Check the header section                                   | A header with the text 'Redirect' in the logo-font should be visible                            | NA                      | PASS |
| Order Summary Section             | 1. Navigate to the Stripe Redirect page <br> 2. Check the 'Order Summary' section                          | "You will be redirected to Stripe now!" message and a spinner should be visible                 | NA                      | PASS |
| Order Number Display              | 1. Navigate to the Stripe Redirect page <br> 2. Check for the order number                                 | The order number should be displayed                                                           | NA                      | PASS |
| Auto-Redirect to Stripe           | 1. Navigate to the Stripe Redirect page <br> 2. Wait for 5 seconds                                         | Automatic redirect to Stripe's payment page should happen                                       | NA                      | PASS |
| Manual Stripe Checkout Button     | 1. Navigate to the Stripe Redirect page <br> 2. Click the 'Stripe Checkout' button                         | Should proceed to the Stripe payment gateway                                                    | NA                      | PASS |
| Password and Username Download    | 1. Navigate to the Stripe Redirect page <br> 2. Check if a password.txt file is downloaded automatically  | A password.txt file containing username and password should be downloaded                       | NA                      | PASS |
| Console Errors                    | 1. Open the browser's console <br> 2. Navigate to the Stripe Redirect page                                 | No JavaScript errors should appear in the console                                               | NA                      | PASS |

- Note: This was just a simple manual test. Due to the magnitude of the project, more comprehensive manual testing is recommended in future iterations!

## Technical Testing

### HTML Validator

Many issues found and all were solved, Jinja templating language made it extremely hard at first.

### CSS Validator - W3C

No issues were found in our custom css at 'static/frontend/css/base.css'.

### JSHint (API by Code Institute)

No particular issues found in our custom JS files at:

- '/py/static/frontend/js/script.js'
- '/py/static/custom/js/script.js'

### Google Developer's Console

We meticulously reviewed every page of the site to identify any potential issues. We discovered a missing favicon.ico on both the admin and user dashboards.

- All issues have been resolved.

### CI Python Linter by Code Institute
Consistently adhering to PEP8 standards can be a tall order. For this reason, we frequently utilized the CI Python Linter throughout the development process. This tool proved invaluable in upholding code structure and enhancing the code's overall aesthetics.

At the development's conclusion, we performed another round with the CI Python Linter, ensuring everything was in order and implementing necessary adjustments.

- [CI Python Linter](https://pep8ci.herokuapp.com/#)

### Lighthouse
Lighthouse offered comprehensive analysis across various aspects of our application. Although its use wasn't obligatory, we paired it with GT-Metrix to guarantee a high-quality product delivery. The outcomes were in line with our expectations.

![Lighthouse](https://github.com/plexoio/musa/blob/main/documentation/assets/img/testing/lighthouse.png)

### GTMetrix
Leveraging its distinct capabilities, GT-Metrix became an integral component of our testing regimen. It furnished us with invaluable recommendations, all of which were considered non-critical for this version. The app is performing optimally and is primed for release.

![GTMetrix](https://github.com/plexoio/musa/blob/main/documentation/assets/img/testing/gtmetrix.png)

### Responsiveness

We tested our app across various screen sizes both during and after development. This seamless adaptability can be attributed to the capabilities of Bootstrap and the vendor templates we employed.

## Bugs

Like any project, ours has had its share of bugs. Below are some of the challenges we've faced:

#### a) Website Performance
We endeavored to consolidate everything using Django, Bootstrap, JQuery, PostgreSQL database and other technologies, aiming for a robust web application that functions seamlessly across all devices. However, we cannot assure consistent performance on devices with limited memory or processing capabilities.

#### b) Cloudinary Error: KeyError 'etag'
We encountered an error that prevented us from submitting our project to the Code Institute on time. Despite many hours of debugging with tutor assistance, the only resolution was to create a 'custom_storage.py' file to circumvent the problem.

**Error breakdown:**

> During the execution of the `collectstatic` command, Django attempted to gather and process static files. The `cloudinary_storage` package managed some or all of these files. As part of its routine, `cloudinary_storage` checks for duplicate content on Cloudinary to avoid redundant uploads. It does this by verifying the ETAG header in Cloudinary's response. However, the ETAG header was absent, resulting in a KeyError.

#### c) Event Completion Status
Events marked as expired only transition to "complete" after a user attempts to vote. This behavior is intentional for performance reasons. In the future, we might programmatically update the status upon loading, similar to the vote count or progress bar.

#### d) Social Media Links
At the moment, social media buttons direct users to the primary pages, intended solely for demonstration.

#### e) Vote Events Deletion
Indeed, in this version, VoteCards are only marked as completed, preventing further voting. Only a superuser or the website owner can delete a VoteCard. Deleting a VoteCard will also remove associated elected persons and vote card records, effectively erasing all data linked to that event.

#### Other Potential Bugs
For other issues, we suggest refreshing the page or clearing cache files. If problems persist, it's likely not an issue with the Musa project but may pertain to third-party services or the specific settings and capabilities of your device.

## Security

Concise explanation of why Django, Bootstrap, and PostgreSQL are considered safe:

### Musa's system

1. **Django**:
   - **Framework Design**: Django follows the "batteries-included" philosophy and provides built-in protection against many common security threats like SQL injection, cross-site scripting (XSS), and cross-site request forgery (CSRF).
   - **Secure Defaults**: By default, Django configurations are set to be secure, ensuring developers don't accidentally expose vulnerabilities.
   - **Regular Updates**: The Django team frequently releases updates and patches to address any identified security concerns.

2. **Bootstrap**:
   - **Sanitized Inputs**: Bootstrap's JavaScript plugins are designed to automatically sanitize inputs to protect against XSS attacks.
   - **Trusted Development**: Bootstrap is maintained by a dedicated team and has a large community that helps in identifying and fixing potential vulnerabilities.
   - **Consistent Updates**: The Bootstrap team provides regular updates to keep the library secure against new threats.

3. **PostgreSQL**:
   - **Robust Access Controls**: PostgreSQL offers fine-grained access controls, allowing administrators to define who can access the database and what actions they can perform.
   - **SQL Injection Prevention**: PostgreSQL has built-in measures to prevent SQL injection attacks, especially when developers use parameterized queries.
   - **Encryption**: PostgreSQL supports data encryption both at rest and in transit, protecting sensitive data from unauthorized access.

All three tools prioritize security in their design and implementation. However, it's essential for us to stay updated with the latest versions and best practices to ensure maximum safety.

### Extra security & Accessibility

1. **`rel` attribute**: For links that lead to external websites (especially on a different domain), it's a good idea to add `rel="noopener noreferrer"` to the anchor tags. This ensures that the new page cannot access your `window` object via `window.opener`, and it doesn't leak referrer information to the new page. This is especially useful if you're linking to sites that you don't control.

2. **`target` attribute**: If you want the links to open in a new tab or window, add `target="_blank"` to the anchor tags. This, combined with the `rel` attribute mentioned above, is a common combination for external links.

3. **`aria-label` or `title` attribute**: To make your links more accessible, especially since they only contain icons and no text, you can use the `aria-label` attribute to describe the purpose of the link to screen readers. Alternatively, you can use the `title` attribute to provide a tooltip when users hover over the link.

We have applied them to all external linking:

```html
<li class="me-4">
   <a href="" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
      <i class="fab fa-github"></i>
   </a>
</li>

<li class="me-4">
   <a href="" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
      <i class="fab fa-facebook-f"></i>
   </a>
</li>

<li class="me-4">
   <a href="" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
      <i class="fab fa-twitter"></i>
   </a>
</li>

<li class="me-4">
   <a href="" target="_blank" rel="noopener noreferrer" aria-label="Google">
      <i class="fab fa-google"></i>
   </a>
</li>

<li class="me-4">
   <a href="" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
      <i class="fab fa-instagram"></i>
   </a>
</li>

<li class="me-4">
   <a href="" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
      <i class="fab fa-linkedin"></i>
   </a>
</li>
```