# Permissions and Groups Setup (bookshelf)

## Custom Permissions
Defined in `CustomUser` model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
- **Editors**: can_view, can_create, can_edit
- **Viewers**: can_view
- **Admins**: all permissions

## Usage
Views are protected using `@permission_required`.  
Assign users to groups via Django Admin or programmatically.  
Test by logging in as different users and verifying access control.