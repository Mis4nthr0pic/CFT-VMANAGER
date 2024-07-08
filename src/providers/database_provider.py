import psycopg2
import os

# Database connection setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:111111@cft.clo4cyc8wwx3.eu-north-1.rds.amazonaws.com:5432/CFT')

def get_db():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn

def create_user(address, minute_credits):
    """Create a new user in the database using plain SQL."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        # SQL query to insert a new user
        query = "INSERT INTO users (address, minute_credits) VALUES (%s, %s) RETURNING id;"
        cursor.execute(query, (address, minute_credits))
        user_id = cursor.fetchone()[0]
        conn.commit()  # Commit the transaction
        return user_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Example function definitions for virtual machine operations
def create_virtual_machine(id_contract, id_host, owner_address):
    """Create a virtual machine entry in the database."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO virtual_machines (id_contract, id_host, owner_address, status) VALUES (%s, %s, %s, %s) RETURNING id;"
        cursor.execute(query, (id_contract, id_host, owner_address, 0))  # status 0 for stopped
        vm_id = cursor.fetchone()[0]
        conn.commit()
        return vm_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# You can define other functions similarly.

