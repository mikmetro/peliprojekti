import mysql.connector
from mysql.connector import Error
from typing import Any
from .upgrades import *
from .airport import *
from .player import *
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = os.environ.get("MARIA_DB_PASSWORD")
        self.database = "peliprojekti"

    def connect(self) -> str:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                collation="utf8mb4_unicode_520_ci" # Laitoin collation että mysql-connector-python uusin versio toimii
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return "Connected"
            return "Connection failed"
        except Error as e:
            print(e)
            return f"Error connecting {str(e)}"
            
    def execute_query(self, query) -> str:
        try:
            self.connect()
            self.cursor.execute(query)
            self.connection.commit()
            return f"Query executed successfully: {query}"
        except Error as e:
            return f"Error executing query: {e}"

    def fetch_query(self, query) -> Any:
            try:
                self.connect()
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result
            except Error as e:
                return(f"Error fetching data: {e}")
            
    def upgrades(self) -> Any:
        get_upgrades = self.fetch_query("select name, level, price, effect, delta_price, delta_effect, max_level from upgrades;")
        return get_upgrades

    def all_airports(self) -> Any:
            game_airports = self.fetch_query("select game_airports.*, airport.name, airport.municipality from game_airports INNER JOIN airport on game_airports.location = airport.ident;")
            return game_airports
        
    def add_player(self, name: str, money: float, co2_used: float, time_left: float) -> Any:
            self.execute_query(f"insert into player (name, money, co2_used, time_left) VALUES ('{name}','{money}','{co2_used}', {time_left});")
            self.execute_query(f"insert into player_airports (player_id) VALUES ('{self.cursor.lastrowid}');")

    def update_player(self, name: str, money: float, co2_used: float, time_left: float) -> Any:
            self.execute_query(f"update player SET money = '{money}', co2_used = '{co2_used}', time_left = '{time_left}' WHERE name = '{name}';")     
