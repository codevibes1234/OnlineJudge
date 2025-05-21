# Repo Structure

Requirements.txt -> contains all the essential python packages to build the project

accounts -> contains all the authentication related stuff

judge -> contains all the components of the core website

# URL Mappings

/admin/ -> admin access

/accounts/login -> login webpage

/accounts/register -> registration webpage

/problems/ -> problem list

/problems/<int:id> -> problem details

/problems/<int:id>/submissions -> submissions made by all users for the given problem

/user/<int:id> -> user profile

/problems/<int:pid>/submissions/user/<int:uid>/ -> submissions made by a specific user for the specified problem

/submissions/<int:sid> -> view specified submission
