# RHC Player Management System

A Flask-based web application for managing players in various clubs for the "Residentes Huanuneños Cochabamba" (Huanuni Residents Cochabamba) community.

## Features

- **Club Management**: Select a club and view registered players in a dynamic table
- **Player Registration**: Add new players with CI uniqueness validation
- **Player Listing**: View all players across clubs
- **Document Viewer**: View player PDFs in a modal
- **Age Calculation**: Automatic age calculation from birthdate
- **Responsive Design**: Bootstrap-based UI with DataTables for enhanced tables
- **Player Card**: Beautiful card view for individual player information with print functionality

## Technologies Used

- **Backend**: Flask 3.0.3, SQLite
- **Frontend**: HTML, Bootstrap 5.3.3, DataTables, jQuery
- **Database**: SQLite (rhc_database.db)

## Installation

1. Clone or download the project files.

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the database file `rhc_database.db` is present in the root directory. If not, the app will create it, but you may need to run the table creation function if necessary.

## Running the Application

1. Navigate to the project directory:
   ```bash
   cd /path/to/rhcpy
   ```

2. Run the Flask app:
   ```bash
   python app.py
   ```

3. Open your browser and go to `http://127.0.0.1:5000/`

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates (base.html, index.html, new_player.html, list_player.html)
- `static/`: Static assets (CSS, JS, resources like PDFs and JSON files)
- `helpers/`: Helper functions (rhc_helper.py)
- `config/`: Configuration files
- `requirements.txt`: Python dependencies
- `rhc_database.db`: SQLite database

## Routes

- `/`: Home page with club selector
- `/login`: Login page
- `/logout`: Logout user
- `/new_player`: Add new player form
- `/list_player`: List all players with action buttons
- `/player_card/<player_id>`: View/print individual player card
- `/club`: AJAX endpoint for club player data
- `/search_ci`: Check CI uniqueness

## Authentication

The application now includes user authentication using Flask-Login.

- **Default User**: Username: `admin`, Password: `admin123`
- Login is required to access all pages except the login form.
- Logout is available in the navigation menu.

## Database Schema

The `player` table includes:
- register (TEXT)
- name (TEXT)
- last (TEXT)
- ci (TEXT)
- fechanacimiento (TEXT)
- parentesco (TEXT)
- notas (TEXT)
- club (TEXT)
- gestion (implied, filtered to '2025')

The `users` table includes:
- id (INTEGER PRIMARY KEY)
- username (TEXT UNIQUE)
- password (TEXT, hashed)

## Notes

- The application is in development and may have some hardcoded values (e.g., gestion year).
- Ensure PDFs are placed in `static/resources/{club_name}/` with naming convention `{name}_{last}.pdf` (lowercase, underscores, ñ replaced with n).

## Contributing

Feel free to contribute by fixing issues or adding features. Please test thoroughly before submitting changes.

## License

[Add license information if applicable]
