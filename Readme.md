# Documentation

- This insurance web app is targeted at both customers and administrators. Administrators will be referred to as admins, users who are not administrators will be referred to as customers. Users refers to both customers and admins. Users who aren’t signed up will be referred to as visitors
- The current insurance offering for the minimum viable product is legal insurance. Further offerings will be added at a later stage.
- Users can log in and log out.

## The following can be done by visitors.

-	Navigate unprotected pages and routes, these include but are not limited to the contact page, home page (which has the about us section), the policy pages (which provide more information on the individual policies and allow the option for getting quote estimates), and the complete estimate page which will require the visitor to input their contact details in order to receive more information about the quotation.
- A visitor may visit the register page, via log in then sign up. A valid email address will be required to sign up.

## Administrators

-	Adminstrators have a an admin dashboard, which shows a carousel with some analytics regarding customers and policies. This will be fleshed out in future versions.
-	The admin dashboard has a sidebar, with links to the customer management, policy management and claims processing pages.
-	Under customer management (click view policies), admins can see all registered users and are able update the details of these users. 
-	Under policy management (click view policies), our current policy offerings are displayed to the admin in a table. The admin may update policy offerings. Changes made here will be reflected in the home page and the policy pages.
-	Under claims processing ( click pending claims ), the admin can see all claims that have yet to be approved. The admin can process claims here.
-	On the top-navbar, policies = policy management; customers = customer management, claims = claims processing.

## Customers

-	The customer dashboard has a sidebar for navigation.  The sidebar has links for filing a new claim, viewing policies, registering for new policies and updating the profile.
-	The rest of the dashboard shows a table with all customer claims, both approved and pending. There is also a second table that shows all customer policies.
-	Users may file a claim, which will have the pending status until it is processed by an admin.
-	Customers can delete their policies, futue version will remove tis functionality to avoid a loss of historical data. Rather the policy will be shown as inactive.
-	After registering for a policym admins process the application and send the result back to the user. Future versions will see this functionality renamed to apply.
-	Customers may update their details by clicking on update my profile.

## RESTful API

- When adding a claim using, do not specify date filed.


