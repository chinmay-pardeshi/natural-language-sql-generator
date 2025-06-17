# 🧾 English-to-SQL Query Generator

This AI-powered application lets users ask **natural language questions** and automatically converts them into **SQL queries** to run on a connected MySQL database.

Built with:
- 🧠 **Google Gemini (LearnLM)**
- 🛠️ **LangChain**
- 💾 **SQLAlchemy**
- 📊 **MySQL (retail_sales_db)**

---


## 🎥 Demo

![App Demo](https://github.com/chinmay-pardeshi/natural-language-sql-generator/blob/main/demo/natural-language-sql-generator-gif.gif)

> A quick look at how you can turn English into SQL and get instant answers from your database!



---

## 🚀 Features

- 🔍 Ask questions in plain English  
- 🤖 Auto-generate SQL queries using Gemini  
- 🧪 Execute queries against your database  
- 📊 Display results in a clear, tabular format  
- ⚠️ Error handling for invalid queries  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- LangChain  
- Google Generative AI (Gemini API)  
- SQLAlchemy & MySQL  
- dotenv  

---

## 💻 How to Run Locally

```bash
# 1. Clone this repository
git clone https://github.com/yourusername/english-to-sql-app.git
cd english-to-sql-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your environment variables
# Create a `.env` file with:
GOOGLE_API_KEY=your_google_api_key

# 4. Start your MySQL database (make sure retail_sales_db exists)

# 5. Run the Streamlit app
streamlit run app.py
