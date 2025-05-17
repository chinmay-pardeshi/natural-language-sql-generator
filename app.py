# import os
# import streamlit as st
# from langchain.chains import create_sql_query_chain
# from langchain_google_genai import GoogleGenerativeAI
# from sqlalchemy import create_engine
# from sqlalchemy.exc import ProgrammingError
# from langchain_community.utilities import SQLDatabase
# from dotenv import load_dotenv
# load_dotenv() 

# # Database connection parameters
# db_user = "root"
# db_password = "Isrdev%40123"
# db_host = "localhost"
# db_name = "mysql"

# # Create SQLAlchemy engine
# engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# # Initialize SQLDatabase
# db = SQLDatabase(engine, sample_rows_in_table_info=3)

# # Initialize LLM
# llm = GoogleGenerativeAI(model="models/learnlm-2.0-flash-experimental", google_api_key=os.environ["GOOGLE_API_KEY"])

# # Create SQL query chain
# chain = create_sql_query_chain(llm, db)

# def execute_query(question):
#     try:
#         # Generate SQL query from question
#         response = chain.invoke({"question": question})

#         # Execute the query
#         result = db.run(response)
                
#         # Return the query and the result
#         return response, result
#     except ProgrammingError as e:
#         st.error(f"An error occurred: {e}")
#         return None, None

# # Streamlit interface
# st.title("Question Answering App")

# # Input from user
# question = st.text_input("Enter your question:")

# if st.button("Execute"):
#     if question:
#         cleaned_query, query_result = execute_query(question)
        
#         if cleaned_query and query_result is not None:
#             st.write("Generated SQL Query:")
#             st.code(response, language="sql")
#             st.write("Query Result:")
#             st.write(query_result)
#         else:
#             st.write("No result returned due to an error.")
#     else:
#         st.write("Please enter a question.")











# import os
# import streamlit as st
# from urllib.parse import quote_plus
# from langchain.chains import create_sql_query_chain
# from langchain_google_genai import GoogleGenerativeAI
# from sqlalchemy import create_engine
# from sqlalchemy.exc import ProgrammingError
# from langchain_community.utilities import SQLDatabase
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Database connection parameters
# db_user = "root"
# db_password = quote_plus("Isrdev@123")  # encode special characters like @
# db_host = "localhost"
# db_name = "student"

# # Create SQLAlchemy engine
# engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# # Initialize SQLDatabase
# db = SQLDatabase(engine, sample_rows_in_table_info=3)

# # Initialize LLM
# llm = GoogleGenerativeAI(
#     model="models/learnlm-2.0-flash-experimental",
#     google_api_key=os.environ["GOOGLE_API_KEY"]
# )

# # Create SQL query chain
# chain = create_sql_query_chain(llm, db)

# def is_valid_sql(query: str) -> bool:
#     """Basic check to see if the string looks like SQL."""
#     return query.strip().lower().startswith(("select", "insert", "update", "delete", "with"))

# def execute_query(question):
#     try:
#         # Generate SQL query from natural language question
#         response = chain.invoke({"question": question})

#         # If response is a dictionary, extract SQL string
#         if isinstance(response, dict) and "query" in response:
#             sql_query = response["query"]
#         else:
#             sql_query = response if isinstance(response, str) else str(response)

#         # Validate SQL
#         if not is_valid_sql(sql_query):
#             st.warning(f"LLM did not return a valid SQL query:\n\n{sql_query}")
#             return sql_query, None

#         # Run the query
#         result = db.run(sql_query)
#         return sql_query, result

#     except ProgrammingError as e:
#         st.error(f"An error occurred: {e}")
#         return None, None

# # Streamlit interface
# st.title("Natural Language to SQL Query App")

# # User input
# question = st.text_input("Enter your question about the database:")

# if st.button("Execute"):
#     if question:
#         cleaned_query, query_result = execute_query(question)

#         if cleaned_query:
#             st.subheader("Generated SQL Query:")
#             st.code(cleaned_query, language="sql")

#             if query_result is not None:
#                 st.subheader("Query Result:")
#                 st.write(query_result)
#             else:
#                 st.info("No result returned or invalid query.")
#         else:
#             st.error("Something went wrong. Check your database or query.")
#     else:
#         st.info("Please enter a question.")







import os
import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
from langchain.chains import create_sql_query_chain
from langchain_google_genai import GoogleGenerativeAI
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# MySQL credentials
db_user = "root"
db_password = quote_plus("Isrdev@123")  # Encode @ properly
db_host = "localhost"
db_name = "student"  # <-- replace with your actual DB name

# Connect to MySQL
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# Setup LangChain SQL DB wrapper
db = SQLDatabase(engine, sample_rows_in_table_info=5)

# LLM setup
llm = GoogleGenerativeAI(
    model="models/learnlm-2.0-flash-experimental",
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

# SQL chain
chain = create_sql_query_chain(llm, db)

def is_valid_sql(query: str) -> bool:
    return query.strip().lower().startswith(("select", "insert", "update", "delete", "with"))

def execute_query(question):
    try:
        # Generate SQL
        response = chain.invoke({"question": question})
        sql_query = response["query"] if isinstance(response, dict) and "query" in response else str(response)

        # Validate SQL
        if not is_valid_sql(sql_query):
            st.warning(f"Not valid SQL:\n\n{sql_query}")
            return sql_query, None

        # Run SQL and return as DataFrame
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            columns = result.keys()
            rows = result.fetchall()
            df = pd.DataFrame(rows, columns=columns)
            return sql_query, df

    except ProgrammingError as e:
        st.error(f"SQL Error: {e}")
        return None, None

# --- Streamlit Interface ---
st.title("Natural Language SQL Query App")

# Show available tables in sidebar
st.sidebar.subheader("Tables in MySQL:")
with engine.connect() as conn:
    tables = conn.execute("SHOW TABLES").fetchall()
    for table in tables:
        st.sidebar.write(f"- {table[0]}")

# User question input
question = st.text_input("Ask a question (e.g., Show top 5 from 'sales'):")

if st.button("Run Query"):
    if question:
        sql, df = execute_query(question)

        if sql:
            st.subheader("Generated SQL:")
            st.code(sql, language="sql")

        if df is not None and not df.empty:
            st.subheader("Query Results:")
            st.dataframe(df)
        else:
            st.warning("Query returned no results.")
    else:
        st.info("Please enter a question.")
