@workspace Students are able to register twice for an activity.
Where could this bug be coming from?
This bug could be coming from several sources, including:
1. Database Constraints: The database may not have proper constraints to prevent duplicate entries for the same student and activity combination.
2. Application Logic: The application code may not be checking for existing registrations before allowing a new registration to be created. This could be due to a missing validation step in the
