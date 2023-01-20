
Make sure you have installed requirements.txt before running the application by running pip install -r requirements.txt in your terminal.

Here are instructions for running the commands to migrate the database using Flask-Migrate:

Make sure you have Flask-Migrate installed by running pip install flask-migrate in your terminal.

Run the command flask db init to create the migration repository. This command should only be run once, when you first set up the application.

Run the command flask db migrate to create the initial migration. This command should be run whenever you make changes to your SQLAlchemy models and want to create a new migration.

Run the command flask db upgrade to apply the migration to the database. This command should be run after you have created a new migration and want to update the database schema.

Make sure your flask application is running and you are in the same directory where the application file is located before running the above commands.

The commands should be run in the command line or terminal, in the same directory where the application file is located.

If you want to rollback a migration you can use the command flask db downgrade



in short, you need to run the following commands in your terminal:
make a new virtual environment and activate it
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
flask run
